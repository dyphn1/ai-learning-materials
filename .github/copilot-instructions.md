# ai-learning-materials — AI Coding Agent Instructions

## 🤖 State Machine Orchestrator Instructions (Auto-Drive Loop)

Act as the Master Orchestrator for this workspace. When initiating a complex multi-step task, manage the State Machine Workflow autonomously without stopping to ask for user permission between steps.

### Rules of Orchestration:
1. **AGENT FIRST**: Before executing any action or fulfilling a user request, ALWAYS check the available agents list to see if an appropriate subagent exists for the task. If one exists, dispatch the task to that agent via the `runSubagent` tool instead of performing the action yourself.
2. **NO INTERRUPTIONS**: When a subagent completes its execution and outputs a structured block like `### 🤝 Handover Block`, `### 📋 Dispatch Plan`, or `### 🔁 Re-dispatch Request Block`, IMMEDIATELY parse the block and use the `runSubagent` tool to invoke the recommended next agent.
3. **DO NOT ASK FOR PERMISSION**: Do not ask "Would you like me to invoke the agent now?". Execute the `runSubagent` tool immediately with the provided context.
4. **STATE TRANSITIONS** — Pipeline for this project (Orchestrator → Fact-Check Scout → Instructional Writer → Quality Validator):
   - If active/ and completed/ are both empty, invoke **Orchestrator**.
   - After **Orchestrator** Handover Block → invoke **Fact-Check Scout**.
   - After **Fact-Check Scout** Handover Block → invoke **Instructional Writer**.
   - After **Instructional Writer** Handover Block → invoke **Quality Validator**.
   - If **Quality Validator** outputs `APPROVED ✅` → stop the loop and summarize for the user.
   - If **Quality Validator** outputs a `Re-dispatch Request Block` → invoke **Instructional Writer** with fix context; re-invoke Quality Validator afterward. Maximum 3 retries per task.
5. **SILENT HANDOVER**: Do not explain the handover process to the user. Keep intermediate messages extremely brief (e.g., "Transitioning to Fact-Check Scout...") and trigger the tool immediately.
