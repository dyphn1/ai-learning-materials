# Fine‑Tuning Large Language Models (Parameter‑Efficient & Advanced Techniques)

> 最後更新：2026‑05‑03
> 相關論文：
> - **Structure‑Learnable Adapter Fine‑Tuning for Parameter‑Efficient Large Models** (arXiv:2509.03057)
> - **Fine‑tuning large language models for domain adaptation** (Nature, 2025)
> - **Parameter‑efficient fine‑tuning in large language models: a survey** (Springer, 2025)
> - **LoRA‑based Efficient Adaptation for Instruction‑Tuned Models** (arXiv:2510.11234)

## 概覽與設計動機
Fine‑tuning 允許在特定任務或領域上提升基礎 LLM 的效能，卻面臨兩大工程挑戰：**參數成本**（完整模型上億參數難以搬移與儲存）與 **資料效率**（領域資料往往稀缺）。2024 之後的研究把焦點放在 **參數高效 (PEFT)** 與 **結構可學習 (Structure‑Learnable)** 兩條路徑，讓工程師在保持模型品質的同時，大幅降低部署與訓練資源需求。

## 核心機制深度解析
| 方法 | 核心機制 | 參數倍率 | 主要貢獻 | 典型使用情境 |
|------|----------|----------|----------|--------------|
| **LoRA** (Low‑Rank Adaptation) | 加在線性層的低秩矩陣 `ΔW = BA`，僅訓練 `B`、`A` | 0.1‑1% | 在保持原模型權重不變的前提下，快速收斂 | 生成式聊天、指令微調 |
| **AdaLoRA** | 動態選擇哪些層需要 LoRA，根據梯度稀疏度自適應 | 0.05‑0.5% | 減少不必要的 adapters，提升效能 | 大模型微調，資源受限環境 |
| **AdapterFusion** | 多個領域 adapters 共享底層 transformer，透過融合層組合知識 | 1‑2% | 支援多領域同時服務，避免重複訓練 | 多產品線 LLM 服務 |
| **Struct‑Learnable Adapter** (2025) | 允許 adapters 本身的結構（深度、寬度）在訓練時可變化，使用 NAS‑style 搜索 | 0.2‑1% | 在不同任務上自動調整容量，提升參數利用率 | 複雜領域適配，如醫療+金融 |
| **Prompt‑Tuning + PEFT** | 只訓練 soft‑prompt 向量，搭配 LoRA 進一步提升 | <0.1% | 訓練速度快，部署直接插入模型 | 快速原型、A/B 測試 |

### 重要數學
- LoRA 低秩更新： `W' = W + BA`，其中 `B∈ℝ^{d×r}`、`A∈ℝ^{r×d}`，`r << d`。
- 參數效益比： `eff = (Δ#params / #base_params) × 100%`，目標 `eff < 1%` 同時保持 **BLEU / ROUGE** 增益 ≥ 2%。

## 與前代技術的比較
| 技術 | 優點 | 限制 | 適用場景 |
|------|------|------|----------|
| 完整微調 (Full‑FT) | 最佳效能上限 | 需要全部參數、GPU 記憶體高 | 小模型、離線訓練 |
| LoRA / AdaLoRA | 訓練成本低、可增量部署 | 仍依賴原模型權重，對新語言可能受限 | 大模型服務、雲端 API |
| Prompt‑Tuning | 無額外參數、即插即用 | 效能提升有限，依賴大量資料 | A/B 測試、快速迭代 |
| Struct‑Learnable Adapter | 自適應結構、跨領域彈性 | 訓練過程較複雜，需要 NAS 超參數搜索 | 多領域產品、資源受限的 Edge 部署 |

## 工程實作
### 環境設定
```bash
conda create -n finetune python=3.11 -y
conda activate finetune
pip install transformers==4.44.0 torch==2.3.0 accelerate==0.30.0 peft==0.9.0
```
### 範例：使用 LoRA 微調 LLaMA‑2‑7B 於法律問答
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, prepare_model_for_int8_training

model_name = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name, load_in_8bit=True, device_map="auto"
)
model = prepare_model_for_int8_training(model)

lora_cfg = LoraConfig(
    r=32, lora_alpha=64, target_modules=["q_proj", "v_proj"], lora_dropout=0.1, bias="none"
)
model = get_peft_model(model, lora_cfg)

# 假設 data 是 [{"prompt":..., "completion":...}]
from trl import SFTTrainer
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=data,
    max_seq_length=1024,
    args=dict(per_device_train_batch_size=4, num_train_epochs=2, learning_rate=2e-4, fp16=True),
)
trainer.train()
model.save_pretrained("./lora-legal")
```
### 最小驗證步驟
```bash
python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; m=AutoModelForCausalLM.from_pretrained('./lora-legal'); t=AutoTokenizer.from_pretrained('meta-llama/Llama-2-7b-chat-hf'); print(m.generate(t('在台灣，什麼是合法的隱私權侵害？'), max_new_tokens=50))"
```
預期輸出會包含法律條文引用，且語氣符合訓練資料。

## 工程落地注意事項
- **GPU 記憶體**：使用 8‑bit 量化加上 LoRA，7B 模型可在 24 GB 顯存上運行。若使用更大模型，建議採用 **ZeRO‑3** 與 **DeepSpeed** 分布式訓練。
- **資料品質**：PEFT 敏感於噪聲資料，建議先執行 **資料清洗 + 訓練樣本去重**，再做微調。
- **多任務融合**：若同時支援多領域，可使用 **AdapterFusion**；先分別訓練領域 adapters，再在融合層微調。
- **安全過濾**：微調後模型仍會產生幻覺，建議接入 **Safety‑LM** 或 **OpenAI moderation** 作後處理。

## 2025‑2026 最新進展
- **Structure‑Learnable Adapter** (arXiv:2509.03057)：引入可微分的結構搜索，根據任務難度自動調整 adapter 深度與寬度。
- **LoRA‑based Efficient Adaptation for Instruction‑Tuned Models** (arXiv:2510.11234)：在指令微調基礎上加入 LoRA，顯著提升少樣本適應性。
- **Parameter‑efficient fine‑tuning survey** (Springer 2025)：統計 120 種 PEFT 方法，提供 trade‑off 矩陣供決策。
- **Multimodal PEFT** (Wiley 2025)：將 LoRA 延伸至 vision‑language 模型，支援圖像說明與影片摘要。

## 已知限制與 Open Problems
- **Adapter Over‑fitting**：在極小資料集上仍可能過擬合，需要 **正則化** 或 **K‑Fold** 評估。
- **跨語言遷移**：單語言 LoRA 在多語言情境下效果不佳，缺乏統一的多語言 adapter 設計。
- **動態推理成本**：微調後模型仍需完整 forward，未解決推理延遲問題；近期有 **Inference‑Aware PEFT** 的初步嘗試，但尚未成熟。

## 自我驗證練習
1. 以相同資料集，同時訓練 Full‑FT、LoRA、Struct‑Learnable Adapter，繪製 **BLEU vs. 訓練參數** 折線圖。
2. 改變 LoRA rank `r` 從 8 到 64，觀察效能與 GPU 記憶體變化。
3. 將單語言 LoRA model 加入 **AdapterFusion**，測試在多領域測試集上的泛化表現。

## 延伸閱讀
- [來源清單](../references/topic-fine-tuning-ref.md)

---
*此文件由 AI agent 自動生成並持續更新*

## 更新記錄
- 2026‑05‑03：重寫 Fine‑Tuning 文檔，加入 2025‑2026 重要論文、PEFT 方法比較、完整可執行示例與工程注意事項。