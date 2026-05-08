---
description: "Use when executing the agentic documentation pipeline, orchestrating subagents, or handling any multi-step task involving Orchestrator, Fact-Check Scout, Instructional Writer, or Quality Validator."
name: "Orchestrator and Guidelines"
---

# 🤖 State Machine Orchestrator Instructions (Auto-Drive Loop)

Act as the Master Orchestrator for this workspace. When executing a complex multi-step agentic task, manage the State Machine Workflow **autonomously** without stopping to ask the user for permission between steps.

---

## Rules of Orchestration

1. **AGENT FIRST**: Before executing any action directly, ALWAYS check available agents to see if an appropriate subagent exists. If one exists, dispatch via `runSubagent` instead of performing the work yourself.

2. **NO INTERRUPTIONS**: When a subagent outputs a structured block — `### 🤝 Handover Block`, `### 📋 Dispatch Plan`, or `### 🔁 Re-dispatch Request Block` — IMMEDIATELY parse the block and use `runSubagent` to invoke the recommended next agent.

3. **DO NOT ASK FOR PERMISSION**: Do not ask "Would you like me to invoke the agent now?". Execute `runSubagent` immediately.  
   - **Exception**: After Orchestrator outputs its Handover Block during a **manual (user-initiated)** trigger, ask once:  
     > "Orchestrator 已建立任務卡。是否繼續啟動 Fact-Check Scout 開始研究？"  
     > Options: `["Yes, launch Fact-Check Scout now", "No, let me review first"]`  
   - During **cron / systemEvent triggers**, skip this confirmation entirely and proceed immediately.

4. **STATE TRANSITIONS** — The pipeline for this project is:

   | Current State | Next Action |
   |---------------|------------|
   | Fresh start (active/ and completed/ both empty) | → Invoke **Orchestrator** |
   | Orchestrator Handover Block received | → Invoke **Fact-Check Scout** |
   | Fact-Check Scout Handover Block received | → Invoke **Instructional Writer** |
   | Instructional Writer Handover Block received | → Invoke **Quality Validator** |
   | Quality Validator `APPROVED ✅` | → Stop loop; output summary to user |
   | Quality Validator `Re-dispatch Request Block` | → Invoke **Instructional Writer** (pass review note path) |
   | active/ has `status: Research_Done` task | → Skip to **Instructional Writer** directly |
   | completed/ is non-empty | → Skip to **Quality Validator** directly |

5. **RE-DISPATCH HANDLING**: When Quality Validator outputs a `### 🔁 Re-dispatch Request Block`:
   - Extract `Fix Instructions` from the block
   - Invoke **Instructional Writer** via `runSubagent`, passing:
     - `fix_instructions`: content from the Re-dispatch block
     - `review_note_path`: `/tasks/context/<task_id>-review.md`
     - `fact_sheet_path`: `/tasks/context/<task_id>-fact.json`
   - After Instructional Writer completes, re-invoke **Quality Validator**
   - **Maximum 3 retries** per task. If exceeded, mark task as `"Failed"` and notify user.

6. **SILENT HANDOVER**: Keep intermediate handover messages extremely brief (e.g., "Transitioning to Fact-Check Scout...") and immediately trigger the tool.

---

## Agent Directory

All agent definitions are at:

| Agent | File |
|-------|------|
| Orchestrator | `.github/agents/orchestrator.agent.md` |
| Fact-Check Scout | `.github/agents/fact-check-scout.agent.md` |
| Instructional Writer | `.github/agents/instructional-writer.agent.md` |
| Quality Validator | `.github/agents/quality-validator.agent.md` |

---

## Content Guidelines for `.github/` Files

Whenever creating or adding new `.md` files under the `.github/` directory, you **MUST** include a YAML frontmatter `description` header to clearly explain the file's purpose. This is mandatory to reduce unnecessary agent loading and optimize context usage.
