# Agentic Workflow 設計指南

## 學習目標
理解並設計不同類型的 AI agent 工作流程模式。

---

## 四種核心設計模式

### 1. Sequential（順序執行）
每個步驟依序完成，前一步的輸出是下一步的輸入：
```
讀取文件 → 摘要 → 翻譯 → 儲存
```
**優點**：邏輯清晰，易於除錯  
**缺點**：效率低，無法並行

### 2. Parallel（平行執行）
多個任務同時執行，最後合併結果：
```
      ┌→ 搜尋 Wikipedia →┐
問題 →│→ 搜尋新聞 -------│→ 整合回答
      └→ 搜尋學術論文 →--┘
```
**優點**：大幅提升速度  
**缺點**：需要合併策略

### 3. Conditional（條件分支）
根據判斷結果走不同路徑：
```
用戶輸入 → 分類 → [程式問題] → 程式碼 agent
                 → [資料問題] → 資料分析 agent
                 → [其他]    → 通用 agent
```

### 4. Iterative Loop（迭代迴圈）
重複執行直到滿足條件（Reflection 模式）：
```
生成初稿 → 評估品質 → [不滿意] → 修改 → 評估品質 → ...
                   → [滿意]  → 輸出
```
openclaw agent 的多輪對話即是 iterative loop 的一種。

---

## LangGraph 簡介

LangGraph 是 LangChain 生態系的 workflow 框架，以**有向圖（DAG）**定義 agent 流程：

```python
from langgraph.graph import StateGraph

graph = StateGraph(State)
graph.add_node("fetch", fetch_data)
graph.add_node("analyze", analyze_data)
graph.add_edge("fetch", "analyze")
graph.add_conditional_edges("analyze", route_fn, {
    "retry": "fetch",
    "done": END
})
```

**特色**：
- 支援 cycles（循環，適合 iterative loop）
- 內建 state 管理（跨步驟共享資料）
- 支援 human-in-the-loop（暫停等待人工確認）

---

## openclaw 對應

| 模式 | openclaw 實作 |
|------|-------------|
| Sequential | cron message 中逐步列出指令 |
| Parallel | 多個 cron job 同時執行 |
| Conditional | agent 在 message 中加入 if/else 邏輯判斷 |
| Iterative | agent session 多輪對話 |

---

*建立時間：2026-04-19*
