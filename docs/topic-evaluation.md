# AI 模型評測框架指南

## 學習目標
了解如何客觀評估 LLM 的能力，選擇適合任務的模型。

---

## 為什麼需要評測？

- 不同模型在不同任務上表現差異巨大
- 廠商宣傳數字不代表你的使用場景
- 評測幫助你用最小成本選出最佳模型

---

## 主要評測基準

### MMLU（Massive Multitask Language Understanding）
- **內容**：57 個學科的選擇題（數學、法律、醫學、歷史等）
- **衡量**：廣泛知識與推理能力
- **分數解讀**：人類專家約 90%，GPT-4 約 86%

### HumanEval
- **內容**：164 道 Python 程式題，從 docstring 生成函數
- **衡量**：程式碼生成能力
- **指標**：pass@k（k 次嘗試中至少通過一次的機率）

### GSM8K
- **內容**：國小等級數學應用題
- **衡量**：基礎算術推理

### MT-Bench
- **內容**：多輪對話能力（GPT-4 作為評審）
- **衡量**：指令遵循、對話一致性

---

## LM Evaluation Harness

Hugging Face / EleutherAI 維護的統一評測工具：

```bash
pip install lm-eval

# 評測本地 Ollama 模型
lm_eval --model local-completions \
  --model_args base_url=http://localhost:11434/v1,model=gemma4 \
  --tasks mmlu \
  --num_fewshot 5
```

支援 100+ 評測基準，可自訂評測集。

---

## openclaw Harness Engine

openclaw 的 Harness Engine 是其**自動評測與回歸測試**機制：

- 定義「黃金測試案例」（輸入 → 期望輸出）
- 自動執行 agent 並比對結果
- 監控模型更新後的能力退化（regression）
- 支援 CI/CD 整合

**應用場景**：
- 更換模型前先跑 harness 確認不會破壞現有功能
- 追蹤 prompt 修改的效果
- 評估不同模型在你的特定任務上的表現

---

## 本地模型評測建議

對於 Ollama 本地模型，可用簡易方式評測：

```python
import ollama

test_cases = [
    {"prompt": "2 + 2 = ?", "expected": "4"},
    {"prompt": "台灣首都是哪裡？", "expected": "台北"},
]

for case in test_cases:
    resp = ollama.chat(model='gemma4', messages=[{"role":"user","content":case["prompt"]}])
    answer = resp['message']['content']
    passed = case["expected"] in answer
    print(f"{'✅' if passed else '❌'} {case['prompt'][:20]}...")
```

---

*建立時間：2026-04-19*
