# Level 3：Agent 設計指南 參考資料

> 最後更新：2026-04-26

## 來源清單

### 來源 1：ReAct: Synergizing Reasoning and Acting in Language Models
- **URL / arXiv ID**：https://arxiv.org/abs/2210.03629 或 arXiv:2210.03629
- **類型**：論文
- **作者 / 機構**：Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
- **發表年份**：2023
- **可信度**：高
- **主要貢獻摘要**：ReAct 展示了 reasoning 與 acting interleaving 的價值，讓 agent 不需要在「先想完」與「直接做」之間二選一。對 agent 設計來說，它定義了最小可行控制迴圈：Thought、Action、Observation。這是理解 planner/executor 分離之前的基礎。
- **用於文件的哪個章節**：概覽與設計動機、與前代技術的比較
- **與現有文件的差異**：補上 agent loop 為什麼成立的原始研究依據。

### 來源 2：MemGPT: Towards LLMs as Operating Systems
- **URL / arXiv ID**：https://arxiv.org/abs/2310.08560 或 arXiv:2310.08560
- **類型**：論文
- **作者 / 機構**：Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez
- **發表年份**：2024
- **可信度**：高
- **主要貢獻摘要**：MemGPT 把長上下文問題提升為作業系統式的虛擬記憶管理問題，說明 agent runtime 需要分層記憶、paging 與 control flow，而不是把所有狀態硬塞進 prompt。這對 stateful agent 設計與 durable workflow 非常關鍵。
- **用於文件的哪個章節**：關鍵名詞與專案拆解、核心機制深度解析
- **與現有文件的差異**：補上 long-term memory 與 checkpoint/runtime 設計背後的系統觀點。

### 來源 3：A Survey on Large Language Model based Autonomous Agents
- **URL / arXiv ID**：https://arxiv.org/abs/2308.11432 或 arXiv:2308.11432
- **類型**：論文 / 綜述
- **作者 / 機構**：Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang, Xu Chen 等
- **發表年份**：2023，持續更新至 2025
- **可信度**：高
- **主要貢獻摘要**：這份 survey 以 construction、applications、evaluation、future directions 四個面向整理 LLM-based autonomous agents。對工程師最有價值的是它把 agent 的問題重新定義為系統性設計與評估問題，而不是單一 prompting 技巧。它也突顯 evaluation 與 deployment control 在最新實務中的重要性。
- **用於文件的哪個章節**：概覽與設計動機、2025-2026 最新進展、已知限制與 Open Problems
- **與現有文件的差異**：把 agent 設計從 demo 心態拉回到可比較、可驗證的系統工程。

## 論文詳細記錄

### ReAct: Synergizing Reasoning and Acting in Language Models
- **論文標題**：ReAct: Synergizing Reasoning and Acting in Language Models
- **DOI / arXiv 連結**：https://doi.org/10.48550/arXiv.2210.03629
- **核心演算法名稱**：ReAct

### MemGPT: Towards LLMs as Operating Systems
- **論文標題**：MemGPT: Towards LLMs as Operating Systems
- **DOI / arXiv 連結**：https://doi.org/10.48550/arXiv.2310.08560
- **核心演算法名稱**：Virtual Context Management

### A Survey on Large Language Model based Autonomous Agents
- **論文標題**：A Survey on Large Language Model based Autonomous Agents
- **DOI / arXiv 連結**：https://doi.org/10.48550/arXiv.2308.11432
- **核心演算法名稱**：Unified LLM-Agent Survey Framework