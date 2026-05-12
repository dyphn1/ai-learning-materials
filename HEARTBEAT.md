# HEARTBEAT.md

## Periodic Checks

```
# Check if pipeline.log has ERROR in the last 24 hours
check: grep -c "ERROR" logs/pipeline.log | awk '{if($1>0) print "PIPELINE_ERROR: " $1 " errors found in logs/pipeline.log"}'
```

**Rule:** 每次 pipeline 執行後，檢查 `logs/pipeline.log` 是否有 `ERROR` 記錄。  
若有錯誤，應分析 `logs/runs/` 中最近一次失敗的 stdout/stderr，找到根本原因並記錄於 `logs/agents/orchestrator.log`。
