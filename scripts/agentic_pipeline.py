#!/usr/bin/env python3
"""Executable runner for the AI documentation agentic workflow.

The cron job should call this file directly.  The runner owns orchestration,
state checks, logs, and the handoff between OpenClaw agent turns.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import time
import subprocess
import sys
from typing import Any


ROOT = Path("/Users/daniel.chang/Desktop/ai")
TASKS = ROOT / "tasks"
CARDS = TASKS / "cards"
CONTEXT = TASKS / "context"
AGENTS = ROOT / ".github" / "agents"
LOGS = ROOT / "logs"
PIPELINE_LOG = LOGS / "pipeline.log"
ORCHESTRATOR_LOG = LOGS / "summary.log"
RUN_LOG_ROOT = LOGS / "runs"
AGENT_LOG_ROOT = LOGS / "agents"
LOCK_FILE = TASKS / ".agentic_pipeline.lock"

ROLE_FILES = {
    "orchestrator": AGENTS / "orchestrator.agent.md",
    "fact-check-scout": AGENTS / "fact-check-scout.agent.md",
    "instructional-writer": AGENTS / "instructional-writer.agent.md",
    "quality-validator": AGENTS / "quality-validator.agent.md",
}


class PipelineError(RuntimeError):
    pass


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def run_id() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().strftime("%Y%m%dT%H%M%S%z")


def append(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line.rstrip() + "\n")


def log(message: str) -> None:
    append(PIPELINE_LOG, f"[{now()}] {message}")


def append_agent_log(role: str, message: str) -> None:
    """Append a one-line action summary to the per-agent cumulative log."""
    log_path = AGENT_LOG_ROOT / f"{role}.log"
    append(log_path, f"[{now()}] {message}")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    tmp.replace(path)


def json_files(path: Path) -> list[Path]:
    if not path.exists():
        return []
    return sorted(p for p in path.glob("*.json") if p.is_file())


def task_id(path: Path) -> str:
    try:
        return str(read_json(path).get("task_id") or path.stem)
    except Exception:
        return path.stem


def load_tasks(path: Path) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for file in json_files(path):
        data = read_json(file)
        data["_path"] = str(file)
        tasks.append(data)
    return tasks


LOCK_MAX_AGE_SECONDS = 1800  # 30 minutes

def acquire_lock() -> None:
    if LOCK_FILE.exists():
        age = time.time() - LOCK_FILE.stat().st_mtime
        if age > LOCK_MAX_AGE_SECONDS:
            log(f"STALE LOCK: removing lock file aged {int(age)}s (max {LOCK_MAX_AGE_SECONDS}s)")
            LOCK_FILE.unlink()
        else:
            raise PipelineError(f"pipeline lock exists: {LOCK_FILE}")
    LOCK_FILE.write_text(f"{os.getpid()} {now()}\n", encoding="utf-8")


def release_lock() -> None:
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()


def normalize_state(rid: str) -> None:
    """No-op: single-file model eliminates the need for folder-state reconciliation."""
    pass


def find_task_file(folder: Path, tid: str) -> Path | None:
    for path in json_files(folder):
        if task_id(path) == tid:
            return path
    return None


def agent_id_for(role: str) -> str:
    env_key = "AI_PIPELINE_" + role.upper().replace("-", "_") + "_AGENT_ID"
    return os.environ.get(env_key) or os.environ.get("AI_PIPELINE_AGENT_ID", "ai-pipeline")


def invoke_agent(role: str, instruction: str, rid: str, timeout: int) -> str:
    agent_file = ROLE_FILES[role]
    definition = agent_file.read_text(encoding="utf-8")
    message = f"""You are invoked by /Users/daniel.chang/Desktop/ai/scripts/agentic_pipeline.py.

This is an executable pipeline run, not a planning conversation.

Rules:
- Perform the file operations required by your role.
- Do not claim success unless the files were actually written or moved.
- If a required tool or source is unavailable, fail explicitly and leave the task state unchanged.
- End with the Handover Block or Validation Report required by the role.

Pipeline run id: {rid}
Workspace root: /Users/daniel.chang/Desktop/ai

Role definition:

{definition}

Runner instruction:

{instruction}
"""
    role_dir = RUN_LOG_ROOT / rid
    role_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = role_dir / f"{role}.stdout.txt"
    stderr_path = role_dir / f"{role}.stderr.txt"

    cmd = [
        "openclaw",
        "agent",
        "--local",
        "--agent",
        agent_id_for(role),
        "--session-id",
        f"ai-agentic-pipeline-{rid}-{role}",
        "--timeout",
        str(timeout),
        "--thinking",
        os.environ.get("AI_PIPELINE_AGENT_THINKING", "low"),
        "--json",
        "--message",
        message,
    ]
    log(f"CALL: {role} via local OpenClaw agent id={agent_id_for(role)}")
    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        timeout=timeout + 30,
        check=False,
    )
    stdout_path.write_text(proc.stdout, encoding="utf-8")
    stderr_path.write_text(proc.stderr, encoding="utf-8")
    if proc.returncode != 0:
        raise PipelineError(
            f"{role} failed with exit code {proc.returncode}; see {stdout_path} and {stderr_path}"
        )
    return proc.stdout


def assert_active_exists() -> None:
    active_statuses = {"Pending", "Active", "Researching"}
    cards = [
        p for p in json_files(CARDS)
        if read_json(p).get("status") in active_statuses
    ]
    if not cards:
        raise PipelineError("Orchestrator finished but no task card in tasks/cards/ has an active status")


def assert_fact_done(tid: str) -> None:
    fact = CONTEXT / f"{tid}-fact.json"
    card = find_task_file(CARDS, tid)
    if not fact.exists():
        raise PipelineError(f"Fact-Check Scout finished but fact sheet is missing: {fact}")
    if not card:
        raise PipelineError(f"Fact-Check Scout finished but task card is missing in tasks/cards/: {tid}")
    status = read_json(card).get("status")
    if status != "Research_Done":
        raise PipelineError(f"Fact-Check Scout finished but card status is {status!r}, not Research_Done")


def assert_completed(tid: str) -> None:
    card = find_task_file(CARDS, tid)
    if not card:
        raise PipelineError(f"Instructional Writer finished but task card is missing in tasks/cards/: {tid}")
    status = read_json(card).get("status")
    if status != "Completed":
        raise PipelineError(f"Instructional Writer finished but card status is {status!r}, not Completed")


def assert_archived(tid: str, rid: str) -> None:
    card = find_task_file(CARDS, tid)
    if not card:
        raise PipelineError(f"Quality Validator finished but task card is missing in tasks/cards/: {tid}")
    status = read_json(card).get("status")
    if status != "Archived":
        raise PipelineError(f"Quality Validator finished but card status is {status!r}, not Archived")


def active_work_items() -> list[dict[str, Any]]:
    active_statuses = {"Pending", "Active", "Researching", "Research_Done"}
    return [t for t in load_tasks(CARDS) if t.get("status") in active_statuses][:2]


def completed_work_items() -> list[dict[str, Any]]:
    return [t for t in load_tasks(CARDS) if t.get("status") == "Completed"][:2]


def validate_with_retries(tid: str, rid: str, args: argparse.Namespace) -> None:
    for attempt in range(args.max_retries + 1):
        instruction = (
            f"Validate completed task {tid}. If rejected, write the review note and leave active status Research_Done."
            if attempt == 0
            else f"Re-validate completed task {tid} after writer fixes."
        )
        invoke_agent("quality-validator", instruction, rid, args.timeout)
        append_agent_log("quality-validator", f"run={rid} task={tid} action=validate attempt={attempt}")

        active_after = find_task_file(CARDS, tid)
        if not active_after or read_json(active_after).get("status") != "Research_Done":
            assert_archived(tid, rid)
            return

        if attempt >= args.max_retries:
            failed = read_json(active_after)
            failed["status"] = "Failed"
            failed["failed_at"] = now()
            failed["failure_reason"] = "Quality Validator rejected more than max retries"
            write_json(active_after, failed)
            log(f"FAILED: {tid} exceeded retries")
            return

        updated = read_json(active_after)
        updated["retry_count"] = int(updated.get("retry_count", 0)) + 1
        write_json(active_after, updated)
        invoke_agent(
            "instructional-writer",
            f"Re-dispatch task {tid}. Apply review note /tasks/context/{tid}-review.md. Do not add facts beyond the fact sheet.",
            rid,
            args.timeout,
        )
        append_agent_log("instructional-writer", f"run={rid} task={tid} action=write")
        assert_completed(tid)


def run_pipeline(args: argparse.Namespace) -> int:
    rid = run_id()
    acquire_lock()
    try:
        log(f"START: run={rid}")
        CARDS.mkdir(parents=True, exist_ok=True)
        if args.normalize_only:
            log(f"DONE: normalize-only run={rid}")
            return 0

        completed = completed_work_items()
        active = active_work_items()

        if active:
            for item in active:
                tid = str(item["task_id"])
                status = str(item.get("status", ""))
                if status in {"Pending", "Active", "Researching"}:
                    invoke_agent(
                        "fact-check-scout",
                        f"Research active task {tid}. Produce /tasks/context/{tid}-fact.json and set active status to Research_Done.",
                        rid,
                        args.timeout,
                    )
                    append_agent_log("fact-check-scout", f"run={rid} task={tid} action=research")
                    assert_fact_done(tid)

                refreshed = find_task_file(CARDS, tid)
                if refreshed and read_json(refreshed).get("status") == "Research_Done":
                    invoke_agent(
                        "instructional-writer",
                        f"Write or revise the target document for task {tid}. Use only /tasks/context/{tid}-fact.json and any review note.",
                        rid,
                        args.timeout,
                    )
                    append_agent_log("instructional-writer", f"run={rid} task={tid} action=write")
                    assert_completed(tid)

                validate_with_retries(tid, rid, args)

            append(ORCHESTRATOR_LOG, f"[{now()}] PIPELINE DONE: processed {len(active)} active task(s)")
            log(f"DONE: run={rid}")
            return 0

        if completed:
            for item in completed:
                tid = str(item["task_id"])
                validate_with_retries(tid, rid, args)
            append(ORCHESTRATOR_LOG, f"[{now()}] PIPELINE DONE: validated {len(completed)} completed task(s)")
            return 0

        invoke_agent(
            "orchestrator",
            "Fresh start: tasks/cards/ has no actionable tasks. Create at most two task cards from backlog.json, saving them to tasks/cards/<task_id>.json.",
            rid,
            args.timeout,
        )
        append_agent_log("orchestrator", f"run={rid} action=fresh-start-dispatch")
        assert_active_exists()
        active = active_work_items()

        for item in active:
            tid = str(item["task_id"])
            status = str(item.get("status", ""))
            if status in {"Pending", "Active", "Researching"}:
                invoke_agent(
                    "fact-check-scout",
                    f"Research active task {tid}. Produce /tasks/context/{tid}-fact.json and set active status to Research_Done.",
                    rid,
                    args.timeout,
                )
                append_agent_log("fact-check-scout", f"run={rid} task={tid} action=research")
                assert_fact_done(tid)

            refreshed = find_task_file(CARDS, tid)
            if refreshed and read_json(refreshed).get("status") == "Research_Done":
                invoke_agent(
                    "instructional-writer",
                    f"Write or revise the target document for task {tid}. Use only /tasks/context/{tid}-fact.json and any review note.",
                    rid,
                    args.timeout,
                )
                append_agent_log("instructional-writer", f"run={rid} task={tid} action=write")
                assert_completed(tid)

            validate_with_retries(tid, rid, args)

        append(ORCHESTRATOR_LOG, f"[{now()}] PIPELINE DONE: processed {len(active)} active task(s) (fresh start)")
        log(f"DONE: run={rid}")
        return 0
    finally:
        release_lock()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the AI documentation agentic pipeline")
    parser.add_argument("--normalize-only", action="store_true", help="only reconcile duplicate task state")
    parser.add_argument("--timeout", type=int, default=int(os.environ.get("AI_PIPELINE_AGENT_TIMEOUT", "900")))
    parser.add_argument("--max-retries", type=int, default=int(os.environ.get("AI_PIPELINE_MAX_RETRIES", "3")))
    args = parser.parse_args()
    try:
        return run_pipeline(args)
    except Exception as exc:
        log(f"ERROR: {exc}")
        print(f"agentic pipeline failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
