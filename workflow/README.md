# Workflow

這裡保留 OpenClaw cron 與 agentic workflow 的設計說明。

正式執行入口不是大型 prompt，而是：

```bash
cd /Users/daniel.chang/Desktop/ai && /usr/bin/env python3 scripts/agentic_pipeline.py
```

`agentic_pipeline.py` 會：

1. 取得 lock。
2. 清理重複狀態副本。
3. 根據 `tasks/` 狀態決定進入點。
4. 透過 `openclaw agent` 逐步呼叫 `.github/agents/` 的角色。
5. 驗證每一步的檔案狀態。
6. 寫入 `logs/agentic_pipeline.log` 與 `logs/agentic-pipeline-runs/<run_id>/`。

保留檔案：

- `agentic-pipeline-cron-task.md`：目前 AI 學習資料 workflow 的 cron 說明。
- `openclaw-learning-cron-task.md`：OpenClaw learning 類任務的歷史設計參考。
