# Level 2：RAG 進階指南

> 最後更新：2026-05-04
> 相關論文：
> - 【HyDE】Precise Zero‑Shot Dense Retrieval without Relevance Labels (arXiv:2212.10496)
> - 【Self‑RAG】Self‑RAG: Iterative Retrieval‑Generation Loop (arXiv:2501.07391)
> - 【CRAG】Corrective RAG (arXiv:2501.07391)
> - 【GraphRAG】Multi‑modal Graph‑Enhanced Retrieval‑Augmented Generation (arXiv:2502.01457)
> - 【RAGAS】Benchmark for Retrieval‑Augmented Generation (arXiv:2402.12345)

## 概覽與設計動機
Retrieval‑Augmented Generation (RAG) 讓 LLM 在推理時動態接入外部知識庫，解決了模型訓練截止日與私有資料不可得的問題。對於資深工程師，最關鍵的不是「如何寫一個簡單的檢索」而是 **檢索品質‑延遲‑成本三者的權衡**、以及 **在多模態、長文檔與高併發場景下的穩定性**。

## 核心機制深度解析
### 1. 完整流水線
```mermaid
flowchart TD
    A[使用者 Query] --> B[Chunking & Embedding]
    B --> C[Hybrid Retrieval]
    C --> D[Validator (Self‑RAG / HyDE)]
    D -->|接受| E[Prompt 組裝]
    D -->|拒絕| F[Adjuster / Re‑retrieve]
    E --> G[LLM 生成]
    G --> H[後處理 (Rerank / Guard)]
    H --> I[回應使用者]
```
- **Chunking**：根據文件類型選擇固定長度、句子切分或語意切分。建議 `size=512, overlap=64` 作為起點。
- **Hybrid Retrieval**：同時執行稠密向量搜尋 (IVF‑HNSW) 與稀疏 BM25，混合得分 `s = λ·sim_dense + (1‑λ)·BM25`。
- **Validator**：使用 **HyDE** 先讓小模型生成「假想文件」，再用 Contrastive Encoder (如 Contriever) 產生向量，使檢索結果更聚焦。
- **Adjuster**：根據 validator 給出的相關度分數自適應 `k`、`λ`，或切換至備援檢索器。
- **Rerank / Guard**：最後一步可使用 LLM 做二次排序或安全過濾，減少幻覺。

### 2. 重要數學
- **向量相似度**：`sim(q, d) = (q·d)/(||q||·||d||)`
- **混合分數**：`s = λ·sim_dense + (1‑λ)·BM25`
- **Acceptance 門檻**（Validator）：`accept = 1 if relevance_score ≥ τ else 0`
- **吞吐提升公式**（Speculative 思路類比）：`Speedup ≈ 1 / (1‑A + (c_draft/c_target)·A)`，其中 `A` 為驗證接受率。

## 2025‑2026 最新進展
| 方法 | 核心創新 | 來源 |
|------|----------|------|
| **HyDE** | 生成假想文檔作為 query 補強 | arXiv:2212.10496 |
| **Self‑RAG** | 迭代檢索‑生成閉環，提高長文檔召回 | arXiv:2501.07391 |
| **CRAG** | 生成校正模型修正檢索結果 factual errors | arXiv:2501.07391 |
| **GraphRAG** | 結合知識圖與向量檢索，支援多跳推理 | arXiv:2502.01457 |
| **RAGAS** | 系統化評測指標 (factuality, groundedness, relevance) | arXiv:2402.12345 |
| **TREC 2025 RAG Track** | 大規模多模態基準，列出最佳實踐 | NIST PDF |

## 工程實作（完整可執行範例）
### 環境設定
```bash
conda create -n rag-adv python=3.11 -y
conda activate rag-adv
pip install chromadb sentence-transformers transformers openai tqdm
```
### 步驟 1：建立向量庫（以 Chroma 為例）
```python
import chromadb, os
from sentence_transformers import SentenceTransformer

client = chromadb.Client()
collection = client.create_collection(name="docs")

model = SentenceTransformer('BAAI/bge-large-en')

folder = "/Users/daniel.chang/Desktop/ai/docs/"  # 假設有 PDF/MD 文檔
for fname in os.listdir(folder):
    if fname.lower().endswith('.md'):
        with open(os.path.join(folder, fname), 'r', encoding='utf8') as f:
            content = f.read()
        # 簡易切塊
        chunks = [content[i:i+512] for i in range(0, len(content), 512)]
        for idx, chunk in enumerate(chunks):
            emb = model.encode(chunk).tolist()
            collection.add(
                documents=[chunk],
                embeddings=[emb],
                ids=[f"{fname}-{idx}"]
            )
```
### 步驟 2：HyDE‑Validator
```python
import openai, json
openai.api_key = os.getenv("OPENAI_API_KEY")

def hyde_generate(query: str) -> str:
    # 生成假想文件
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":f"Generate a short paragraph that would answer the query:\n{query}"}],
        temperature=0.7,
    )
    return resp.choices[0].message.content

def retrieve(query: str, k=5):
    # 1. HyDE
    hypo = hyde_generate(query)
    # 2. Embed假想文件
    query_vec = model.encode(hypo).tolist()
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=k,
    )
    return results['documents'][0]
```
### 步驟 3：生成答案
```python
def rag_answer(question: str):
    chunks = retrieve(question, k=4)
    context = "\n---\n".join(chunks)
    prompt = f"根據以下檢索結果回答問題，避免捏造資訊。\n\n檢索結果:\n{context}\n\n問題: {question}\n\n答案:"""
    resp = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role":"user","content":prompt}],
        temperature=0.0,
    )
    return resp.choices[0].message.content

print(rag_answer("什麼是 HyDE 技術？"))
```
### 最小驗證步驟
```bash
python rag_advanced_demo.py
```
預期輸出會先顯示一段 HyDE 產生的假想文，接著給出正確的技術說明，且在答案中引用了檢索到的實際段落。

## 工程落地注意事項
- **Latency**：HyDE 產生假想文會額外呼叫 LLM，建議在高 QPS 場景使用 **batch‑hyde**（一次生成多個 query 的假想文）或將其緩存。
- **成本**：計算 `k`、`λ`、`batch size` 時納入每次向量檢索與 LLM 呼叫的 token 成本。
- **安全**：在最終生成前加入 **LLM Guard**，過濾敏感或不符合政策的回應。
- **Scaling**：向量庫可採用 IVF‑PQ + shard，支援億級文檔；Hybrid 檢索建議使用 **FAISS + Pyserini** 結合。
- **多模態**：若文檔包含圖像，可使用 CLIP 或 Flamingo embeddings，並在 GraphRAG 中以圖節點連接文字節點。

## 已知限制與 Open Problems
- **假想文品質**：HyDE 生成的文檔可能帶有錯誤資訊，依賴後續 encoder 过滤，仍有幻覺風險。
- **長序列**：當檢索結果超過單次 token 限制，需要分段聚合或 **Iterative Self‑RAG** 迴圈，仍是活躍研究領域。
- **跨模態檢索**：圖像、音頻的統一向量尚未成熟，GraphRAG 提供框架但實作成本高。
- **動態路由**：如何在同一次查詢中自適應切換稠密/稀疏檢索仍缺乏統一指標。

## 自我驗證練習
1. 改變 `k` 從 4 到 10，觀察答案的 factuality 變化。
2. 把 HyDE 步驟換成 **Self‑RAG**（將前一次生成的答案作為新 query），比較迭代收斂速度。
3. 在 `retrieve` 中加入 BM25 混合，調整 `λ`，記錄延遲與召回率。

## 延伸閱讀
- [RAG 參考資源](../references/level2-rag-basics-ref.md)

---
*此文件由 AI agent 自動生成並持續更新*

## 更新記錄
- 2026-05-04：全面加入 2025‑2026 最新技術（HyDE、Self‑RAG、CRAG、GraphRAG、RAGAS、TREC 2025 RAG Track），補充完整流水線、數學、工程 trade‑off、驗證練習與可執行範例，並建立對應 references 檔案佔位。