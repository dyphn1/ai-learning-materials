# AI 學習清單（依主題分類）

> 目標讀者：有技術背景，系統性掌握各個 AI 技術領域
> 請 openclaw 依此清單建立對應文件

---

## 主題一：LLM 基礎原理

**對應標籤**：`ai/foundations`
**重要性**：⭐⭐⭐⭐⭐（所有技術的根基）

### 必學
- [ ] Transformer 架構：Self-Attention 機制圖解
- [ ] 預訓練 vs 微調 vs 提示工程的差異
- [ ] Tokenization：BPE、SentencePiece 原理
- [ ] 為什麼 LLM 會「幻覺」（Hallucination）？
- [ ] 模型規模定律（Scaling Law）
- [ ] GGUF 量化：4-bit 模型為何能跑在 CPU？

### 建議 openclaw 搜尋的關鍵字
```
Transformer architecture explained
LLM tokenization BPE
model quantization GGUF
LLM hallucination causes
```

---

## 主題二：Prompt Engineering

**對應標籤**：`ai/prompt-engineering`
**重要性**：⭐⭐⭐⭐⭐（短期最高 ROI 技能）

### 必學
- [ ] Zero-shot vs Few-shot vs Many-shot 對比實驗
- [ ] Chain-of-Thought（CoT）：加一句「Let's think step by step」的效果
- [ ] Tree-of-Thought（ToT）：多路徑推理
- [ ] Structured Output：讓模型輸出可解析的 JSON
- [ ] Prompt 長度與模型性能的權衡
- [ ] Negative Prompting（告訴模型不要做什麼）

### 實作任務
- [ ] 建立自己的 Prompt Library（常用 System Prompt 模板集）
- [ ] A/B 測試：同一任務，比較 3 種不同 prompt 的輸出

---

## 主題三：RAG（檢索增強生成）

**對應標籤**：`ai/rag`
**重要性**：⭐⭐⭐⭐⭐（讓 AI 讀你的資料）

### 核心概念
- [ ] 為什麼需要 RAG？（解決 context window 限制 + 知識截止問題）
- [ ] Embedding 空間可視化理解
- [ ] 向量相似度：cosine similarity vs dot product
- [ ] Chunking 策略比較：
  - Fixed-size（固定長度切割）
  - Sentence-based（依句子切割）
  - Semantic（依語意切割）

### 進階 RAG
- [ ] Hybrid Search：向量搜尋 + BM25 全文搜尋結合
- [ ] Re-ranking：Cross-Encoder 二次精排
- [ ] Parent-Child Chunking：存小塊、回傳大塊
- [ ] Hypothetical Document Embeddings（HyDE）
- [ ] Graph RAG：用知識圖譜增強檢索

### 工具清單
| 工具 | 用途 | 難度 |
|------|------|------|
| ChromaDB | 本地向量庫 | 入門 |
| Qdrant | 高效能向量庫 | 中階 |
| LlamaIndex | RAG 完整框架 | 中階 |
| RAGAS | RAG 評測 | 進階 |

---

## 主題四：Function Calling & Tool Use

**對應標籤**：`ai/tool-use`
**重要性**：⭐⭐⭐⭐（Agent 的手腳）

### 必學
- [ ] Function Calling 的 JSON Schema 格式
- [ ] 模型如何「決定」要呼叫哪個工具
- [ ] 工具執行結果如何回饋給模型
- [ ] MCP（Model Context Protocol）：openclaw 的工具標準
- [ ] 設計安全的工具（沙盒、權限控制）
- [ ] openclaw 的 denyCommands 設計原理

### 實作任務
- [ ] 為 openclaw 新增一個自訂工具（讀取本機 JSON / 搜尋檔案）
- [ ] 測試工具呼叫的 error handling

---

## 主題五：AI Agents

**對應標籤**：`ai/agents`
**重要性**：⭐⭐⭐⭐⭐（openclaw 的核心能力）

### 必學
- [ ] ReAct 論文精讀（Reasoning + Acting 迴圈）
- [ ] Agent 的四個核心模組：規劃、記憶、工具、執行
- [ ] Memory 類型：
  - Sensory（當前輸入）
  - Short-term（對話歷史）
  - Long-term（持久化向量記憶）
- [ ] Self-correction：Agent 如何重試與修正
- [ ] Plan-and-Execute vs ReAct 的適用場景

### openclaw 專項
- [ ] 分析 openclaw 的 agent 設定結構（`~/.openclaw/openclaw.json`）
- [ ] 理解 primary + fallback 模型切換機制
- [ ] per-channel-peer 會話隔離的應用場景

---

## 主題六：Multi-Agent Systems

**對應標籤**：`ai/multi-agent`
**重要性**：⭐⭐⭐⭐（Harness Engine 的精髓）

### 必學
- [ ] Orchestrator / Subagent 架構模式
- [ ] Agent 角色設計（Planner、Executor、Critic、Summarizer）
- [ ] 代理間通訊與任務分派
- [ ] 框架對比：
  - **CrewAI**：角色扮演式多代理
  - **AutoGen**（Microsoft）：對話式多代理
  - **LangGraph**：有狀態圖形工作流
- [ ] 何時用 Multi-Agent vs 單一 Agent？

### 實作任務
- [ ] 設計一個「研究助手」：一個 Agent 搜尋 + 一個 Agent 整理 + 一個 Agent 撰寫

---

## 主題七：Fine-tuning（模型微調）

**對應標籤**：`ai/fine-tuning`
**重要性**：⭐⭐⭐（特定任務最佳化）

### 必學
- [ ] 什麼情況下需要 fine-tune？（vs prompt engineering）
- [ ] LoRA 原理：低秩矩陣為何能高效微調
- [ ] QLoRA：量化 + LoRA 的記憶體節省
- [ ] 訓練資料格式：Alpaca、ShareGPT、JSONL
- [ ] DPO（Direct Preference Optimization）取代 RLHF 的趨勢
- [ ] Unsloth：最快的本地微調工具

### 必要硬體
- 8GB VRAM 可跑 7B QLoRA
- 24GB VRAM 可跑 13B LoRA

---

## 主題八：本地模型部署

**對應標籤**：`ai/local-models`
**重要性**：⭐⭐⭐⭐（openclaw 的底層基礎）

### 必學
- [ ] Ollama 完整使用：pull、run、serve、Modelfile
- [ ] GGUF 量化等級對比：Q4_K_M vs Q5_K_M vs Q8_0
- [ ] 硬體效能計算：模型大小 × 量化位元 ≈ 需要 RAM
- [ ] Ollama REST API：與 openclaw 的整合方式
- [ ] 多模型並行管理

### 目前 openclaw 已設定的本地模型
- `gemma4:e4b` ✅
- `glm-4.7-flash` ✅

---

## 主題九：Agentic Workflow 設計

**對應標籤**：`ai/agentic-workflow`
**重要性**：⭐⭐⭐⭐⭐（進階 openclaw 使用的關鍵）

### 設計模式
- [ ] **Sequential**：A → B → C（線性任務）
- [ ] **Parallel**：同時執行多個不相依的子任務
- [ ] **Conditional**：依輸出品質決定下一步
- [ ] **Iterative Loop**：生成 → 評估 → 修正 → 重複
- [ ] **Map-Reduce**：分散處理大量資料再彙整

### 實作任務（openclaw 情境）
- [ ] 設計一個「每日摘要」工作流：搜尋新聞 → 摘要 → 儲存到知識庫
- [ ] 設計一個「程式碼審查」工作流：讀取程式 → 分析 → 提出建議 → 輸出報告
- [ ] 設計一個帶 Human-in-the-loop 的決策工作流

---

## 主題十：評測框架（Evaluation & Harness）

**對應標籤**：`ai/evaluation`
**重要性**：⭐⭐⭐⭐（Harness Engine 命名來源）

### 必學
- [ ] 為什麼需要系統性評測？（避免靠感覺評估 AI）
- [ ] LM Evaluation Harness（EleutherAI）使用
- [ ] 常見 Benchmark 含義：
  - MMLU：知識廣度測試
  - GSM8K：數學推理
  - HumanEval：程式碼生成
  - HellaSwag：常識推理
- [ ] RAG 評測：RAGAS 指標（faithfulness、answer relevancy）
- [ ] 自訂評測：為 openclaw 任務設計成功率指標

---

## openclaw 文件建立指示

> 請 openclaw 依以下對應關係，在 `Desktop/ai/docs/` 建立主題文件：

| 文件名稱 | 主題 | 格式 |
|---------|------|------|
| `topic-llm-foundations.md` | LLM 原理 | 概念 + 圖解說明 |
| `topic-prompt-engineering.md` | Prompt 技術 | 技巧清單 + 範例 |
| `topic-rag.md` | RAG 完整指南 | 概念 + 工具 + 實作 |
| `topic-tool-use.md` | 工具呼叫 | MCP + openclaw 整合 |
| `topic-agents.md` | Agent 設計 | ReAct + openclaw 實作 |
| `topic-multi-agent.md` | 多代理系統 | 框架對比 + 設計模式 |
| `topic-fine-tuning.md` | 模型微調 | LoRA + 工具指南 |
| `topic-local-models.md` | 本地部署 | Ollama + 效能指南 |
| `topic-agentic-workflow.md` | 工作流設計 | 設計模式 + 實作範例 |
| `topic-evaluation.md` | 評測框架 | Harness + 自訂指標 |
