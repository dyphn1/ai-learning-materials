# Agentic Pipeline Workflow

Entry point:

```bash
cd /Users/daniel.chang/Desktop/ai && /usr/bin/env python3 scripts/agentic_pipeline.py
```

The runner manages locks, state normalization, agent dispatch via `openclaw agent`, and file verification after each step.

---

## Architecture

```
Orchestrator (Brain)
  ↓ Phase 0: Sub-topic decomposition (broad topics → focused sub-topics in backlog.json)
  ↓ Phase 1: Environment scan (tasks/cards/)
  ↓ Phase 2: Creates task cards in tasks/cards/
  ↓ [Gate 1: verify cards/<id>.json status=Pending]
Fact-Check Scout (Eyes)
  ↓ Produces tasks/context/<id>-fact.json
  ↓ Updates tasks/cards/<id>.json status → Research_Done
  ↓ [Gate 2: verify fact.json + status=Research_Done]
Instructional Writer (Hands)
  ↓ Writes target_doc
  ↓ Updates tasks/cards/<id>.json status → Completed
  ↓ [Gate 3: verify status=Completed + target_doc]
Quality Validator (Judge)
  ↓ Pass → tasks/cards/<id>.json status → Archived ✅
  ↓ [Gate 4: verify status=Archived]
  ↓ Reject → tasks/context/<id>-review.md → back to Writer 🔁
```

Each Gate is a mandatory file-existence check. If the expected files are missing, the same agent is re-dispatched (up to 3 retries).

---

## Agent Definitions

| Role | File | Scope |
|------|------|-------|
| Orchestrator | `.github/agents/orchestrator.agent.md` | Reads `backlog.json`, creates `tasks/cards/<task_id>.json` |
| Fact-Check Scout | `.github/agents/fact-check-scout.agent.md` | Researches and produces fact sheets |
| Instructional Writer | `.github/agents/instructional-writer.agent.md` | Writes deep docs from fact sheets |
| Quality Validator | `.github/agents/quality-validator.agent.md` | Audits docs; archives on pass, rejects on fail |

---

## Task State Flow

All task JSON files live in `tasks/cards/<task_id>.json`. The `status` field is the sole state machine — files are never moved or copied between directories.

```
backlog.json           status: Pending
       │
       ▼ Orchestrator Phase 0 (if broad topic detected)
backlog.json           sub-topics added as new entries; parent → decomposed=true, status=Skipped
       │
       ▼ Orchestrator Phase 2 → creates tasks/cards/<id>.json
tasks/cards/           status: Pending
       │
       ▼ Fact-Check Scout claims
tasks/cards/           status: Researching
       │
       ▼ Fact-Check Scout completes
tasks/cards/           status: Research_Done
tasks/context/         <id>-fact.json created
       │
       ▼ Instructional Writer completes
tasks/cards/           status: Completed
docs/ or learning_materials/  target_doc written
       │
       ▼ Quality Validator — PASS
tasks/cards/           status: Archived ✅

       ▼ Quality Validator — REJECT
tasks/cards/           status: Research_Done (reset in-place)
tasks/context/         <id>-review.md created
       → back to Instructional Writer (max 3 retries)
       
       ▼ Exceeded retries
tasks/cards/           status: Failed
```

> Stale folder (`tasks/stale/`) is no longer used; the single-file model eliminates the need for orphan detection.

---

## Logs Flow

```
logs/
  pipeline.log              Runner events (start, step, done, errors)
  summary.log               Per-task archive record (written by Quality Validator on pass)
  agents/
    orchestrator.log        Orchestrator per-run action log
    fact-check-scout.log    Fact-Check Scout per-run action log
    instructional-writer.log
    quality-validator.log
  runs/
    <run_id>/               Per-run stdout/stderr for each role
      orchestrator.stdout.txt
      orchestrator.stderr.txt
      fact-check-scout.stdout.txt
      ...
```

`pipeline.log` is the primary debug log. `summary.log` is the high-level archive history. Agent logs are written by the runner after each `openclaw agent` call; per-run files contain raw stdout/stderr for deep debugging.

---

## Cron Setup (OpenClaw)

Daily at 08:00 Asia/Taipei:

```json
{
  "schedule": {
    "kind": "cron",
    "expr": "0 8 * * *",
    "tz": "Asia/Taipei",
    "staggerMs": 60000
  },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "執行可驗證的 AI 學習資料 agentic pipeline runner。請只執行以下命令，不要自行模擬 Orchestrator / Fact-Check Scout / Instructional Writer / Quality Validator，也不要只輸出摘要：\n\ncd /Users/daniel.chang/Desktop/ai && /usr/bin/env python3 /Users/daniel.chang/Desktop/ai/scripts/agentic_pipeline.py\n\n完成後回報 exit code；若命令失敗，回報 stderr 與 logs/pipeline.log 的最後幾行。"
  },
  "delivery": {
    "mode": "announce"
  }
}
```

> The payload explicitly forbids the cron agent from simulating individual agents. It must execute the Python runner directly.

---

## Manual Trigger

To run the pipeline once (outside cron), or to check state without running:

```bash
# Full pipeline run
cd /Users/daniel.chang/Desktop/ai && python3 scripts/agentic_pipeline.py

# Normalize stale state only (no agent dispatch)
cd /Users/daniel.chang/Desktop/ai && python3 scripts/agentic_pipeline.py --normalize-only
```

Runner options:
- `--timeout <seconds>` — per-agent timeout (default: 900s)
- `--max-retries <n>` — Quality Validator retry limit (default: 3)
