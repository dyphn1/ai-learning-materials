# ai-learning-materials

這個資料夾是 AI / OpenClaw 學習資料庫，並由一個可執行的 agentic workflow 維護。

## 目錄結構

```text
.
├── .github/                 # agent、skill、workspace instructions
├── core_learning/           # OpenClaw 基礎學習筆記
├── docs/                    # 主要 AI 技術學習文件
│   └── references/          # 論文、官方文件、PDF 與引用紀錄
├── learning_materials/      # 由 docs 轉成的讀書筆記 / glossary
├── logs/                    # runner 與 workflow 執行紀錄
├── requirements/            # 原始需求與需求拆解
├── scripts/                 # 可執行自動化，主入口是 agentic_pipeline.py
├── tasks/                   # agentic workflow 狀態機與任務資料
├── weekly-challenges/       # 保留的手動學習挑戰
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
  -> tasks/active/*.json
  -> tasks/context/*-fact.json
  -> docs/*.md
  -> tasks/completed/*.json
  -> tasks/archived/*.json
```

角色定義放在 `.github/agents/`：

- `orchestrator.agent.md`
- `fact-check-scout.agent.md`
- `instructional-writer.agent.md`
- `quality-validator.agent.md`

`tasks/` 只保留 workflow 狀態與任務規格；過時的 prompt 和失敗的每日更新產物已移除。
