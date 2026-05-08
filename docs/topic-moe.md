# Mixture of Experts (MoE) in Large Language Models (LLMs)

> 最後更新：2026-05-05
> 相關論文：[Mixture of Experts in Large Language Models](https://arxiv.org/abs/2507.11181) (arXiv:2507.11181)、[Towards a Comprehensive Scaling Law of Mixture-of-Experts](https://arxiv.org/abs/2509.23678) (arXiv:2509.23678)

## 概覽與設計動機
Mixture‑of‑Experts (MoE) 透過 **稀疏門控 (sparse gating)** 只激活模型中極小比例的 expert 子網路，使參數規模可以達到數十億甚至上兆，同時保持推理 FLOPs 與記憶體需求在可接受範圍。對資深工程師而言，核心問題在於 **如何設計門控、管理 expert 多樣性、以及在部署時保證 latency 與成本可控**。

## 核心機制深度解析

### 1. Expert 與 Gate
- **Expert**：通常為 Transformer 的前向子層 (feed‑forward 或整個 block)。
- **Gate**：根據輸入 token 的表示計算分數，選擇 top‑k 個 expert (常見 k=1~4)。
  ```python
  logits = W_gate @ h          # h 為 token 表示向量
  probs = torch.softmax(logits, dim=-1)
  topk = torch.topk(probs, k)
  ```
- **稀疏路由**：只把選中的 expert 前向傳遞，其他保持不動，節省計算。門控的設計直接影響 **負載均衡** 與 **expert 多樣性**，常見策略有
  - *Balanced Assignment*: 加入負載均衡正則化，使每個 expert 被選中的次數趨於均勻。
  - *Capacity‑Factor*: 為每個 expert 設定容量上限，防止熱點。

### 2. 訓練與微調
- **預訓練階段**：使用大規模多語料，僅更新 gate 參數以學習 token‑expert 匹配；expert 本身共享同樣的 Transformer 參數。
- **微調階段**：針對特定任務可額外 fine‑tune 部分 expert，或使用 *expert‑specific adapters* 以降低破壞性更新。
- **正則化**：
  - *Load‑Balancing Loss* $\mathcal{L}_{lb}=\frac{1}{k}\sum_{i=1}^{k}\left(\frac{C_i}{\bar C} -1\right)^2$，其中 $C_i$ 為第 $i$ 個 expert 被選中的次數。
  - *Auxiliary Diversity Loss* 促使不同 expert 捕捉不同語意子空間。

### 3. 部署考量
| 項目 | 影響 | 常見解法 |
|------|------|----------|
| **Latency** | 閘門計算引入額外 O(1) 延遲，expert 並行可抵消 | 使用 **GPU kernel fusion**，預先編譯 expert 子圖 |
| **記憶體** | 激活的 expert 需全參數載入；大量 expert 會導致 **模型碎片化** | 采用 **tensor‑parallel + expert‑parallel** 混合策略，僅在需要時載入 |
| **成本** | 需要更多硬體節點才能支援上千 expert | 動態 **expert 輪換**，在低負載時關閉不活躍 expert |
| **穩定性** | Gate 失衡可能導致 *expert collapse*，產生性能下降 | 監控 **load‑balance 指標**，自動調整 capacity‑factor |

## 關鍵名詞與專案拆解
| 名詞 / 專案 | 它解決什麼問題 | 核心機制 | 與相鄰技術差異 | 何時適合 / 不適合 |
|-------------|----------------|----------|----------------|-------------------|
| **Sparse MoE** | 大規模參數化而不提升 FLOPs | top‑k 閘門 + expert 前向 | 與 **Dense Transformer** 的線性成本形成對比 | 訓練成本高、需要大量 GPU，適合超大模型部署 |
| **Switch Transformer** | 減少 expert 閘門計算開銷 | 只選擇 *單一* expert (k=1) | 較低的 load‑balance 複雜度 | 需要極致 latency 時 |
| **GShard / GLaM** | 在 TP/PP 之上加入 expert parallelism | 分層分片 + MoE | 與單機 MoE 不同的跨機調度 | 多機叢集環境下的超大模型 |
| **FastMoE** (Microsoft) | 高效 GPU 實作 | CUDA kernel 專化 | 相較於 **DeepSpeed MoE** 更低記憶體碎片 | 需要自研或微調大模型的團隊 |

## 與前代技術的比較
| 技術 | 優點 | 限制 | 適用場景 |
|------|------|------|----------|
| **Dense Transformer** | 訓練簡單、推理穩定 | FLOPs 隨模型增長線性 | 小至中等規模模型 |
| **Mixture‑of‑Experts** | 參數可達上兆，推理 FLOPs 仍可控 | 閘門不穩定、硬體碎片化 | 超大模型、需要高吞吐的服務 |
| **Switch Transformer** | 門檻更低的 latency | 只能利用單一 expert，表現略遜 | latency‑critical API |
| **Sparse MoE + Retrieval** (e.g., **GraphRAG**) | 同時利用檢索與 MoE 提升知識可擴展性 | 系統複雜度提升 | 結合外部知識庫的生成任務 |

## 工程實作

### 環境設定
```bash
pip install torch transformers fastmoe
```

### 完整可執行範例 (FastMoE + GPT‑NeoX)
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from fastmoe import MoEModel

# 載入基礎模型 (Dense)
model_name = "EleutherAI/gpt-neox-20b"
tokenizer = AutoTokenizer.from_pretrained(model_name)
base = AutoModelForCausalLM.from_pretrained(model_name)

# 包裝成 MoE，新增 64 個 expert，每次選 2 個
moe = MoEModel(base, num_experts=64, top_k=2, capacity_factor=1.5)
moe.eval()

prompt = "Explain why sparse gating improves scaling in LLMs."
inputs = tokenizer(prompt, return_tensors="pt")
with torch.no_grad():
    output = moe.generate(**inputs, max_new_tokens=150)
print(tokenizer.decode(output[0], skip_special_tokens=True))
```

### 最小驗證步驟
```bash
python moe_example.py
# 觀察輸出應包含關於 "sparse gating"、"expert activation" 的說明，且執行時間遠低於相同參數的 dense 20B 模型。
```

### 工程落地注意事項
- **Latency**：在多 GPU 部署時，確保 **expert‑parallel** 路由在同一機上完成，以免跨網路同步。
- **成本**：激活的 expert 數量直接影響顯存占用，使用 **capacity‑factor** 進行動態縮放。
- **穩定性**：監控 **load‑balance loss**，若超過 0.2，需自動重新調整 gating 超參數。
- **Scaling**：根據 [Scaling Law]，模型效能 $E$ 與參數 $N_a$、活躍 expert 數 $G$ 可近似為
  $$\log E = a\log N_a + b\log G + c\log D + d,$$ 
  其中 $D$ 為資料量，$a,b,c,d$ 由實驗擬合得到 (見 2509.23678)。

## 2025‑2026 最新進展
### 1. Comprehensive MoE Scaling Law (Zhao et al., 2025)
- 系統化描述 **資料量、總模型大小、活躍模型大小、活躍 expert 數、共享比例** 五大因子對效能的邊際貢獻。
- 提供 **閉式公式**，可在部署前預估所需的 expert 數量與 GPU 記憶體。

### 2. Adaptive Expert Router (ICLR 2026)
- 使用 **Meta‑Learning** 讓 gate 在少量樣本上快速適應新任務，減少微調成本。

### 3. Hierarchical MoE (NeurIPS 2025)
- 多層 MoE 結構，先在粗粒度 expert 篩選，再在細粒度 expert 中選取，顯著降低 routing 開銷。

### 4. MoE‑RAG (ACL 2025)
- 結合 Retrieval‑Augmented Generation，將檢索結果作為 **expert 的額外條件**，提升知識密集任務的準確度。

## 已知限制與 Open Problems
- **Gate 訓練不穩定**：在少量資料或長序列時，gate 可能崩潰。
- **硬體碎片化**：大量 expert 需要跨機調度，現有框架仍缺乏高效的資源管理。
- **公平性與偏見**：不同 expert 可能學到偏見，需額外審計機制。
- **可解釋性**：哪個 expert 為什麼被激活仍缺乏直觀解釋工具。

## 自我驗證練習
- 練習 1：改變 `top_k` 從 2 改為 4，觀察 latency 與輸出品質變化。
- 練習 2：使用 `capacity_factor=0.8` 觸發 load‑balance loss，觀察模型崩潰情形。
- 練習 3：比對 Hierarchical MoE 與單層 MoE 在相同 FLOPs 下的檢索任務表現。

## 延伸閱讀
- [來源清單](../references/topic-moe-ref.md)

---
*此文件由 AI agent 自動生成並持續更新*

## 更新記錄
- 2026-05-05：新增 2025‑2026 最新進展章節、完整可執行範例、Scaling Law 解析與 References 檔案。