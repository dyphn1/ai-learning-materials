# Logs

目前保留與 agentic workflow 有關的執行紀錄：

- `agentic_pipeline.log`：runner 的狀態與錯誤紀錄。
- `orchestrator.log`：workflow 摘要。
- `agentic-pipeline-runs/<run_id>/`：每個角色 agent turn 的 stdout/stderr。

舊的 `autodoc-*`、`daily_tasks_*`、失敗搜尋輸出的每日更新紀錄已移除，避免干擾真正的 workflow 診斷。
