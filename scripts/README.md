# Scripts

正式 workflow runner：

- `agentic_pipeline.py`：主要 runner，cron 入口。執行時寫入以下 logs：
  - `logs/pipeline.log` — pipeline 層級事件（START / CALL / ERROR / DONE）
  - `logs/summary.log` — 每次執行完成的摘要（PIPELINE DONE）
  - `logs/runs/{run_id}/` — 每個 agent turn 的 stdout/stderr 原始輸出
  - `logs/agents/{role}.log` — 每個 agent 的累計行動紀錄

支援腳本：

- `gen_deep_tasks.py`：生成 deep task spec 檔案到 `tasks/specs/`
- `gen_learning_materials.py`：生成學習材料到 `docs/`（包含更新 `docs/AI_Glossary.md`）
- `gen_roadmap.py`：重新生成 `roadmap.md`

Cron 設定：

```
python3 scripts/agentic_pipeline.py
```

Legacy 腳本：

- `legacy/`：保留舊的 shell 自動化腳本。這些腳本不再由 OpenClaw cron 自動執行，避免產生低價值占位內容。
