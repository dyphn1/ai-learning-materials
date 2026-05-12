# GraphRAG 參考資料

> 最後更新：2026-04-24

## 來源清單

### 來源 1：Towards Practical GraphRAG: Efficient Knowledge Graph Construction and Hybrid Retrieval at Scale
- **URL / arXiv ID**：arXiv:2507.03226
- **類型**：論文
- **作者 / 機構**：Sahil Bansal, et al. (SAP)
- **發表年份**：2025
- **可信度**：高（來自企業研究實驗室，具備實際應用經驗）
- **主要貢獻摘要**：
  提出依賴解析取代 LLM 的知識圖建構方法，達到 94% 的 LLM 性能但成本大幅降低，並設計混合檢索策略結合圖遍歷與向量相似度，在企業代碼遷移任務上優於傳統 RAG 15%。
- **用於文件的哪個章節**：核心機制深度解析、工程實作
- **與現有文件的差異**：
  提供了依賴解析的具體實作方法和性能數據，填補了現有文件缺乏建構效率分析的空白

### 來源 2：ApeRAG Production-ready GraphRAG Implementation
- **URL / arXiv ID**：https://github.com/apecloud/ApeRAG
- **類型**：工程部落格
- **作者 / 機構**：ApeCloud Team
- **發表年份**：2025
- **可信度**：高（開源專案，具備生產環境驗證）
- **主要貢獻摘要**：
  實作了完整的 GraphRAG 平台，支援多模態索引、AI Agent 協調、Kubernetes 部署，集成了 LightRAG 的改進版本，實現了企業級的圖檢索增強生成系統。
- **用於文件的哪個章節**：工程實作、核心實作範例
- **與現有文件的差異**：
  提供了實際的部署架構和程式碼範例，展示了如何將 GraphRAG 應用於生產環境

### 來源 3：LightRAG Simple and Fast Retrieval-Augmented Generation
- **URL / arXiv ID**：arXiv:2410.05779
- **類型**：論文
- **作者 / 機構**：Zirui Guo, et al. (HKU)
- **發表年份**：2024
- **可信度**：高（學術界研究，引用數持續增長）
- **主要貢獻摘要**：
  提出輕量級 GraphRAG 架構，使用雙層實體-關係索引加速檢索，簡化了傳統 GraphRAG 的複雜度，在保持推理能力的同时大幅提升查詢效率。
- **用於文件的哪個章節**：2025-2026 最新進展、架構圖
- **與現有文件的差異**：
  提供了輕量級實現的技術細節，這是現有文件完全沒有涵蓋的優化方向

### 來源 4：Microsoft GraphRAG Framework Documentation
- **URL / arXiv ID**：https://microsoft.github.io/graphrag/
- **類型**：程式庫文件
- **作者 / 橋構**：Microsoft Research
- **發表年份**：2025
- **可信度**：高（微軟官方文件）
- **主要貢獻摘要**：
  提供完整的 GraphRAG 框架實作，包含知識圖建構、社群發現、多跳推理等完整功能，支援大型企業知識庫的檢索增強生成。
- **用於文件的哪個章節**：實作框架、延伸閱讀
- **與現有文件的差異**：
  提供了官方框架的使用指南和最佳實踐，填補了現有文件缺乏實際工具介紹的空白

## 論文詳細記錄

### Towards Practical GraphRAG: Efficient Knowledge Graph Construction and Hybrid Retrieval at Scale
- **論文標題**：Towards Practical GraphRAG: Efficient Knowledge Graph Construction and Hybrid Retrieval at Scale
- **DOI / arXiv 連結**：https://arxiv.org/abs/2507.03226
- **核心演算法名稱**：Dependency-based Knowledge Graph Construction, Hybrid Graph Retrieval
- **主要發現**：
  - 依賴解析達到 94% 的 LLM 性能但成本大幅降低
  - 混合檢索策略提升 15% 的檢索精確度
  - 在企業代碼遷移任務上證實了 GraphRAG 的實用價值

### LightRAG: Simple and Fast Retrieval-Augmented Generation
- **論文標題**：LightRAG: Simple and Fast Retrieval-Augmented Generation
- **DOI / arXiv 連結**：https://arxiv.org/abs/2410.05779
- **核心演算法名稱**：Dual-level Entity-Relation Indexing
- **主要發現**：
  - 雙層索引架構大幅提升檢索效率
  - 簡化了傳統 GraphRAG 的複雜度
  - 在多跳推理任務上保持與複雜架構相當的性能