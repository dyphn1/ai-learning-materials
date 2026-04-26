# Level 3：Agent 設計指南 學習筆記
*來源檔案: level3-agent-design.md*
*同步更新: 2026-04-26*

## 一句話理解
從學習路徑來看，Level 3 的重點不是再多認識一個新名詞，而是理解什麼情況下「把 LLM 包進工作流」才真的值得。當任務只需要單輪摘要或翻譯時，直接呼叫模型通常最便宜；但只要任務開始依賴搜尋、工具、副作用、重試、狀態恢復與人工審批，系統的核心問題就不再是文本生成，而是控制流。Agent 設計要解決的正是這個問題：如何讓模型在可控邊界內成為決策器，而不是讓它直接接管整個系統。

## 必記重點
- Planner：將目標拆成可執行子步驟
- Executor：逐步執行並收集 observation
- Working Memory：把當前任務上下文放在短期記憶
- Episodic / Semantic Memory：事件流 + 向量檢索或結構化儲存
- Approval Gate：在危險操作前中斷等待人工批准

## 核心名詞速記
- Planner：長任務容易迷航
- Executor：把抽象計畫落成工具操作
- Working Memory：保留本輪所需狀態
- Episodic / Semantic Memory：記住過去事件與事實
- Approval Gate：防止高風險副作用誤執行

## 流程速記
1. 接收目標，建立初始狀態與停止條件。
2. 從工作記憶與歷史任務中檢索可用資訊。
3. 由 planner 提出下一步行動與其理由。
4. 經過 tool policy 驗證是否允許執行。
5. 執行工具並取得 observation。
6. 將 observation 與錯誤寫入狀態，必要時持久化 checkpoint。
7. 若結果不滿足停止條件，則 replan；否則輸出結果並關閉流程。

## 必背公式
$$
score = \alpha \cdot relevance + \beta \cdot recency + \gamma \cdot importance
$$

## 實作範例重點
### 範例片段
```python
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class AgentState:
  goal: str
  completed_steps: list[str] = field(default_factory=list)
  observations: list[str] = field(default_factory=list)


def search_docs(query: str) -> str:
  return f"docs search result for: {query}"


def write_report(text: str) -> str:
  return f"report written: {text[:30]}..."


TOOLS = {
  "search_docs": search_docs,
  "write_report": write_report,
}


def plan(state: AgentState) -> list[tuple[str, str]]:
  if not state.completed_steps:
    return [("search_docs", state.goal)]
  return [("write_report", "Summarize findings into a report")]


def requires_approval(tool_name: str) -> bool:
  return tool_name == "write_report"


def checkpoint(state: AgentState, file_path: Path) -> None:
  file_path.write_text(json.dumps(asdict(state), ensure_ascii=False, indent=2), encoding="utf-8")


def run_agent(goal: str, approved: set[str]) -> AgentState:
  state = AgentState(goal=goal)
  checkpoint_file = Path("agent_state.json")

  for tool_name, payload in plan(state):
    if requires_approval(tool_name) and tool_name not in approved:
      state.observations.append(f"blocked: {tool_name} requires approval")
      checkpoint(state, checkpoint_file)
      return state

    observation = TOOLS[tool_name](payload)
    state.completed_steps.append(tool_name)
    state.observations.append(observation)
    checkpoint(state, checkpoint_file)

  for tool_name, payload in plan(state):
    if requires_approval(tool_name) and tool_name not in approved:
      state.observations.append(f"blocked: {tool_name} requires approval")
      checkpoint(state, checkpoint_file)
      return state

    observation = TOOLS[tool_name](payload)
    state.completed_steps.append(tool_name)
    state.observations.append(observation)
    checkpoint(state, checkpoint_file)

  return state


if __name__ == "__main__":
  print(run_agent("collect best practices for agent safety", approved={"search_docs"}))
  print(run_agent("collect best practices for agent safety", approved={"search_docs", "write_report"}))
```

### 驗證時要觀察什麼
- 第一次執行只批准 `search_docs` 時，流程應停在 `write_report` 前並留下 checkpoint。
- 第二次執行批准 `write_report` 後，流程應完成並更新 `agent_state.json`。
- 狀態檔案應包含 `completed_steps` 與 `observations`，方便恢復與審計。

## 自我檢查
- 練習 1：在範例中加入第三個高風險工具，設計不同 approval policy。
- 練習 2：讓 `plan` 根據上一輪 observation 重新規劃，觀察 replan 何時會失控。
- 練習 3：為 `agent_state.json` 設計版本欄位，思考 workflow 升級時如何兼容舊狀態。