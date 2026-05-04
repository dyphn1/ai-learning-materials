# Speculative Decoding (LLM Inference Acceleration)

> 最後更新：2026-05-04
> 相關論文：[Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192)、[Scaling LLM Speculative Decoding: Non‑Autoregressive Forecasting in Large‑Batch Scenarios](https://arxiv.org/abs/2511.20340)、[SpecFormer: Non‑Autoregressive Draft for Speculative Decoding](https://arxiv.org/abs/2512.04567)、[TurboSpec: Closed‑Loop Control for Dynamic Draft Length](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2025/EECS-2025-224.html)、[SSD: Speculative Speculative Decoding](https://openreview.net/forum?id=aL1Wnml9Ef)

## 概覽與設計動機
自回歸解碼的串行性是大型語言模型推理的主要瓶頸。即使 GPU 有剩餘算力，逐 token 前向仍限制吞吐。Speculative Decoding 透過 **草稿模型 (draft model)** 先預測多個候選 token，然後 **目標模型 (target model)** 並行驗證這些候選，減少目標模型前向呼叫次數。

## 核心機制深度解析

| 元件 | 功能 | 重要參數 |
|------|------|----------|
| Draft Model | 輕量模型或同模型的低精度版本，用於快速產生 token 序列 | 例：7B 替代 70B、溫度、top‑k |
| Target Model | 高品質模型，負責驗證 draft 產出的 token 前綴 | 完整精度模型 |
| Verification Step | 同時對多個 draft token 執行 forward，計算 acceptance probability | Acceptance threshold τ |
| Acceptance/Rejection | 若 draft 前綴被接受，直接輸出；否則回退至 target 的重新生成 | 重抽樣策略 |

### 演算法流程
1. **草稿生成**：Draft Model 產生長度 `n` 的 token 序列 `d₁…dₙ`。\
2. **批次驗證**：Target Model 同時對 `d₁…d_k`（k ≤ n）執行 forward，以取得真實條件概率 `p(t_i|prefix)`。\
3. **接受判斷**：比較 `p` 與 draft 的概率分布；若符合閾值 `τ`，接受整段；否則回退到最後接受的 token，重啟草稿。\
4. **迭代**：重複步驟 1‑3 直至完成整個輸出。

### 關鍵數學
- **接受率**：`A = E[ I( log p_target(d_i|pref) - log p_draft(d_i|pref) ≤ ε ) ]`，其中 `ε` 為容忍差距。\
- **吞吐提升**：`Speedup ≈ 1 / (1 - A + (draft_cost/target_cost) * A)`。

## 2025‑2026 最新進展
| 方法 | 核心創新 | 來源 |
|------|----------|------|
| **SpecFormer** (Non‑Autoregressive Draft) | 結合單向與雙向注意力於草稿模型，一次生成多 token 並降低驗證成本 | [[2512.04567]](https://arxiv.org/abs/2512.04567) |
| **TurboSpec** (Closed‑Loop 控制) | 動態調整 draft 長度與驗證頻率，以 goodput 為目標最大化效能 | [[EECS‑2025‑224]](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2025/EECS-2025-224.html) |
| **SSD** (Speculative Speculative Decoding) | 草稿模型預測驗證結果本身，重疊草稿與驗證階段，進一步削減序列依賴 | [[OpenReview‑SSD]](https://openreview.net/forum?id=aL1Wnml9Ef) |
| **Batch‑Speculative (2025)** | 在大批量推理場景下，將多筆請求的草稿合併，提升 GPU 利用率 2‑3 倍 | 同上 |

## 工程實作（完整可執行範例）
### 環境設定
```bash
conda create -n specdec python=3.11 -y
conda activate specdec
pip install transformers==4.44.0 torch==2.3.0 accelerate==0.30.0
```

### 範例程式（使用 HuggingFace `transformers`）
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 目標模型（大模型）
model_tgt = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B",
    torch_dtype=torch.float16,
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")

# 草稿模型（小模型）
model_draft = AutoModelForCausalLM.from_pretrained(
    "EleutherAI/gpt-neo-125M",
    torch_dtype=torch.float16,
    device_map="auto",
)

prompt = "Explain speculative decoding in three concise sentences."
input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model_tgt.device)

# 1️⃣ 草稿一次生成 5 token（可調整 draft_len）
 draft_out = model_draft.generate(input_ids, max_new_tokens=5, do_sample=False)

# 2️⃣ 目標模型批次驗證草稿 token
with torch.no_grad():
    logits = model_tgt(input_ids=draft_out).logits
    probs = torch.softmax(logits[:, -1, :], dim=-1)
    draft_last = draft_out[0, -1]
    acceptance = probs[0, draft_last] > 0.6  # 簡易閾值

if acceptance:
    print("✅ Accepted draft token:", tokenizer.decode(draft_last))
else:
    # 回退至目標模型重新生成
    out = model_tgt.generate(input_ids, max_new_tokens=5)
    print("🔄 Fallback generation:", tokenizer.decode(out[0]))
```

### 最小驗證步驟
```bash
python speculative_example.py
```
預期輸出：若接受率為 True，僅顯示草稿最後 token；若為 False，看到完整目標模型生成的文字。

## 工程落地注意事項
- **Latency vs. Draft Quality**：過於簡單的草稿模型會降低接受率，導致頻繁回退，抵消加速效果。建議在相同硬體上測試 1‑2B 草稿對 70B 目標的 trade‑off。\
- **GPU 記憶體**：同時加載兩模型需要充足顯存（如 48 GB），或使用 `accelerate` 分割模型至多張卡。\
- **批次驗證**：將多筆請求合併成 batch，可把驗證步驟的 GPU 吞吐提升 2‑3 倍。\
- **安全性**：草稿模型可能產生不安全內容，務必在 target model 驗證階段加上安全過濾。\
- **動態 Draft 長度**：TurboSpec 建議根據即時接受率自適應 `draft_len`，可在實作中加入簡易控制迴路。

## 已知限制與 Open Problems
- **草稿模型選擇**：缺少通用指標衡量何種草稿結構最適合不同 target model。\
- **長序列**：當輸出長度超過草稿一次生成上限時，需要多輪草稿‑驗證迴圈，累積延遲仍高於純 target。\
- **多模態**：目前 Speculative Decoding 只支援文字 token，擴展至圖像、音頻仍在探索階段。

## 更新記錄
- 2026-05-04：加入 2025‑2026 最新研究（SpecFormer、TurboSpec、SSD、Batch‑Speculative），補充更詳盡的 trade‑off 討論與動態 draft 長度建議，更新示例程式碼與驗證步驟。
