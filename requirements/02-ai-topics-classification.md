# AI 技術分類清單（給 openclaw 作為知識分類依據）

> 涵蓋範圍：從早期 Prompt Engine 到現代 Harness Engine
> 雙軸視角：① AI 技術演進史  ② openclaw 工具演進對照

---

## 技術演進時間軸

```
2017  Transformer 架構誕生
  │
2020  GPT-3 出現 → Prompt Engineering 崛起
  │   [Prompt Engine 時代開始]
  │
2022  ChatGPT 爆紅 → LLM 應用普及
  │   RAG 成為主流補強方案
  │
2023  LangChain / AutoGPT → Agent 時代開始
  │   Function Calling / Tool Use 標準化
  │   本地模型：llama.cpp、Ollama 出現
  │
2024  Multi-Agent 框架成熟（CrewAI、AutoGen）
  │   Agentic Workflow 成為工程標準
  │   評測框架（harness）需求升高
  │   [Harness Engine 時代]
  │
2025+ Local AI Agent（如 openclaw）成為個人工具
      MCP（Model Context Protocol）標準化
```

---

## 分類一：LLM 基礎（Foundations）

**標籤**：`ai/foundations`

- Transformer 架構（Attention Is All You Need）
- BERT、GPT、T5 系列演進
- Tokenization、Embedding、Context Window
- 推理參數：temperature、top-p、top-k
- 量化技術：GGUF、GGML、4-bit / 8-bit
- Context Window 管理（sliding window、KV cache）

---

## 分類二：Prompt Engineering（提示工程）

**標籤**：`ai/prompt-engineering`

> 對應 openclaw **Prompt Engine 時代**

- Zero-shot / Few-shot Prompting
- Chain-of-Thought（CoT）推理
- Tree-of-Thought（ToT）
- System Prompt 設計原則
- Role Prompting
- Prompt Injection 防禦
- Structured Output（JSON mode）
- Prompt Chaining（串接多個 prompt）

---

## 分類三：RAG（Retrieval-Augmented Generation）

**標籤**：`ai/rag`

- 向量資料庫概念（ChromaDB、Qdrant、Weaviate）
- Embedding 模型選擇（text-embedding、bge、nomic）
- Chunking 策略（固定長度 vs 語意切割）
- Similarity Search（cosine、dot product）
- Reranking（交叉編碼器）
- Hybrid Search（向量 + 關鍵字）
- RAG Evaluation（RAGAS 框架）
- Graph RAG（知識圖譜增強）
- agentic RAG（主動查詢決策）

---

## 分類四：Tool Use / Function Calling

**標籤**：`ai/tool-use`

- OpenAI Function Calling 規範
- MCP（Model Context Protocol）
- Tool Schema 設計
- 工具執行沙盒安全設計
- openclaw 的 node/tool 系統（denyCommands 機制）
- 電腦操作工具（shell、browser、file I/O）

---

## 分類五：AI Agents（智能代理）

**標籤**：`ai/agents`

- ReAct 框架（Reasoning + Acting）
- Plan-and-Execute 架構
- Memory 系統設計：
  - Short-term（conversation buffer）
  - Long-term（向量記憶庫）
  - Episodic memory
- Reflection & Self-correction
- LangChain Agent
- LlamaIndex Agent
- AutoGPT / BabyAGI 架構分析

---

## 分類六：Multi-Agent Systems（多代理系統）

**標籤**：`ai/multi-agent`

> 對應 openclaw **Harness Engine 時代**

- Orchestrator / Worker 架構
- CrewAI 框架
- AutoGen（Microsoft）
- Agent 通訊協定設計
- 任務分解與委派（Task Decomposition）
- 代理間信任與驗證
- openclaw 的 per-channel-peer 會話隔離機制

---

## 分類七：Fine-tuning（微調）

**標籤**：`ai/fine-tuning`

- 指令微調（Instruction Tuning）
- LoRA / QLoRA（低秩調整）
- RLHF（人類反饋強化學習）
- DPO（Direct Preference Optimization）
- 資料集準備與格式（JSONL、Alpaca 格式）
- 評估：MMLU、HellaSwag、HumanEval

---

## 分類八：本地模型部署（Local Models）

**標籤**：`ai/local-models`

- llama.cpp 原理與量化
- Ollama 使用與模型管理
- 硬體需求評估（RAM / VRAM）
- 模型格式：GGUF、Safetensors
- 效能調優（num_threads、num_gpu）
- openclaw × Ollama 整合設定

---

## 分類九：Agentic Workflow（代理工作流）

**標籤**：`ai/agentic-workflow`

- 工作流設計模式：
  - Sequential（線性）
  - Parallel（並行）
  - Conditional（條件分支）
  - Loop（自我修正迴圈）
- Human-in-the-loop 設計
- 錯誤處理與 fallback 策略
- 狀態管理（stateful agent）
- 工作流框架：LangGraph、Prefect + LLM

---

## 分類十：Evaluation & Harness（評測框架）

**標籤**：`ai/evaluation`

> 對應 openclaw **Harness Engine** 的核心能力

- LM Evaluation Harness（EleutherAI）
- MMLU、GSM8K、HumanEval benchmark
- RAG 評測：RAGAS、TruLens
- Agent 行為評測設計
- 回應品質指標：faithfulness、relevance、coherence
- Prompt regression testing
- openclaw 的任務成功率追蹤

---

## 分類十一：AI 安全（Safety & Alignment）

**標籤**：`ai/safety`

- Prompt Injection 攻防
- Jailbreak 類型分析
- Guardrails 設計（NeMo Guardrails、Guardrails AI）
- openclaw denyCommands 機制解析
- PII 過濾與隱私保護
- 本地 AI 的安全優勢（資料不出機器）

---

## openclaw 引擎演進對照表

| 版本特徵 | Prompt Engine 時代 | Harness Engine 時代 |
|---------|------------------|-------------------|
| 核心機制 | 單輪 Prompt 設計 | 評測驅動的任務執行 |
| 記憶 | 無或短期 | 長期向量記憶 |
| 工具 | 有限工具呼叫 | 完整 tool/node 系統 |
| 多代理 | 無 | per-channel 隔離代理 |
| 模型 | 雲端為主 | Local + Cloud 混合 |
| 評測 | 主觀評估 | benchmark 量化評測 |
