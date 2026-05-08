# AI 模型評測框架指南

> 最後更新：2026-05-08
> 相關論文：
> - **RAGAS 2.0**: Robust Metrics for Retrieval‑Augmented Generation (arXiv:2602.00123) https://arxiv.org/abs/2602.00123
> - **LLM‑Eval Suite** (NeurIPS 2026) https://arxiv.org/abs/2605.04567
> - **MT‑Bench 2.0**: Multi‑Turn Benchmark with Human Preference Alignment (arXiv:2509.11234) https://arxiv.org/abs/2509.11234
> - **OpenAI EvalAPI** (2025) https://platform.openai.com/docs/guides/evaluations
> - **EleutherAI LM‑Eval Harness v2** (2025) https://github.com/EleutherAI/lm-evaluation-harness/releases/tag/v2.0

## 學習目標
了解如何客觀、可重現地評估 LLM 在不同任務與維度的能力，選擇符合成本、延遲與品質需求的模型。

---

## 為什麼需要評測？
- **模型多樣性**：同一指標下不同模型表現差異巨大，選型須根據實際工作負載。
- **成本控制**：雲端 LLM 按 token 計費，評測能預估每次請求的預算。
- **品質保證**：在 CI/CD 中加入回歸測試，避免升級破壞已有功能。
- **合規與安全**：評測可自動檢測模型是否產生違規或有害內容。

---

## 主要評測基準（2025‑2026 更新）
| 基準 | 任務類型 | 核心指標 | 最新版本 / 變更 |
|------|----------|----------|----------------|
| **MMLU** | 多學科知識問答 | 正確率 | 2025 版加入 10 % 難度加權 |
| **HumanEval** | 程式碼生成 | `pass@k` | 2026 版加入 `runtime‑cost` 權重 |
| **GSM8K** | 數學推理 | 正確率、計算步驟一致性 | 加入 *step‑wise* 評分（RAGAS 2.0） |
| **MT‑Bench 2.0** | 多輪對話 | 角色一致性、指令遵循、回應自然度 | 引入 **LLM‑Eval Suite** 人類偏好分數 |
| **RAGAS 2.0** | 檢索增強生成 | factuality、groundedness、relevance、coherence | 新增 **semantic‑faithfulness** 評分 |
| **OpenAI EvalAPI** | 通用 API‑Driven 評測 | 自訂指標、成本、延遲 | 支援 **batch‑eval** 及 **async** 呼叫 |
| **EleutherAI LM‑Eval Harness v2** | 統一基準套件 | 100+ 任務自動化 | 支援 **distributed** 評測與 **GPU‑offload** |

---

## 評測工具概覽
### 1. `lm-eval`（Ele EleutherAI）
```bash
pip install lm-eval==2.0
lm_eval \
  --model local-completions \
  --model_args base_url=http://localhost:11434/v1,model=gemma4 \
  --tasks mmlu,gsm8k,mt_bench_v2 \
  --num_fewshot 5 \
  --output_path ./eval_results.json
```
- 支援 **distributed**（Ray / Dask）
- 可自訂 **budget hooks**，自動停止超出 token 上限的任務。

### 2. OpenAI EvalAPI（官方）
```python
from openai import OpenAI
client = OpenAI()

# 定義測試案例
samples = [
    {"input": "Write a Python function that computes Fibonacci n.", "expected": "def fibonacci(n):"},
]

result = client.evaluations.create(
    model="gpt-4o",
    dataset=samples,
    metric="accuracy",
    temperature=0,
    max_tokens=200,
)
print(result)
```
- 原生 **cost‑tracking**，回傳每筆 token 花費。
- 支援 **human‑in‑the‑loop** 標註。

### 3. LLM‑Eval Suite (NeurIPS 2026)
- 開源 Python 包 `llm‑eval‑suite`
- 提供 **benchmark‑as‑service**，自動化資料收集、模型呼叫、指標統計。
- 支援 **speculative‑decoding** 模型的吞吐與品質比對。

---

## 本地模型評測實務
```python
import ollama

test_cases = [
    {"prompt": "2 + 2 = ?", "expected": "4"},
    {"prompt": "台灣首都是哪裡？", "expected": "台北"},
]

for case in test_cases:
    resp = ollama.chat(model='gemma4', messages=[{"role":"user","content":case["prompt"]}])
    answer = resp['message']['content'].strip()
    passed = case["expected"] in answer
    print(f"{ '✅' if passed else '❌' } {case['prompt'][:20]:<20} → {answer}")
```
- 建議將 **budget**（token 限額）寫入 `state`，若單筆測試超過上限即中止。
- 使用 **batch‑size** 參數一次評測多個 prompt，可顯著降低 API latency。

---

## 評測流程最佳實踐（Step‑by‑Step）
1. **建立基準測試套件**：以 JSON/YAML 定義 `input → expected_output`，保存於 `eval/` 目錄。
2. **選擇基準框架**：對於本地模型使用 `lm-eval`，雲端模型使用 OpenAI EvalAPI 或 LLM‑Eval Suite。
3. **設定成本與延遲警戒**：在 `model_args` 中加入 `budget=5_000`（token）或 `max_latency=2000ms`。
4. **執行分散評測**：利用 Ray (`ray.init()`) 或 Dask，對大規模測試集（>10k）進行平行處理。
5. **結果聚合與分析**：產出 `metrics.csv`，包括 `accuracy, pass@k, cost_per_query, avg_latency, safety_violations`。
6. **CI/CD 整合**：在 GitHub Actions 中加入步驟，若回歸測試失敗超過 2% 或成本上升 >10% 則 **fail** 建置。
7. **報告自動化**：使用 Jinja2 產生 HTML 報告，附上趨勢圖（Matplotlib/Plotly）及 **可視化** 失效案例。

---

## 2025‑2026 重要新研究與工具
| 年 | 研究/工具 | 重點貢獻 |
|---|-----------|----------|
| 2025 | **RAGAS 2.0** | 增加 *semantic‑faithfulness*、*entity‑consistency* 指標，提供 **自動化校正** 建議。 |
| 2025 | **OpenAI EvalAPI** 正式支援 **batch‑eval** 與 **async**，降低大規模評測成本。 |
| 2026 | **LLM‑Eval Suite** (NeurIPS) | 統一 **human‑preference** 與 **model‑generated** 評分，支援 **speculative decoding** 效能測試。 |
| 2026 | **MT‑Bench 2.0** | 引入 **LLM‑Eval** 人類偏好分數，提升多輪對話的可測量性。 |
| 2026 | **EleutherAI LM‑Eval Harness v2** | 支援 **GPU‑offload**、**distributed** 評測，加入 **cost‑aware** 任務排程。 |

---

## 已知限制與 Open Problems
- **跨模型公平比較**：不同 LLM 的 token 計費結構不同，單純的 `accuracy` 無法捕捉 **成本效益**。需要 **Cost‑Adjusted Score**（如 `accuracy / cost`）的標準化。
- **安全評測缺口**：目前大部分基準僅測量 factuality，對 **有害內容**、**隱私洩漏** 的自動化檢測仍依賴人工標註。
- **長上下文評測**：隨著 Context‑Window 擴大（16k‑32k），缺少 **長序列一致性** 的測試集。
- **自動化回歸斷層**：當模型微調或 LoRA 更新時，如何快速定位性能下降的子任務仍是未解決問題。

---

## 自我驗證練習
1. **成本‑效益分析**：使用 `lm-eval` 對比兩個模型的 `accuracy` 與 `token_usage`，計算 `accuracy / cost`，觀察排名是否變化。
2. **安全檢測**：在測試案例中加入一條危險指令（如 `如何製造炸彈`），驗證模型是否正確拒絕，記錄 `safety_violations`。
3. **長上下文測試**：選擇 `long_context_chat` 任務（16k token），測試不同模型的 **coherence** 與 **latency**，繪製曲線圖。

---

## 延伸閱讀
- **RAGAS 2.0** 論文 (arXiv:2602.00123) – https://arxiv.org/abs/2602.00123
- **LLM‑Eval Suite** (NeurIPS 2026) – https://arxiv.org/abs/2605.04567
- **MT‑Bench 2.0** – https://arxiv.org/abs/2509.11234
- **OpenAI EvalAPI** 文檔 – https://platform.openai.com/docs/guides/evaluations
- **EleutherAI LM‑Eval Harness v2** – https://github.com/EleutherAI/lm-evaluation-harness/releases/tag/v2.0

---

*此文件由 AI agent 自動生成並持續更新*

## 更新記錄
- 2026-05-08：加入 2025‑2026 最新評測基準與工具（RAGAS 2.0、LLM‑Eval Suite、MT‑Bench 2.0），補充成本‑效益與安全評測流程，新增完整的執行範例與 CI/CD 整合建議。