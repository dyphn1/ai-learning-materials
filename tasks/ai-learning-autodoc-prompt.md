# AI 學習資料自動化更新提示（三階段版）

> 將下方 `## 提示詞` 區塊的內容貼入 OpenClaw 定時任務的 `payload.text` 欄位。

---

## 設定範例（Cron）

```json
{
  "schedule": {
    "kind": "cron",
    "expr": "0 7 * * *",
    "tz": "Asia/Taipei",
    "staggerMs": 30000
  },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "<見下方提示詞>"
  },
  "delivery": {
    "mode": "announce"
  }
}
```

---

## 提示詞

```
你是我的 AI 學習文件自動維護 agent。每次被喚醒時，請嚴格依照下方三個階段依序執行，
並在每個 write 操作後確認工具回傳成功。若工具無回應或回傳錯誤，立即停止並在 log 中記錄失敗原因。

## 環境資訊
- docs 目錄：/Users/daniel.chang/Desktop/ai/docs/
- tasks 目錄：/Users/daniel.chang/Desktop/ai/tasks/
- 參考資料目錄：/Users/daniel.chang/Desktop/ai/docs/references/
- 執行日誌：/Users/daniel.chang/Desktop/ai/logs/autodoc-YYYY-MM-DD.log（請填入今天日期）

---

## 第一階段：主題盤點與缺口發現

### 步驟 1.1 — 列出現有 docs 主題
使用 list 或 read 工具，取得 /Users/daniel.chang/Desktop/ai/docs/ 下所有 .md 檔名（不含 references/ 子目錄）。
將每個檔名去掉 .md 後綴，記錄為「已涵蓋主題清單」。

### 步驟 1.2 — 搜尋當前 AI 主要主題
使用 web_search，搜尋以下查詢（每次搜尋後記錄結果）：
1. "2025 2026 AI engineer learning roadmap topics"
2. "top AI machine learning topics to learn in 2025"
3. "LLM agent RAG fine-tuning latest AI techniques 2025"

從搜尋結果中整理出業界公認的主要 AI 學習主題清單，至少包含以下類別：
- LLM 基礎（Transformers、訓練、推理）
- Prompt Engineering（基礎、進階、評估）
- RAG（基礎、進階、GraphRAG）
- Agent 設計（單 Agent、Multi-Agent、工具整合）
- Fine-tuning（LoRA、QLoRA、RLHF）
- 評估與測試（Benchmark、LLM-as-judge、Evals）
- 本地部署（Ollama、llama.cpp、量化）
- MCP（Model Context Protocol、工具協議標準）
- Agentic Workflow（TaskFlow、人機協作、工作流設計）
- AI 安全（Alignment、紅隊測試、guardrails）
- 向量資料庫（ChromaDB、Pinecone、Qdrant）
- 多模態（Vision-Language、Audio、Video 理解）

### 步驟 1.3 — 找出缺口主題
比對「已涵蓋主題清單」與搜尋得到的業界主題清單。
對每個業界主題，檢查 docs 目錄是否有對應的 .md 檔案（以主題關鍵字匹配，不要求完全一致）。
將「docs 中尚未涵蓋」的主題列為「待新增主題清單」。

### 步驟 1.4 — 為缺口主題建立 task 檔案
對「待新增主題清單」中的每個主題：
1. 命名格式：topic-<英文主題名小寫用連字號>.md（例：topic-fine-tuning.md）
2. 建立對應的 deep-topic-<英文主題名>.md 至 /Users/daniel.chang/Desktop/ai/tasks/ 目錄
3. task 檔案格式：

```markdown
# 深度學習任務清單 - <主題名>

> 建立日期：YYYY-MM-DD
> 對應 doc：/Users/daniel.chang/Desktop/ai/docs/topic-<名稱>.md
> 狀態：待執行

## 架構深度解析
- [ ] 核心原理說明
- [ ] 流程圖與元件拆解

## 實作範例
- [ ] 完整可執行程式碼（含環境設定）

## 應用場景
- [ ] 實際案例 1（含優缺點）
- [ ] 實際案例 2
- [ ] 實際案例 3

## 擴充與進階
- [ ] 進階技術與變體
- [ ] 相關論文或資源

## 優化技巧
- [ ] 常見問題與解法
- [ ] 效能調優重點

## 參考資源
- [ ] 待填入（第二階段執行後補充）
```

使用 write 工具寫入，確認成功後繼續。

---

## 第二階段：docs 文件撰寫與更新

對以下兩類文件依序處理（每次處理一個，完成後才進行下一個）：

**類型 A：** docs 中已存在但內容不足（少於 200 字或缺少實作範例）的文件
**類型 B：** 第一階段新增的缺口主題（對應 doc 尚未建立）

### 每個主題的處理步驟：

#### 步驟 2.1 — 研究主題
執行以下搜尋（每個主題）：
- web_search: "<主題名> tutorial best practices 2025"
- web_search: "<主題名> implementation example python"
- web_fetch: 從搜尋結果中選取 2-3 個最高品質的技術文章（優先選 official docs、arxiv、GitHub、知名技術部落格）

#### 步驟 2.2 — 撰寫 doc 文件
使用 write 工具，將完整內容寫入 /Users/daniel.chang/Desktop/ai/docs/topic-<名稱>.md
（如已存在則覆蓋更新，如為 level 文件則寫入 level<N>-<名稱>.md）

doc 文件必須包含以下結構：

```markdown
# <主題中文名稱> (<英文名>)

> 最後更新：YYYY-MM-DD

## 什麼是 <主題>？
（100-200 字清晰定義，說明解決什麼問題）

## 核心原理
（用文字 + 步驟清單說明運作流程，若有公式用 LaTeX 格式 $...$ 表示）

## 實作範例

### 環境設定
\`\`\`bash
pip install ...
\`\`\`

### 核心程式碼
\`\`\`python
# 完整可執行的範例，含註解
...
\`\`\`

## 應用場景
1. **場景一**：描述 + 適用條件 + 優缺點
2. **場景二**：...
3. **場景三**：...

## 進階技術
- 技術 A：說明
- 技術 B：說明
- 相關論文：...

## 常見問題與優化
| 問題 | 原因 | 解法 |
|------|------|------|
| ... | ... | ... |

## 參考資源
- [資源標題](URL) — 摘要說明
- [資源標題](URL) — 摘要說明
- [資源標題](URL) — 摘要說明

---
*此文件由 AI agent 自動生成，最後更新：YYYY-MM-DD*
```

#### 步驟 2.3 — 儲存參考資料
將研究過的文章摘要使用 write 工具儲存至：
/Users/daniel.chang/Desktop/ai/docs/references/<主題名>-ref.md

參考檔格式：
```markdown
# <主題> 參考資料

> 收集日期：YYYY-MM-DD

## 資料來源

### 1. <文章標題>
- URL：<完整 URL>
- 重點摘要：（3-5 條重點，每條一行）

### 2. <文章標題>
...
```

---

## 第三階段：更新 task 狀態與執行日誌

### 步驟 3.1 — 更新 task 檔案狀態
對第二階段已完成的每個主題，讀取對應的 deep-*.md task 檔案：
- 將已完成的 `- [ ]` 項目改為 `- [x]`
- 在檔案頂部更新「狀態：已完成」
- 使用 write 工具寫回

### 步驟 3.2 — 寫入執行日誌
使用 write 工具，將本次執行結果追加寫入：
/Users/daniel.chang/Desktop/ai/logs/autodoc-YYYY-MM-DD.log

日誌格式：
```
=== 執行時間：YYYY-MM-DD HH:MM ===

【第一階段 - 主題盤點】
- 現有 docs 主題數：N 個
- 業界主題總數：N 個
- 新發現缺口主題：N 個
  - 新增：topic-xxx.md
  - 新增：topic-yyy.md

【第二階段 - docs 撰寫】
- 成功更新：N 個
  - topic-xxx.md（新建）
  - topic-yyy.md（更新）
- 失敗：N 個（若有，列出原因）

【第三階段 - 狀態更新】
- task 狀態已更新：N 個

【本次執行摘要】
- 總處理主題數：N
- 總耗時（估計）：N 分鐘
- 下次建議優先處理：<主題名>
```

---

## 執行優先順序規則

1. **優先處理** docs 不存在但 tasks 已存在的主題（修補缺漏）
2. **其次處理** docs 存在但內容少於 200 字的主題（補充深度）
3. **最後處理** 第一階段新發現的缺口主題（擴充廣度）
4. 每次執行**最多處理 3 個主題**（避免超時），未完成的下次繼續

## 重要規則

- 所有 write 操作必須確認工具回傳成功，否則停止並記錄錯誤
- 不可只在文字中描述「已完成」，必須實際執行 write 工具
- 每個主題完成後才進行下一個，不可並行跳躍
- 若 web_search 無結果，改用 web_fetch 直接抓取已知的參考 URL
- 所有文件使用繁體中文撰寫，程式碼範例使用英文
```

---

## 版本說明

| 版本 | 日期 | 變更 |
|------|------|------|
| v1.0 | 2026-04-21 | 原始版本（只建立 tasks，不建立 docs） |
| v2.0 | 2026-04-21 | 三階段版：盤點缺口 → 撰寫 docs → 更新狀態 |
