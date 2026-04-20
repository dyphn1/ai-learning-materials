# AI 主題分類參考文件：檢索增強生成 (RAG)

## 🔍 什麼是 RAG?
Retrieval Augmented Generation (RAG) 的核心思想是：不讓 LLM 僅靠其「訓練內存」回答問題，而是先從外部資料庫中「檢索」相關資訊，再將這些資訊作為「上下文」餵給 LLM，讓它基於事實來生成答案。

## ⚙️ RAG 的工作流程
1.  **載入 (Loading):** 讀取原始文件 (PDF, DOCX, TXT)。
2.  **切塊 (Chunking):** 將長文件切分成大小適中、語義連續的塊 (Chunks)。過大會稀釋上下文，過小會丟失語境。
3.  **嵌入 (Embedding):** 使用 Embedding 模型（如 BGE, text-embedding-ada-2）將每個文本塊轉換成高維度的向量（Vector）。
4.  **儲存 (Storage):** 將這些向量及原始文本塊存儲到 **向量資料庫 (Vector Database)** 中 (如 Chroma, Pinecone)。
5.  **檢索 (Retrieval):** 當用戶提問時，先將提問轉換成向量，然後在向量資料庫中進行 **餘弦相似度 (Cosine Similarity)** 搜索，找到最相關的 $K$ 個文本塊。
6.  **生成 (Generation):** 將用戶問題和檢索到的 $K$ 個文本塊作為上下文，一次性輸入給 LLM，要求它基於此上下文回答問題。

## 💡 關鍵概念
*   **Embedding 模型:** 決定了向量的品質。
*   **向量資料庫:** 提供了高效的相似度搜索能力。
*   **Hybrid Search:** 結合語義搜索（向量）和關鍵字搜索（BM25），提高檢索的準確性。
