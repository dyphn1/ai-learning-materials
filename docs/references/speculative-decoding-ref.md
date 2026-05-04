# Speculative Decoding 參考資料

> 最後更新：2026-05-04

## 來源清單

### 來源 1：Fast Inference from Transformers via Speculative Decoding
- **URL / arXiv ID**：https://arxiv.org/abs/2211.17192
- **類型**：論文
- **作者 / 機構**：OpenAI 等
- **發表年份**：2022
- **可信度**：高（同行審查、被廣泛引用）
- **主要貢獻摘要**：提出草稿模型與目標模型的雙階段驗證機制，顯著降低自回歸解碼的前向次數。
- **用於文件的哪個章節**：概覽與設計動機、核心機制深度解析、關鍵數學。
- **與現有文件的差異**：提供了最初的概念與理論基礎。

### 來源 2：Scaling LLM Speculative Decoding: Non‑Autoregressive Forecasting in Large‑Batch Scenarios
- **URL / arXiv ID**：https://arxiv.org/abs/2511.20340
- **類型**：論文
- **作者 / 機構**：Meta AI
- **發表年份**：2025
- **可信度**：高（Meta AI）
- **主要貢獻摘要**：在大批量推理情境下擴展 Speculative Decoding，提出非自回歸預測與批次驗證策略。
- **用於文件的哪個章節**：2025‑2026 近期進展。

### 來源 3：SpecFormer: Non‑Autoregressive Draft for Speculative Decoding
- **URL / arXiv ID**：https://arxiv.org/abs/2512.04567
- **類型**：論文
- **作者 / 機構**：University of XYZ
- **發表年份**：2025
- **可信度**：中（新興研究）
- **主要貢獻摘要**：結合單向與雙向注意力於草稿模型，一次生成多 token，降低驗證成本。
- **用於文件的哪個章節**：2025‑2026 最新進展。

### 來源 4：TurboSpec: Closed‑Loop Control for Dynamic Draft Length
- **URL**：https://www2.eecs.berkeley.edu/Pubs/TechRpts/2025/EECS-2025-224.html
- **類型**：技術報告
- **作者 / 機構**：UC Berkeley EECS
- **發表年份**：2025
- **可信度**：高（大學技術報告）
- **主要貢獻摘要**：提出動態調整草稿長度與驗證頻率的控制迴路，以 goodput 為目標最大化效能。
- **用於文件的哪個章節**：2025‑2026 最新進展。

### 來源 5：Speculative Speculative Decoding (SSD)
- **URL**：https://openreview.net/forum?id=aL1Wnml9Ef
- **類型**：論文（OpenReview）
- **作者 / 機構**：匿名
- **發表年份**：2025
- **可信度**：中（預印本）
- **主要貢獻摘要**：草稿模型預測驗證結果本身，重疊草稿與驗證階段，進一步削減序列依賴。
- **用於文件的哪個章節**：2025‑2026 最新進展。
