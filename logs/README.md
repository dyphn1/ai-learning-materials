# Logs

執行紀錄目錄：

- `pipeline.log` — pipeline 層級事件（START / CALL / ERROR / DONE）
- `summary.log` — 每次執行完成的摘要（PIPELINE DONE）
- `runs/{run_id}/` — 每次執行中每個 agent turn 的 stdout/stderr 原始輸出
- `agents/{role}.log` — 每個 agent 的累計行動紀錄，作為下次執行的參考
