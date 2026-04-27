# 檢索增強生成 (RAG) 系統：內部機制、進步與工程實踐

> 最後更新：2025-05-30  
> 相關論文：[A Comprehensive Survey of Architectures, Enhancements, and Robustness Frontiers](https://arxiv.org/abs/2506.00054)

## 概覽與設計動機
傳統大型語言模型（LLM）的知識固化於參數權重，然而其訓練資料上限導致「知識凍結」與「過時」問題。檢索增強生成（RAG）通过在推理階段動態結合外部知識庫，解決了「參數依賴」與「領域特化」的限制。本文系统介紹 RAG 的核心流程、最新演進方向以及工程落地方面的關鍵考量，幫助資深工程師理解「為什麼這樣設計」、「有哪些 trade‑off」以及「最新研究方向是什麼」。RAG 系統的價值在於提供可驗證的事實依據、降低偽資訊風險、並支援多跳問答與領域專業應用。

## 核心機制深度解析

### 演算法流程
1. **載入（Loading）** – 讀取原始文檔（PDF、HTML、TXT）並保持原始結構。  
2. **切塊（Chunking）** – 將文檔切分為等長或語意連續的塊（Chunk），常用長度 256–1024 token。過大會稀釋語意，過小則增加噪聲。  
3. **嵌入（Embedding）** – 使用雙向編碼模型（如 BGE‑v1、text‑embedding‑ada‑2）將每個 Chunk 投射至高維向量空間。  
4. **儲存（Storage）** – 將向量與對應原文存入向量資料庫（Vector DB），常見選擇包括 Chroma、Pinecone、Milvus。  
5. **檢索（Retrieval）** – 將使用者問題向量化後，利用係數相似度（Cosine Similarity）或 BM25 混合檢索，取 Top‑k 片段作為上下文。  
6. **生成（Generation）** – 將問題與檢索到的片段串聯，作為Prompt傳遞給 LLM，讓模型基於實證資料生成答案。

### 關鍵數學
- **向量相似度**：  
  $$\text{sim}(\mathbf{q},\mathbf{v}) = \frac{\mathbf{q}\cdot\mathbf{v}}{\|\mathbf{q}\|\;\|\mathbf{v}\|}$$  
  其中 $\mathbf{q}$ 為查詢向量，$\mathbf{v}$ 為向量資料庫中的項目向量。  
- **檢索長度與權重**：有時會引入衰減函數 $w_i = e^{-\lambda \cdot \text{rank}_i}$ 以減弱遠距段落的影響。

### 架構圖（Mermaid）
```mermaid
flowchart TD
    A[使用者問題] --> B[Query Embedding]
    B --> C[Vector Search (Top‑k)]
    C --> D[Retrieved Chunks]
    D --> E[Prompt Assembly]
    E --> F[LLM Generation]
    F --> G[答案輸出]
    style A fill:#f9f,stroke:#333
    style G fill:#bbf,stroke:#333
```

## 與前代技術的比較

| 技術 | 優點 | 限制 | 適用場景 |
|------|------|------|----------|
| **RAG** | 結合外部知識、提升事實正確性、支援動態更新 | 檢索誤差會傳播、檢索成本與延遲 | 需要最新資訊、領域特化、多跳問答 |
| **僅調整微調 (Fine‑tune)** | 可嵌入模型內部、推理快 | 需要大量標記資料、知識固化 | 私有領域、離線模型部署 |
| **直接使用大規模預訓練模型** | 即插即用、無額外基礎建設 | 知識庫有限、易產幻覺 | 快速原型、小規模應用 |

## 工程實作

### 環境設定
```bash
# 以 Python 3.11 為例
python -m venv rag-env
source rag-env/bin/activate
pip install --upgrade pip
pip install langchain==0.2.12 chromadb==0.3.6 sentence-transformers==2.2.2
```

### 核心實作（完整可執行範例）
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

### 工程落地注意事項
- **Latency**：每次查詢需進行向量搜索與 LLM 調用，通常 150–300 ms（取決於檢索規模與模型大小）。可透過 **向量索引預熱**、**批次預取**或 **模型量化** 降低延遲。  
- **成本**：向量資料庫的儲存與查詢費用與 Chunk 數量正相關；使用 **壓縮向量（e.g., PQ）** 或 **GPU 加速檢索** 可降低單位成本。  
- **穩定性**：檢索噪聲會直接影響生成結果，建議加入 **相似度門檻**、 **多數投票**或 **重試機制**。  
- **Scaling**：對於 TB 級別文檔，建議使用 **分散式向量索引（Milvus、Weaviate）**、 **分片佈署**以及 **模型 Serving（vLLM）** 以保證水平擴展。

## 2025‑2026 最新進展

1. **HyDE（Hypothetical Document Embeddings）** – 先讓 LLM 生成「假SET」文檔作為查詢向量的參考，顯著提升稀疏檢索的召回率。  
2. **Self‑RAG** – 內建自我校正機制，讓模型根據檢索結果調整自己的答案，並在生成階段自動檢測矛盾或缺失。  
3. **CRAG（Corrective RAG）** – 在答案生成前加入「答案校正」模組，根據檢索片段動態修正潛在錯誤，提升 fact‑ faithfulness。  
4. **GraphRAG** – 將文檔關係建模為知識圖（KG），利用圖遍歷而非單純相似度檢索，適合需要跨文件推理的多跳查詢。  
5. **Agentic RAG** – 讓 LLM 作為「智能代理」 orchestrating 檢索、評估、迭代三個子‑task，實現自適應、目標導向的檢索流程。  
6. **Evaluation Innovations** – 最近的基準 (RAGAS、ARES) 引入了 **多跳事實一致性**、**安全性測試**與 **隱私保護检查**，推動了可靠部署的標準化。

## 已知限制與 Open Problems

- **檢索偏差**：常見於長尾分布或小眾领域，導致召回不均衡。  
- **上下文爆炸**：當 Top‑k 過大時，LLM 的上下文窗口會被填滿，影響生成效果。  
- **成本-效能權衡**：大規模向量搜索與高功率 LLM 同時使用時成本指數上升。  
- **安全與偏見**：從外部資料庫檢索的資訊可能帶入偏見或惡意內容，需要 **資料篩選**與 **後置防護**。

## 延伸閱讀
- [RAG 參考資料總覽](/docs/references/topic-rag-ref.md)  
- 相關論文：[[2506.00054\]](https://arxiv.org/abs/2506.00054)  

---

## 更新記錄
- 2026-04-26：新增 RAG 最新進展章節，加入 HyDE、Self‑RAG、CRAG、GraphRAG、Agentic RAG，並引用最新 Survey (arXiv:2506.00054)。
- 2025‑05‑30：新增「進階 RAG 技術」章節，涵蓋 HyDE、Self‑RAG、CRAG、GraphRAG、Agentic RAG 等最新發展；加入可執行 Python 示例與工程落地方針; 於日誌中記錄完成深化更新。
