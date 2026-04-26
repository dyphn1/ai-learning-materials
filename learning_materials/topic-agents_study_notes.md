# AI Agent 設計與框架 (AI Agents) 學習筆記
*來源檔案: topic-agents.md*
*同步更新: 2026-04-26*

## 一句話理解
AI Agent 不是「會聊天的 LLM」換一個名字，而是把語言模型包進一個可持續執行的控制迴圈。傳統 LLM 擅長單次生成，但它對外部世界的觀測能力有限、對長任務的狀態維護薄弱、對工具副作用缺乏原生保證，因此一旦任務需要搜尋、規劃、分步執行、狀態恢復與安全邊界，單次 prompt 很快就會失效。Agent 的設計動機，就是把「推理」從一次性文字生成，改造成一個可以讀取環境、決定下一步、執行工具、檢查結果，再更新內部狀態的閉環系統。

## 必記重點
- ReAct：交錯輸出 Thought、Action、Observation
- Plan-and-Execute：先產生子任務，再逐步執行與重規劃
- Memory 系統：分成 working memory、episodic memory、semantic memory
- MemGPT：以 OS 分層記憶概念在上下文與外部儲存之間 paging
- Tool Router / Function Calling：用 schema 約束工具輸入輸出，模型只負責選擇與組合

## 核心名詞速記
- ReAct：純推理缺乏外部證據，純 action 缺少理由
- Plan-and-Execute：長任務會在中途迷航
- Memory 系統：context window 太短，無法記住長期資訊
- MemGPT：長上下文成本過高
- Tool Router / Function Calling：模型不知道何時該呼叫工具

## 流程速記
1. 接收目標與上下文，建立當前工作記憶。
2. 從長期記憶中檢索與任務最相關的事件、事實與過去失敗案例。
3. 由 planner 產生下一步候選行動，可能是直接回答、呼叫工具、拆分子任務或要求人工確認。
4. 若需要工具，先以 schema 或參數驗證器檢查輸入是否合法。
5. 執行工具，收集 Observation，並把結果寫回工作記憶。
6. 若 Observation 顯示失敗、衝突或不完整，觸發 replan 或 reflection。
7. 當停止條件成立時，輸出最終答案與必要的執行摘要。

## 必背公式
$$
score(m_i, q) = \alpha \cdot sim(m_i, q) + \beta \cdot recency(m_i) + \gamma \cdot importance(m_i)
$$

## 實作範例重點
### 範例片段
```python
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable


@dataclass
class MemoryItem:
    text: str
    importance: float
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Tool:
    name: str
    description: str
    handler: Callable[[str], str]


def weather_tool(_: str) -> str:
    return "台北 27C，晴天，降雨機率 10%"


def calculator_tool(expression: str) -> str:
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        raise ValueError("unsafe expression")
    return str(eval(expression, {"__builtins__": {}}, {}))


def retrieve(memory: list[MemoryItem], query: str) -> list[MemoryItem]:
    keywords = set(query.lower().split())
    scored = []
    for item in memory:
        overlap = len(keywords & set(item.text.lower().split()))
        score = overlap + item.importance
        scored.append((score, item))
    return [item for score, item in sorted(scored, reverse=True)[:2] if score > 0]


def choose_action(goal: str) -> tuple[str, str]:
    lowered = goal.lower()
    if any(token in lowered for token in ["天氣", "weather"]):
        return ("weather", "taipei")
    if any(token in lowered for token in ["計算", "calculate", "+", "-", "*", "/"]):
        return ("calculator", goal.replace("計算", "").strip())
    return ("answer", "目前無需工具，直接根據已有資訊回答")


def run_agent(goal: str) -> str:
    memory = [
        MemoryItem("user prefers concise engineering answers", importance=1.2),
        MemoryItem("weather queries should use the weather tool", importance=2.0),
    ]
    tools = {
        "weather": Tool("weather", "fetch current weather", weather_tool),
        "calculator": Tool("calculator", "evaluate math", calculator_tool),
    }

    context = retrieve(memory, goal)
    action, payload = choose_action(goal)

    if action in tools:
        observation = tools[action].handler(payload)
        memory.append(MemoryItem(f"{action} -> {observation}", importance=1.5))
        return f"Goal: {goal}\nContext: {[item.text for item in context]}\nObservation: {observation}"

    return f"Goal: {goal}\nContext: {[item.text for item in context]}\nAnswer: {payload}"


if __name__ == "__main__":
    print(run_agent("請告訴我台北今天天氣"))
    print(run_agent("請計算 (12 + 30) / 7"))
```

### 驗證時要觀察什麼
- 第一個查詢應命中 weather tool，輸出 weather observation。
- 第二個查詢應命中 calculator tool，輸出正確算式結果 `6.0`。
- 若輸入包含危險字元，例如字母與底線混入算式，calculator tool 應拒絕執行。

## 自我檢查
- 練習 1：把範例中的 `choose_action` 擴充成三種工具，觀察工具選擇錯誤時的 failure mode。
- 練習 2：把 `retrieve` 的分數改成不同權重，測試相同查詢下記憶檢索結果如何變化。
- 練習 3：加入一個需要人工批准的危險工具，設計何時必須中斷等待使用者確認。