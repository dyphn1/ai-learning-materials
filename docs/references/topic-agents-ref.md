# AI Agents 參考資料

> 最後更新：2026-04-26

## 來源清單

### 來源 1：ReAct: Synergizing Reasoning and Acting in Language Models
- **URL / arXiv ID**：https://arxiv.org/abs/2210.03629 或 arXiv:2210.03629
- **類型**：論文
- **作者 / 機構**：Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
- **發表年份**：2023
- **可信度**：高（ICLR 論文，已有大量後續框架引用）
- **主要貢獻摘要**：這篇論文把 reasoning traces 與 task-specific actions 交錯在同一條軌跡中，證明 LLM 不需要只在「先想完再做」或「只做不想」之間二選一。ReAct 讓模型在 HotpotQA 與 FEVER 類任務中透過 Wikipedia API 補充證據，也在 ALFWorld 與 WebShop 等互動任務中提升成功率。論文的重要價值在於指出：推理與行動的協同，比單獨強化其中一項更能降低 hallucination 與 error propagation。這使 ReAct 成為之後 agent 框架的基礎控制模式。
- **用於文件的哪個章節**：概覽與設計動機、核心機制深度解析、與前代技術的比較
- **與現有文件的差異**：補上 agent 不是單純 CoT 延伸，而是可與外部環境互動的控制迴圈這個核心設計點。

### 來源 2：LLM Powered Autonomous Agents
- **URL / arXiv ID**：https://lilianweng.github.io/posts/2023-06-23-agent/
- **類型**：工程部落格 / 技術綜述
- **作者 / 機構**：Lilian Weng
- **發表年份**：2023
- **可信度**：高（OpenAI 研究主管撰寫，內容整合大量原始論文）
- **主要貢獻摘要**：文章從 planning、memory、tool use 三大模組系統性拆解 agent 架構，並把短期記憶、長期記憶、向量搜尋、工具調用與 reflection 串成一個完整系統視角。與單篇論文相比，這份資料的價值在於把 agent 視為系統工程問題，而不是單一 prompting trick。文中也明確指出 finite context、long-term planning、natural language interface reliability 等常見瓶頸。
- **用於文件的哪個章節**：概覽與設計動機、記憶檢索數學、已知限制與 Open Problems
- **與現有文件的差異**：補上記憶分層、ANN/MIPS 觀點與 agent 可靠性問題，讓文件從概念介紹提升到工程設計層次。

### 來源 3：MemGPT: Towards LLMs as Operating Systems
- **URL / arXiv ID**：https://arxiv.org/abs/2310.08560 或 arXiv:2310.08560
- **類型**：論文
- **作者 / 機構**：Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez
- **發表年份**：2024
- **可信度**：高（Berkeley 系統研究背景，問題定義清楚）
- **主要貢獻摘要**：MemGPT 將有限 context window 問題類比為作業系統的虛擬記憶管理問題，提出分層記憶與 paging 機制，讓 LLM 在表面上擁有遠超上下文限制的工作記憶。這個設計把「外部記憶」從單純檢索器提升成 runtime control 問題，也讓記憶切換、interrupt 與長任務狀態維護有更清楚的抽象。
- **用於文件的哪個章節**：關鍵名詞與專案拆解、2025-2026 最新進展、已知限制與 Open Problems
- **與現有文件的差異**：補上長上下文管理不只是多塞一些 token，而是需要記憶階層與控制流設計的觀點。

### 來源 4：A Survey on Large Language Model based Autonomous Agents
- **URL / arXiv ID**：https://arxiv.org/abs/2308.11432 或 arXiv:2308.11432
- **類型**：論文 / 綜述
- **作者 / 機構**：Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang, Xu Chen 等
- **發表年份**：2023，2025 仍持續更新版本
- **可信度**：高（系統性綜述，且有持續維護）
- **主要貢獻摘要**：這份 survey 提出統一的 LLM agent 分析框架，將 agent construction、applications、evaluation 與 future directions 放在同一個比較坐標系。其重要性在於把 agent 從 demo 集合整理成可比較的研究領域，並指出長期規劃、可靠評估與部署可控性仍是主線挑戰。更新版也顯示領域焦點逐漸從「能不能做」轉向「如何穩定做」。
- **用於文件的哪個章節**：概覽與設計動機、2025-2026 最新進展
- **與現有文件的差異**：提供 2025 時點下對整個 agent 領域的收斂觀點，而不是只列框架名稱。

## 論文詳細記錄

### ReAct: Synergizing Reasoning and Acting in Language Models
- **論文標題**：ReAct: Synergizing Reasoning and Acting in Language Models
- **DOI / arXiv 連結**：https://doi.org/10.48550/arXiv.2210.03629
- **核心演算法名稱**：ReAct

### MemGPT: Towards LLMs as Operating Systems
- **論文標題**：MemGPT: Towards LLMs as Operating Systems
- **DOI / arXiv 連結**：https://doi.org/10.48550/arXiv.2310.08560
- **核心演算法名稱**：Virtual Context Management / Tiered Memory Paging

### A Survey on Large Language Model based Autonomous Agents
- **論文標題**：A Survey on Large Language Model based Autonomous Agents
- **DOI / arXiv 連結**：https://doi.org/10.48550/arXiv.2308.11432
- **核心演算法名稱**：Unified LLM-Agent Survey Framework