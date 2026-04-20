# Level 3：Agent 設計指南

## 學習目標
理解 AI Agent 的架構設計，能夠用 openclaw 建立具備工具呼叫能力的自主 agent。

---

## 什麼是 Agent？

Agent = LLM + 工具（Tools）+ 記憶（Memory）+ 規劃（Planning）

一般 LLM 只能生成文字；Agent 能夠：
- 呼叫外部工具（執行程式、搜尋網路、讀寫文件）
- 根據工具回傳結果繼續推理
- 完成多步驟任務

---

## ReAct 框架

**ReAct = Reasoning + Acting**，LLM 交替輸出推理與行動：

```
思考（Thought）：我需要知道今天的天氣
行動（Action）：web_search("台北今天天氣")
觀察（Observation）：搜尋結果：27°C，晴天
思考（Thought）：已取得天氣資訊，可以回答用戶
回答（Final Answer）：台北今天 27°C，晴天
```

openclaw 的 agent 即採用類似 ReAct 的迴圈架構。

---

## openclaw Agent 實作

### 設定檔位置
`~/.openclaw/openclaw.json`

### 工具允許清單（toolsAllow）
```json
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

### denyCommands 安全邊界
限制 agent 不能執行危險指令：
```json
{
  "tools": {
    "exec": {
      "denyCommands": ["rm -rf", "sudo rm", "format", "mkfs", "dd if="]
    }
  }
}
```

**建議的安全邊界設定**：
- 永遠加上 `rm -rf /` 等破壞性指令的 deny
- 生產環境中 `ask: "always"` 讓人類確認高風險操作
- 開發環境可用 `ask: "off"` 加速迭代

---

## Memory 系統

| 類型 | 說明 | openclaw 對應 |
|------|------|-------------|
| Short-term | 當前 session 的對話歷史 | session context |
| Long-term | 跨 session 的記憶 | memory 插件 |
| Episodic | 過去任務的執行記錄 | cron runs JSONL |
| Semantic | 知識庫（RAG） | 向量資料庫整合 |

---

## Plan-and-Execute 模式

適合複雜多步驟任務：
1. **Planner**：LLM 先生成完整執行計畫（步驟清單）
2. **Executor**：逐步執行每個步驟，可使用工具
3. **Replanner**：若某步驟失敗，重新規劃後續步驟

openclaw cron 的 message prompt 即可設計成先要求 agent 輸出計畫，再執行。

---

*建立時間：2026-04-19*
