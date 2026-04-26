# Fine-tuning 參考資料

> 最後更新：2026-04-26

## 來源清單

### 來源 1：LoRA: Low-Rank Adaptation of Large Language Models
- **URL / arXiv ID**：https://arxiv.org/abs/2106.09685 或 arXiv:2106.09685
- **類型**：論文
- **作者 / 機構**：Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen
- **發表年份**：2021
- **可信度**：高（參數高效微調代表論文）
- **主要貢獻摘要**：LoRA 提出將權重更新表示為低秩矩陣分解，凍結原始模型權重，只訓練小型 adapter 矩陣。論文顯示在 GPT-3 175B 等大型模型上，LoRA 可以把可訓練參數量降低約 10,000 倍，同時保持接近甚至優於 full fine-tuning 的效果。其工程價值在於大幅降低儲存與切換不同任務版本的成本。
- **用於文件的哪個章節**：概覽與設計動機、關鍵數學、與前代技術的比較
- **與現有文件的差異**：補上 PEFT 路線的數學核心，而不是只把 LoRA 當成一個框架名詞。

### 來源 2：QLoRA: Efficient Finetuning of Quantized LLMs
- **URL / arXiv ID**：https://arxiv.org/abs/2305.14314 或 arXiv:2305.14314
- **類型**：論文
- **作者 / 機構**：Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, Luke Zettlemoyer
- **發表年份**：2023
- **可信度**：高（低成本 LLM 微調代表論文）
- **主要貢獻摘要**：QLoRA 在 4-bit quantized backbone 上訓練 LoRA adapters，並引入 NF4、double quantization 與 paged optimizers，使 65B 模型可在單張 48GB GPU 上完成微調，同時維持接近 16-bit fine-tuning 的表現。它最重要的工程意義，是把大型模型微調從高門檻叢集作業推向單卡可行。
- **用於文件的哪個章節**：關鍵名詞與專案拆解、工程落地注意事項、2025-2026 最新進展
- **與現有文件的差異**：補上為什麼 QLoRA 不是單純「LoRA + 量化」，而是一組完整的記憶體管理設計。

### 來源 3：Direct Preference Optimization: Your Language Model is Secretly a Reward Model
- **URL / arXiv ID**：https://arxiv.org/abs/2305.18290 或 arXiv:2305.18290
- **類型**：論文
- **作者 / 機構**：Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, Chelsea Finn
- **發表年份**：2023，2024 更新版本
- **可信度**：高（alignment / preference optimization 代表工作）
- **主要貢獻摘要**：DPO 把 RLHF 的 reward model + PPO pipeline 轉成更直接的 preference optimization 問題，使用 closed-form objective 直接學會偏好對齊。它的價值不只是訓練更簡單，而是大幅降低 alignment pipeline 的工程複雜度，使偏好對齊更容易進入一般團隊的實作範圍。
- **用於文件的哪個章節**：關鍵數學、與前代技術的比較、2025-2026 最新進展
- **與現有文件的差異**：補上 fine-tuning 不只等於 SFT，還包含 alignment 階段的方法選擇。

### 來源 4：PEFT Documentation
- **URL / arXiv ID**：https://huggingface.co/docs/peft/index
- **類型**：官方文件
- **作者 / 機構**：Hugging Face
- **發表年份**：2026 文件版本
- **可信度**：高（主流開源工具官方文件）
- **主要貢獻摘要**：PEFT 文件系統化整理了參數高效微調方法，並說明其與 Transformers、Diffusers、Accelerate 等生態系的整合方式。對工程團隊而言，這份文件的價值在於把 adapter-based fine-tuning 變成可維護、可部署的標準工程能力，而不是零散腳本。
- **用於文件的哪個章節**：工程實作、2025-2026 最新進展
- **與現有文件的差異**：補上從研究方法到開源工具鏈的橋接，使主文範例可以落在真實可用的 API 之上。

### 來源 5：TRL Documentation
- **URL / arXiv ID**：https://huggingface.co/docs/trl/index
- **類型**：官方文件
- **作者 / 機構**：Hugging Face TRL Team
- **發表年份**：2026 文件版本
- **可信度**：高（主流 post-training / alignment 工具官方文件）
- **主要貢獻摘要**：TRL 文件把 post-training 方法分成 offline methods、online methods、reward modeling 與 knowledge distillation，並提供 DPO、ORPO、GRPO、Online DPO 等 trainer。這說明 2025-2026 的對齊實務已從單一路線走向方法工具箱化，工程團隊可以更系統地選擇與比較訓練策略。
- **用於文件的哪個章節**：2025-2026 最新進展、工程落地注意事項
- **與現有文件的差異**：補上最新 post-training 工具生態，不讓文件停留在只有 LoRA / QLoRA 的 2023 視角。

## 論文詳細記錄

### LoRA: Low-Rank Adaptation of Large Language Models
- **論文標題**：LoRA: Low-Rank Adaptation of Large Language Models
- **DOI / arXiv 連結**：https://doi.org/10.48550/arXiv.2106.09685
- **核心演算法名稱**：LoRA

### QLoRA: Efficient Finetuning of Quantized LLMs
- **論文標題**：QLoRA: Efficient Finetuning of Quantized LLMs
- **DOI / arXiv 連結**：https://doi.org/10.48550/arXiv.2305.14314
- **核心演算法名稱**：QLoRA

### Direct Preference Optimization: Your Language Model is Secretly a Reward Model
- **論文標題**：Direct Preference Optimization: Your Language Model is Secretly a Reward Model
- **DOI / arXiv 連結**：https://doi.org/10.48550/arXiv.2305.18290
- **核心演算法名稱**：DPO