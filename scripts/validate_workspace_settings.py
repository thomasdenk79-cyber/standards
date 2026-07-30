"""Validate workspace-settings.yml against its local JSON Schema subset."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


def find_workspace_root(start: Path) -> Path | None:
    for directory in (start, *start.parents):
        if (directory / "workspace-settings.yml").exists():
            return directory
    return None


def resolve(schema: dict[str, Any], root: dict[str, Any]) -> dict[str, Any]:
    reference = schema.get("$ref")
    if not reference:
        return schema
    if not reference.startswith("#/$defs/"):
        raise ValueError(f"Unsupported schema reference: {reference}")
    return root["$defs"][reference.removeprefix("#/$defs/")]


def validate(value: Any, schema: dict[str, Any], root: dict[str, Any], path: str = "$") -> list[str]:
    schema = resolve(schema, root)
    errors: list[str] = []

    expected_type = schema.get("type")
    if expected_type == "object":
        if not isinstance(value, dict):
            return [f"{path}: expected object"]
        required = schema.get("required", [])
        errors.extend(f"{path}.{key}: missing required setting" for key in required if key not in value)
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            errors.extend(f"{path}.{key}: unknown setting" for key in value if key not in properties)
        for key, item in value.items():
            if key in properties:
                errors.extend(validate(item, properties[key], root, f"{path}.{key}"))
        return errors

    if expected_type == "string" and not isinstance(value, str):
        return [f"{path}: expected string"]
    if expected_type == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
        return [f"{path}: expected integer"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected {schema['const']!r}, got {value!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} is not one of {schema['enum']}")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: value is too short")
        if pattern := schema.get("pattern"):
            if re.fullmatch(pattern, value) is None:
                errors.append(f"{path}: {value!r} does not match {pattern!r}")
    return errors


def main() -> int:
    workspace = find_workspace_root(Path(__file__).resolve().parent)
    if workspace is None:
        print("SKIP: workspace-settings.yml not found")
        return 0

    settings = yaml.safe_load((workspace / "workspace-settings.yml").read_text(encoding="utf-8"))
    schema = json.loads((workspace / "workspace-settings.schema.json").read_text(encoding="utf-8"))
    errors = validate(settings, schema, schema)

    policy_names = {
        "AI-" + key.removeprefix("default_ai_").replace("_", "-").upper()
        for key in settings
        if key.startswith("default_ai_")
    }
    if "default_data_classification" in settings:
        policy_names.add("DATA-CLASSIFICATION")

    root_router = (workspace / "AGENTS.md").read_text(encoding="utf-8")
    template = (workspace / "standards" / "docs" / "templates" / "agents-template.md").read_text(encoding="utf-8")
    for policy in sorted(policy_names):
        if f"`{policy}`" not in root_router:
            errors.append(f"$.{policy}: missing semantics in root AGENTS.md")
        if f"**{policy}:**" not in template:
            errors.append(f"$.{policy}: missing from AGENTS template")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"OK: {workspace / 'workspace-settings.yml'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
