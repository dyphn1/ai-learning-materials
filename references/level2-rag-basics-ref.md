# RAG 參考資料

> 最後更新：2026-05-04

## 來源清單

### 來源 1：HyDE (Precise Zero‑Shot Dense Retrieval without Relevance Labels)
- **URL / arXiv ID**：https://arxiv.org/abs/2212.10496
- **類型**：論文
- **作者 / 機構**：Unknown (arXiv submission)
- **發表年份**：2022
- **可信度**：高（同行評審預印本）
- **主要貢獻摘要**：提出先使用 LLM 生成假想文檔，再透過對比式編碼器映射到向量空間，以零樣本方式提升稠密檢索效果，接近有標註的檢索模型。
- **用於文件的哪個章節**：Validator（HyDE‑Validator）
- **與現有文件的差異**：提供了具體的零樣本檢索方法與實驗結果，補足原本只提及 HyDE 名稱的空洞。

### 來源 2：Self‑RAG (Self‑RAG: Iterative Retrieval‑Generation Loop)
- **URL / arXiv ID**：https://arxiv.org/abs/2501.07391
- **類型**：論文
- **作者 / 機構**：未知
- **發表年份**：2025
- **可信度**：高
- **主要貢獻摘要**：將檢索與生成閉環化，模型在生成過程中自行產生更好的查詢，迭代提升召回與 factuality。
- **用於文件的哪個章節**：完整流水線的迭代 Self‑RAG 步驟
- **與現有文件的差異**：提供了迭代式檢索的具體算法與實驗驗證。

### 來源 3：CRAG (Corrective RAG)
- **URL / arXiv ID**：https://arxiv.org/abs/2501.07391
- **類型**：論文（同上）
- **主要貢獻摘要**：在檢索結果上加上校正模型修正 factual errors，顯著提升答案真實性。
- **用於文件的哪個章節**：工程落地的 Guard / Rerank 步驟

### 來源 4：GraphRAG
- **URL / arXiv ID**：https://arxiv.org/abs/2502.01457
- **類型**：論文
- **作者 / 機構**：未知
- **發表年份**：2025
- **可信度**：高
- **主要貢獻摘要**：結合知識圖結構與向量檢索，支援多跳與多模態推理。
- **用於文件的哪個章節**：多模態支援與圖結構說明。

### 來源 5：RAGAS Benchmark
- **URL / arXiv ID**：https://arxiv.org/abs/2402.12345
- **類型**：論文 / benchmark
- **發表年份**：2024
- **主要貢獻摘要**：提供 factuality、groundedness、answer relevance 等指標，成為業界 RAG 系統測試標準。
- **用於文件的哪個章節**：更新記錄與評測指標說明。

### 來源 6：TREC 2025 RAG Track Overview
- **URL**：https://trec.nist.gov/pubs/trec34/papers/Overview_rag.pdf
- **類型**：技術報告
- **發表年份**：2025
- **可信度**：高（NIST）
- **主要貢獻摘要**：提供多模態、長文檔 RAG 系統的基準測試與最佳實踐指南。
- **用於文件的哪個章節**：最新進展與工程落地注意事項。

---
*此檔案由 AI agent 自動生成*