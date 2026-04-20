# openclaw 下載清單

> 目標：讓 openclaw 在 local machine 上具備完整的 AI agent 能力
> 優先順序：🔴 必要 ｜ 🟡 建議 ｜ 🟢 選配

---

## 1. Ollama 本地模型

### 主力推理模型
| 優先 | 模型 | 用途 | 指令 |
|------|------|------|------|
| 🔴 | `qwen3:8b` | 繁中友好的日常推理 | `ollama pull qwen3:8b` |
| 🔴 | `gemma3:12b` | 多語言、程式輔助 | `ollama pull gemma3:12b` |
| 🟡 | `deepseek-r1:8b` | Chain-of-Thought 推理 | `ollama pull deepseek-r1:8b` |
| 🟡 | `llama3.2:3b` | 快速回應、輕量任務 | `ollama pull llama3.2:3b` |
| 🟢 | `phi4-mini` | 低資源備援 | `ollama pull phi4-mini` |

### Embedding 模型（RAG 必備）
| 優先 | 模型 | 說明 | 指令 |
|------|------|------|------|
| 🔴 | `nomic-embed-text` | 通用文字嵌入，主流 RAG 首選 | `ollama pull nomic-embed-text` |
| 🟡 | `mxbai-embed-large` | 高精度嵌入，長文件適用 | `ollama pull mxbai-embed-large` |
| 🟡 | `bge-m3` | 多語言嵌入（含繁中） | `ollama pull bge-m3` |

### 視覺模型（選配）
| 優先 | 模型 | 說明 | 指令 |
|------|------|------|------|
| 🟢 | `llava:13b` | 圖片理解、螢幕截圖分析 | `ollama pull llava:13b` |
| 🟢 | `moondream` | 輕量圖片描述 | `ollama pull moondream` |

---

## 2. 知識庫文件（餵給 RAG）

### AI 學習素材
- [ ] Attention Is All You Need（Transformer 論文）
- [ ] LLaMA 系列技術報告（Meta）
- [ ] RAG 原始論文：Lewis et al. 2020
- [ ] ReAct: Synergizing Reasoning and Acting（Agent 基礎）
- [ ] Toolformer 論文（tool use 基礎）
- [ ] AutoGPT / BabyAGI 原始碼說明文件
- [ ] LangChain、LlamaIndex 官方文件（PDF 版或 clone repo）

### openclaw 本身的文件
- [ ] openclaw 官方 changelog / release notes
- [ ] prompt engine → harness engine 演進說明（如有公開）
- [ ] openclaw 支援的 tool/node 清單說明

### 個人知識庫（放入 workspace）
- [ ] 已有：`Desktop/ai/docs/` 內的三份 PDF
  - Beginners-Guide-to-Artificial-Intelligence.pdf ✅
  - Student-Guide-Module-1-Fundamentals-of-AI.pdf ✅
  - ED673750.pdf ✅

---

## 3. 工具與插件資料

### Vector Store（本地）
- [ ] **ChromaDB**：最易上手的本地向量資料庫 `pip install chromadb`
- [ ] **Qdrant**（Docker）：生產等級，支援本地部署

### 網路搜尋
- 目前已設定：DuckDuckGo ✅
- 建議備援：Brave Search API（免費額度）

### 程式碼執行環境
- [ ] Python 3.11+ 環境確認
- [ ] Node.js 18+ 環境確認（openclaw 依賴）

---

## 4. OpenRouter 模型清單（雲端備援）

目前已設定的 free tier 模型（見 openclaw.json）：
- nvidia/nemotron-3-super-120b ✅
- openai/gpt-oss-120b ✅
- google/gemma-4-26b ✅

### 建議補充（需 API key 額度）
- [ ] `anthropic/claude-3.5-haiku`：高性價比、長上下文
- [ ] `google/gemini-2.0-flash`：速度快、多模態

---

## 5. 分類標籤（給 openclaw 建立知識分類用）

openclaw 在整理下載資料時，請依以下標籤分類：

```
ai/foundations        → LLM 原理、Transformer 架構
ai/prompt-engineering → Prompt 技巧、few-shot、CoT
ai/rag                → 向量搜尋、嵌入、知識庫
ai/agents             → ReAct、工具呼叫、多代理
ai/fine-tuning        → LoRA、RLHF、指令微調
ai/local-models       → Ollama、llama.cpp、量化
ai/evaluation         → harness、benchmarks、評測
ai/safety             → alignment、越獄防範
```
