---
title: "Self-RAG — 自迭代檢索生成"
parent: ../topic-rag.md
last_updated: 2026-05-13
---

# Self-RAG — 自迭代檢索生成

> 相關論文：[Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection (Asai et al., 2023)](https://arxiv.org/abs/2310.11511)

## 動機與背景

傳統 RAG 的問題在於：無論問題難易，都強制檢索，導致簡單問題被無關上下文干擾；複雜問題只檢索一次也無法深入。  
Self-RAG 的核心貢獻是讓模型**自行決定何時該檢索、檢索後如何批判性評估結果**，透過特殊的反射 token（Reflection Token）融入訓練。

## 核心演算法

Self-RAG 在模型詞彙中加入 4 種特殊 token：

| Token | 意義 | 可能值 |
|-------|------|-------|
| `[Retrieve]` | 是否需要檢索 | `yes` / `no` / `continue` |
| `[IsREL]` | 檢索片段與問題的相關性 | `relevant` / `irrelevant` |
| `[IsSUP]` | 生成內容是否受片段支持 | `fully supported` / `partially supported` / `no support` |
| `[IsUSE]` | 整體回應是否有用 | `5` / `4` / `3` / `2` / `1` |

### 生成流程

```mermaid
flowchart TD
    Q[User Query] --> R{[Retrieve]?}
    R -- yes --> Fetch[Retriever: Top-k passages]
    R -- no --> Direct[直接生成回應]
    Fetch --> Eval[逐段評估 IsREL]
    Eval --> Gen[逐段條件生成]
    Gen --> Sup[IsUSE + IsSUP 評分]
    Sup --> Rank[依分數排列候選回應]
    Rank --> Output[最終回應]
    Direct --> Output
```

### 訓練策略

Self-RAG 使用**兩階段訓練**：
1. **Critic 模型訓練**：訓練一個獨立分類器，針對每個檢索片段與生成段落，標記 IsREL / IsSUP / IsUSE。
2. **Generator 微調**：使用增強後的語料（含 Reflection Token）透過標準 next-token prediction 訓練 Generator，使其學會原生輸出 Reflection Token。

### 推理時的排名策略

對每個候選片段 $p_i$ 生成的候選回應 $y_i$，計算綜合分數：

$$\text{score}(y_i) = p(\text{IsUSE} \geq 4 \mid y_i, p_i) + \lambda \cdot p(\text{IsSUP} = \text{fully} \mid y_i, p_i)$$

最終選取分數最高的 $(y_i, p_i)$ 組合。

## 與 Naive RAG 的比較

| 面向 | Naive RAG | Self-RAG |
|------|-----------|---------|
| 檢索觸發 | 永遠 | 模型自決 |
| 批判機制 | 無 | IsREL / IsSUP / IsUSE |
| 多跳支持 | 有限 | 透過 `[Retrieve]=continue` 迭代 |
| 幻覺率（ASQA） | 較高 | ~15% 降低 |
| 推理成本 | 低 | 中（多次前向傳播） |

## 適用 / 不適用情境

**適用**：
- 開放領域問答（開放域 QA）
- 需要多跳推理的場景
- 對幻覺容忍度低、需要 citation 的應用

**不適用**：
- 即時對話（延遲敏感）
- 完全封閉域（上下文固定、不需外部知識）
- 資源受限的邊緣部署

## 工程注意事項

- Self-RAG 需要微調基礎模型，無法直接套用至通用 API（如 OpenAI GPT-4）
- 開源實作：[AkariAsai/self-rag](https://github.com/AkariAsai/self-rag)（Llama 2 7B / 13B）
- 推理效能：比同規模模型慢約 2–3×（每個片段需獨立前向傳播）
- 與 RAGAs 評估框架相容，可使用 `groundedness` 指標衡量 IsSUP 的精確度

---
*父頁面：[RAG 主概覽](../topic-rag.md)*
