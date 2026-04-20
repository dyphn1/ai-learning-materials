# AI 學習清單（依程度分級）

> 目標讀者：有技術背景，從 AI 入門到 Agentic Workflow 進階
> 請 openclaw 依此清單建立對應文件

---

## Level 1：入門（AI Beginner）

**目標**：理解 AI 是什麼、能做什麼、怎麼用

### 概念理解
- [ ] 什麼是機器學習、深度學習、LLM 的差別
- [ ] GPT 系列演進（GPT-1 → GPT-4o）
- [ ] Token 是什麼？Context Window 的限制
- [ ] Temperature、Top-p 參數的意義
- [ ] ChatGPT vs API 使用的差異

### 第一個動手實作
- [ ] 用 OpenRouter API 呼叫一個 LLM（curl / Python）
- [ ] 用 Ollama 在本機跑第一個模型（`ollama run gemma3:4b`）
- [ ] 寫第一個 System Prompt
- [ ] 讓 AI 輸出 JSON 格式回應

### 推薦資源
- `Desktop/ai/docs/Beginners-Guide-to-Artificial-Intelligence.pdf`（已有）
- `Desktop/ai/docs/Student-Guide-Module-1-Fundamentals-of-AI.pdf`（已有）
- 影片：3Blue1Brown「But what is a neural network?」

---

## Level 2：中階（Prompt Engineer）

**目標**：掌握 LLM 的輸入輸出控制，能設計有效的 Prompt

### Prompt Engineering
- [ ] Zero-shot / Few-shot 實驗對比
- [ ] Chain-of-Thought（CoT）讓模型「先想後答」
- [ ] Role Prompting：賦予 AI 角色身分
- [ ] Structured Output：強制輸出 JSON Schema
- [ ] Prompt Chaining：多個 prompt 串接完成複雜任務
- [ ] Prompt Injection 辨識與防禦

### LLM API 進階使用
- [ ] Streaming response 實作
- [ ] 多輪對話管理（message history）
- [ ] System / User / Assistant 角色分工
- [ ] Function Calling 基礎（定義工具讓 AI 呼叫）
- [ ] 使用 OpenRouter 切換不同模型做對比測試

### RAG 入門
- [ ] 向量嵌入概念（把文字變成數字向量）
- [ ] 建立第一個向量資料庫（ChromaDB + nomic-embed-text）
- [ ] 讀入 PDF，用 RAG 問答
- [ ] Chunk size 對回答品質的影響實驗

---

## Level 3：進階（AI Agent Builder）

**目標**：設計並實作能自主完成任務的 AI Agent

### Agent 核心概念
- [ ] ReAct 框架：模型如何「決策 → 呼叫工具 → 觀察 → 再決策」
- [ ] Memory 系統：短期（buffer）vs 長期（向量）vs 摘要記憶
- [ ] Plan-and-Execute：任務先規劃、再分步執行
- [ ] Self-reflection：讓 Agent 評估自己的輸出並修正
- [ ] Human-in-the-loop：何時需要人工介入

### 實作 openclaw Agent
- [ ] 閱讀 openclaw 的 tool/node 系統設計
- [ ] 撰寫一個自訂 tool（例如：讀取本機檔案並摘要）
- [ ] 設計 Agent 的 System Prompt（任務範圍、工具使用規則）
- [ ] 設計 fallback 模型策略（已有設定，深入理解）
- [ ] 測試 denyCommands 的安全邊界

### RAG 進階
- [ ] Hybrid Search（向量 + BM25 關鍵字混合）
- [ ] Reranking（二次排序提升精度）
- [ ] agentic RAG：Agent 自主決定是否要查詢知識庫
- [ ] 用 RAGAS 評測 RAG 回答品質

### Agentic Workflow 設計
- [ ] 設計線性工作流（A → B → C）
- [ ] 設計條件分支流程（if 結果不好 → 重試）
- [ ] 設計並行任務（同時執行多個子任務）
- [ ] 用 LangGraph 實作有狀態的 Agent loop
- [ ] Multi-Agent：讓兩個 Agent 協作完成一個任務（openclaw per-channel 機制）

### 評測與調優
- [ ] 建立自己的 prompt regression test suite
- [ ] 用 LM Evaluation Harness 跑 benchmark
- [ ] 分析模型在不同任務上的成功率
- [ ] 記錄 openclaw 任務執行的成功/失敗模式

---

## 學習路徑建議

```
Week 1-2   → Level 1 全部完成
Week 3-5   → Level 2 前半（Prompt Engineering）
Week 6-8   → Level 2 後半（RAG 入門）
Week 9-12  → Level 3 前半（Agent 概念 + openclaw 實作）
Week 13-16 → Level 3 後半（Agentic Workflow + 評測）
```

---

## openclaw 文件建立指示

> 請 openclaw 依以下對應關係，在 `Desktop/ai/docs/` 建立學習筆記：

| 文件名稱 | 對應等級 | 內容摘要來源 |
|---------|---------|------------|
| `level1-ai-basics.md` | Level 1 | 整合已有的三份 PDF |
| `level2-prompt-engineering.md` | Level 2 | 從網路搜尋並整理 |
| `level2-rag-basics.md` | Level 2 | RAG 論文 + 實作筆記 |
| `level3-agent-design.md` | Level 3 | ReAct 論文 + openclaw 實作 |
| `level3-agentic-workflow.md` | Level 3 | LangGraph + 設計模式 |
| `level3-evaluation.md` | Level 3 | harness 評測方法 |
