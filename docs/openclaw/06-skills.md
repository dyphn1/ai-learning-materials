# Skill 開發與應用

## 什麼是 Skill？

在 OpenClaw 中，Skill 是一種可重用的功能模組，封裝了特定領域的知識和操作。Skill 讓代理人能夠：
- 使用專業工具（如 GitHub、Apple Notes、1Password）
- 執行特定任務（如搜尋 GIF、編輯 PDF、擷取相機畫面）
- 訪問外部服務（如 Discord、天氣 API、MCP 伺服器）

Skill 本質上是一組經過精心設計的腳本和配置，遵循 OpenClaw 的 AgentSkills 規格，使得代理人能夠安全、可靠地調用它們。

## Skill 的結構

一個典型的 Skill 目錄包含：

```
my-skill/
├── SKILL.md           # 技能說明文件（必填）
├── scripts/           # 可執行腳本（選填）
│   ├── install.sh     # 安裝腳本
│   └── my-command.py  # 主要功能腳本
├── references/        # 參考文件和資料（選填）
└── ...                # 其他資源
```

### SKILL.md 必填內容
- **name**：技能名稱
- **description**：技能用途描述
- **location**：技能文件的路徑（由系統自動填寫）
- 可選：`tools`、`env`、`permissions` 等欄位，用於聲明技能需要的資源

## 開發流程

### 步驟一：構思與規劃
1. 確定你想封裝的功能或工具
2. 調查是否已有類似技能（可透過 `openclaw clawhub search` 檢查）
3. 定義技能的輸入、輸出和副作用

### 步驟二：建立目錄結構
```bash
mkdir -p ~/my-skill/{scripts,references}
touch ~/my-skill/SKILL.md
```

### 步驟三：編寫 SKILL.md
範例：
```markdown
# my-skill - 個人ised helper

## 描述
這是一個示範技能，展示如何在 OpenClaw 中建立自己的功能模組。

## 工具
此技能使用以下內建工具：
- read
- write
- web_search

## 權限
此技能需要以下權限：
- 執行網路請求（用於 web_search）
- 讀寫使用者工作空間內的檔案
```

### 步驟四：實作功能
在 `scripts/` 目錄中添加實現功能的腳本。可以是任何語言，但必須可執行。

範例 Python 腳本 (`scripts/greet.py`)：
```python
#!/usr/bin/env python3
import sys

def main():
    name = sys.argv[1] if len(sys.argv) > 1 => "World"
    print(f"Hello, {name}!")

if __name__ == "__main__":
    main()
```

### 步驟五：測試技能
在開發過程中，您可以直接執行腳本來測試功能。
當準備好時，使用 ClawHub 發布技能：
```bash
openclaw clawhub publish ~/my-skill
```

### 步驟六：使用技能
發布後，您可以在任何 OpenClaw 會話中使用：
```bash
openclaw my-skill greet "Alice"
```
或在代理人提示詞中調用：
```
使用 my-skill 技能向 Alice 打招呼。
```

## 常見 Skill 類型

### 1. 工具整合類
將外部 CLI 工具或 API 包裝成 OpenClaw 可調用的形式。
例如：`github`, `apple-notes`, `1password`, `mcporter`

### 2. 資訊處理類
專注於資訊的擷取、轉換和摘要。
例如：`summarize`, `video-frames`, `gifgrep`, `nano-pdf`

### 3. 平台互動類
與特定平台或服務進行互動。
例如：`discord`, `weather`, `healthcheck`, `node-connect`

### 4. 工作流增強類
提供工作流管理、狀態追蹤或進階規劃功能。
例如：`taskflow`, `taskflow-inbox-triage`

## 安全考量

### 權限最小化
在 SKILL.md 中嚴格聲明技能真正需要的工具和權限。避免使用 `*` 萬用字元。

### 資料清理
如果技能處理敏感資訊（如密碼、個人資料），確保在使用後適當清理。

### 外部依賴審查
檢查腳本中呼叫的外部命令或 API，確保它們來自可信來源。

## 版本控制與更新

### 使用 Git 建議
建議將技能目錄納入 Git 版本控制，以便追蹤變更和協作。

### 更新流程
1. 修改技能內容
2. 測試變更是否正常工作
3. 重新發布：
   ```bash
   openclaw clawhub publish ~/my-skill
   ```
4. ClawHub 會處理版本遞增和更新通知

## 進階技巧

### 動態技能載入
OpenClaw 支持在運行時載入新技能，無需重啟會話。

### 技能組合
複雜任務可以組合多個簡單技能。例如：先使用 `web_search` 搜尋資訊，再使用 `summarize` 生成摘要。

### 自定義工具
如果內建工具不足，您可以在技能腳本中直接使用 `exec` 呼叫系統命令（但請注意安全）。

### 本地技能與共享技能區分
- 本地技能：僅在您的工作空間中可用，適合實驗和個人化工具
- 共享技能：透過 ClawHub 發布，可供其他 OpenClaw 實例使用

## 參考資源
- OpenClaw 官方技能規格：參考現有技能的 SKILL.md 檔案
- ClawHub 文檔：https://clawhub.ai
- 內建技能列表：執行 `openclaw clawhub list` 查看已安裝的技能
- 技能開發教學：搜尋 `skill-creator` 技能，它專門用於建立和改進其他技能