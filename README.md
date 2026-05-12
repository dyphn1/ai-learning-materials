# ai-learning-materials

這個資料夾是 AI / OpenClaw 學習資料庫，並由一個可執行的 agentic workflow 維護。

## 目錄結構

```text
.
├── .github/                 # agent、skill、workspace instructions
├── docs/                    # 主要 AI 技術學習文件
│   ├── openclaw/            # OpenClaw 學習文件（安裝、CLI、cron、MCP 等）
│   ├── rag/                 # RAG 子主題深度文件
│   └── AI_Glossary.md       # AI 術語詞典
├── references/              # 論文、官方文件、PDF 與引用紀錄
├── logs/                    # runner 執行紀錄（pipeline.log / summary.log / runs/ / agents/）
├── scripts/                 # 可執行自動化，主入口是 agentic_pipeline.py
├── tasks/                   # agentic workflow 狀態機與任務資料
│   └── specs/               # 需求規格與 deep task 模板
├── weekly-challenges/       # 每週一個主題的學習挑戰
└── workflow/                # cron / workflow 設定說明
```

## Agentic Workflow

目前正式入口：

```bash
cd /Users/daniel.chang/Desktop/ai && /usr/bin/env python3 scripts/agentic_pipeline.py
```

workflow 對應：

```text
tasks/backlog.json
  -> tasks/active/{task_id}.json           # 機器可讀狀態
  -> tasks/{timestamp}_{slug}.md           # 人類可讀任務紀錄
  -> tasks/context/{task_id}-fact.json     # fact sheet
  -> docs/*.md                             # 最終知識文件
  -> tasks/completed/{task_id}.json
  -> tasks/archived/{task_id}.json
  -> logs/agents/{role}.log                # per-agent 行動紀錄
```

角色定義放在 `.github/agents/`：

- `orchestrator.agent.md`
- `fact-check-scout.agent.md`
- `instructional-writer.agent.md`
- `quality-validator.agent.md`

`tasks/` 只保留 workflow 狀態與任務規格；過時的 prompt 和失敗的每日更新產物已移除。
