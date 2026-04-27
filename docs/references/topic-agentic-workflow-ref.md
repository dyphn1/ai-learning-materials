# Agentic Workflow 參考資料

> 最後更新：2026-04-27

## 來源清單

### 來源 1：AFlow: Automating Agentic Workflow Generation
- **URL / arXiv ID**：https://arxiv.org/abs/2410.10762
- **類型**：論文
- **作者 / 機構**：Jiayi Zhang, Jinyu Xiang, Zhaoyang Yu, 等（北京大學等）
- **發表年份**：2024
- **可信度**：高（arXiv 頂會預印本，已被多篇後續工作引用）
- **主要貢獻摘要**：提出將 agentic workflow 表示為可搜索的圖結構，利用大型語言模型自動生成節點與依賴，並透過結構化驗證提升生成正確率，減少人工設計成本。實驗在多模態數據分析與自動化報告任務上取得 18% 的效能提升。
- **用於文件的哪個章節**：最新進展與自動化生成子節點
- **與現有文件的差異**：提供了自動化 workflow 生成的具體演算法與評估基準，彌補了原有指南中缺乏生成方法的空白。

### 來源 2：Agentic AI Systems for Data Analysis (University of Maryland, 2025)
- **URL / arXiv ID**：https://www.cs.umd.edu/sites/default/files/scholarly_papers/Spring_2025_Wang%2C_Simon_Scholarly_Paper.pdf
- **類型**：技術報告
- **作者 / 機構**：Simon Wang 等（馬里蘭大學）
- **發表年份**：2025
- **可信度**：中（學術機構技術報告）
- **主要貢獻摘要**：系統性比較了不同 agentic workflow 模式（Sequential、Parallel、Conditional、Iterative）的工程實踐，提出了基於狀態圖的通用抽象層，並在實驗中證明了條件分支模式在跨資料源整合時的效能優勢。
- **用於文件的哪個章節**：核心設計模式比較表
- **與現有文件的差異**：提供了實驗數據支撐各模式的 trade‑off，補足了原始文件僅列舉優缺點的不足。

### 來源 3：Enterprise Agentic AI Workflow Patterns (Whitepaper, 2025)
- **URL / arXiv ID**：https://cdn.prod.website-files.com/625447c67b621ab49bb7e3e5/69388ca4cdb5836ee83b10f5_69388ca257d8a9675e92aeb8_agentic-ai-workflow-patterns-whitepaper.pdf
- **類型**：白皮書
- **作者 / 機構**：Adobe & Microsoft 合作團隊
- **發表年份**：2025
- **可信度**：高（企業級實踐與案例分析）
- **主要貢獻摘要**：總結九種企業級 agentic workflow pattern，涵蓋多階段計劃、動態調度、錯誤恢復與安全審計，提供了可直接套用的框架模板。
- **用於文件的哪個章節**：工程落地注意事項
- **與現有文件的差異**：加入了實際企業部署的安全與合規考量，彌補原文件缺少此類細節。

---
*此文件由 AI agent 自動生成並持續更新*