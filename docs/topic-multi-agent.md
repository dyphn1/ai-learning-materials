# Multi-Agent 系統指南

## 學習目標
理解多 agent 協作架構，能夠設計 Orchestrator/Worker 模式的 AI 系統。

---

## 為什麼需要 Multi-Agent？

單一 agent 的限制：
- Context window 有限，無法處理超長任務
- 複雜任務需要不同專長（寫程式 vs. 分析資料 vs. 搜尋）
- 單點失敗風險高

Multi-Agent 解法：分工協作，每個 agent 專注特定能力。

---

## Orchestrator / Worker 架構

```
用戶請求
    │
    ▼
Orchestrator（規劃 & 協調）
    │
    ├→ Worker A（程式碼生成）
    ├→ Worker B（網路搜尋）
    └→ Worker C（文件整理）
    │
    ▼
整合結果 → 回覆用戶
```

**Orchestrator 職責**：
- 分解任務為子任務
- 分配給合適的 worker
- 收集並整合結果
- 處理錯誤重試

**Worker 職責**：
- 專注單一能力
- 接收明確指令
- 回傳結構化結果

---

## 主流框架對比

| 框架 | 特色 | 適合場景 |
|------|------|---------|
| **CrewAI** | 以「角色」定義 agent，直觀易用 | 快速原型 |
| **AutoGen** | 微軟出品，支援多輪對話協作 | 研究 / 複雜任務 |
| **LangGraph** | 圖形化 workflow，靈活可控 | 生產環境 |
| **openclaw** | 本地執行，隱私安全 | 個人 / 企業內網 |

### CrewAI 範例
```python
from crewai import Agent, Task, Crew

researcher = Agent(role="研究員", goal="蒐集資訊", ...)
writer = Agent(role="寫作者", goal="整理成報告", ...)

crew = Crew(agents=[researcher, writer], tasks=[...])
result = crew.kickoff()
```

### AutoGen 範例
```python
from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent("assistant", llm_config={...})
user_proxy = UserProxyAgent("user", code_execution_config={...})
user_proxy.initiate_chat(assistant, message="分析這份資料...")
```

---

## openclaw 的 Per-Channel-Peer 機制

openclaw 支援多個 agent 透過 Discord / Telegram 頻道互相傳訊協作：
- 每個頻道可綁定不同 agent（不同模型、不同工具）
- Agent 可以互相 @mention 傳遞子任務
- `groupPolicy: "open"` 允許同 server 的 agent 互動

---

*建立時間：2026-04-19*
