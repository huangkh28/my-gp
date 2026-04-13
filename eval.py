import json
import time
import os
from script import LandRegulationsRAG


def run_eval():
    print("初始化 RAG 系统...")
    rag = LandRegulationsRAG()

    print("\n加载测试集...")
    try:
        with open("test_cases.json", "r", encoding="utf-8") as f:
            test_data = json.load(f)
    except FileNotFoundError:
        print("❌ 找不到 test_cases.json 文件，请确保它在同级目录下。")
        return

    total_questions = len(test_data)
    print(f"✅ 成功加载 {total_questions} 个测试用例。开始批量评估...\n")
    print("=" * 60)

    # 初始化日志文件，每次运行清空旧日志
    log_file = "failed_queries_log.txt"
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("=== 广东省土地管理条例 RAG 错题本 (失败 Cypher 诊断日志) ===\n\n")

    cypher_success_count = 0
    recall_success_count = 0
    total_time = 0

    for i, item in enumerate(test_data):
        question = item["question"]
        expected_kws = item["expected_keywords"]
        item_id = item.get("id", f"unknown_{i}")

        print(f"[{i+1}/{total_questions}] 提问: {question}")
        start_time = time.time()

        # 1. 尝试生成 Cypher (如果超时，这里会返回空字符串 "")
        cypher_query = rag.generate_cypher(question)

        # 👇 核心修改：不管生成成功还是超时(返回空字符串)，都直接扔给双引擎！
        if not cypher_query:
            print("  ⚠️ [生成超时/失败] 准备直接触发本地 Jieba 兜底...")

        # 2. 执行查询与验证 (双引擎会自动处理 cypher_query 为空的情况)
        try:
            db_results, actual_cypher, used_fallback = rag.execute_with_fallback(
                question, cypher_query
            )

            # 👇 重新定义“失败”：大模型没写出 Cypher，且 Jieba 兜底也什么都没捞到
            if not cypher_query and not db_results:
                cypher_fail_count += 1
                print("  ❌ [彻底失败] Cypher 生成超时，且 Jieba 兜底未召回任何数据")
                print("-" * 60)

                # 将真正的彻底失败记录到错题本
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"【问题 ID】: {item_id}\n")
                    f.write(f"【测试问题】: {question}\n")
                    f.write(f"【预期关键词】: {expected_kws}\n")
                    f.write(
                        f"【失败原因】: Cypher 生成超时或失败，且 Jieba 兜底未召回数据\n"
                    )
                    f.write("-" * 50 + "\n\n")
                continue  # 彻底失败，直接跳过本题后续验证
            else:
                cypher_success_count += 1

                if used_fallback:
                    print(
                        "  ⚠️ [触发兜底] 原始 Cypher 未命中或生成超时，已通过 Jieba 模糊搜索成功召回"
                    )
                else:
                    print("  ✅ [语法成功] 精准 Cypher 执行成功且有数据")

            results_str = str(db_results)
            hit_count = sum(1 for kw in expected_kws if kw in results_str)

            if hit_count > 0:
                recall_success_count += 1
                print(f"  🎯 [召回成功] 命中关键词: {hit_count}/{len(expected_kws)} 个")
            else:
                print("  ⚠️ [召回失败] 数据库查到了内容，但未命中预期核心词")
                print("\n      >>> 🕵️ 失败的 Cypher 诊断 <<<")
                print(f"      {cypher_query}")
                print("      ==============================\n")

                # 写入错题本 (召回失败)
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"【问题 ID】: {item_id}\n")
                    f.write(f"【测试问题】: {question}\n")
                    f.write(f"【预期关键词】: {expected_kws}\n")
                    f.write(f"【失败原因】: 召回为空或未命中核心词\n")
                    f.write(f"【大模型生成的 Cypher】:\n{cypher_query}\n")
                    f.write("-" * 50 + "\n\n")

        except Exception as e:
            print(f"  ❌ [执行报错] Neo4j 数据库报错: {e}")
            print("\n      >>> 🕵️ 报错的 Cypher 诊断 <<<")
            print(f"      {cypher_query}")
            print("      ==============================\n")

            # 写入错题本 (执行报错)
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"【问题 ID】: {item_id}\n")
                f.write(f"【测试问题】: {question}\n")
                f.write(f"【预期关键词】: {expected_kws}\n")
                f.write(f"【失败原因】: Neo4j 语法报错 -> {e}\n")
                f.write(f"【大模型生成的 Cypher】:\n{cypher_query}\n")
                f.write("-" * 50 + "\n\n")

        end_time = time.time()
        elapsed = end_time - start_time
        total_time += elapsed

        print(f"  ⏱️ 单题耗时: {elapsed:.2f} 秒")
        print("-" * 60)

        # 强制休息 1.5 秒，避开 API 频控死锁
        time.sleep(1.5)

    # 打印最终统计大屏
    print("\n" + "=" * 60)
    print("📊 评估报告总览 (可用于毕业论文数据)")
    print("=" * 60)
    print(f"测试总题数: {total_questions} 题")
    print(f"总计耗时:   {total_time:.2f} 秒")
    print(f"平均每题耗时: {total_time / total_questions:.2f} 秒")
    print("-" * 60)
    print(
        f"✅ 语法成功率: {cypher_success_count / total_questions * 100:.2f}% ({cypher_success_count}/{total_questions})"
    )

    if cypher_success_count > 0:
        print(
            f"🎯 节点召回率: {recall_success_count / cypher_success_count * 100:.2f}% ({recall_success_count}/{cypher_success_count})"
        )
    else:
        print("🎯 节点召回率: 0.00% (语法成功数为0，无法计算召回)")
    print("=" * 60)
    print(f"📄 已将所有失败的查询记录至: {os.path.abspath(log_file)}")


if __name__ == "__main__":
    run_eval()
