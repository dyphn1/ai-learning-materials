# Multi-Agent 系統指南 學習筆記
*來源檔案: topic-multi-agent.md*
*同步更新: 2026-04-26*

## 一句話理解
*無法自動摘要，請回看主文的概覽與設計動機章節。*

## 必記重點
- **CrewAI**
- **AutoGen**
- **LangGraph**
- **openclaw**
- Orchestrator 職責

## 核心名詞速記
- **CrewAI**
- **AutoGen**
- **LangGraph**
- **openclaw**
- Orchestrator 職責
- Worker 職責
- CrewAI
- AutoGen

## 必背公式
*本篇無核心公式*

## 實作範例重點
### 範例片段
```python
from crewai import Agent, Task, Crew

researcher = Agent(role="研究員", goal="蒐集資訊", ...)
writer = Agent(role="寫作者", goal="整理成報告", ...)

crew = Crew(agents=[researcher, writer], tasks=[...])
result = crew.kickoff()
```

## 自我檢查
*無自我檢查題目*