import streamlit as st
import time
from script import LandRegulationsRAG

# --- 页面配置 ---
st.set_page_config(
    page_title="广东省土地管理条例 AI 助手",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS 样式 ---
st.markdown(
    """
    <style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 15px; padding: 10px; margin-bottom: 10px; }
    .source-card {
        background-color: #ffffff;
        border-left: 5px solid #1d4ed8;
        padding: 15px;
        margin-bottom: 8px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        font-size: 0.9em;
    }
    .source-type { font-weight: bold; color: #1d4ed8; font-size: 0.8rem; margin-bottom: 4px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- 初始化 Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "latest_results" not in st.session_state:
    st.session_state.latest_results = []  # 存储最近一次查询结果用于侧边栏


# --- 连接后端 (使用 cache 避免重复连接) ---
@st.cache_resource
def get_backend():
    try:
        return LandRegulationsRAG()
    except Exception as e:
        return None


rag_engine = get_backend()

# --- 侧边栏 ---
with st.sidebar:
    st.title("⚖️ 系统控制台")
    st.subheader("连接状态")

    if rag_engine:
        st.success("● 后端逻辑已加载 (script.py)")
        st.success("● Neo4j 数据库已连接")
    else:
        st.error("❌ 连接失败：请检查 script.py 中的密码配置")

    st.divider()
    if st.button("📑 清空对话历史", use_container_width=True):
        st.session_state.messages = []
        st.session_state.latest_results = []
        st.rerun()

# --- 主界面 ---
col1, col2 = st.columns([7, 3])

# 左侧：对话区
with col1:
    st.title("广东省土地管理条例智能问答")
    st.caption("前端: Streamlit | 后端: Neo4j + Qwen (script.py)")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("请输入您的问题..."):
        if not rag_engine:
            st.error("系统后端未连接，无法回答。")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # 使用 status 组件显示真实处理过程
            with st.status("🔍 正在调用后端逻辑...", expanded=True) as status:

                # 1. 生成 Cypher
                status.write("script.py: 尝试生成 Cypher 查询语句...")
                cypher = rag_engine.generate_cypher(prompt)

                # 💡 无论 Cypher 生成成功还是失败，都将其打印并继续向下执行
                if cypher:
                    status.code(cypher, language="cypher")
                else:
                    status.write("⚠️ Cypher 生成失败或超时，准备直接触发纯向量语义兜底...")

                # 2. 查询 Neo4j (不管 cypher 有没有，都交给引擎去处理)
                status.write("script.py: 启动双路协同检索引擎...")

                # 【核心修复】：必须用 3 个变量接收，且明确指定参数名称
                results, actual_cypher, retrieval_strategy = rag_engine.execute_hybrid_search(
                    question=prompt, 
                    primary_cypher=cypher
                )
                st.session_state.latest_results = results

                # 更新前端状态显示
                status.write(f"💡 当前采用策略: **{retrieval_strategy}**")
                if "纯向量" in retrieval_strategy:
                    status.write("⚠️ 图结构未命中，已自动无缝切换至向量语义匹配！")

                status.write(f"数据库共召回 {len(results)} 条信息")

                # 3. 生成回答
                status.write("script.py: 整理最终回复...")
                full_response = rag_engine.generate_answer(prompt, results)

                status.update(
                    label="✅ 回答生成完毕", state="complete", expanded=False
                )
                st.markdown(full_response)
                
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )


with col2:
    st.subheader("🔍 知识溯源")

    if st.session_state.latest_results:
        st.caption(f"关联节点 ({len(st.session_state.latest_results)})")

        # 👇 新增：添加一个固定高度带滚动条的容器，高度设为 700px (可自行调整)
        with st.container(height=700):

            for i, item in enumerate(st.session_state.latest_results):

                # --- 🛠️ 终极修复：扁平化处理任意嵌套结构 ---
                content = ""
                label = "未知节点"
                valid_texts = []

                # 1. 递归提取字典中所有的字符串值
                def extract_strings(data):
                    strings = []
                    if isinstance(data, dict):
                        for k, v in data.items():
                            # 过滤掉 score, id 等不适合展示的元数据
                            if isinstance(k, str) and k.lower() in ["score", "id", "embedding"]:
                                continue
                            strings.extend(extract_strings(v))
                    elif isinstance(data, list):
                        for el in data:
                            strings.extend(extract_strings(el))
                    elif isinstance(data, str) and data.strip():
                        # 只收集有效的非空字符串
                        if data.strip().lower() != "none":
                            strings.append(data.strip())
                    return strings

                # 提取所有有效文本
                valid_texts = extract_strings(item)

                if not valid_texts:
                    # 如果什么都没提取出来，跳过这条或者给个默认提示
                    continue

                # 2. 寻找最像“正文”的段落（通常是最长的那段）
                content = max(valid_texts, key=len)

                # 3. 寻找最像“标题”的段落（较短的，且不是正文的片段）
                title_candidates = [t for t in valid_texts if len(t) < 30 and t != content]
                
                # 尝试从字典原始结构中定向寻找 title/number/name
                def find_title(data):
                    if isinstance(data, dict):
                        for k, v in data.items():
                            if isinstance(k, str) and any(kw in k.lower() for kw in ["number", "title", "name", "label"]):
                                if isinstance(v, str) and v.strip() and v.strip().lower() not in ["none", "无"]:
                                    return v.strip()
                            # 递归找
                            found = find_title(v)
                            if found: return found
                    return None
                
                explicit_title = find_title(item)

                if explicit_title:
                    label = explicit_title
                elif title_candidates:
                    label = title_candidates[0]
                else:
                    label = "相关条目"

                # --- 🛠️ 修改结束 ---

                # 截断长文本，防止单个卡片太长 (放宽到了 200 字)
                display_content = (content[:200] + "...") if len(content) > 200 else content

                st.markdown(
                    f"""
                    <div class="source-card">
                        <div class="source-type">#{i+1} {label}</div>
                        <div style="color: #333;">{display_content}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.write("暂无检索数据。")
        st.caption("请在左侧输入问题，后端 script.py 返回的数据将显示在这里。")
