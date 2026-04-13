import json
import time
import os
from openai import OpenAI
from script import LandRegulationsRAG, API_KEY, BASE_URL, MODEL_NAME

# 初始化独立的 OpenAI Client 用于 Baseline 和 Judge
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def get_baseline_answer(question):
    """组别 A：直接提问大模型 (裸奔状态)"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的法律助手，请回答关于《广东省土地管理条例》的问题。",
                },
                {"role": "user", "content": question},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"  ❌ Baseline 请求失败: {e}")
        return ""


def get_rag_answer(rag, question):
    """组别 B：走完整的 Graph RAG 流程 """
    cypher = rag.generate_cypher(question)
    if not cypher:
        return "未能生成图谱查询语句。"

    # 👇 核心修改：使用双引擎查询替代原来的单步执行
    results, actual_cypher, used_fallback = rag.execute_with_fallback(question, cypher)

    # 将召回结果喂给大模型生成最终回答
    answer = rag.generate_answer(question, results)
    return answer


def llm_as_a_judge(question, expected_answer, model_answer):
    """LLM 作为裁判，判断是否出现幻觉"""
    # 如果回答极度简短或是系统报错词，直接判定为幻觉/失效
    if (
        not model_answer
        or "未能生成" in model_answer
        or "没有找到相关信息" in model_answer
    ):
        return {
            "hallucination": True,
            "reason": "系统未能召回有效信息或未给出回答，属于知识缺失/任务失败。",
        }

    prompt = f"""
    你是一个严厉的法律事实核查员。
    用户提问：{question}
    【条例标准答案（Ground Truth）】：{expected_answer}
    【待评估的模型回答】：{model_answer}

    请判断【待评估的模型回答】是否出现了“幻觉”（Hallucination）。
    幻觉的定义：
    1. 捏造了标准答案中不存在的法条、数字、处罚标准、政府部门等具体实体。
    2. 张冠李戴，改变了标准答案的核心逻辑（例如把县级政府写成省级政府，或者搞错处罚条件）。
    3. 引入了其他法律（如《刑法》、《民法典》）中无关的内容，强行解释《广东省土地管理条例》。
    （注意：如果待评估回答比标准答案少了一些细节，但不包含错误信息，不算幻觉；如果有明确的捏造或逻辑冲突，算作幻觉）。

    请严格按照以下 JSON 格式输出，不要输出任何其他 markdown 字符或多余解释：
    {{"hallucination": true, "reason": "具体的判断理由"}}
    或者
    {{"hallucination": false, "reason": "符合标准答案，无编造"}}
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,  # 裁判需要极其稳定，Temperature 设为 0
        )
        result_text = response.choices[0].message.content.strip()

        # 清洗可能存在的 markdown 代码块符号
        result_text = result_text.replace("```json", "").replace("```", "").strip()

        return json.loads(result_text)
    except Exception as e:
        print(f"  ❌ Judge 评估失败: {e}")
        return {"hallucination": True, "reason": f"裁判评估过程报错: {e}"}


def run_hallucination_eval():
    print("初始化 RAG 系统...")
    rag = LandRegulationsRAG()

    print("\n加载测试集...")
    try:
        with open("test_cases.json", "r", encoding="utf-8") as f:
            test_data = json.load(f)
    except FileNotFoundError:
        print("❌ 找不到 test_cases.json")
        return

    total_questions = len(test_data)
    print(f"✅ 成功加载 {total_questions} 个测试用例。开始幻觉率对比评估...\n")

    log_file = "hallucination_comparison_log.txt"
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("=== Graph RAG vs Baseline 幻觉率对比实验 ===\n\n")

    baseline_hallucination_count = 0
    rag_hallucination_count = 0

    for i, item in enumerate(test_data):
        question = item["question"]
        expected_ans = item["expected_answer_points"]
        print(f"[{i+1}/{total_questions}] 评估中: {question}")

        # 1. 获取两组回答
        baseline_ans = get_baseline_answer(question)
        time.sleep(1)  # 防频控
        rag_ans = get_rag_answer(rag, question)
        time.sleep(1)

        # 2. 裁判打分
        print("  ⚖️ 裁判打分中...")
        baseline_judge = llm_as_a_judge(question, expected_ans, baseline_ans)
        time.sleep(1)
        rag_judge = llm_as_a_judge(question, expected_ans, rag_ans)
        time.sleep(1)

        # 3. 统计结果
        if baseline_judge.get("hallucination", True):
            baseline_hallucination_count += 1
            b_mark = "❌ 存在幻觉"
        else:
            b_mark = "✅ 无幻觉"

        if rag_judge.get("hallucination", True):
            rag_hallucination_count += 1
            r_mark = "❌ 存在幻觉"
        else:
            r_mark = "✅ 无幻觉"

        print(f"  -> Baseline 表现: {b_mark} | RAG 表现: {r_mark}")

        # 4. 记录日志，供论文提取案例
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"【问题】: {question}\n")
            f.write(f"【预期标准答案】: {expected_ans}\n\n")

            f.write(f"[组别 A - 裸大模型 Baseline]\n")
            f.write(f"回答: {baseline_ans}\n")
            f.write(f"裁判判定: {baseline_judge}\n\n")

            f.write(f"[组别 B - Graph RAG 系统]\n")
            f.write(f"回答: {rag_ans}\n")
            f.write(f"裁判判定: {rag_judge}\n")
            f.write("-" * 60 + "\n\n")

    # 打印对比结果
    print("\n" + "=" * 60)
    print("📊 幻觉率对比实验报告 (直接填入论文)")
    print("=" * 60)
    print(f"测试总题数: {total_questions} 题")

    b_rate = (baseline_hallucination_count / total_questions) * 100
    r_rate = (rag_hallucination_count / total_questions) * 100

    print(
        f"🔴 Baseline (直接提问) 幻觉率: {b_rate:.2f}% ({baseline_hallucination_count}/{total_questions})"
    )
    print(
        f"🟢 Graph RAG (本系统) 幻觉率: {r_rate:.2f}% ({rag_hallucination_count}/{total_questions})"
    )

    diff = b_rate - r_rate
    print(f"\n💡 结论: 引入 Graph RAG 后，系统幻觉率绝对下降了 {diff:.2f}%")
    print(f"📄 详细对比案例已保存至: {os.path.abspath(log_file)}")
    print("=" * 60)


if __name__ == "__main__":
    run_hallucination_eval()
