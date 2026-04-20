# Level 3：Agent 設計指南
*來源檔案: level3-agent-design.md*

## 核心概念
- Short-term
- Long-term
- Episodic
- Semantic
- ReAct = Reasoning + Acting
- 建議的安全邊界設定
- Planner
- Executor
- Replanner

## 實作範例
### 範例 1
```
思考（Thought）：我需要知道今天的天氣
行動（Action）：web_search("台北今天天氣")
觀察（Observation）：搜尋結果：27°C，晴天
思考（Thought）：已取得天氣資訊，可以回答用戶
回答（Final Answer）：台北今天 27°C，晴天
```

### 範例 2
```
{
  "tools": {
    "exec": { "ask": "off" },
    "read": {},
    "write": {},
    "web_search": {},
    "web_fetch": {}
  }
}
```

### 範例 3
```
{
  "tools": {
    "exec": {
      "denyCommands": ["rm -rf", "sudo rm", "format", "mkfs", "dd if="]
    }
  }
}
```


---

*生成時間: 2026-04-20 21:18:47*