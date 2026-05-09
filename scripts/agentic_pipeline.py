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
import shutil
import subprocess
import sys
from typing import Any


ROOT = Path("/Users/daniel.chang/Desktop/ai")
TASKS = ROOT / "tasks"
ACTIVE = TASKS / "active"
COMPLETED = TASKS / "completed"
ARCHIVED = TASKS / "archived"
CONTEXT = TASKS / "context"
STALE = TASKS / "stale"
AGENTS = ROOT / ".github" / "agents"
LOGS = ROOT / "logs"
PIPELINE_LOG = LOGS / "agentic_pipeline.log"
ORCHESTRATOR_LOG = LOGS / "orchestrator.log"
RUN_LOG_ROOT = LOGS / "agentic-pipeline-runs"
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


def acquire_lock() -> None:
    if LOCK_FILE.exists():
        raise PipelineError(f"pipeline lock exists: {LOCK_FILE}")
    LOCK_FILE.write_text(f"{os.getpid()} {now()}\n", encoding="utf-8")


def release_lock() -> None:
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()


def move_to_stale(path: Path, reason: str, rid: str) -> None:
    state = path.parent.name
    dest_dir = STALE / rid / state
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / path.name
    shutil.move(str(path), str(dest))
    log(f"STALE: moved {path} -> {dest} ({reason})")


def normalize_state(rid: str) -> None:
    """Keep task state single-owner.

    If a task is archived, stale copies in active/completed confuse future cron
    runs.  Preserve those copies under tasks/stale instead of deleting them.
    """
    archived_ids = {task_id(p) for p in json_files(ARCHIVED)}
    for folder in (ACTIVE, COMPLETED):
        for path in json_files(folder):
            tid = task_id(path)
            if tid in archived_ids:
                move_to_stale(path, "archived task had duplicate state copy", rid)


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
    if not json_files(ACTIVE):
        raise PipelineError("Orchestrator finished but no active task card exists")


def assert_fact_done(tid: str) -> None:
    fact = CONTEXT / f"{tid}-fact.json"
    active = find_task_file(ACTIVE, tid)
    if not fact.exists():
        raise PipelineError(f"Fact-Check Scout finished but fact sheet is missing: {fact}")
    if not active:
        raise PipelineError(f"Fact-Check Scout finished but active task is missing: {tid}")
    status = read_json(active).get("status")
    if status != "Research_Done":
        raise PipelineError(f"Fact-Check Scout finished but active status is {status!r}, not Research_Done")


def assert_completed(tid: str) -> None:
    completed = find_task_file(COMPLETED, tid)
    if not completed:
        raise PipelineError(f"Instructional Writer finished but completed task is missing: {tid}")
    status = read_json(completed).get("status")
    if status != "Completed":
        raise PipelineError(f"Instructional Writer finished but completed status is {status!r}, not Completed")


def assert_archived(tid: str, rid: str) -> None:
    normalize_state(rid)
    archived = find_task_file(ARCHIVED, tid)
    if not archived:
        raise PipelineError(f"Quality Validator finished but archived task is missing: {tid}")
    if find_task_file(ACTIVE, tid) or find_task_file(COMPLETED, tid):
        raise PipelineError(f"Quality Validator finished but duplicate active/completed state remains: {tid}")


def active_work_items() -> list[dict[str, Any]]:
    return load_tasks(ACTIVE)[:2]


def completed_work_items() -> list[dict[str, Any]]:
    return load_tasks(COMPLETED)[:2]


def validate_with_retries(tid: str, rid: str, args: argparse.Namespace) -> None:
    for attempt in range(args.max_retries + 1):
        instruction = (
            f"Validate completed task {tid}. If rejected, write the review note and leave active status Research_Done."
            if attempt == 0
            else f"Re-validate completed task {tid} after writer fixes."
        )
        invoke_agent("quality-validator", instruction, rid, args.timeout)

        active_after = find_task_file(ACTIVE, tid)
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
        assert_completed(tid)


def run_pipeline(args: argparse.Namespace) -> int:
    rid = run_id()
    acquire_lock()
    try:
        log(f"START: run={rid}")
        normalize_state(rid)
        if args.normalize_only:
            log(f"DONE: normalize-only run={rid}")
            return 0

        completed = completed_work_items()
        active = active_work_items()

        if completed:
            for item in completed:
                tid = str(item["task_id"])
                validate_with_retries(tid, rid, args)
            append(ORCHESTRATOR_LOG, f"[{now()}] PIPELINE DONE: validated {len(completed)} completed task(s)")
            return 0

        if not active:
            invoke_agent(
                "orchestrator",
                "Fresh start: active/ and completed/ are empty. Create at most two active task cards from backlog.json.",
                rid,
                args.timeout,
            )
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
                assert_fact_done(tid)

            refreshed = find_task_file(ACTIVE, tid)
            if refreshed and read_json(refreshed).get("status") == "Research_Done":
                invoke_agent(
                    "instructional-writer",
                    f"Write or revise the target document for task {tid}. Use only /tasks/context/{tid}-fact.json and any review note.",
                    rid,
                    args.timeout,
                )
                assert_completed(tid)

            validate_with_retries(tid, rid, args)

        append(ORCHESTRATOR_LOG, f"[{now()}] PIPELINE DONE: processed {len(active)} active task(s)")
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
