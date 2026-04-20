# Agentic Workflow 設計指南
*來源檔案: topic-agentic-workflow.md*

## 核心概念
- Sequential
- Parallel
- Conditional
- Iterative
- 優點
- 缺點
- 有向圖（DAG）
- 特色

## 實作範例
### 範例 1
```
讀取文件 → 摘要 → 翻譯 → 儲存
```

### 範例 2
```
┌→ 搜尋 Wikipedia →┐
問題 →│→ 搜尋新聞 -------│→ 整合回答
      └→ 搜尋學術論文 →--┘
```

### 範例 3
```
用戶輸入 → 分類 → [程式問題] → 程式碼 agent
                 → [資料問題] → 資料分析 agent
                 → [其他]    → 通用 agent
```

### 範例 4
```
生成初稿 → 評估品質 → [不滿意] → 修改 → 評估品質 → ...
                   → [滿意]  → 輸出
```

### 範例 5
```
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


---

*生成時間: 2026-04-20 21:18:47*