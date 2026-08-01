"""Archive native AI sessions and publish searchable, sanitized WHY summaries."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from settings import load_settings


SAFE_ID = re.compile(r"^[A-Za-z0-9._-]+$")
SECRET_PATTERNS = (
    (
        "private-key",
        re.compile(
            r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?"
            r"-----END [A-Z0-9 ]*PRIVATE KEY-----",
            re.DOTALL,
        ),
    ),
    (
        "known-token",
        re.compile(
            r"\b(?:github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9_]{20,}|"
            r"glpat-[A-Za-z0-9_-]{16,})\b"
        ),
    ),
    (
        "bearer-token",
        re.compile(r"(?i)(\bBearer\s+)[A-Za-z0-9._~+/=-]{16,}"),
    ),
    (
        "named-secret",
        re.compile(
            r"""(?ix)
            (
              ["']?
              (?:password|passwd|access[_-]?token|refresh[_-]?token|
                 api[_-]?(?:token|key)|client[_-]?secret|private[_-]?key|
                 authorization)
              ["']?\s*[:=]\s*["']?
            )
            ([^"'\s,}\]]{6,})
            """
        ),
    ),
    (
        "url-credentials",
        re.compile(r"(?i)(https?://[^/\s:@]+:)[^@\s/]+(@)"),
    ),
)


@dataclass(frozen=True)
class SessionSnapshot:
    payload: bytes
    extension: str
    agent: str
    model: str
    source_location: str


def workspace_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    return Path(__file__).resolve().parents[2]


def validate_identifier(value: str, label: str) -> str:
    if value in {".", ".."} or not SAFE_ID.fullmatch(value):
        raise ValueError(f"Invalid {label}: {value!r}")
    return value


def filename_component(value: str, fallback: str) -> str:
    component = re.sub(r"[^a-z0-9.-]+", "-", value.lower()).strip("-.")
    return component or fallback


def topic_component(value: str | None, allow_pending: bool) -> str:
    topic = filename_component(value or "", "topic-pending" if allow_pending else "")
    if not topic:
        raise ValueError("A meaningful topic is required")
    if len(topic) > 30:
        raise ValueError(f"Topic exceeds 30 characters after normalization: {topic}")
    return topic


def artifact_numbers(directory: Path) -> list[int]:
    numbers: list[int] = []
    current = re.compile(r"^(\d+)(?:-\d+)?__")
    legacy = re.compile(r"^(?:raw|sanitized)-(\d+)[_-]")
    if directory.is_dir():
        for path in directory.iterdir():
            match = current.match(path.name) or legacy.match(path.name)
            if match:
                numbers.append(int(match.group(1)))
    return numbers


def resolve_chat_number(
    root: Path,
    settings: dict[str, object],
    requested: int | None,
    session_id: str | None = None,
    source: str | None = None,
) -> int:
    if requested is not None:
        if requested < 1:
            raise ValueError("Chat number must be greater than zero")
        return requested
    private = root / str(settings["chat_private_dir"])
    if session_id and source and private.is_dir():
        pattern = re.compile(r"^(\d+)-\d+__original-")
        for path in private.iterdir():
            match = pattern.match(path.name)
            if match and archived_session_id(path, source) == session_id:
                return int(match.group(1))
    directories = (
        private,
        root / str(settings["chat_shared_dir"]),
    )
    numbers = [number for directory in directories for number in artifact_numbers(directory)]
    return max(numbers, default=0) + 1


def next_snapshot_revision(directory: Path, chat_number: int) -> int:
    pattern = re.compile(rf"^{chat_number:03d}-(\d+)__original-")
    revisions = [
        int(match.group(1))
        for path in directory.iterdir()
        if (match := pattern.match(path.name))
    ]
    return max(revisions, default=0) + 1


def archived_session_id(path: Path, source: str) -> str | None:
    try:
        if source == "copilot" and path.suffix.lower() == ".jsonl":
            for line in path.read_text(encoding="utf-8").splitlines():
                event = json.loads(line)
                if event.get("type") == "session.start":
                    return str((event.get("data") or {}).get("sessionId") or "") or None
        if source == "opencode" and path.suffix.lower() == ".json":
            document = json.loads(path.read_text(encoding="utf-8"))
            return str((document.get("info") or {}).get("id") or "") or None
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return None


def load_copilot(session_id: str, home: Path | None = None) -> SessionSnapshot:
    base = home or Path(os.environ.get("COPILOT_HOME", Path.home() / ".copilot"))
    source = base / "session-state" / session_id / "events.jsonl"
    if not source.is_file():
        raise FileNotFoundError(
            f"Copilot events not found: {source}. Export the session to a file and use --input instead."
        )

    payload = source.read_bytes()
    version = "unknown"
    models: list[str] = []
    for line in payload.decode("utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        data = event.get("data") or {}
        if event.get("type") == "session.start":
            version = str(data.get("copilotVersion") or version)
            selected_model = str(data.get("selectedModel") or "")
            if selected_model and selected_model != "auto" and selected_model not in models:
                models.append(selected_model)
        if event.get("type") == "session.model_change":
            model = str(data.get("newModel") or "")
            if model and model not in models:
                models.append(model)

    return SessionSnapshot(
        payload=payload,
        extension="jsonl",
        agent=f"GitHub Copilot CLI {version}",
        model=" and ".join(models) or "unknown",
        source_location=str(source),
    )


def load_opencode(
    session_id: str,
    runner: Callable[..., subprocess.CompletedProcess[bytes]] = subprocess.run,
) -> SessionSnapshot:
    executable = shutil.which("opencode")
    if not executable:
        raise FileNotFoundError("OpenCode executable not found")
    result = runner(
        [executable, "export", session_id],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        error = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"OpenCode export failed: {error}")
    payload = result.stdout
    document = json.loads(payload)
    info = document["info"]
    model_info = info.get("model") or {}
    model = "/".join(
        part
        for part in (
            str(model_info.get("providerID") or ""),
            str(model_info.get("modelID") or model_info.get("id") or ""),
        )
        if part
    )
    return SessionSnapshot(
        payload=payload,
        extension="json",
        agent=f"OpenCode {info.get('version', 'unknown')}",
        model=model or "unknown",
        source_location="OpenCode native session database",
    )


def load_input(path: Path, source: str) -> SessionSnapshot:
    payload = path.read_bytes()
    return SessionSnapshot(
        payload=payload,
        extension=path.suffix.lstrip(".") or "log",
        agent=source,
        model="unknown",
        source_location=str(path.resolve()),
    )


def redact_secrets(text: str, extra_patterns: list[str] | None = None) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    result = text
    for name, pattern in SECRET_PATTERNS:
        if name == "bearer-token":
            result, count = pattern.subn(r"\1[REDACTED-SECRET]", result)
        elif name == "named-secret":
            result, count = pattern.subn(r"\1[REDACTED-SECRET]", result)
        elif name == "url-credentials":
            result, count = pattern.subn(r"\1[REDACTED-SECRET]\2", result)
        else:
            result, count = pattern.subn("[REDACTED-SECRET]", result)
        if count:
            counts[name] = count
    for index, expression in enumerate(extra_patterns or (), start=1):
        result, count = re.compile(expression).subn("[REDACTED-SECRET]", result)
        if count:
            counts[f"custom-{index}"] = count
    return result, counts


def private_directory(root: Path, settings: dict[str, object]) -> Path:
    return root / str(settings["chat_private_dir"])


def archive(
    root: Path,
    settings: dict[str, object],
    source: str,
    session_id: str,
    snapshot: SessionSnapshot,
    chat_logging: str,
    sensitive_data_policy: str,
    secret_handling: str,
    chat_number: int | None = None,
    topic: str | None = None,
    extra_patterns: list[str] | None = None,
) -> tuple[Path, bool, int]:
    if chat_logging != "transcript":
        raise ValueError("Private archive requires effective AI-CHAT-LOGGING: transcript")
    if sensitive_data_policy not in {"all", "only_at_user_memory"}:
        raise ValueError("Userdata policy does not allow a private transcript in user-memory")
    if secret_handling == "preserve":
        if extra_patterns:
            raise ValueError("Extra secret regexes conflict with transcript_secret_handling: preserve")
        archived = snapshot.payload
    elif secret_handling == "redact":
        clean_text, _ = redact_secrets(snapshot.payload.decode("utf-8"), extra_patterns)
        archived = clean_text.encode("utf-8")
    else:
        raise ValueError(f"Unsupported transcript secret handling: {secret_handling}")
    directory = private_directory(root, settings)
    directory.mkdir(parents=True, exist_ok=True)
    number = resolve_chat_number(root, settings, chat_number, session_id, source)
    existing_pattern = f"{number:03d}-*__original-*"
    for existing in sorted(directory.glob(existing_pattern)):
        if source in {"copilot", "opencode"} and archived_session_id(existing, source) != session_id:
            raise ValueError(f"Chat number {number:03d} belongs to another native session")
        if existing.read_bytes() == archived:
            return existing, False, number

    revision = next_snapshot_revision(directory, number)
    agent_name = filename_component(snapshot.agent, "unknown-agent")
    model_name = filename_component(snapshot.model, "unknown-model")
    topic_name = topic_component(topic, allow_pending=True)
    filename = (
        f"{number:03d}-{revision:02d}__original-restricted__{agent_name}__"
        f"{model_name}__{topic_name}.{snapshot.extension}"
    )
    destination = directory / filename

    temporary = destination.with_name(destination.name + ".tmp")
    temporary.write_bytes(archived)
    temporary.replace(destination)
    return destination, True, number


def shared_summary(
    root: Path,
    settings: dict[str, object],
    chat_number: int,
    topic: str,
    title: str,
    body_path: Path,
    agent: str,
    model: str,
    classification: str,
    confirm_sanitized: bool,
) -> tuple[Path, bool]:
    if not confirm_sanitized:
        raise ValueError("--confirm-sanitized is required after reviewing the neutral summary")
    if chat_number < 1:
        raise ValueError("Chat number must be greater than zero")
    body = body_path.read_text(encoding="utf-8").strip()
    _, secret_counts = redact_secrets(body)
    if secret_counts or "[REDACTED-SECRET]" in body:
        raise ValueError("Shared summary still contains a secret marker or detected secret")
    if not body:
        raise ValueError("Shared summary body is empty")

    directory = root / str(settings["chat_shared_dir"])
    directory.mkdir(parents=True, exist_ok=True)
    policy = summary_classification_policy(directory, root)
    allowed = {"public"} if policy == "public" else {"public", "internal"}
    if classification not in allowed:
        raise ValueError(
            f"Summary classification {classification!r} is not allowed by {policy!r} target policy"
        )
    agent_name = filename_component(agent, "unknown-agent")
    model_name = filename_component(model, "unknown-model")
    topic_name = topic_component(topic, allow_pending=False)
    content = (
        "---\n"
        f"title: {json.dumps(title, ensure_ascii=False)}\n"
        "doc_type: conversation-summary\n"
        "status: accepted\n"
        f"classification: {classification}\n"
        f"chat_number: {chat_number:03d}\n"
        f"agent: {json.dumps(agent, ensure_ascii=False)}\n"
        f"model: {json.dumps(model, ensure_ascii=False)}\n"
        "---\n\n"
        f"# {title}\n\n{body}\n"
    )
    target = directory / (
        f"{chat_number:03d}__ai-summary-{classification}__{agent_name}__"
        f"{model_name}__{topic_name}.md"
    )
    if target.exists() and target.read_text(encoding="utf-8") == content:
        return target, False
    temporary = target.with_name(target.name + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(target)
    return target, True


def summary_classification_policy(directory: Path, root: Path) -> str:
    current = directory
    while current == root or root in current.parents:
        router = current / "AGENTS.md"
        if router.is_file():
            match = re.search(
                r"\*\*DATA-CLASSIFICATION:\*\*\s*(public|internal|confidential|restricted)",
                router.read_text(encoding="utf-8"),
                re.IGNORECASE,
            )
            if match:
                policy = match.group(1).lower()
                if policy not in {"public", "internal"}:
                    raise ValueError(
                        f"Central summary target does not allow shared classifications: {policy}"
                    )
                return policy
        if current == root:
            break
        current = current.parent
    return "public"


def snapshot_from_args(args: argparse.Namespace) -> SessionSnapshot:
    validate_identifier(args.session_id, "session ID")
    if args.input:
        return load_input(Path(args.input), args.source)
    if args.source == "copilot":
        return load_copilot(args.session_id)
    if args.source == "opencode":
        return load_opencode(args.session_id)
    raise ValueError(f"--input is required for source {args.source!r}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", help="Workspace root; defaults to C:\\GIT")
    parser.add_argument("--user", help="User override directory below user-memory")
    subparsers = parser.add_subparsers(dest="command", required=True)

    archive_parser = subparsers.add_parser("archive", help="Archive a native session privately")
    archive_parser.add_argument("--source", required=True, choices=("copilot", "opencode", "other"))
    archive_parser.add_argument("--session-id", required=True)
    archive_parser.add_argument("--chat-number", type=int)
    archive_parser.add_argument("--input", help="Explicit native export path")
    archive_parser.add_argument(
        "--topic",
        help="Known session topic; defaults to topic-pending and may evolve in later snapshots",
    )
    archive_parser.add_argument(
        "--extra-secret-regex",
        action="append",
        default=[],
        help="Additional secret pattern to redact; may be repeated",
    )
    archive_parser.add_argument(
        "--chat-logging",
        choices=("off", "summary", "transcript"),
        help="Effective scoped policy; defaults to the workspace setting",
    )
    archive_parser.add_argument(
        "--secret-handling",
        choices=("redact", "preserve"),
        help="Effective user choice; defaults to merged user/workspace settings",
    )

    summary_parser = subparsers.add_parser(
        "publish-summary", help="Publish a reviewed neutral WHY summary centrally"
    )
    summary_parser.add_argument("--chat-number", type=int, required=True)
    summary_parser.add_argument("--topic", required=True)
    summary_parser.add_argument("--title", required=True)
    summary_parser.add_argument("--summary", required=True, help="Reviewed Markdown body")
    summary_parser.add_argument("--agent", required=True, help="Agent/tool that wrote the summary")
    summary_parser.add_argument("--model", required=True, help="Exact LLM model ID")
    summary_parser.add_argument(
        "--classification",
        choices=("public", "internal"),
        default="public",
        help="Allowed central summary class; current standards/why policy may be stricter",
    )
    summary_parser.add_argument("--confirm-sanitized", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = workspace_root(args.workspace)
    settings = load_settings(root, args.user)

    if args.command == "archive":
        snapshot = snapshot_from_args(args)
        destination, changed, chat_number = archive(
            root,
            settings,
            args.source,
            args.session_id,
            snapshot,
            args.chat_logging or str(settings["default_ai_chat_logging"]),
            str(settings["store_user_sensitive_data"]),
            args.secret_handling or str(settings["transcript_secret_handling"]),
            args.chat_number,
            args.topic,
            args.extra_secret_regex,
        )
        print(f"status={'created' if changed else 'current'}")
        print(f"chat_number={chat_number:03d}")
        print(f"raw={destination}")
        return 0

    target, changed = shared_summary(
        root,
        settings,
        args.chat_number,
        args.topic,
        args.title,
        Path(args.summary),
        args.agent,
        args.model,
        args.classification,
        args.confirm_sanitized,
    )
    relative = target.relative_to(root).as_posix()
    print(f"status={'created' if changed else 'current'}")
    print(f"chat_number={args.chat_number:03d}")
    print(f"why-ref: {relative}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, FileExistsError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
