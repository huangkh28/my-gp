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
                status.write("script.py: 生成 Cypher 查询语句...")
                cypher = rag_engine.generate_cypher(prompt)

                if cypher:
                    status.code(cypher, language="cypher")

                    # 2. 查询 Neo4j
                    status.write("script.py: 查询图数据库...")
                    """results = rag_engine.execute_cypher(cypher)
                    st.session_state.latest_results = results  # 更新到状态以供右侧显示"""

                    results, actual_cypher, used_fallback = (
                        rag_engine.execute_with_fallback(prompt, cypher)
                    )
                    st.session_state.latest_results = results

                    if used_fallback:
                        status.write(
                            "⚠️ 精准图匹配未命中，已自动触发 Jieba NLP 模糊召回兜底！"
                        )
                        status.code(actual_cypher, language="cypher")

                    status.write(f"数据库召回 {len(results)} 条信息")

                    """status.write(f"数据库召回 {len(results)} 条信息")"""

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
                else:
                    status.update(label="⚠️ 无法生成查询", state="error")
                    st.error("抱歉，后端无法生成有效的数据库查询语句。")


with col2:
    st.subheader("🔍 知识溯源")

    if st.session_state.latest_results:
        st.caption(f"关联节点 ({len(st.session_state.latest_results)})")

        # 👇 新增：添加一个固定高度带滚动条的容器，高度设为 700px (可自行调整)
        with st.container(height=700):

            # 👇 修改：去掉了原先的 [:10] 限制，遍历全部召回结果
            for i, item in enumerate(st.session_state.latest_results):

                # --- 🛠️ 核心修改开始：增强的数据解析逻辑 (包含之前修复 None 的逻辑) ---
                content = ""
                label = "未知节点"

                # 1. 尝试获取数据源 (兼容 'node' 键存在或不存在的情况)
                data_source = item.get("node", item)

                if not isinstance(data_source, dict):
                    content = str(data_source)
                else:
                    found_content = False
                    found_label = False
                    valid_texts = []  # 用来收集所有非空的有效文本

                    # 2. 智能搜索：遍历所有键值对
                    for key, value in data_source.items():
                        # 彻底过滤掉 None 值和空列表/空字符串
                        if value is None or value == "" or value == []:
                            continue

                        key_lower = key.lower()
                        val_str = str(value).strip()

                        # 再次防范转换后变为空白或 "None" 字符串
                        if not val_str or val_str.lower() == "none":
                            continue

                        # 排除 score 这种数字字段
                        if "score" in key_lower:
                            continue

                        valid_texts.append(val_str)

                        # 找标题 (优先找 number, name, title, id)
                        if not found_label and any(
                            k in key_lower for k in ["number", "name", "title", "id"]
                        ):
                            label = val_str
                            found_label = True
                            continue

                        # 找正文 (优先找 full_text, text, description, content)
                        if not found_content and any(
                            k in key_lower
                            for k in [
                                "full_text",
                                "text",
                                "description",
                                "content",
                                "def",
                            ]
                        ):
                            content = val_str
                            found_content = True
                            continue

                    # 3. 兜底策略：如果通过键名没匹配到
                    if not content and valid_texts:
                        # 把收集到的最长的一段有效文本作为正文
                        content = max(valid_texts, key=len)

                    if not found_label:
                        # 如果没找到标题，尝试在剩余的有效文本里挑一个短的当标题
                        short_texts = [
                            t for t in valid_texts if len(t) < 15 and t != content
                        ]
                        if short_texts:
                            label = short_texts[0]
                        else:
                            label = "相关条目"

                # --- 🛠️ 修改结束 ---

                # 截断长文本，防止单个卡片太长 (放宽到了 200 字)
                display_content = (
                    (content[:200] + "...") if len(content) > 200 else content
                )

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
