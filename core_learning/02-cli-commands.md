# OpenClaw CLI 命令完整說明

## 基本結構

OpenClaw 透過 `openclaw` 命令列介面進行操作，遵循子命令模式：

```
openclaw <subcommand> [options] [arguments]
```

## 常用子命令

### 1. 狀態與資訊
- `openclaw status` - 顯示當前會話狀態（使用時間、模型、成本等）
- `openclaw gateway status` - 查看 Gateway 服務狀態
- `openclaw gateway start|stop|restart` - 管理 Gateway 服務
- `openclaw help` - 顯示幫助資訊

### 2. 會話管理
- `openclaw sessions list` - 列出可見的會話
- `openclaw sessions history <sessionKey>` - 取得會話歷史
- `openclaw sessions send <sessionKey> <message>` - 向另一個會話發送訊息
- `openclaw sessions spawn <task>` - 生成子會話（subagent）執行任務
- `openclaw sessions yield` - 結束當前回合，等待子會話結果

### 3. 子協作者管理
- `openclaw subagents list` - 列出當前會話生成的子協作者
- `openclaw subagents kill <target>` - 終止子協作者
- `openclaw subagents steer <target> <message>` - 對子協作者發送指令

### 4. 記憶體管理
- `openclaw memory_search <query>` - 搜尋長期記憶（MEMORY.md）
- `openclaw memory_get <path>` - 讀取特定記憶檔案片段

### 5. 網路與搜尋
- `openclaw web_search <query>` - 使用 DuckDuckGo 搜尋網頁
- `openclaw web_fetch <url>` - 抓取並提取網頁內容為 markdown 或純文字

### 6. 技能管理（透過 clawhub）
- `openclaw clawhub search <query>` - 搜尋 ClawHub 上的技能
- `openclaw clawhub install <skillId>` - 安裝技能
- `openclaw clawhub update [<skillId>]` - 更新技能
- `openclaw clawhub publish <path>` - 發布或更新技能

### 7. 其他專用工具
依據已安裝的技能，可使用以下專用命令（範例）：
- `openclaw github` - GitHub 操作（issues, PRs, CI）
- `openclaw weather [<location>]` - 取得天氣資訊
- `openclaw apple-notes` - 管理 Apple Notes
- `openclaw apple-reminders` - 管理 Apple Reminders
- `openclaw 1password` - 1Password CLI 整合
- `openclaw openai-whisper` - 本地語音轉文字
- `openclaw nano-pdf` - 編輯 PDF
- `openclaw video-frames` - 從影片擷取幀
- `openclaw gifgrep` - 搜尋與處理 GIF
- `openclaw camsnap` - 擷取相機畫面
- `openclaw healthcheck` - 系統安全與風險檢查
- `openclaw mcporter` - MCP 伺服器管理
- `openclaw discord` - Discord 訊息操作
- `openclaw summarize` - 網站、播客、檔案摘要

## 進階用法

### 指定工作目錄
```
openclaw --cwd /path/to/workdir sessions spawn "task description"
```

### 指定模型與思考級別
```
openclaw --model openrouter/gpt-4 --template thinking sessions spawn "complex task"
```

### 背景執行與輸出導向
- 使用 `--background` 立即在背景執行命令
- 使用 `--streamTo parent` 將子會話的輸出串流回父會話

### 權限與安全
- `--elevated`：在允許的情況下以提升權限執行命令（需審核）
- `--security deny|allowlist|full`：設定執行安全模式
- `--ask off|on-miss|always`：控制何時詢問使用者同意

## 範例

### 1. 快速問答
```bash
openclaw "什麼是 ReAct 框架？"
```

### 2. 生成子協作者進行程式碼重構
```bash
openclaw sessions spawn "重構 src/util.py 中的錯誤處理邏輯，加入日誌與單元測試" --model openrouter/claude-3-opus
```

### 3. 搜尋網路並摘要
```bash
openclaw web_search "最新多模態 LLM 進展 2024" | openclaw summarize
```

### 4. 管理 Apple Reminders
```bash
openclaw apple-reminders add "明天買牛奶" --list "購物清單" --due "tomorrow 09:00"
```

### 5. 建立及發布新技能
```bash
# 建立技能結構
mkdir -p ~/my-skill/{scripts,references}
echo "# My Skill" > ~/my-skill/SKILL.md
# 發布至 ClawHub
openclaw clawhub publish ~/my-skill
```

## 小技巧

1. **使用 tab 完整**：OpenClaw CLI 支持子命令與選項的 tab 完整。
2. **查看子命令說明**：任何子命令後加 `--help` 可看到詳細用法。
3. **環境變數覆寫**：許多選項可透過環境變數設定，例如 `OPENCLAW_DEFAULT_MODEL`。
4. **日誌與除錯**：使用 `--debug` 旗標啟用除錯輸出。
5. **安全先行**：對於會變更系統的操作（如 `exec rm`），OpenClaw 會要求額外確認。

## 參考資源
- OpenClaw 官方文件：https://docs.openclaw.ai
- CLI 參考手冊：`openclaw help`
- 子命令完整列表：執行 `openclaw --list-commands`