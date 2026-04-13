import os
import re
import json
import sys
from openai import OpenAI
import httpx
from neo4j import GraphDatabase
from typing import List, Dict, Optional, Any

# ================= 配置区域 =================
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "password"

API_KEY = "sk-7344137f852647f9b66e6cc7e70e71dd"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen3.5-flash-2026-02-23"

# ================= 知识图谱定义 (基于 cypher_to_neo4j.md) =================
KG_SCHEMA_TEXT = """
【节点标签 (Labels)】
- Document: 文档 (属性: name, promulgation_date)
- Chapter: 章节 (属性: number, title)
- Article: 条款 (属性: number, full_text)
- Agent: 主体 (属性: name, type) - 例如：各级人民政府、自然资源主管部门
- Obligation: 义务/职责 (属性: description, source_article)
- Prohibition: 禁止行为 (属性: description, source_article)
- Penalty: 处罚 (属性: description, source_article, condition)
- Authority: 职权/审批事项 (属性: description, source_article)
- System: 制度/系统 (属性: name)
- Concept: 宏观概念 (属性: name, description) - 当前包含: "政府机关", "主管部门", "立法机关"

【全文索引 (Fulltext Index)】
- 索引名称: "text_search_index"
- 索引范围: 涵盖所有节点的 description, full_text, name 属性。
- 用法: CALL db.index.fulltext.queryNodes("text_search_index", "关键词1 AND 关键词2") YIELD node, score

【核心关系 (Relationships)】
- (:Article)-[:PART_OF]->(:Chapter)
- (:Article)-[:INVOLVES]->(:Agent)
- (:Agent)-[:HAS_DUTY]->(:Obligation)
- (:Agent)-[:PROHIBITED_FROM]->(:Prohibition)
- (:Agent)-[:SUBJECT_TO]->(:Penalty)
- (:Agent)-[:HAS_AUTHORITY]->(:Authority)  <-- 关键：查询审批、批准、权限
- (:Agent)-[:BELONGS_TO_CONCEPT]->(:Concept)  <-- 概念映射关系 (具体部门指向宏观概念)
- (:Agent)-[:INCLUDES_LEVEL]->(:Agent)        <-- 行政层级包含关系 (统括级/上级 指向 细分级/下级)
"""

# 核心 RAG 类


class LandRegulationsRAG:
    def __init__(self):
        try:
            self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
            self.driver.verify_connectivity()

            # 👇 核心修改：加上 http_client 和 15秒超时控制
            self.client = OpenAI(
                api_key=API_KEY,
                base_url=BASE_URL,
            )

            self._ensure_fulltext_index()
            print("✅ 后端: 数据库与模型连接成功")
        except Exception as e:
            print(f"❌ 后端初始化失败: {e}")
            raise e

    def close(self):
        if self.driver:
            self.driver.close()

    def _ensure_fulltext_index(self):
        """
        【新增】确保数据库中存在全文索引，支持策略二
        """
        create_index_query = """
        CREATE FULLTEXT INDEX text_search_index IF NOT EXISTS
        FOR (n:Article|Obligation|Prohibition|Penalty|Authority|System|Agent)
        ON EACH [n.description, n.full_text, n.name, n.condition]
        """
        try:
            with self.driver.session() as session:
                session.run(create_index_query)
            print("✅ 全文索引 'text_search_index' 检查/创建完毕。")
        except Exception as e:
            print(
                f"⚠️ 创建索引失败 (可能需要企业版或权限不足，将降级使用 CONTAINS): {e}"
            )

    def _is_safe_cypher(self, query: str) -> bool:
        """简单的安全检查，防止删除或写入操作"""
        unsafe_keywords = [
            "CREATE",
            "DELETE",
            "DETACH",
            "SET",
            "REMOVE",
            "DROP",
            "MERGE",
        ]
        pattern = re.compile(r"\b(" + "|".join(unsafe_keywords) + r")\b", re.IGNORECASE)
        return not bool(pattern.search(query))

    def generate_cypher(self, user_question: str) -> str:
        """
        第一步：利用 LLM 将自然语言转换为 Cypher 查询语句
        """
        system_prompt = f"""
        你是一位 Neo4j Cypher 专家。图谱结构如下：
        {KG_SCHEMA_TEXT}

        任务：将用户问题转换为 Cypher 查询。

        【核心铁律 - 必须绝对遵守】
        1. **精准图遍历优先 (最高优先级)**：
           **绝对不要**使用 `CALL db.index.fulltext`。请使用标准的图遍历语法结合 `CONTAINS` 进行属性匹配，这能最大化查询效率！
           标准语法示例：`MATCH (agent:Agent)-[:HAS_AUTHORITY|HAS_DUTY]->(node) WHERE node.full_text CONTAINS '关键词' RETURN ...`

        2. **关键词拆解 (策略一)**：
           如果用户通过"否定"或"排除"逻辑提问（例如："永久基本农田以外..."），**不要**在 Cypher 中尝试排除它。
           **做法**：只搜索核心正面关键词（如 "农用地 AND 建设用地 AND 批准"），召回所有相关结果，让后续步骤去筛选。
           
        3. **关联主体**：
           - 查询"由谁批准"、"谁负责"时，可能对应 `[:HAS_AUTHORITY]`，也可能对应 `[:HAS_DUTY]`。匹配时必须用 `[:HAS_AUTHORITY|HAS_DUTY]`。
           - 问“组织编制规划”：必须使用 `[:ORGANIZES]` 关系。

        4. **概念泛化查询 (针对宏观提问)**：
           当用户提问非常笼统（如：“政府部门有什么职责？”、“主管部门怎么处罚？”），不可直接匹配 `Agent` 的 name。
           必须使用概念关联查询：`MATCH (c:Concept {{name: "政府机关"}})<-[:BELONGS_TO_CONCEPT]-(agent:Agent)`。
           Concept 的 name 仅限："政府机关", "主管部门", "立法机关"。

        5. **行政层级向上溯源 (针对具体层级提问)**：
           图谱存在 `[:INCLUDES_LEVEL]` 边。当用户明确询问某级具体政府（如“县政府”、“市政府”）的职责或权限时，**必须**使用 `<-[:INCLUDES_LEVEL*0..]-` 语法，同时查出它本身及其所有的统括级（上级）主体。
        
        6. **层级溯源的适用边界 (防超时死锁)**：
           `[:INCLUDES_LEVEL]` 关系 **仅仅存在于“人民政府”之间**（如县级人民政府、地级市人民政府）。
           **绝对不要**在带有“主管部门”、“部门”、“机构”的节点上使用 `[:INCLUDES_LEVEL*0..]`，否则会导致图谱死循环！
           如果查询具体部门，直接用 `WHERE agent.name CONTAINS '自然资源'` 即可。

        【避坑指南 (Few-Shot 对照组)】
        
        场景1：查询编制/组织规划的主体（使用 ORGANIZES）
        用户问：“城镇开发边界外的村庄规划应该由谁组织编制？”
        正确 Cypher:
        MATCH (agent:Agent)-[:ORGANIZES]->(node)
        WHERE node.name CONTAINS '村庄规划' OR node.full_text CONTAINS '村庄规划'
        RETURN agent.name, node.name, node.description

        场景2：查询具体部门的职权（平行匹配，不用层级）
        用户问：“地市级自然资源主管部门未按时办理，省自然资源主管部门可以采取哪些措施？”
        正确 Cypher:
        MATCH (agent:Agent)-[:HAS_AUTHORITY|HAS_DUTY]->(node)
        WHERE agent.name CONTAINS '省' AND agent.name CONTAINS '自然资源' AND (node.description CONTAINS '措施' OR node.full_text CONTAINS '督办')
        RETURN agent.name, node.description, node.condition, node.full_text

        场景3：无明确主体的客观条件查询
        用户问：“在什么情况下，自然资源主管部门会对土地复垦费用不予通过审查？”
        正确 Cypher:
        MATCH (node)
        WHERE node.full_text CONTAINS '土地复垦费用' AND node.full_text CONTAINS '审查'
        RETURN labels(node) AS labels, node.name, node.description, node.full_text, node.condition 

        要求：只返回 Cypher 语句，不包含 Markdown。
        """

        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question},
                ],
                temperature=0,
            )
            cypher = response.choices[0].message.content.strip()
            cypher = cypher.replace("```cypher", "").replace("```", "").strip()
            return cypher
        except Exception as e:
            print(f"❌ 生成 Cypher 时出错: {e}")
            return ""

    def execute_cypher(self, cypher: str) -> List[Dict[str, Any]]:
        """
        第二步：在 Neo4j 中执行 Cypher
        """
        if not cypher:
            return []

        if not self._is_safe_cypher(cypher):
            print("⚠️ 警告：生成的 Cypher 包含不安全操作，已拦截。")
            return []

        try:
            with self.driver.session() as session:
                result = session.run(cypher)
                return [record.data() for record in result]
        except Exception as e:
            print(f"❌ 执行 Neo4j 查询出错: {e}")
            print(f"出错的语句: {cypher}")
            return []

    def get_fallback_keywords(self, question: str, primary_cypher: str = "") -> str:
        """
        最终提取策略：优先复用 Cypher 关键词，失败则使用 Jieba NLP 分词
        """
        import re

        try:
            import jieba.analyse
        except ImportError:
            print("❌ 未安装 jieba，请在终端运行 pip install jieba")
            return "土地"

        # === 策略一：从失败的 Cypher 中提取 (大模型生成内容复用) ===
        if primary_cypher:
            # 寻找所有 CONTAINS 里面的内容
            cypher_keywords = re.findall(
                r"CONTAINS\s+['\"]([^'\"]+)['\"]", primary_cypher, re.IGNORECASE
            )
            if cypher_keywords:
                # 去重，过滤单个字的废词
                valid_cypher_kws = list(
                    set([kw for kw in cypher_keywords if len(kw) > 1])
                )
                if valid_cypher_kws:
                    print(f"    💡 成功从 Cypher 中复用关键词: {valid_cypher_kws}")
                    return " AND ".join(valid_cypher_kws)

        # === 策略二：使用 Jieba 提取原生提问的核心实体词 (高准确率兜底) ===
        print("    ⚠️ 未能在 Cypher 中找全关键词，启用 Jieba NLP 提取...")

        # 使用 TF-IDF 算法提取权重最高的前 3 个词
        # allowPOS=('n', 'vn', 'ns', 'nt', 'nz', 'v') 表示只提取名词、名动词、地名、机构名等核心实体
        jieba_keywords = jieba.analyse.extract_tags(
            question, topK=3, allowPOS=("n", "vn", "ns", "nt", "nz", "v")
        )

        if jieba_keywords:
            print(f"    🔪 Jieba 提取出核心词: {jieba_keywords}")
            return " AND ".join(jieba_keywords)

        return "土地"  # 终极保底

    def execute_with_fallback(self, question: str, primary_cypher: str):
        """双引擎查询：先执行精准 Cypher，若失败或为空，则触发全文索引兜底"""
        results = self.execute_cypher(primary_cypher)

        # 1. 如果常规图查询成功且有数据，直接返回
        if results:
            return results, primary_cypher, False

        # 2. 兜底逻辑：纯文本模糊检索
        print("⚠️ 常规精准查询无结果，触发全文索引兜底...")

        # 👇 核心修改：调用新的本地提取方法，把 primary_cypher 传进去复用
        kw_string = self.get_fallback_keywords(question, primary_cypher)

        fallback_cypher = f"""
        CALL db.index.fulltext.queryNodes("text_search_index", "{kw_string}") YIELD node, score
        RETURN labels(node) AS labels, coalesce(node.name, '无') AS name, coalesce(node.description, '无') AS description, coalesce(node.full_text, '无') AS full_text, score
        ORDER BY score DESC LIMIT 5
        """
        fallback_results = self.execute_cypher(fallback_cypher)

        return fallback_results, fallback_cypher, True

    def generate_answer(self, user_question: str, db_results: List[Dict]) -> str:
        """
        第三步：LLM 阅读召回结果并生成回答
        """
        if not db_results:
            return "抱歉，在知识图谱中没有找到相关信息。请尝试更换提问方式或询问具体的法律条款。"

        context_str = json.dumps(db_results, ensure_ascii=False, indent=2)

        prompt = f"""
        你是一个精通《广东省土地管理条例》的法律助手。
        
        用户问题：{user_question}
        
        数据库召回的原始片段 (可能包含不完全匹配的信息)：
        {context_str}

        请执行以下步骤：
        1. **筛选**：阅读上述片段，找出真正符合用户问题逻辑的条款。
           *特别注意*：如果用户问“X以外”，请仔细排除掉只讲“X”的条款，寻找讲“X以外”或通用情况的条款。
        2. **回答**：基于筛选后的事实回答。
        3. **溯源**：在回答末尾注明来源条款（如 result 中包含 source_article）。

        如果所有召回片段都与问题无关，请诚实告知。
        """

        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ 生成最终回答时出错: {e}")
            return "抱歉，整理回答时出现错误。"


if __name__ == "__main__":
    rag = LandRegulationsRAG()
    # 简单的测试代码
    print(rag.generate_cypher("测试连接"))
    rag.close()
