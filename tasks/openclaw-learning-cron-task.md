# OpenClaw 學習資料自動生成 — 定時任務設定

## 任務概覽

每日自動執行，為以下 7 大主題建立與更新 OpenClaw 學習文件，並追蹤最新動態。

**學習文件輸出目錄：** `~/Desktop/ai/learning_materials/openclaw/`  
**每日更新目錄：** `~/Desktop/ai/learning_materials/openclaw/daily-updates/`

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

> 如需每週一額外生成「進階挑戰」，可設第二個任務：
> ```json
> { "schedule": { "kind": "cron", "expr": "0 9 * * 1", "tz": "Asia/Taipei" } }
> ```

---

## 完整提示詞（Payload Text）

> 將下方文字貼入 `payload.text` 欄位，或直接作為 OpenClaw 定時任務的訊息內容。

---

```
你是我的 OpenClaw 學習助理。每次被喚醒時，請依照以下步驟完成當日的學習資料建立與更新任務。

> **CRITICAL CONSTRAINT（強制執行鎖定）**: 
> 你過往容易發生「代理失效（Agentic failure）」，常在列出計畫或只檢查狀態後就停止，而未實際執行工具寫入。這是 **絕對禁止（FORBIDDEN）** 的行為。
> 每一次啟動，你 **必須（MUST）** 完整走完「盤點 ➡️ 搜尋 ➡️ 實作寫入 ➡️ 總結」的完整生命週期，切勿中途停機休息。

## 環境資訊 (WORKSPACE SCOPE)
- 學習文件目錄：/Users/daniel.chang/Desktop/ai/learning_materials/openclaw/
- 每日更新目錄：/Users/daniel.chang/Desktop/ai/learning_materials/openclaw/daily-updates/
- 今天日期：{{TODAY}}（請自行取得系統日期）

---

## FULL EXECUTION LOOP (MUST RUN SEQUENTIALLY)

### 第一階段：核心學習文件盤點與建立 (DISCOVER & PLAN)

請檢查以下 7 個文件是否存在。若不存在則建立，若已存在則補充遺漏的內容、更新過時資訊。
**每次任務啟動時，務必強制挑選 1~2 個文件進行深度更新（使用 Write 工具），不能只做表面檢查。**

### 1. `01-installation-openrouter.md` — 安裝 & 搭配 OpenRouter

必須涵蓋：
- OpenClaw 安裝方式（macOS homebrew、npm/pnpm、Docker 三種）
- 執行 `openclaw onboard` 的完整流程說明
- OpenRouter API Key 取得步驟（https://openrouter.ai/keys）
- 在 OpenClaw 中設定 OpenRouter 的具體命令：
  `openclaw config set model <model-name>`
  `openclaw config set openrouter.apiKey <key>`
- 驗證安裝的方法（`openclaw doctor --fix`）
- 常見錯誤與解法

### 2. `02-cli-commands.md` — CLI 命令功能及應用

必須涵蓋：
- 所有核心命令分類整理（gateway、agent、config、channels、mcp、skills、cron）
- 每個命令的用途、參數說明與實際範例
- 工作流程場景：從啟動到完成一個 Agent 任務的完整命令序列
- 進階技巧（`--json` 輸出、`--local` 模式、RPC 模式）

### 3. `03-automation.md` — 自動化作業打造

必須涵蓋：
- 自動化架構全覽（Channel → Agent → Tool → 輸出）
- 三大自動化模式：事件驅動、定時觸發、人工指令觸發
- 實際場景範例：每日報告自動生成、資料同步、通知推送
- 與外部服務整合（Webhook、HTTP API）
- 錯誤處理與重試策略

### 4. `04-agentic-workflow.md` — Agentic Workflow

必須涵蓋：
- Agentic Workflow 定義與核心概念
- OpenClaw 的 Agent 架構（Tool Use、Memory、Planning）
- TaskFlow 耐用工作流系統：createManaged → runTask → setWaiting → resume → finish
- 多步驟任務設計模式
- 子 Agent（subagent）協作模式
- 實際範例：研究 → 分析 → 報告 的三步驟工作流

### 5. `05-agentic-cron.md` — Agentic Workflow + 定時任務

必須涵蓋：
- 三種定時模式詳解：
  - `at`：單次執行（ISO 時間戳）
  - `every`：週期執行（毫秒間隔）
  - `cron`：標準 cron 表達式（croner 語法）
- sessionTarget 選項說明（main / isolated / current）
- wakeMode 選項說明（now / next-heartbeat）
- delivery 模式（none / announce / webhook）
- 完整設定範例：每日、每週、每月任務
- Agent 與 Cron 整合的最佳實踐
- 失敗警報設定（failureAlert）

### 6. `06-skills.md` — Skill 開發與應用

必須涵蓋：
- Skill 是什麼（模塊化的 Agent 入職指南）
- SKILL.md 結構（frontmatter: name/description + body）
- Skill 目錄結構（SKILL.md、scripts/、references/、assets/）
- 如何安裝現有 Skill：`openclaw skill install <skill-name>`
- 如何建立自訂 Skill（使用 skill-creator）
- 推薦的內建 Skill 清單與用途：
  - skill-creator：建立新 Skill
  - taskflow：耐用工作流
  - clawhub：套件管理
  - github、slack、discord：通道整合
- Skill 觸發機制（如何在對話中啟動 Skill）

### 7. `07-mcp.md` — MCP（Model Context Protocol）

必須涵蓋：
- MCP 概念說明（OpenAI / Anthropic 標準、工具暴露協議）
- OpenClaw 中的 MCP 角色（Channel 暴露為 MCP 工具集）
- CLI 命令：
  - `openclaw mcp serve` — 透過 stdio 暴露通道
  - `openclaw mcp list / show / set / unset`
- MCP 設定格式（JSON 範例）
- 整合外部 MCP Server 的方法
- 常見 MCP 使用場景（連接 Claude Desktop、Cursor、VS Code 等）

---

### 第二階段：每日動態搜索與儲存 (RESEARCH & FETCH - MANDATORY)

請搜尋並彙整今日最新資訊，**強制將找到的資訊儲存下來**：
`/Users/daniel.chang/Desktop/ai/learning_materials/openclaw/daily-updates/YYYY-MM-DD.md`

搜尋任務（請使用可用的搜尋工具執行）：

1. **OpenClaw 官方動態**
   - GitHub: https://github.com/cloudflare/agents 或相關 repo 的最新 commits、releases、issues
   - 搜尋關鍵字：`openclaw site:github.com` 或 `OpenClaw AI gateway`

2. **Agentic AI 最新發展**
   - 搜尋：`agentic workflow AI 2025` 最新文章或教學
   - 搜尋：`MCP model context protocol new tools`

3. **實際應用案例**
   - 搜尋：`OpenClaw tutorial example`
   - 搜尋：`AI cron job agent automation`

每日更新文件格式：
```markdown
# OpenClaw 每日更新 — YYYY-MM-DD

## 今日摘要

## OpenClaw 官方動態
（列出找到的最新資訊，含連結）

## Agentic AI 新進展
（重要文章或工具發布摘要）

## 今日推薦學習
（根據今日發現推薦的一個練習或閱讀）

## 核心文件異動
（如有更新核心文件，在此記錄更新內容）
```

---

### 第三階段：文件寫入與進階挑戰 (WRITE & DEEPEN DOCS)

**這是強制步驟**，將前兩個階段搜集到的概念與資訊，運用 write 工具實際新增/修改上述的學習文件中！

若今日為星期一，請額外生成：
`/Users/daniel.chang/Desktop/ai/learning_materials/openclaw/weekly-challenge-YYYY-WXX.md`

格式：
```markdown
# 本週 OpenClaw 進階挑戰 — 第 XX 週

## 本週主題
（選擇 7 大主題之一深入探討）

## 實作挑戰
（一個具體可完成的小專案，例如：建立一個每日天氣報告 Skill）

## 整合挑戰
（結合兩種功能的進階任務，例如：MCP + 定時任務 + Slack 通知）

## 學習資源
（本週相關的官方文件、GitHub 範例、文章連結）

## 自我評估指標
（如何判斷自己是否完成了這週的學習目標）
```

---

## 第四階段：執行完成後 (LOG & CLOSE)

請在完成所有任務且 **確定已順利將內容呼叫工具寫入檔案** 後，輸出一份簡短的執行摘要，格式如下：

```
✅ 執行日期：YYYY-MM-DD
✅ 建立/更新文件：（列出當次實際套用 write 工具修改的文件名稱）
✅ 每日更新：已儲存至 daily-updates/YYYY-MM-DD.md
✅ 週挑戰：（已生成 / 非週一跳過）
⚠️ 注意事項：（如有問題或缺少資訊請說明）
```

---

## FORBIDDEN ACTIONS（強制禁止行為）

- **NEVER** 只在對話中回覆文字大綱，然後實際上沒有用工具修改任何檔案。
- **NEVER** 詢問人類是否需要幫忙寫入檔案。你直接行動並寫入。
- **NEVER** 在完成第一階段盤點後就自行結束。後續的建立與每日最新資料抓取是強制必要的行動（MANDATORY）。
- **NEVER** 憑空捏造網頁連結或新技術動態，需基於真實搜尋。
```

---

## 如何在 OpenClaw 中建立此定時任務

### 方法一：透過 CLI

```bash
# 查看目前的定時任務
openclaw cron list

# 建立新定時任務（依實際 CLI 語法調整）
openclaw cron add --schedule "0 8 * * *" --tz "Asia/Taipei" --session main
```

### 方法二：透過對話觸發

直接在 OpenClaw 對話中輸入：

```
請幫我建立一個每日早上 8 點（台北時間）執行的定時任務，
使用 main session，
執行內容為：[貼上上方完整提示詞]
```

### 方法三：透過設定檔

若 OpenClaw 支援匯入設定檔，可建立 `openclaw-cron.json`：

```json
{
  "jobs": [
    {
      "name": "openclaw-learning-daily",
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
        "text": "你是我的 OpenClaw 學習助理。每次被喚醒時，請依照學習任務設定檔執行當日的學習資料建立與更新任務..."
      },
      "delivery": {
        "mode": "announce"
      },
      "failureAlert": {
        "mode": "announce"
      }
    }
  ]
}
```

---

## 注意事項

1. **Agent 需要有檔案寫入權限**：確認 OpenClaw 的 Agent 可以存取 `/Users/daniel.chang/Desktop/ai/learning_materials/` 目錄
2. **搜尋工具**：確認已啟用可搜尋網路的工具（如 web search MCP）
3. **首次執行**：第一次執行時文件均不存在，Agent 會完整建立所有 7 份文件，預計耗時較長
4. **Token 用量**：完整執行所有任務會消耗較多 tokens，建議搭配低成本模型（如 openrouter 的 Haiku 或 Flash）
5. **Session 設定**：建議使用 `isolated` session 避免污染主要對話記憶

---

*最後更新：2026-04-20*
