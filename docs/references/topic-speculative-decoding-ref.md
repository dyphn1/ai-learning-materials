# Speculative Decoding 參考資料

> 最後更新：2026-04-26

## 來源清單

### 來源 1：Fast Inference from Transformers via Speculative Decoding
- **URL / arXiv ID**：https://arxiv.org/abs/2211.17192 或 arXiv:2211.17192
- **類型**：論文
- **作者 / 機構**：Yaniv Leviathan, Matan Kalman, Yossi Matias
- **發表年份**：2023
- **可信度**：高（ICML 2023 Oral，原始演算法論文）
- **主要貢獻摘要**：論文提出 speculative decoding，利用較便宜的 approximation model 先草擬多個 token，再由 target model 並行驗證，並透過新的採樣程序保持最終分布不變。其重要價值在於證明這不是啟發式加速，而是 distribution-preserving 的 exact acceleration。論文在 T5-XXL 上展示約 2X-3X 加速，且不需要修改主模型架構。
- **用於文件的哪個章節**：概覽與設計動機、演算法流程、關鍵數學
- **與現有文件的差異**：提供 acceptance / rejection 與重採樣的理論核心，讓文件不只停留在「小模型先猜、大模型驗證」的口語描述。

### 來源 2：Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads
- **URL / arXiv ID**：https://arxiv.org/abs/2401.10774 或 arXiv:2401.10774
- **類型**：論文
- **作者 / 機構**：Tianle Cai, Yuhong Li, Zhengyang Geng, Hongwu Peng, Jason D. Lee, Deming Chen, Tri Dao
- **發表年份**：2024
- **可信度**：高（後續 inference acceleration 代表工作）
- **主要貢獻摘要**：Medusa 不再依賴獨立 draft model，而是在同一 backbone 上增加多個 decoding heads 並配合 tree-based attention 一次驗證多個候選延續。這讓 speculative family 的方法從雙模型協作擴展成單模型多頭加速路線。論文同時提供 Medusa-1 與 Medusa-2 兩種訓練模式，分別對應 lossless acceleration 與更高速度增益。
- **用於文件的哪個章節**：關鍵名詞與專案拆解、2025-2026 最新進展
- **與現有文件的差異**：補上「不想維護獨立 draft model 時還有哪些替代路線」這個工程決策點。

### 來源 3：TGI Speculation Documentation
- **URL / arXiv ID**：https://huggingface.co/docs/text-generation-inference/en/conceptual/speculation
- **類型**：官方文件
- **作者 / 機構**：Hugging Face Text Generation Inference Team
- **發表年份**：2026 文件版本
- **可信度**：高（主流 serving stack 官方文件）
- **主要貢獻摘要**：文件把 speculative decoding、assisted generation、Medusa 視為同一類 runtime acceleration idea，並清楚整理 TGI 支援的兩條主線：Medusa 與 n-gram speculation。其工程價值在於展示哪些情況下 n-gram speculation 能以極低導入成本獲得收益，以及如何透過 `--speculate` 等配置直接啟用服務端 speculation。
- **用於文件的哪個章節**：工程落地注意事項、2025-2026 最新進展
- **與現有文件的差異**：把 speculative decoding 從研究方法拉到真實 serving stack 配置與場景適配層次。

### 來源 4：vLLM Speculative Decode Documentation Attempt
- **URL / arXiv ID**：https://docs.vllm.ai/en/latest/features/spec_decode.html
- **類型**：官方文件
- **作者 / 機構**：vLLM Development Team
- **發表年份**：2026 文件版本
- **可信度**：中（官方來源，但此次抓取未成功）
- **主要貢獻摘要**：本次抓取嘗試未能成功抽出可用內容，因此沒有直接用於正文撰寫。之所以仍記錄，是因為它是本輪探索過的實際來源，符合 references 全量保存規則。後續若需要補 vLLM 實作細節，可再以人工閱讀或不同抓取方式補齊。
- **用於文件的哪個章節**：未直接使用
- **與現有文件的差異**：保留探索歷程，避免之後誤以為該來源未被檢查過。

## 論文詳細記錄

### Fast Inference from Transformers via Speculative Decoding
- **論文標題**：Fast Inference from Transformers via Speculative Decoding
- **DOI / arXiv 連結**：https://doi.org/10.48550/arXiv.2211.17192
- **核心演算法名稱**：Speculative Decoding

### Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads
- **論文標題**：Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads
- **DOI / arXiv 連結**：https://doi.org/10.48550/arXiv.2401.10774
- **核心演算法名稱**：Medusa Multi-Head Speculation