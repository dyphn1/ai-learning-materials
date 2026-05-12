---
title: "HyDE — 假設文件嵌入"
parent: ../topic-rag.md
last_updated: 2026-05-13
---

# HyDE — Hypothetical Document Embeddings（假設文件嵌入）

> 相關論文：[Precise Zero-Shot Dense Retrieval without Relevance Labels (Gao et al., 2022)](https://arxiv.org/abs/2212.10496)

## 動機與背景

標準稠密檢索的缺點：**Query 與文件的向量分佈不一致**。用戶的問題（短、口語化）與知識庫中的文件（長、正式）在向量空間中往往距離較遠，即使語意完全相符。  
HyDE 的洞察：「先讓 LLM 生成一個假設性的回答文件，再用這個文件的向量去檢索，比用原始 Query 向量更準確。」

## 核心演算法

```mermaid
flowchart LR
    Q[User Query] --> LLM[LLM: 生成假設性答案文件\nhypothetical document]
    LLM --> HEmb[Embedding: 假設文件向量\nhyp_emb]
    HEmb --> Ret[向量庫檢索 Top-k]
    Ret --> Real[真實相關文件]
    Real --> LLM2[LLM: 最終回答生成]
```

**步驟說明**：
1. 給定 Query $q$，使用 LLM 生成 $n$ 個假設性答案文件 $\hat{d}_1, ..., \hat{d}_n$（無需包含正確答案，僅需語言風格接近）
2. 對每個 $\hat{d}_i$ 計算嵌入 $\mathbf{e}_i = \text{Encoder}(\hat{d}_i)$
3. 若 $n > 1$，取均值：$\bar{\mathbf{e}} = \frac{1}{n}\sum_i \mathbf{e}_i$
4. 用 $\bar{\mathbf{e}}$ 在向量庫中執行 $k$-NN 搜尋
5. 將真實文件作為 Context，LLM 生成最終答案

## 關鍵數學

向量相似度搜尋（MIPS）：
$$\hat{d}^* = \arg\max_{d \in \mathcal{D}} \cos(\bar{\mathbf{e}}, \text{Encoder}(d))$$

假設文件的 Prompt 設計（GenInst）：
- TREC-COVID: *"Write a scientific abstract that answers the question: {q}"*
- WebQuestions: *"Produce a Wikipedia passage that answers: {q}"*

## 召回率提升

原始論文報告（BEIR benchmark）：

| 資料集 | BM25 | DPR | HyDE |
|-------|------|-----|------|
| TREC-COVID | 65.6 | 33.2 | **77.4** |
| FiQA-2018 | 23.6 | 11.2 | **29.0** |
| SCIDOCS | 15.8 | 7.7 | **17.8** |

HyDE 在**零樣本場景**（不需要對齊訓練資料）下尤其出色。

## 何時失效

1. **LLM 對主題一無所知**：若假設文件嚴重錯誤，向量方向偏移，反而降低召回
2. **極短/模糊的 Query**：LLM 難以生成有意義的假設文件
3. **高延遲敏感應用**：多一次 LLM 生成增加端到端延遲 100–500ms
4. **封閉域程式碼搜尋**：假設文件（自然語言描述）與程式碼的向量空間差異過大

## 與 Query Expansion 的差異

| | Query Expansion | HyDE |
|---|---|---|
| 擴展目標 | 原始 Query 詞彙 | 假設答案文件 |
| 使用 LLM | 可選（基於同義詞也可） | 必須 |
| 向量空間對齊 | Query→Query | Query→Document 橋接 |
| 效果瓶頸 | Query 品質 | LLM 生成品質 |

## 工程注意事項

- 推薦與 `text-embedding-3-large` 或 `BGE-M3` 搭配使用
- $n=1$ 通常足夠（更多假設文件僅在 Query 非常模糊時有額外增益）
- LangChain 整合：[HypotheticalDocumentEmbedder](https://python.langchain.com/docs/integrations/retrievers/hyde/)
- 生成 Prompt 的語言應與向量庫一致（中英混合庫需考慮）

---
*父頁面：[RAG 主概覽](../topic-rag.md)*
