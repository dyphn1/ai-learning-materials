# 深度學習任務清單 - topic-multi-agent

## 架構深度解析
- [ ] 了解原理
- [ ] 流程圖說明
- [ ] 核心元件拆解

## 實作範例
- [ ] 完整可執行程式碼範例（含環境設定）

### 參考程式碼片段
**片段 1：**
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

**片段 2：**
```
python
from crewai import Agent, Task, Crew

researcher = Agent(role="研究員", goal="蒐集資訊", ...)
writer = Agent(role="寫作者", goal="整理成報告", ...)

crew = Crew(agents=[researcher, writer], tasks=[...])
result = crew.kickoff()
```


## 應用場景
- [ ] 案例 1
- [ ] 案例 2
- [ ] 案例 3

### 相關概念與術語
- Orchestrator 職責
- Worker 職責
- CrewAI
- AutoGen
- LangGraph
- openclaw

## 擴充與進階
- [ ] 進階技術
- [ ] 變體
- [ ] 相關論文

### 參考表格
**表格 1：**
| 框架 | 特色 | 適合場景 |
|------|------|---------|
| **CrewAI** | 以「角色」定義 agent，直觀易用 | 快速原型 |
| **AutoGen** | 微軟出品，支援多輪對話協作 | 研究 / 複雜任務 |
| **LangGraph** | 圖形化 workflow，靈活可控 | 生產環境 |
| **openclaw** | 本地執行，隱私安全 | 個人 / 企業內網 |



## 優化技巧
- [ ] 常見問題與解決方案
- [ ] 效能調優方法

## 參考資源
- [ ] 搜尋相關文章並填入 URL

*此文件由腳本自動生成，來源：topic-multi-agent.md*
*生成時間：2026-04-21 20:06:43*