# Agentic Workflow + 定時任務整合

## 什麼是 Agentic Cron？

Agentic Cron 是將 Agentic Workflow 的智能決策能力與傳統 cron 的精確定時觸發結合的機制。它允許您：
- 在固定時間觸發複雜的 AI 工作流（而非簡單的腳本執行）
- 讓 AI 代理人根據當前情況動態規劃執行步驟
- 結合定時性與適應性，創造真正智能的自動化系統

## 為何需要 Agentic Cron？

傳統 cron 的限制：
- 只能執行預先寫好的腳本，無法根據當前狀態調整行為
- 複雜決策需要寫死在腳本中，難以維護和更新
- 無法利用 LLM 的推理能力進行即時適應

Agentic Cron 的優勢：
- **動態規劃**：每次觸發時，AI 重新根據當前環境規劃最佳行動路徑
- **上下文感知**：能讀取最新的郵件、日曆、新聞等資訊來決策
- **易於維護**：更新工作流邏輯只需修改提示詞或知識庫，而非腳本
- **學習能力**：可結合記憶體，隨時間改進決策品質

## 在 OpenClaw 中實作 Agentic Cron

### 基本結構
Agentic Cron 由兩部分組成：
1. **排程觸發器**：使用系統 cron 在固定時間執行一個指令
2. **智能工作流**：該指令啟動 OpenClaw 會話，執行預定義的 Agentic Workflow

### 實作步驟

#### 步驟一：建立工作流腳本
創建一個腳本，每次被呼叫時會啟動 OpenClaw 並執行特定的 Agentic 工作流。

範例：`~/ai/scripts/daily_agentic_workflow.sh`
```bash
#!/bin/bash
# 每日 08:00 觸發的 Agentic 工作流

# 設定工作目錄
WORK_DIR="/Users/daniel.chang/Desktop/ai"
LOG_FILE="$WORK_DIR/logs/agentic_cron_$(date +%Y-%m-%d).log"

# 確保目錄存在
mkdir -p "$(dirname "$LOG_FILE")"

# 執行 OpenClaw 工作流
{
  echo "=== 開始 Agentic Cron 工作流 $(date) ==="
  
  # 這裡可以是一個複雜的提示詞，或呼叫預先定義的工作流
  openclaw sessions spawn \
    "執行每日智慧檢查工作流：\
    1. 檢查未讀郵件並摘要重要內容\
    2. 查看今日日曆事件並提醒重要會議\
    3. 搜尋 OpenClaw 最新動態和 Agentic AI 新聞\
    4. 生成每日簡報並存至 knowledge-base/daily/$(date +%Y-%m-%d).md\
    5. 如果發現緊急資訊，透過 Discord 通知使用者" \
    --model openrouter/gpt-4 \
    --template thinking \
    --streamTo parent \
    --timeoutSeconds 300
  
  echo "=== Agentic Cron 工作流結束 $(date) ==="
} >> "$LOG_FILE" 2>&1
```

#### 步驟二：設定 cron 觸發
編輯 crontab 加入排程：
```
# 每日早上 08:00 (台北時間) 執行 Agentic Cron
0 8 * * * /Users/daniel.chang/Desktop/ai/scripts/daily_agentic_workflow.sh
```

#### 步驟三：進階選項
##### 使用 TaskFlow 維護狀態
若工作流需要跨天維護狀態（例如：追蹤一個長期專案的進度），可使用 TaskFlow：
```bash
openclaw sessions spawn \
  --label "daily-check" \
  --mode session \
  "執行每日檢查工作流（使用 TaskFlow 維護狀態）" \
  --model openrouter/claude-3-opus
```

##### 增加條件觸發
結合 Heartbeat 與 cron：讓 Heartbeat 輪詢某些條件（例如：網站是否有更新），
只有當條件達成時才触发完整的 Agentic Cron 工作流。

## 安全與最佳實踐

### 1. 超時控制
Always set a reasonable timeout (`--timeoutSeconds`) to prevent runaway workflows.

### 2. 資源監控
監控日誌檔案大小，避免無限增長。考慮使用 logrotate。

### 3. 錯誤處理
腳本中應該捕获錯誤並記錄，必要時發送失敗通知。

### 4. 隔離環境
建議為 Agentic Cron 建立專用的工作目錄或使用乾淨的環境變數。

### 5. 測試排程
在加入 crontab 前，先手動執行腳本確認無誤：
```bash
/Users/daniel.chang/Desktop/ai/scripts/daily_agentic_workflow.sh
```

## 範例應用

### 案例 1：每日研究助手
每天早上 08:00 自動：
- 搜尋用戶指定主題的最新論文
- 生成文獻综述
- 識別研究空白點
- 建議下一步實驗方向

### 案例 2：代碼審查助手
每天早上 08:00 自動：
- 檢查指定倉庫的最新 commit
- 跑靜態分析工具
- 生成程式碼品質報告
- 如果發現安全漏洞，立即通知團隊

### 案例 3：個人知識園丁
每天早上 08:00 自動：
- 整理昨天筆記本中的零散資訊
- 更新 Obsidian/Zettelkasten 知識庫
- 識別知識間的關聯並建議新連結
- 生成每日學習複習卡片

## 進階整合：週挑戰與 Agentic Cron

Agentic Cron 不只限於每日任務。結合週排程，可以創建：
- **週一進階挑戰**：每週一 08:00 自動生成當週的實作挑戰題目
- **週三回顧**：每週三自動生成過去兩天的學習摘要
- **週五展望**：每週五自動規劃下週的學習目標

這些都可以透過相同的原理實作：在特定時間觸發 OpenClaw，執行預定義的 Agentic 工作流。

## 參考資源
- OpenClaw AGENTS.md：關於記憶與工作流的說明
- OpenClaw TOOLS.md：記錄您的 Agentic Cron 所需的本地資訊
- 各技能的 SKILL.md：如 `web_search`, `write`, `read`, `edit`, `sessions_spawn` 等的具體用法
- Unix Cron 手冊：`man 5 crontab`
-  ReAct 與 Plan-and-Execute 框架：參考 04-agentic-workflow.md