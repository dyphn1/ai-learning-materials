# Fine‑Tuning 參考資料

> 最後更新：2026-05-04

## 來源清單

### 來源 1：Evolution Strategies at Scale: LLM Fine‑Tuning Beyond Reinforcement Learning
- **URL / arXiv ID**：https://arxiv.org/abs/2509.24372
- **類型**：論文
- **作者 / 機構**：未知（arXiv 預印本）
- **發表年份**：2025
- **可信度**：高（同行評審前置）
- **主要貢獻摘要**：首次在十億參數 LLM 上完整參數 ES 微調，展示了在無梯度限制下的穩定收斂與對 reward‑hacking 的抗性。
- **用於文件的哪個章節**：Evolution Strategies（ES）微調
- **與現有文件的差異**：提供了具體的 ES 演算法式與實驗結果，補足原始文件中僅提及名稱的空缺。

### 來源 2：Parameter‑efficient Fine‑Tuning Survey (Springer 2025)
- **URL**：https://link.springer.com/article/10.1007/s10462-025-11236-4
- **類型**：期刊 Survey
- **作者**：多位作者
- **發表年份**：2025
- **可信度**：高（Springer 期刊）
- **主要貢獻摘要**：系統化整理 LoRA、Adapter、Prefix‑Tuning 的原理、實驗比較與最佳實踐指引。
- **用於文件的哪個章節**：PEFT 概述與 trade‑off 分析

### 來源 3：Efficient Multimodal LLM Fine‑Tuning (Frontiers AI 2026)
- **URL**：https://www.frontiersin.org/articles/10.3389/frai.2026.1665992/full
- **類型**：期刊論文
- **發表年份**：2026
- **主要貢獻摘要**：提出在視覺‑語言模型上僅微調投影層與 Adapter，實驗顯示在 VQA、圖文生成上提升 5‑10% 而參數增長 <0.2%。
- **用於文件的哪個章節**：多模態微調

---
*此檔案由 AI agent 自動生成*