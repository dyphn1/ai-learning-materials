# AI 學習路線拓樸 (Learning Roadmap Topology)
*自動生成於: 2026-04-20 21:13:56*

## 總覽

| 文件 | 主題 | 核心概念數量 |
|------|------|--------------|
| level1-ai-basics.md | Level 1：AI 入門基礎 | 9 |
| level2-prompt-engineering.md | Level 2：Prompt Engineering 指南 | 7 |
| level2-rag-basics.md | Level 2：RAG 入門指南 | 9 |
| level3-agent-design.md | Level 3：Agent 設計指南 | 9 |
| topic-agentic-workflow.md | Agentic Workflow 設計指南 | 8 |
| topic-agents.md | AI 主題分類參考文件：AI Agent 設計與框架 | 8 |
| topic-evaluation.md | AI 模型評測框架指南 | 6 |
| topic-llm-foundations.md | AI 主題分類參考文件：大型語言模型基礎 (LLM Foundations) | 4 |
| topic-local-models.md | 本地模型部署指南 | 26 |
| topic-multi-agent.md | Multi-Agent 系統指南 | 10 |
| topic-prompt-engineering.md | AI 主題分類參考文件：提示工程 (Prompt Engineering) | 6 |
| topic-rag.md | AI 主題分類參考文件：檢索增強生成 (RAG) | 11 |

## 詳細學習路線

### Level 1：AI 入門基礎 (`level1-ai-basics.md`)

**核心概念與術語：**
- Token
- Context Window
- Temperature
- Inference
- Fine-tuning
- Embedding
- AI（人工智慧）
- Machine Learning（ML）
- Deep Learning

---

### Level 2：Prompt Engineering 指南 (`level2-prompt-engineering.md`)

**核心概念與術語：**
- 明確角色
- 具體指令
- 提供脈絡
- 限制格式
- 迭代優化
- 風險
- 防禦策略

**實作範例摘錄：**
```
將以下中文翻譯成英文：「今天天氣很好」
```

```
情感分析範例：
輸入：「這部電影太棒了！」→ 輸出：正面
輸入：「服務態度很差」→ 輸出：負面
輸入：「還算可以」→ 輸出：？
```

*... 及另外 2 個範例 ...*

---

### Level 2：RAG 入門指南 (`level2-rag-basics.md`)

**核心概念與術語：**
- 固定大小
- 句子切分
- 語意切分
- 重疊切分
- 問題
- 解法
- 建議起點
- LangChain
- LlamaIndex

**實作範例摘錄：**
```
用戶問題 → 向量搜尋知識庫 → 取得相關段落 → LLM 生成回答
```

```
# 使用 nomic-embed-text（已安裝）
import ollama
response = ollama.embeddings(model='nomic-embed-text', prompt='你好')
vector = response['embedding']  # 長度 768 的浮點陣列
```

*... 及另外 2 個範例 ...*

---

### Level 3：Agent 設計指南 (`level3-agent-design.md`)

**核心概念與術語：**
- Short-term
- Long-term
- Episodic
- Semantic
- ReAct = Reasoning + Acting
- 建議的安全邊界設定
- Planner
- Executor
- Replanner

**實作範例摘錄：**
```
思考（Thought）：我需要知道今天的天氣
行動（Action）：web_search("台北今天天氣")
觀察（Observation）：搜尋結果：27°C，晴天
思考（Thought）：已取得天氣資訊，可以回答用戶
回答（Final Answer）：台北今天 27°C，晴天
```

```
{
  "tools": {
    "exec": { "ask": "off" },
    "read": {},
    "write": {},
    "web_search": {},
    "web_fetch": {}
  }
}
```

*... 及另外 1 個範例 ...*

---

### Agentic Workflow 設計指南 (`topic-agentic-workflow.md`)

**核心概念與術語：**
- Sequential
- Parallel
- Conditional
- Iterative
- 優點
- 缺點
- 有向圖（DAG）
- 特色

**實作範例摘錄：**
```
讀取文件 → 摘要 → 翻譯 → 儲存
```

```
┌→ 搜尋 Wikipedia →┐
問題 →│→ 搜尋新聞 -------│→ 整合回答
      └→ 搜尋學術論文 →--┘
```

*... 及另外 3 個範例 ...*

---

### AI 主題分類參考文件：AI Agent 設計與框架 (`topic-agents.md`)

**核心概念與術語：**
- 循環的思考-行動-觀察 (Observe-Think-Act)
- ReAct (Reasoning and Acting):
- 流程:
- Plan-and-Execute:
- Memory 系統:
- Tools/Functions Calling:
- 安全邊界 (Safety):
- 狀態管理 (State Management):

---

### AI 模型評測框架指南 (`topic-evaluation.md`)

**核心概念與術語：**
- 內容
- 衡量
- 分數解讀
- 指標
- 自動評測與回歸測試
- 應用場景

**實作範例摘錄：**
```
pip install lm-eval

# 評測本地 Ollama 模型
lm_eval --model local-completions \
  --model_args base_url=http://localhost:11434/v1,model=gemma4 \
  --tasks mmlu \
  --num_fewshot 5
```

```
import ollama

test_cases = [
    {"prompt": "2 + 2 = ?", "expected": "4"},
    {"prompt": "台灣首都是哪裡？", "expected": "台北"},
]

for case in test_cases:
    resp = ollama.chat(model='gemma4', messages=[{"role":"user","content":case["prompt"]}])
    answer = resp['message']['content']
    passed = case["expected"] in answer
    print(f"{'✅' if passed else '❌'} {case['prompt'][:20]}...")
```

---

### AI 主題分類參考文件：大型語言模型基礎 (LLM Foundations) (`topic-llm-foundations.md`)

**核心概念與術語：**
- Transformer 架構:
- Self-Attention 機制:
- 位置編碼 (Positional Encoding):
- 實務應用:

---

### 本地模型部署指南 (`topic-local-models.md`)

**核心概念與術語：**
- Q8_0
- Q6_K
- Q5_K_M
- **Q4_K_M**
- Q3_K_M
- Q2_K
- gemma3:1b
- gemma3:4b
- gemma4:12b
- qwen3:8b
- deepseek-r1:8b
- gemma4:27b
- `gemma4:latest`
- `gemma4:e4b`
- `nomic-embed-text:latest`
- `openai/gpt-oss-120b:free`
- `nvidia/nemotron-3-super-120b:free`
- `google/gemma-4-26b-a4b-it:free`
- `arcee-ai/trinity-large-preview:free`
- 精度
- 速度
- Q4_K_M
- 建議
- 中等
- 現有模型
- 建議優先下載

**實作範例摘錄：**
```
brew install ollama
# 路徑：/opt/homebrew/bin/ollama
```

```
ollama list                    # 列出已下載模型
ollama pull gemma4             # 下載模型
ollama run gemma4              # 互動式對話
ollama rm gemma4               # 刪除模型
ollama show gemma4 --modelfile # 查看模型設定
```

*... 及另外 3 個範例 ...*

---

### Multi-Agent 系統指南 (`topic-multi-agent.md`)

**核心概念與術語：**
- **CrewAI**
- **AutoGen**
- **LangGraph**
- **openclaw**
- Orchestrator 職責
- Worker 職責
- CrewAI
- AutoGen
- LangGraph
- openclaw

**實作範例摘錄：**
```
用戶請求
    │
    ▼
Orchestrator（規劃 & 協調）
    │
    ├→ Worker A（程式碼生成）
    ├→ Worker B（網路搜尋）
    └→ Worker C（文件整理）
    │
    ▼
整合結果 → 回覆用戶
```

```
from crewai import Agent, Task, Crew

researcher = Agent(role="研究員", goal="蒐集資訊", ...)
writer = Agent(role="寫作者", goal="整理成報告", ...)

crew = Crew(agents=[researcher, writer], tasks=[...])
result = crew.kickoff()
```

*... 及另外 1 個範例 ...*

---

### AI 主題分類參考文件：提示工程 (Prompt Engineering) (`topic-prompt-engineering.md`)

**核心概念與術語：**
- Zero-shot Prompting:
- Few-shot Prompting:
- Chain-of-Thought (CoT):
- Structured Output:
- Prompt Injection:
- 防禦策略:

---

### AI 主題分類參考文件：檢索增強生成 (RAG) (`topic-rag.md`)

**核心概念與術語：**
- 載入 (Loading):
- 切塊 (Chunking):
- 嵌入 (Embedding):
- 儲存 (Storage):
- 向量資料庫 (Vector Database)
- 檢索 (Retrieval):
- 餘弦相似度 (Cosine Similarity)
- 生成 (Generation):
- Embedding 模型:
- 向量資料庫:
- Hybrid Search:

---
