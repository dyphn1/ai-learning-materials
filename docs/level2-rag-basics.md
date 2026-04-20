# Level 2：RAG 入門指南

## 學習目標
理解 Retrieval-Augmented Generation（RAG）架構，能夠建立基本的本地知識庫問答系統。

---

## 什麼是 RAG？

**問題**：LLM 的知識有訓練截止日，無法回答私有文件內容  
**解法**：先從知識庫「檢索」相關段落，再連同問題一起送給 LLM 生成回答

```
用戶問題 → 向量搜尋知識庫 → 取得相關段落 → LLM 生成回答
```

---

## 核心元件

### 1. Embedding（向量嵌入）
將文字轉換成高維向量，語意相近的文字向量距離也近：
```python
# 使用 nomic-embed-text（已安裝）
import ollama
response = ollama.embeddings(model='nomic-embed-text', prompt='你好')
vector = response['embedding']  # 長度 768 的浮點陣列
```

### 2. 向量資料庫（ChromaDB）
儲存並快速搜尋向量：
```bash
pip install chromadb
```

```python
import chromadb
client = chromadb.Client()
collection = client.create_collection("my_docs")

# 新增文件
collection.add(
    documents=["文件內容..."],
    ids=["doc1"]
)

# 查詢
results = collection.query(query_texts=["我的問題"], n_results=3)
```

### 3. Chunking（分段策略）

| 策略 | Chunk Size | 適合場景 |
|------|-----------|---------|
| 固定大小 | 256-512 tokens | 一般文件 |
| 句子切分 | 依句號 | 對話、FAQ |
| 語意切分 | 依段落 | 技術文件 |
| 重疊切分 | 50-100 token 重疊 | 避免邊界遺失 |

**建議起點**：chunk_size=512，overlap=50

---

## Hybrid Search（混合搜尋）

結合向量搜尋（語意）+ 關鍵字搜尋（精確）：
- 向量搜尋：找語意相近的段落
- BM25 / 全文搜尋：找精確關鍵字
- 加權合併兩種分數（RRF 演算法）

ChromaDB 支援基本向量搜尋，進階 hybrid search 可用 **LangChain** 或 **LlamaIndex**。

---

## 快速實驗步驟

1. `pip install chromadb` 安裝向量資料庫
2. 讀取 `Desktop/ai/docs/` 的 PDF，用 PyPDF2 提取文字
3. 切成 512 token chunks，用 `nomic-embed-text` 生成向量
4. 存入 ChromaDB
5. 輸入問題 → 搜尋 top-3 chunks → 送給 gemma4 回答

---

*建立時間：2026-04-19*
