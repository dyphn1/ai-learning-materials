# 檢索增強生成 (RAG) 系統：內部機制、進步與工程實踐 學習筆記
*來源檔案: topic-rag.md*
*同步更新: 2026-04-26*

## 一句話理解
傳統大型語言模型（LLM）的知識固化於參數權重，然而其訓練資料上限導致「知識凍結」與「過時」問題。檢索增強生成（RAG）通过在推理階段動態結合外部知識庫，解決了「參數依賴」與「領域特化」的限制。本文系统介紹 RAG 的核心流程、最新演進方向以及工程落地方面的關鍵考量，幫助資深工程師理解「為什麼這樣設計」、「有哪些 trade‑off」以及「最新研究方向是什麼」。RAG 系統的價值在於提供可驗證的事實依據、降低偽資訊風險、並支援多跳問答與領域專業應用。

## 必記重點
- **載入（Loading）** – 讀取原始文檔（PDF、HTML、TXT）並保持原始結構。
- **切塊（Chunking）** – 將文檔切分為等長或語意連續的塊（Chunk），常用長度 256–1024 token。過大會稀釋語意，過小則增加噪聲。
- **嵌入（Embedding）** – 使用雙向編碼模型（如 BGE‑v1、text‑embedding‑ada‑2）將每個 Chunk 投射至高維向量空間。
- **儲存（Storage）** – 將向量與對應原文存入向量資料庫（Vector DB），常見選擇包括 Chroma、Pinecone、Milvus。
- **檢索（Retrieval）** – 將使用者問題向量化後，利用係數相似度（Cosine Similarity）或 BM25 混合檢索，取 Top‑k 片段作為上下文。

## 核心名詞速記
- **RAG**
- **僅調整微調 (Fine‑tune)**
- **直接使用大規模預訓練模型**
- 載入（Loading）
- 切塊（Chunking）
- 嵌入（Embedding）
- 儲存（Storage）
- 檢索（Retrieval）

## 流程速記
1. **載入（Loading）** – 讀取原始文檔（PDF、HTML、TXT）並保持原始結構。
2. **切塊（Chunking）** – 將文檔切分為等長或語意連續的塊（Chunk），常用長度 256–1024 token。過大會稀釋語意，過小則增加噪聲。
3. **嵌入（Embedding）** – 使用雙向編碼模型（如 BGE‑v1、text‑embedding‑ada‑2）將每個 Chunk 投射至高維向量空間。
4. **儲存（Storage）** – 將向量與對應原文存入向量資料庫（Vector DB），常見選擇包括 Chroma、Pinecone、Milvus。
5. **檢索（Retrieval）** – 將使用者問題向量化後，利用係數相似度（Cosine Similarity）或 BM25 混合檢索，取 Top‑k 片段作為上下文。
6. **生成（Generation）** – 將問題與檢索到的片段串聯，作為Prompt傳遞給 LLM，讓模型基於實證資料生成答案。

## 必背公式
$$
\text{sim}(\mathbf{q},\mathbf{v}) = \frac{\mathbf{q}\cdot\mathbf{v}}{\|\mathbf{q}\|\;\|\mathbf{v}\|}
$$

## 實作範例重點
### 範例片段
```python
# rag_demo.py
import chromadb
from sentence_transformers import SentenceTransformer
from langchain import PromptTemplate, LLM
from langchain.chat_models import ChatOpenAI

# 1️⃣ 建立 Chroma DB
client = chromadb.Client()
collection = client.create_collection(name="docs")

# 2️⃣ 嵌入並存儲（示例用 3 個片段）
embeddings = SentenceTransformer("bge/encoding-large").encode
texts = [
    "BERT 是一種雙向Transformer模型，能捕捉上下文關係。",
    "RAG 結合檢索與生成，能降低幻覺現象。",
    "HyDE 先產生假設文檔再嵌入，提升檢索質量。"
]
ids = ["txt1", "txt2", "txt3"]
embeds = embeddings(texts)
for idx, vec in zip(ids, embeds):
    collection.add(id=idx, embedding=vec.tolist(), text=texts[idx])

# 3️⃣ 檢索功能
def retrieve(query, k=2):
    q_vec = embeddings([query])[0].tolist()
    results = collection.query(query_embeddings=q_vec, n_results=k)
    return results["documents"][0]

# 4️⃣ 生成回答
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)

template = """你是一位資深工程師，根據以下檢索到的段落回答問題：
{retrieved_text}

問題：{question}
答案：
"""
prompt = PromptTemplate.from_template(template)

def rag_answer(question):
    retrieved = retrieve(question, k=2)
    ctx = "\n\n".join(retrieved)
    llm_input = prompt.format(retrieved_text=ctx, question=question)
    return llm(llm_input).content

# 測試
print(rag_answer("什麼是 RAG"))
```

## 常見限制
- **檢索偏差**：常見於長尾分布或小眾领域，導致召回不均衡。
- **上下文爆炸**：當 Top‑k 過大時，LLM 的上下文窗口會被填滿，影響生成效果。
- **成本-效能權衡**：大規模向量搜索與高功率 LLM 同時使用時成本指數上升。
- **安全與偏見**：從外部資料庫檢索的資訊可能帶入偏見或惡意內容，需要 **資料篩選**與 **後置防護**。

## 自我檢查
*無自我檢查題目*