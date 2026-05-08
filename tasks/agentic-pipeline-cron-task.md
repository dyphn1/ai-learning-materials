# OpenClaw Agentic Pipeline — 定時任務設定

## 任務概覽

每日自動執行，透過四個 Agent 的閉環工作流，確保所有文件任務都有真實的研究基礎、深度的內容產出、以及獨立的品質驗證。

**工作目標：**
1. **AI 學習資料**：研究 AI/ML 最新論文並撰寫深度文件 → `/Desktop/ai/docs/`
2. **OpenClaw 學習資料**：分析 OpenClaw 原始碼並撰寫學習文件 → `/Desktop/ai/learning_materials/openclaw/`
3. **OpenClaw 分析**：針對 OpenClaw 架構進行技術解析

---

## 定時任務設定（Cron Job Configuration）

在 OpenClaw 中透過以下設定建立定時任務（每日早上 8:00 台北時間執行）：

```json
{
  "schedule": {
    "kind": "cron",
    "expr": "0 8 * * *",
    "tz": "Asia/Taipei",
    "staggerMs": 60000
  },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "<見下方完整提示詞>"
  },
  "delivery": {
    "mode": "announce"
  }
}
```

---

## 完整提示詞（Payload Text）

> 將下方文字貼入 `payload.text` 欄位。

---

```
啟動 OpenClaw Agentic Documentation Pipeline。

> **EXECUTION MANDATE**: 你必須完整執行整個閉環流程，不得在中間停下來詢問是否繼續。每個 Agent 完成後立即呼叫下一個。

## 前置條件確認

讀取以下狀態後再決定從哪個節點進入工作流：
- `/Users/daniel.chang/Desktop/ai/tasks/active/` — 有無進行中任務
- `/Users/daniel.chang/Desktop/ai/tasks/completed/` — 有無等待審核的任務

## 工作流進入點

### 情況 A：全新啟動
若 active/ 和 completed/ 均為空：
  1. 呼叫 **Orchestrator** agent — 掃描文件缺口，建立最多 2 個任務卡
  2. 等待 Orchestrator 的 Handover Block
  3. 呼叫 **Fact-Check Scout** agent — 對每個新任務進行研究，產出 Fact Sheet
  4. 等待 Fact-Check Scout 的 Handover Block
  5. 呼叫 **Instructional Writer** agent — 以 Fact Sheet 為基礎撰寫深度文件
  6. 等待 Instructional Writer 的 Handover Block
  7. 呼叫 **Quality Validator** agent — 交叉比對文件與 Fact Sheet，通過則歸檔，退回則重回步驟 5

### 情況 B：有 Research_Done 的任務
直接從步驟 5（Instructional Writer）開始。

### 情況 C：有 Completed 任務待審核
直接呼叫 **Quality Validator**。若退回，呼叫 **Instructional Writer** 修正。

## Agent 位置

所有 agent 的定義檔存放於：
`/Users/daniel.chang/Desktop/ai/.github/agents/`

## 執行守則

1. 每個步驟透過 runSubagent 工具呼叫對應 agent
2. 必須等待 Handover Block 或 Re-dispatch Request Block 才能進入下一步
3. Quality Validator 退回時，最多允許 3 次重試同一任務
4. 若超過 3 次退回，將任務標記為 Failed 並停止該任務的流程
5. 每輪最多處理 2 個任務，確保品質優於數量

## 完成標準

工作流結束條件（任一）：
- Quality Validator 對本輪所有任務輸出 APPROVED ✅
- 任務因超過重試次數標記為 Failed

最終輸出一份本輪執行摘要至 `/Users/daniel.chang/Desktop/ai/logs/orchestrator.log`。
```

---

## 工作流架構圖

```
OpenClaw Cron（每日 08:00）
        │
        ▼
  [入口狀態判斷]
        │
        ├──→ Orchestrator Agent
        │    ├─ 掃描 docs 缺口
        │    ├─ 讀取 backlog.json
        │    └─ 建立 /tasks/active/*.json
        │
        ├──→ Fact-Check Scout Agent
        │    ├─ 讀取 Pending 任務卡
        │    ├─ 研究原始碼 / 論文 / 官方文件
        │    └─ 產出 /tasks/context/<id>-fact.json
        │
        ├──→ Instructional Writer Agent
        │    ├─ 讀取 Fact Sheet
        │    ├─ 撰寫 ≥1500 字深度文件
        │    └─ 複製任務至 /tasks/completed/
        │
        └──→ Quality Validator Agent
             ├─ 交叉比對文件 vs Fact Sheet
             ├─ 通過 → 歸檔至 /tasks/archived/ ✅
             └─ 退回 → 回到 Instructional Writer 🔁
```

---

## 任務目錄說明

| 目錄 | 用途 |
|------|------|
| `/tasks/backlog.json` | 所有待辦任務總表 |
| `/tasks/active/` | 當前執行中的任務卡 (`.json`) |
| `/tasks/context/` | Fact Sheet (`<id>-fact.json`) 與 Review Note (`<id>-review.md`) |
| `/tasks/completed/` | 等待 Quality Validator 審核的任務 |
| `/tasks/archived/` | 通過驗證的最終歸檔任務 |

---

## Agent 職責速查

| Agent | 輸入 | 輸出 | 關鍵限制 |
|-------|------|------|---------|
| **Orchestrator** | docs 目錄 + backlog.json | `/tasks/active/<id>.json` | 禁止撰寫文件 |
| **Fact-Check Scout** | 任務卡 | `/tasks/context/<id>-fact.json` | 禁止憑空想像 |
| **Instructional Writer** | Fact Sheet | 最終 `.md` 文件 | 只能引用 Fact Sheet 內的事實 |
| **Quality Validator** | 文件 + Fact Sheet | APPROVED / REJECTED | 禁止修改文件 |
