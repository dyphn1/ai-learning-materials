# Multi-Agent 系統指南
*來源檔案: topic-multi-agent.md*

## 核心概念
- **CrewAI**
- **AutoGen**
- **LangGraph**
- **openclaw**
- Orchestrator 職責
- Worker 職責
- CrewAI
- AutoGen
- LangGraph
- openclaw

## 實作範例
### 範例 1
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

### 範例 2
```
from crewai import Agent, Task, Crew

researcher = Agent(role="研究員", goal="蒐集資訊", ...)
writer = Agent(role="寫作者", goal="整理成報告", ...)

crew = Crew(agents=[researcher, writer], tasks=[...])
result = crew.kickoff()
```

### 範例 3
```
from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent("assistant", llm_config={...})
user_proxy = UserProxyAgent("user", code_execution_config={...})
user_proxy.initiate_chat(assistant, message="分析這份資料...")
```


---

*生成時間: 2026-04-20 21:18:47*