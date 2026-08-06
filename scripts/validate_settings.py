"""Validate the hierarchical workspace settings."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from settings import (
    GOVERNANCE_ROOT_ENV,
    REPOS_ROOT_ENV,
    find_governance_root,
    find_workspace_root,
    load_settings,
    read_settings,
    validate_settings_data,
)


def main() -> int:
    start = Path(__file__).resolve().parent
    governance = find_governance_root(start)
    if governance is None:
        print(f"ERROR: {GOVERNANCE_ROOT_ENV} is unset and governance was not found", file=sys.stderr)
        return 1
    workspace = find_workspace_root(start)
    if workspace is None:
        print(f"ERROR: {REPOS_ROOT_ENV} is unset and workspace was not found", file=sys.stderr)
        return 1

    defaults_path = governance / "settings.yml"
    schema_path = governance / "settings.schema.json"
    settings = read_settings(defaults_path)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = validate_settings_data(settings, schema, complete=True)
    for memory_setting in ("load_user_memory", "load_agent_memory"):
        if settings.get(memory_setting) is not False:
            errors.append(f"$.{memory_setting}: base default must be false")

    override_paths = [workspace / "user-memory" / "settings.yml"]
    override_paths.extend(sorted((workspace / "user-memory").glob("*/settings.yml")))
    for override_path in override_paths:
        if not override_path.is_file():
            continue
        override_settings = read_settings(override_path)
        errors.extend(
            f"{override_path}: {error}"
            for error in validate_settings_data(override_settings, schema)
        )

    try:
        load_settings(workspace, user="", governance_root=governance)
        for user_path in sorted((workspace / "user-memory").glob("*/settings.yml")):
            load_settings(workspace, user_path.parent.name, governance_root=governance)
    except (FileNotFoundError, ValueError) as error:
        errors.append(str(error))

    policy_names = {
        "AI-" + key.removeprefix("default_ai_").replace("_", "-").upper()
        for key in settings
        if key.startswith("default_ai_")
    }
    if "default_data_classification" in settings:
        policy_names.add("DATA-CLASSIFICATION")

    root_router = (workspace / "AGENTS.md").read_text(encoding="utf-8")
    governance_router = (governance / "AGENTS.md").read_text(encoding="utf-8")
    template = (governance / "docs" / "templates" / "agents-template.md").read_text(
        encoding="utf-8"
    )
    for policy in sorted(policy_names):
        if f"`{policy}`" not in governance_router:
            errors.append(f"$.{policy}: missing semantics in governance AGENTS.md")
        if f"**{policy}:**" not in template:
            errors.append(f"$.{policy}: missing from AGENTS template")
    for memory_setting in ("load_user_memory", "load_agent_memory"):
        if f"`{memory_setting}`" not in governance_router:
            errors.append(f"$.{memory_setting}: missing semantics in governance AGENTS.md")
    for variable in (REPOS_ROOT_ENV, GOVERNANCE_ROOT_ENV):
        if variable not in root_router:
            errors.append(f"$.{variable}: missing from workspace router")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"OK: {defaults_path} + inherited user settings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
