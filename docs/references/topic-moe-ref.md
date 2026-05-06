# Mixture of Experts (MoE) 參考資料

> 最後更新：2026-05-05

## 來源清單

### 來源 1：A Comprehensive Survey of Mixture-of-Experts: Algorithms, Theory, and Applications
- **URL / arXiv ID**：https://arxiv.org/abs/2503.07137
- **類型**：論文
- **作者 / 機構**：Siyuan Mu, Sen Lin 等
- **發表年份**：2025（預印）
- **可信度**：高（arXiv 預印，廣受引用）
- **主要貢獻摘要**：系統性整理 MoE 的演算法、理論基礎與應用，涵蓋門控機制、專家多樣性、訓練技巧與效能評估。
- **用於文件的哪個章節**：核心機制深度解析、關鍵名詞與專案拆解。
- **與現有文件的差異**：提供更完整的門控正則化方法與最新實驗結果，補足原始文件中缺失的訓練穩定性討論。

### 來源 2：Towards a Comprehensive Scaling Law of Mixture-of-Experts
- **URL / arXiv ID**：https://arxiv.org/abs/2509.23678
- **類型**：論文
- **作者 / 機構**：Guoliang Zhao, Yuhan Fu, Shuaipeng Li 等
- **發表年份**：2025（預印）
- **可信度**：高（大量實驗，系統性分析）
- **主要貢獻摘要**：提出 MoE 專屬的縮放律，辨識五個關鍵因素（資料量、總模型大小、激活模型大小、活躍專家數、共享專家比例），並透過 446 場受控實驗量化其影響。
- **用於文件的哪個章節**：最新進展、工程落地注意事項（特別是 scaling law）
- **與現有文件的差異**：提供量化的 scaling law，補足原文件僅有概念描述的不足。
