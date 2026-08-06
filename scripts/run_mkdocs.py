"""Run MkDocs after resolving portable engineering-workspace placeholders."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Sequence


VARIABLES = (
    "ENGINEERING_REPOS_ROOT",
    "ENGINEERING_GOVERNANCE_ROOT",
)


def resolve_placeholders(content: str, environment: dict[str, str]) -> str:
    resolved = content
    for name in VARIABLES:
        placeholder = "${" + name + "}"
        if placeholder not in resolved:
            continue
        value = environment.get(name)
        if not value:
            raise ValueError(f"{name} is required by the MkDocs configuration")
        resolved = resolved.replace(placeholder, Path(value).as_posix())
    return resolved


def extract_config(arguments: Sequence[str], cwd: Path) -> tuple[Path, list[str]]:
    remaining: list[str] = []
    config = cwd / "mkdocs.yml"
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        if argument in {"-f", "--config-file"}:
            if index + 1 >= len(arguments):
                raise ValueError(f"{argument} requires a path")
            config = Path(arguments[index + 1])
            index += 2
            continue
        if argument.startswith("--config-file="):
            config = Path(argument.split("=", 1)[1])
            index += 1
            continue
        remaining.append(argument)
        index += 1
    if not config.is_absolute():
        config = cwd / config
    return config, remaining


def main(arguments: Sequence[str] | None = None) -> int:
    args = list(arguments if arguments is not None else sys.argv[1:])
    cwd = Path.cwd()
    config, mkdocs_args = extract_config(args, cwd)
    if not config.is_file():
        raise FileNotFoundError(f"MkDocs configuration not found: {config}")

    content = config.read_text(encoding="utf-8")
    resolved = resolve_placeholders(content, dict(os.environ))
    temporary: Path | None = None
    selected = config
    if resolved != content:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".yml",
            prefix=".engws-mkdocs-",
            dir=config.parent,
            delete=False,
        ) as stream:
            stream.write(resolved)
            temporary = Path(stream.name)
        selected = temporary

    try:
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "mkdocs",
                *mkdocs_args,
                "--config-file",
                str(selected),
            ],
            cwd=config.parent,
            check=False,
        )
        return completed.returncode
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
