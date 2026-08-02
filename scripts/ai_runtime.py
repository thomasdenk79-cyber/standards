"""Control-plane guard for cost-aware AI worker launches.

The guard records metadata only. It never stores prompts, model responses,
credentials, or source contents. Local workers are protected by the canonical
lease and are blocked while a configured game process or a manual blocker is
active. Cloud workers remain available while local compute is unavailable.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import time
from typing import Any, Callable, Optional, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parent))
import local_model_lease as lease


WORKSPACE_ROOT = Path(r"C:\GIT") if os.name == "nt" else Path.home() / "c-git"
DEFAULT_POLICY_PATH = WORKSPACE_ROOT / ".memory" / "ai-runtime-policy.json"
DEFAULT_STATE_DIR = WORKSPACE_ROOT / ".runtime" / "ai-runtime"
DEFAULT_OPENCODE_CONFIG = Path.home() / ".config" / "opencode" / "opencode.json"
BLOCKERS_FILENAME = "blockers.json"
LEDGER_FILENAME = "ledger.sqlite3"


class RuntimeErrorBase(RuntimeError):
    """Base class for control-plane failures."""


class LocalRuntimeBlockedError(RuntimeErrorBase):
    """Raised before a local worker starts while a blocker is active."""


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default
    except json.JSONDecodeError as exc:
        raise RuntimeErrorBase(f"invalid JSON in {path}: {exc}") from exc


def _atomic_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_policy(path: Path) -> dict[str, Any]:
    policy = _read_json(path, None)
    if not isinstance(policy, dict):
        raise RuntimeErrorBase(f"policy must be a JSON object: {path}")
    context = policy.get("context")
    local = policy.get("local")
    routing = policy.get("routing")
    if not isinstance(context, dict) or not isinstance(local, dict) or not isinstance(routing, dict):
        raise RuntimeErrorBase("policy requires context, local, and routing objects")
    for field in ("target_input_tokens", "warn_input_tokens", "new_session_input_tokens", "max_output_tokens"):
        value = context.get(field)
        if not isinstance(value, int) or value <= 0:
            raise RuntimeErrorBase(f"context.{field} must be a positive integer")
    if not (
        context["target_input_tokens"]
        < context["warn_input_tokens"]
        < context["new_session_input_tokens"]
    ):
        raise RuntimeErrorBase("context thresholds must increase from target through new-session")
    processes = local.get("game_processes")
    if not isinstance(processes, list) or not all(isinstance(value, str) and value for value in processes):
        raise RuntimeErrorBase("local.game_processes must be a non-empty list of executable names")
    return policy


def _running_process_names() -> set[str]:
    if os.name != "nt":
        return set()
    completed = subprocess.run(
        ["tasklist", "/FO", "CSV", "/NH"],
        capture_output=True,
        text=True,
        check=False,
        encoding="utf-8",
        errors="replace",
    )
    if completed.returncode != 0:
        raise RuntimeErrorBase(f"tasklist failed with exit code {completed.returncode}")
    names: set[str] = set()
    for line in completed.stdout.splitlines():
        if not line.startswith('"'):
            continue
        name = line.split('","', 1)[0].strip('"').casefold()
        if name:
            names.add(name)
    return names


def blocker_path(state_dir: Path) -> Path:
    return state_dir / BLOCKERS_FILENAME


def active_blockers(
    policy: dict[str, Any],
    state_dir: Path,
    process_names: Callable[[], set[str]] = _running_process_names,
) -> list[str]:
    stored = _read_json(blocker_path(state_dir), {"manual": []})
    if not isinstance(stored, dict) or not isinstance(stored.get("manual", []), list):
        raise RuntimeErrorBase(f"invalid blocker state: {blocker_path(state_dir)}")
    reasons = [
        f"manual:{entry}"
        for entry in stored["manual"]
        if isinstance(entry, str) and entry.strip()
    ]
    active_processes = process_names()
    games = {
        process.casefold()
        for process in policy["local"]["game_processes"]
        if process.casefold() in active_processes
    }
    reasons.extend(f"game:{process}" for process in sorted(games))
    return reasons


def local_block_reason(
    policy: dict[str, Any],
    state_dir: Path,
    process_names: Callable[[], set[str]] = _running_process_names,
) -> Optional[str]:
    blockers = active_blockers(policy, state_dir, process_names)
    return "; ".join(blockers) if blockers else None


def set_manual_blocker(state_dir: Path, reason: str) -> None:
    clean_reason = reason.strip()
    if not clean_reason:
        raise RuntimeErrorBase("blocker reason must not be empty")
    path = blocker_path(state_dir)
    stored = _read_json(path, {"manual": []})
    manual = stored.get("manual", []) if isinstance(stored, dict) else []
    if not isinstance(manual, list):
        raise RuntimeErrorBase(f"invalid blocker state: {path}")
    _atomic_json(path, {"manual": sorted({*manual, clean_reason})})


def clear_manual_blocker(state_dir: Path, reason: str) -> None:
    path = blocker_path(state_dir)
    stored = _read_json(path, {"manual": []})
    manual = stored.get("manual", []) if isinstance(stored, dict) else []
    if not isinstance(manual, list):
        raise RuntimeErrorBase(f"invalid blocker state: {path}")
    _atomic_json(path, {"manual": [entry for entry in manual if entry != reason]})


def initialize_ledger(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS runtime_events (
                id INTEGER PRIMARY KEY,
                created_at TEXT NOT NULL,
                event TEXT NOT NULL,
                runtime TEXT NOT NULL,
                provider TEXT NOT NULL,
                model TEXT NOT NULL,
                session_id TEXT,
                phase TEXT,
                input_tokens INTEGER,
                output_tokens INTEGER,
                cache_read_tokens INTEGER,
                cost REAL,
                detail TEXT
            )
            """
        )
        connection.commit()
    finally:
        connection.close()


def record_event(
    state_dir: Path,
    *,
    event: str,
    runtime: str,
    provider: str,
    model: str,
    session_id: str | None = None,
    phase: str | None = None,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
    cache_read_tokens: int | None = None,
    cost: float | None = None,
    detail: str | None = None,
) -> None:
    ledger = state_dir / LEDGER_FILENAME
    initialize_ledger(ledger)
    connection = sqlite3.connect(ledger)
    try:
        connection.execute(
            """
            INSERT INTO runtime_events (
                created_at, event, runtime, provider, model, session_id, phase,
                input_tokens, output_tokens, cache_read_tokens, cost, detail
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                utc_now(),
                event,
                runtime,
                provider,
                model,
                session_id,
                phase,
                input_tokens,
                output_tokens,
                cache_read_tokens,
                cost,
                detail,
            ),
        )
        connection.commit()
    finally:
        connection.close()


def cap_opencode_config(path: Path, policy: dict[str, Any]) -> bool:
    """Limit OpenCode's declared operating windows without touching credentials."""
    original = path.read_bytes()
    config = json.loads(original.decode("utf-8-sig"))
    if not isinstance(config, dict):
        raise RuntimeErrorBase(f"OpenCode config root must be an object: {path}")
    providers = config.get("provider")
    if not isinstance(providers, dict):
        raise RuntimeErrorBase(f"OpenCode config has no provider object: {path}")
    max_context = policy["context"]["new_session_input_tokens"]
    max_output = policy["context"]["max_output_tokens"]
    for provider in providers.values():
        if not isinstance(provider, dict):
            continue
        models = provider.get("models")
        if not isinstance(models, dict):
            continue
        for definition in models.values():
            if not isinstance(definition, dict):
                continue
            limits = definition.setdefault("limit", {})
            if not isinstance(limits, dict):
                raise RuntimeErrorBase("OpenCode model limit must be an object")
            configured_context = limits.get("context", max_context)
            configured_output = limits.get("output", max_output)
            if not isinstance(configured_context, int) or configured_context <= 0:
                raise RuntimeErrorBase("OpenCode model context limit must be a positive integer")
            if not isinstance(configured_output, int) or configured_output <= 0:
                raise RuntimeErrorBase("OpenCode model output limit must be a positive integer")
            limits["context"] = min(configured_context, max_context)
            limits["output"] = min(configured_output, max_output)
    updated = (json.dumps(config, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    if updated == original:
        return False
    backup = path.with_name(f"{path.name}.runtime-guard.bak")
    if not backup.exists():
        backup.write_bytes(original)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_bytes(updated)
    temporary.replace(path)
    return True


def projected_context(policy: dict[str, Any], input_tokens: int, output_tokens: int) -> str:
    if input_tokens < 0 or output_tokens < 0:
        raise RuntimeErrorBase("token counts must not be negative")
    total = input_tokens + output_tokens
    limits = policy["context"]
    if total >= limits["new_session_input_tokens"]:
        return "block"
    if total >= limits["warn_input_tokens"]:
        return "warn"
    return "allow"


def unload_ollama(model: str) -> None:
    request = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import json, urllib.request; "
                f"data=json.dumps({{'model': {model!r}, 'keep_alive': 0, 'prompt': '', 'stream': False}}).encode(); "
                "req=urllib.request.Request('http://127.0.0.1:11434/api/generate', data=data, "
                "headers={'Content-Type':'application/json'}); "
                "urllib.request.urlopen(req, timeout=10).read()"
            ),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if request.returncode != 0:
        raise RuntimeErrorBase(f"could not unload Ollama model {model}: {request.stderr.strip()}")


def run_local_worker(
    policy: dict[str, Any],
    state_dir: Path,
    *,
    provider: str,
    model: str,
    owner: str,
    command: Sequence[str],
    poll_seconds: float,
) -> int:
    if not command:
        raise RuntimeErrorBase("run requires a command after --")
    reason = local_block_reason(policy, state_dir)
    if reason:
        raise LocalRuntimeBlockedError(reason)
    manager = lease.LeaseManager(
        availability_check=lambda: local_block_reason(policy, state_dir)
    )
    workload = f"{provider}/{model}"
    metadata = manager.acquire("local-llm", owner, workload)
    process: subprocess.Popen[str] | None = None
    stopped_for_game = False
    try:
        record_event(
            state_dir, event="started", runtime="wrapper", provider=provider, model=model, detail=metadata.lease_id
        )
        process = subprocess.Popen(list(command))
        while process.poll() is None:
            reason = local_block_reason(policy, state_dir)
            if reason:
                stopped_for_game = True
                process.terminate()
                break
            time.sleep(max(0.2, poll_seconds))
        exit_code = process.wait()
        if stopped_for_game:
            if provider == "ollama":
                unload_ollama(model)
            record_event(
                state_dir, event="stopped_by_blocker", runtime="wrapper", provider=provider, model=model, detail=reason
            )
            return 75
        record_event(state_dir, event="finished", runtime="wrapper", provider=provider, model=model)
        return exit_code
    finally:
        with contextlib.suppress(lease.LeaseOwnershipError):
            manager.release("local-llm", metadata.lease_id)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH)
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE_DIR)
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser("status", help="Show current routing and local resource state.")
    status.add_argument("--input-tokens", type=int, default=0)
    status.add_argument("--output-tokens", type=int, default=0)

    block = subparsers.add_parser("block", help="Persist a manual local-model blocker.")
    block.add_argument("--reason", required=True)
    unblock = subparsers.add_parser("unblock", help="Remove one manual local-model blocker.")
    unblock.add_argument("--reason", required=True)

    cap = subparsers.add_parser(
        "cap-opencode-config",
        help="Cap configured OpenCode model windows to the runtime policy.",
    )
    cap.add_argument("--config", type=Path, default=DEFAULT_OPENCODE_CONFIG)

    usage = subparsers.add_parser("usage-record", help="Record provider-reported metadata only.")
    usage.add_argument("--runtime", required=True)
    usage.add_argument("--provider", required=True)
    usage.add_argument("--model", required=True)
    usage.add_argument("--session-id")
    usage.add_argument("--phase")
    usage.add_argument("--input-tokens", type=int)
    usage.add_argument("--output-tokens", type=int)
    usage.add_argument("--cache-read-tokens", type=int)
    usage.add_argument("--cost", type=float)

    run = subparsers.add_parser("run", help="Run one local worker under lease and game protection.")
    run.add_argument("--provider", required=True, choices=("ollama", "llama-cpp"))
    run.add_argument("--model", required=True)
    run.add_argument("--owner", required=True)
    run.add_argument("--poll-seconds", type=float, default=2.0)
    run.add_argument("worker_command", nargs=argparse.REMAINDER)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    policy = load_policy(args.policy)
    if args.command == "status":
        input_tokens = args.input_tokens
        output_tokens = args.output_tokens
        print(
            json.dumps(
                {
                    "context_action": projected_context(policy, input_tokens, output_tokens),
                    "local_blockers": active_blockers(policy, args.state_dir),
                    "routing": policy["routing"],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "block":
        set_manual_blocker(args.state_dir, args.reason)
        return 0
    if args.command == "unblock":
        clear_manual_blocker(args.state_dir, args.reason)
        return 0
    if args.command == "cap-opencode-config":
        print(json.dumps({"updated": cap_opencode_config(args.config, policy)}))
        return 0
    if args.command == "usage-record":
        action = projected_context(policy, args.input_tokens or 0, args.output_tokens or 0)
        if action == "block":
            raise RuntimeErrorBase("new session required before recording another request")
        record_event(
            args.state_dir,
            event="usage",
            runtime=args.runtime,
            provider=args.provider,
            model=args.model,
            session_id=args.session_id,
            phase=args.phase,
            input_tokens=args.input_tokens,
            output_tokens=args.output_tokens,
            cache_read_tokens=args.cache_read_tokens,
            cost=args.cost,
        )
        print(json.dumps({"context_action": action}))
        return 0
    if args.command == "run":
        command = list(args.worker_command)
        if command[:1] == ["--"]:
            command.pop(0)
        return run_local_worker(
            policy,
            args.state_dir,
            provider=args.provider,
            model=args.model,
            owner=args.owner,
            command=command,
            poll_seconds=args.poll_seconds,
        )
    raise AssertionError(f"unknown command {args.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeErrorBase, lease.LeaseError, OSError, ValueError) as error:
        print(f"AI RUNTIME ERROR: {error}", file=sys.stderr)
        raise SystemExit(3)
