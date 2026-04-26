# Prompt Engineering 參考資料

> 最後更新：2026-04-26

## 來源清單

### 來源 1：Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
- **URL / arXiv ID**：https://arxiv.org/abs/2201.11903 或 arXiv:2201.11903
- **類型**：論文
- **作者 / 機構**：Jason Wei, Xuezhi Wang, Dale Schuurmans, Quoc Le, Denny Zhou 等
- **發表年份**：2022
- **可信度**：高（NeurIPS 脈絡的重要基礎論文）
- **主要貢獻摘要**：論文證明對大型模型提供 chain-of-thought exemplars，能顯著提升 arithmetic、commonsense 與 symbolic reasoning 任務表現。它的重要性不在於「逐步思考」這句話本身，而在於揭示推理能力會隨模型規模與 prompt 結構共同出現。這篇論文讓 prompt engineering 從經驗技巧進入可被量化比較的研究議題。
- **用於文件的哪個章節**：概覽與設計動機、核心機制深度解析
- **與現有文件的差異**：補上 CoT 為什麼有效的研究根據，而不是只把它當成口訣。

### 來源 2：Least-to-Most Prompting Enables Complex Reasoning in Large Language Models
- **URL / arXiv ID**：https://arxiv.org/abs/2205.10625 或 arXiv:2205.10625
- **類型**：論文
- **作者 / 機構**：Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei 等
- **發表年份**：2023
- **可信度**：高（ICLR 研究脈絡，直接比較 CoT 與 decomposition）
- **主要貢獻摘要**：這篇論文指出 CoT 在難度超過 exemplars 的任務上仍會失敗，因此提出先拆成子問題、再逐步求解的 least-to-most prompting。它最有工程價值的地方，是把 prompt 設計從「描述怎麼想」提升為「設計問題拆分流程」。對長推理或組合任務來說，這通常比要求模型一次解完整題目更穩定。
- **用於文件的哪個章節**：關鍵名詞與專案拆解、與前代技術的比較
- **與現有文件的差異**：補上 decomposition 觀點，避免文件只停留在 zero-shot / few-shot / CoT 三分法。

### 來源 3：Structured model outputs
- **URL / arXiv ID**：https://developers.openai.com/api/docs/guides/structured-outputs
- **類型**：官方文件
- **作者 / 機構**：OpenAI
- **發表年份**：2026 文件版本
- **可信度**：高（官方 API 規格）
- **主要貢獻摘要**：文件清楚區分 Structured Outputs 與 JSON mode，指出前者的真正價值在 schema adherence，而不是單純輸出合法 JSON。也提供 Pydantic/Zod 綁定、required fields、`additionalProperties: false`、refusal handling 與 schema 限制等重要細節。對工程實務來說，這是把 prompt 輸出轉成可驗證 API contract 的核心依據。
- **用於文件的哪個章節**：核心機制深度解析、工程實作、2025-2026 最新進展
- **與現有文件的差異**：補上 prompt 與 output schema 的系統連結，讓提示工程不再只是文字模板技巧。

### 來源 4：LLM Prompt Injection Prevention Cheat Sheet
- **URL / arXiv ID**：https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html
- **類型**：安全實務文件
- **作者 / 機構**：OWASP Cheat Sheet Series Team
- **發表年份**：2026
- **可信度**：高（業界安全最佳實踐匯整）
- **主要貢獻摘要**：文件整理 direct injection、remote injection、typoglycemia、Best-of-N、agent-specific attacks、RAG poisoning 等攻擊類型，並提出 input validation、structured prompts、output monitoring、HITL 與 least privilege 等防禦措施。它把 prompt injection 從概念風險具體化成可測試的工程問題。對 agent 與 tool use 系統尤其重要。
- **用於文件的哪個章節**：工程實作、2025-2026 最新進展、已知限制與 Open Problems
- **與現有文件的差異**：補上完整攻擊面與具體防禦策略，而不是只有一句「要注意 prompt injection」。

## 論文詳細記錄

### Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
- **論文標題**：Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
- **DOI / arXiv 連結**：https://doi.org/10.48550/arXiv.2201.11903
- **核心演算法名稱**：Chain-of-Thought Prompting

### Least-to-Most Prompting Enables Complex Reasoning in Large Language Models
- **論文標題**：Least-to-Most Prompting Enables Complex Reasoning in Large Language Models
- **DOI / arXiv 連結**：https://doi.org/10.48550/arXiv.2205.10625
- **核心演算法名稱**：Least-to-Most Prompting