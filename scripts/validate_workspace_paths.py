"""Find non-portable workspace paths in active Markdown and configuration files."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys
from typing import Iterable


SCANNED_SUFFIXES = {
    ".bat",
    ".cfg",
    ".cmd",
    ".conf",
    ".ini",
    ".json",
    ".jsonc",
    ".md",
    ".mdx",
    ".ps1",
    ".psm1",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
SKIPPED_DIRECTORIES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".venv",
    ".vs",
    ".workflow",
    "__pycache__",
    "benchmark_results",
    "bin",
    "build",
    "dist",
    "node_modules",
    "obj",
    "site",
    "venv",
    "vscode-chat-backup",
}
PATTERNS = (
    re.compile(r"(?i)\b[a-z]:[\\/]GIT\b|/mnt/[a-z]/git\b"),
    re.compile(r"(?i)\.\.[\\/]+standards[\\/]"),
    re.compile(r"(?i)\bstandards[\\/](?:AGENTS\.md|docs|scripts|settings|why)"),
)


def is_historical(relative: Path) -> bool:
    parts = tuple(part.lower() for part in relative.parts)
    if "llm-benchmarks" in parts or "agent-memory" in parts:
        return True
    if ".chat" in parts or ".workflow" in parts or "benchmarks" in parts:
        return True
    if "why" in parts and "conversations" in parts:
        return True
    if relative.name.lower() in {"changelog.md", "session-log.md"}:
        return True
    if parts[:2] == (".memory", "decisions.md"):
        return True
    if parts[:2] == (".memory", "workspace-layout-proposal.md"):
        return True
    if "standards" in parts and "engineering-governance" not in parts:
        return True
    if "scripts" in parts and "docs" in parts and "project" in parts:
        return True
    if relative.as_posix().endswith(
        "engineering-governance/scripts/test_validate_workspace_paths.py"
    ):
        return True
    return False


def iter_files(root: Path) -> Iterable[Path]:
    for directory, names, files in os.walk(root):
        names[:] = [name for name in names if name not in SKIPPED_DIRECTORIES]
        base = Path(directory)
        for name in files:
            path = base / name
            if path.suffix.lower() in SCANNED_SUFFIXES:
                yield path


def has_local_standards(path: Path, root: Path) -> bool:
    for parent in path.parents:
        if parent == root:
            return False
        if (parent / "standards").is_dir():
            return True
    return False


def has_nonportable_reference(line: str, path: Path, root: Path) -> bool:
    if PATTERNS[0].search(line) or PATTERNS[1].search(line):
        return True
    return bool(PATTERNS[2].search(line) and not has_local_standards(path, root))


def findings(root: Path) -> tuple[list[str], list[str]]:
    active: list[str] = []
    historical: list[str] = []
    for path in iter_files(root):
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as error:
            active.append(f"{path}: unreadable: {error}")
            continue
        relative = path.relative_to(root)
        target = historical if is_historical(relative) else active
        for line_number, line in enumerate(lines, 1):
            if has_nonportable_reference(line, path, root):
                preview = line.strip()
                if len(preview) > 300:
                    preview = preview[:297] + "..."
                target.append(f"{relative}:{line_number}: {preview}")
    return active, historical


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=os.environ.get("ENGINEERING_REPOS_ROOT"),
        help="Repository root; defaults to ENGINEERING_REPOS_ROOT",
    )
    parser.add_argument("--show-historical", action="store_true")
    args = parser.parse_args()
    if args.root is None:
        parser.error("--root or ENGINEERING_REPOS_ROOT is required")
    root = args.root.absolute()
    active, historical = findings(root)
    for item in active:
        print(f"ACTIVE: {item}")
    if args.show_historical:
        for item in historical:
            print(f"HISTORICAL: {item}")
    print(f"active={len(active)} historical={len(historical)}")
    return 1 if active else 0


if __name__ == "__main__":
    raise SystemExit(main())
