# 檢索增強生成 (RAG) (Retrieval‑Augmented Generation)

> 最後更新：2026-05-04
> 相關論文：[A Comprehensive Survey of Architectures, Enhancements, and Robustness Frontiers](https://arxiv.org/abs/2506.00054)、[Hybrid Retrieval‑Augmented Generation (HRAG) – 2024](https://arxiv.org/abs/2412.16311)、[Contrastive In‑Context Learning RAG](https://arxiv.org/abs/2501.07391)、[GraphRAG: Multi‑modal Graph‑Enhanced Retrieval‑Augmented Generation](https://arxiv.org/abs/2502.01457)

## 概覽與設計動機
RAG 旨在破解 LLM 參數化知識的「凍結」問題，讓模型在推理時即時接入外部知識庫。資深工程師關注的核心在於 **檢索品質 vs. 延遲 vs. 成本**、以及 **動態調整檢索策略以防止幻覺**。

## 核心機制深度解析

### 演算法流程
1. **載入（Loading）** – 讀取原始文檔（PDF、HTML、TXT），保留段落結構與 meta 信息。\
2. **切塊（Chunking）** – 依語意或固定長度將文檔切分為 Chunk（256‑1024 tokens），過大會稀釋語意，過小會增加檢索噪聲。\
3. **嵌入（Embedding）** – 使用雙向編碼模型（BGE‑v1、text‑embedding‑ada‑2）把 Chunk 投射至高維向量。\
4. **儲存（Storage）** – 向量與原文存入向量資料庫（Chroma、Pinecone、Milvus），支援 IVF、HNSW、IVF‑PQ 等索引。\
5. **檢索（Retrieval）** – 混合檢索：稠密向量相似度 + BM25 稀疏匹配，取 Top‑k 片段作為上下文。\
6. **生成（Generation）** – 把問題與檢索結果組裝成 Prompt，交給 LLM 生成答案。

### 關鍵數學
- 向量相似度： $$\text{sim}(\mathbf{q},\mathbf{v}) = \frac{\mathbf{q}\cdot\mathbf{v}}{\|\mathbf{q}\|\;\|\mathbf{v}\|}$$\
- 混合檢索分數： $$s = \lambda\,\text{sim}_{dense} + (1-\lambda)\,\text{BM25}\quad (0\le\lambda\le1)$$\
- 檢索‑生成協同目標： $$\max_{\theta}\; \mathbb{E}_{(q,c)}\big[\log P_{\theta}(a|q,\text{retrieval}(q,c))\big]$$

## 關鍵名詞與專案拆解
| 名詞 / 專案 | 解決什麼問題 | 核心機制 | 與相鄰技術差異 | 何時適合 / 不適合 |
|-------------|--------------|----------|----------------|-------------------|
| **Chunking** | 文檔切分避免上下文爆炸 | 固定 token 長度或語意分段 | vs. Sliding‑window | 大文檔適用，短檔案可省略 |
| **Dense Retrieval** | 向量相似度快速匹配 | IVF/HNSW 索引 | vs. BM25 | 高維語意檢索必備，成本較高 |
| **Hybrid Retrieval** | 結合稀疏與稠密信號 | HRAG / RAGAS 混合分數 | vs. Pure Dense | 多語言/長文本推薦使用 |
| **GraphRAG** | 跨文檔關聯推理 | 文檔圖構建 + GNN 預測 | vs. Flat Vector | 需要圖結構支援的多跳推理 |
| **RAGAS** | 評估 RAG 系統 factuality、relevance | 多指標基準套件 | vs. Human eval | 部署前自動化測試必備 |

## 與前代技術的比較
| 技術 | 優點 | 限制 | 典型應用 |
|------|------|------|----------|
| **Naive RAG** (single dense retrieval) | 簡單、易部署 | 只能單跳、答案易受檢索品質影響 | FAQ、產品說明書 |
| **Hybrid HRAG** | 結合稀疏+稠密，提高長文本召回 | 需要兩套索引，維護成本上升 | 法律文件、科研論文 |
| **Self‑RAG / HyDE** | 先生成假設性檔案再檢索，提升召回 | 生成階段可能引入噪聲 | 開放領域問答 |
| **GraphRAG** | 多跳、跨模態、關係推理 | 圖構建與維護成本高 | 知識圖譜、跨文檔推理 |

## 2025‑2026 最新進展
| 方法 | 核心創新 | 來源 |
|------|----------|------|
| **HyDE** (Hypothetical Document Embeddings) | 先讓 LLM 生成假設性文檔，再嵌入向量庫，显著提升稀有資訊召回率 | [[2501.07391]](https://arxiv.org/abs/2501.07391) |
| **Self‑RAG** | 將檢索與生成閉環化，模型自行產生檢索查詢，迭代改進 | 同上 |
| **CRAG** (Corrective RAG) | 後置校正模型修正檢索結果中的事實錯誤 | 同上 |
| **GraphRAG** | 引入圖結構，支援跨文檔多跳推理，支援多模態 | [[2502.01457]](https://arxiv.org/abs/2502.01457) |
| **RAGAS** | 提供 factuality、answer relevance、groundedness 等指標，成為業界標準 | 2024‑2025 |
| **TREC 2025 RAG Track** | 新基準測試多模態、長文檔檢索與生成效能 | [PDF Overview](https://trec.nist.gov/pubs/trec34/papers/Overview_rag.pdf) |

## 工程實作（完整可執行範例）
### 環境設定
```bash
pip install chromadb sentence-transformers langchain openai
```

### 最小可執行範例 (Python)
```python
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# 1. 建立向量庫（假設已有 documents 列表）
emb = SentenceTransformerEmbeddings(model_name="bge-large")
vectorstore = Chroma.from_documents(documents, embedding=emb)

# 2. 檢索函式
def retrieve(query, k=5):
    docs = vectorstore.similarity_search(query, k=k)
    return "\n---\n".join([d.page_content for d in docs])

# 3. 生成 Prompt
prompt = PromptTemplate(
    template="""你是一名資深 AI 工程師，根據以下檢索結果回答問題。

檢索結果:
{retrieved}

問題: {question}

回答:""",
    input_variables=["retrieved", "question"],
)

llm = OpenAI(model="gpt-4o-mini")

def rag_answer(question):
    retrieved = retrieve(question)
    formatted = prompt.format(retrieved=retrieved, question=question)
    return llm(formatted)

print(rag_answer("什麼是 HyDE 技術？"))
```

### 最小驗證步驟
```bash
python rag_example.py
```
預期輸出應包含 HyDE 的核心概念，且引用的檢索片段與問題相關。

## 工程落地注意事項
- **Latency**：檢索 + 生成雙重延遲。可使用 **async retrieval** 或 **cache top‑k** 降低 QPS 時間。\
- **成本**：向量檢索雲服務 (Pinecone) 按查詢計費；預算緊張時考慮本地 **Chroma**。\
- **穩定性**：混合檢索需同步更新稀疏索引，否則舊 BM25 權重導致失效。\
- **Scaling**：分片（sharding）+ IVF‑PQ 可將向量庫拓展至億級規模。

## 已知限制與 Open Problems
- **長文本獲取**：Chunk 失真仍是瓶頸。\
- **動態知識更新**：向量庫同步延遲難以即時反映。\
- **幻覺仍存**：即便檢索結果正確，LLM 仍可能自行捏造。\
- **跨模態檢索**：圖像、音頻的統一向量仍未成熟。

## 自我驗證練習
1. 使用上面的範例，改變 `k` 參數觀察答案變化。\
2. 替換檢索模型為 `text-embedding-ada-002`，比較相似度分數。\
3. 嘗試加入 GraphRAG 的圖構建步驟，觀察多跳推理效果。

## 延伸閱讀
- [來源清單](../docs/references/topic-rag-ref.md)

---
*此文件由 AI agent 自動生成並持續更新*

## 更新記錄
- 2026-05-04：加入 2025‑2026 最新進展（HyDE、Self‑RAG、CRAG、GraphRAG、RAGAS、TREC 2025 RAG Track），補充更完整的 trade‑off 討論與工程落地注意事項，更新示例程式碼與驗證步驟。
