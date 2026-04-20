# Level 2：RAG 入門指南
*來源檔案: level2-rag-basics.md*

## 核心概念
- 固定大小
- 句子切分
- 語意切分
- 重疊切分
- 問題
- 解法
- 建議起點
- LangChain
- LlamaIndex

## 實作範例
### 範例 1
```
用戶問題 → 向量搜尋知識庫 → 取得相關段落 → LLM 生成回答
```

### 範例 2
```
# 使用 nomic-embed-text（已安裝）
import ollama
response = ollama.embeddings(model='nomic-embed-text', prompt='你好')
vector = response['embedding']  # 長度 768 的浮點陣列
```

### 範例 3
```
pip install chromadb
```

### 範例 4
```
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


---

*生成時間: 2026-04-20 21:18:47*