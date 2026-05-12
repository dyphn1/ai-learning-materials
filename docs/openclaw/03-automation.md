# OpenClaw 自動化作業打造

## 什麼是自動化？

在 OpenClaw 中，自動化指的是讓代理人在無需持續人工干預的情況下，根據時間、事件或條件執行預定義任務。這包括定時任務、事件觸發的工作流以及主動式檢查。

## 核心自動化機制

### 1. Cron（定時任務）
適合需要固定時間執行的任務（例如：每日早上 8:00 檢查郵件）。

**使用方式**：
- 透過 `crontab -e` 編輯個人 crontab
- 每行格式：`分 時 日 月 星期 預執行指令`
- 範例：`0 8 * * * /path/to/script.sh` （每日 08:00 執行）

### 2. Heartbeat（心跳檢查）
適合需要週期性檢查但時間不需精確的任務（例如：每 30 分鐘檢查一次未讀訊息）。

**特點**：
- 觸發間隔可彈性（約每 30 分鐘一次）
- 可在同一回合中執行多項檢查（例如：郵件 + 日曆 + 天氣）
- 透過編輯 `HEARTBEAT.md` 加入檢查項目

### 3. TaskFlow（持久工作流）
適合需要跨多個子任務、維護狀態、可中斷後繼續的複雜自動化。

**功能**：
- 為工作流賦予身份，使其可被追蹤和管理
- 支援子任務鏈結、狀態等待、修改檢查
- 適合需要人工介入或外部事件回呼的流程

## 自動化範例架構

### 案例 1：每日新聞摘要
**目標**：每天早上 7:30 自動抓取科技新聞，生成摘要並存檔。

**實作**：
1. 建立腳本 `fetch_tech_news.sh`：
   ```bash
   #!/bin/bash
   DATE=$(date +%Y-%m-%d)
   openclaw web_search "科技新聞 最新 24小時" > /tmp/search_results.txt
   openclaw web_fetch $(head -1 /tmp/search_results.txt) --extractMode markdown > /tmp/news_content.md
   openclaw summarize /tmp/news_content.md > ~/ai/daily-news/$DATE.md
   ```
2. 加入 crontab：
   ```
   30 7 * * * /Users/daniel.chang/Desktop/ai/scripts/fetch_tech_news.sh
   ```

### 案例 2：GitHub Issue 監控
**目標**：每小時檢查特定倉庫是否有新 issue，若有則發送 Discord 通知。

**實作**：
1. 使用 `openclaw github` 指令列出最新 issue
2. 比較與上次執行的紀錄（可存於 `state/` 目錄）
3. 若有新 issue，使用 `openclaw sessions_send` 發送訊息至 Discord
4. 設定為 cron 每小時執行

### 案例 3：主動式知識庫更新
**目標**：每天早上 8:00 自動搜尋 OpenClaw 相關資訊，更新知識庫。

**實作**：
- 這正是本系統的第二階段 — 每日動態更新（詳細見後續說明）

## 最佳實踐

1. **分離職責**：讓 cron 負責觸發，腳本負責具體工作，避免在 crontab 中寫入過長指令。
2. **錯誤處理**：腳本中加入錯誤檢查並記錄 log（例如：`>> /path/to/logfile 2>&1`）。
3. **避免重複執行**：對於需要互斥的任務，可使用 lockfile 機制。
4. **資訊安全**：不要在腳本中硬編碼敏感資訊（如 API 金鑰），使用環境變數或安全儲存。
5. **可觀測性**：讓自動化任務執行後產出明確的產物（如 markdown 報告、更新的檔案）或發送通知。
6. **測試與除錯**：先手動執行腳本確認無誤後再加入排程。

## 進階技巧

### 使用 TaskFlow 建立可復原的工作流
若自動化任務包含多個步驟且中間可能失敗，可考慮使用 TaskFlow：
- 每個步驟為一個子任務
- 工作流會記錄每個步驟的狀態
- 失敗時可從失敗點重試，而非從頭開始

### 結合 Heartbeat 與 Cron
- 使用 Heartbeat 輪詢外部資源（例如：檢查網站是否更新）
- 若偵測到變化，則觸發較重度的 Cron 任務進行完整處理
- 此模式可減少不必要的重複工作

## 參考資源
- OpenClaw AGENTS.md：關於 heartbeat 与 cron 的說明
- OpenClaw TOOLS.md：記錄您的自動化腳本所需的本地資訊（如 SSH 主機、相機名稱等）
- 各技能的 SKILL.md：如 `github`, `web_search`, `summarize` 等的具體用法