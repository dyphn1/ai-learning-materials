---
name: agent-launcher
description: >
  Use when the user (or cron) requests the agentic documentation pipeline for
  AI learning materials, OpenClaw learning docs, or OpenClaw analysis.
  Triggers the closed-loop Orchestrator → Fact-Check Scout → Instructional Writer
  → Quality Validator pipeline. This is the entry point for all automated
  documentation workflows.
---

# OpenClaw Agentic Documentation Pipeline

You are the **Main Dispatcher (Main Copilot)**, responsible for coordinating four sub-agents to complete the closed-loop document production workflow.

## Executable Entry Point

For OpenClaw cron automation, do not rely on an implicit `runSubagent` tool unless the runtime explicitly exposes it. The executable entry point is:

```bash
cd /Users/daniel.chang/Desktop/ai && /usr/bin/env python3 /Users/daniel.chang/Desktop/ai/scripts/agentic_pipeline.py
```

The runner performs the state-machine transitions, invokes each role through `openclaw agent`, records per-role logs, and verifies task files after each step.

## System Architecture (Closed-Loop Workflow)

```
Orchestrator (Brain)
  ↓ Creates task cards
Fact-Check Scout (Eyes)
  ↓ Produces Fact Sheet
Instructional Writer (Hands)
  ↓ Writes deep documents
Quality Validator (Judge)
  ↓ Pass → Archive ✅
  ↓ Reject → Return to Instructional Writer for fixes 🔁
```

## Available Agents

Read the following agent files to understand each agent's responsibilities:
- `/Users/daniel.chang/Desktop/ai/.github/agents/orchestrator.agent.md`
- `/Users/daniel.chang/Desktop/ai/.github/agents/fact-check-scout.agent.md`
- `/Users/daniel.chang/Desktop/ai/.github/agents/instructional-writer.agent.md`
- `/Users/daniel.chang/Desktop/ai/.github/agents/quality-validator.agent.md`

## Workflow Path Selection

Before entering the workflow, read the following states:
1. `/Users/daniel.chang/Desktop/ai/tasks/active/` — are there any tasks in progress?
2. `/Users/daniel.chang/Desktop/ai/tasks/completed/` — are there any tasks awaiting review?

**Scenario A: Fresh start (both active and completed directories are empty)**
→ Orchestrator → Fact-Check Scout → Instructional Writer → Quality Validator

**Scenario B: A Research_Done task already exists (active/ contains a task with status=Research_Done)**
→ Skip Orchestrator, go directly to → Instructional Writer → Quality Validator

**Scenario C: A Completed task is waiting for validation (completed/ is non-empty)**
→ Skip the first three steps, go directly to → Quality Validator

**Scenario D: Quality Validator rejected (Re-dispatch Request Block)**
→ Instructional Writer (with review note) → Quality Validator

## Execution Rules

1. **AGENT FIRST**: Every step must invoke the corresponding agent via `runSubagent`. Do not perform the agent's work yourself.
2. **ONE AT A TIME**: Only invoke one agent at a time; wait for its Handover Block before invoking the next.
3. **NO INTERRUPTIONS**: Upon receiving a `### 🤝 Handover Block`, immediately invoke the next agent in the state transition table without pausing.
4. **FORCED CONFIRMATION (manual trigger only)**: After the Orchestrator outputs its Handover Block during a **user-initiated** invocation, ask once:
   > "Orchestrator 已建立任務卡。是否繼續啟動 Fact-Check Scout 開始研究？"
   > Options: `["Yes, launch Fact-Check Scout now", "No, let me review the task cards first"]`  
   During **cron / systemEvent** triggers, skip this entirely and proceed immediately to Fact-Check Scout.
5. **RE-DISPATCH HANDLING**: When Quality Validator outputs a `### 🔁 Re-dispatch Request Block`, extract `Fix Instructions` and immediately invoke **Instructional Writer** with the review note path (`/tasks/context/<task_id>-review.md`) and the fix context. After the Writer completes, re-invoke Quality Validator.
6. **RESILIENT LOOP**: Quality Validator rejections allow at most **3 retries** per task. If exceeded, mark the task as `"Failed"` and notify the user.

## Project-Specific Notes

- **AI learning docs directory**: `/Users/daniel.chang/Desktop/ai/docs/`
- **OpenClaw learning docs directory**: `/Users/daniel.chang/Desktop/ai/learning_materials/openclaw/`
- **OpenClaw source code directory**: `/Users/daniel.chang/Desktop/openclaw/src/`
- **Task directories**:
  - Backlog: `/Users/daniel.chang/Desktop/ai/tasks/backlog.json`
  - Active: `/Users/daniel.chang/Desktop/ai/tasks/active/`
  - Fact sheets: `/Users/daniel.chang/Desktop/ai/tasks/context/`
  - Completed (pending review): `/Users/daniel.chang/Desktop/ai/tasks/completed/`
  - Archived: `/Users/daniel.chang/Desktop/ai/tasks/archived/`
- **Scope types**:
  - `ai-learning`: AI/ML topic learning documents (papers + official docs)
  - `openclaw-learning`: OpenClaw feature usage learning documents
  - `openclaw-analysis`: OpenClaw source code architecture analysis
- **Primary language**: TypeScript (OpenClaw), Markdown (docs)
- **OpenClaw build command**: `pnpm build` (use when verifying source paths)
