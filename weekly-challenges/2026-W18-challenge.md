# 每週進階挑戰 - 第 18 週 (2026)

*週期: 2026-04-27 ~ 2026-05-03*  
*主題: MCP 技能開發*

## 挑戰: OpenClaw MCP Skill 開發

開發一個 OpenClaw Skill，封裝對特定 MCP 伺服器的操作。

### 目標

選擇一個 MCP 伺服器（下列任一）並建立對應的 OpenClaw Skill：

**選項 A — 本地檔案系統 MCP**
透過 `filesystem` MCP 伺服器，建立一個能讀寫工作目錄檔案的 Skill。

**選項 B — GitHub MCP**
透過 `github` MCP 伺服器，建立一個能列出 Issue、建立 PR 的 Skill。

**選項 C — 自選 MCP 伺服器**
選擇任一已有社群實作的 MCP 伺服器（參考 [modelcontextprotocol.io/servers](https://modelcontextprotocol.io/servers)）。

### 實作要求

1. 建立 `SKILL.md`，說明 Skill 的用途、輸入參數、輸出格式
2. 實作 Skill 的 `invoke` 入口點
3. 定義 MCP 伺服器的連線參數與 `tools` 列表
4. 撰寫至少 2 個使用範例（含實際工具呼叫的輸入/輸出）
5. 加入錯誤處理：連線失敗、工具不存在、逾時

### 驗收標準

- [ ] Skill 可以透過 `openclaw skill invoke` 正確執行
- [ ] SKILL.md 有完整的 YAML frontmatter 與說明
- [ ] 兩個使用範例有預期的輸入與輸出
- [ ] 錯誤情境有適當的錯誤訊息
