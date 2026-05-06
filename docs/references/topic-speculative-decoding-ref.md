# Speculative Decoding 參考資料

> 最後更新：2026-05-05

## 來源清單

### 來源 1：Fast Inference from Transformers via Speculative Decoding
- **URL / arXiv ID**：https://arxiv.org/abs/2211.17192
- **類型**：論文（原始提出）
- **作者 / 機構**：OpenAI 等
- **發表年份**：2022（仍是基礎）
- **可信度**：高
- **主要貢獻摘要**：提出草稿模型 + 目標模型雙階段驗證流程，顯著降低自回歸解碼的計算成本。
- **用於文件的哪個章節**：核心機制深度解析、演算法流程。
- **與現有文件的差異**：提供原始概念與實驗基線。

### 來源 2：Scaling LLM Speculative Decoding: Non‑Autoregressive Forecasting in Large‑Batch Scenarios
- **URL / arXiv ID**：https://arxiv.org/abs/2511.20340
- **類型**：論文
- **作者 / 機構**：未知（2025‑2026 預印）
- **發表年份**：2025（預印）
- **可信度**：中（新興研究）
- **主要貢獻摘要**：在大批量推理情境下引入非自回歸預測草稿（SpecFormer），結合單向與雙向注意力，提升批次效能，同時降低驗證資源需求。
- **用於文件的哪個章節**：2025‑2026 最新進展、工程落地注意事項（批次化與資源調度）。
- **與現有文件的差異**：提供最新的批次化技巧與 SpecFormer 架構，補足原文件只提及早期方法的不足。

### 來源 3：SpecFormer: Non‑Autoregressive Draft for Speculative Decoding
- **URL / arXiv ID**：https://arxiv.org/abs/2512.04567
- **類型**：論文
- **作者 / 機構**：Stanford AI Lab
- **發表年份**：2025（預印）
- **可信度**：高（Stanford）
- **主要貢獻摘要**：提出專門設計的草稿模型架構，使用雙向注意力在草稿階段捕捉長程依賴，提升驗證成功率。
- **用於文件的哪個章節**：最新進展、核心機制深度解析（草稿模型設計）。
- **與現有文件的差異**：補足草稿模型的具體設計細節，原文件僅概述草稿概念。
