"""Resolve the workspace settings hierarchy from general to specific."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

import yaml


SAFE_ID = re.compile(r"^[A-Za-z0-9._-]+$")
BASE_SETTINGS = Path("standards/settings.yml")
GLOBAL_USER_SETTINGS = Path("user-memory/settings.yml")


def find_workspace_root(start: Path) -> Path | None:
    for directory in (start, *start.parents):
        if (directory / BASE_SETTINGS).is_file():
            return directory
    return None


def resolve_user(explicit: str | None = None) -> str | None:
    selected = (
        explicit
        if explicit is not None
        else os.environ.get("AI_WORKSPACE_USER") or os.environ.get("USERNAME")
    )
    if not selected:
        return None
    if selected in {".", ".."} or SAFE_ID.fullmatch(selected) is None:
        raise ValueError(f"Invalid user: {selected!r}")
    return selected


def settings_paths(root: Path, user: str | None = None) -> list[Path]:
    base = root / BASE_SETTINGS
    if not base.is_file():
        raise FileNotFoundError(f"Base settings not found: {base}")

    paths = [base]
    global_user = root / GLOBAL_USER_SETTINGS
    if global_user.is_file():
        paths.append(global_user)

    selected = resolve_user(user)
    if selected:
        user_settings = root / "user-memory" / selected / "settings.yml"
        if user_settings.is_file():
            paths.append(user_settings)
    return paths


def read_settings(path: Path) -> dict[str, object]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Settings must be a mapping: {path}")
    if "schema_version" not in data:
        raise ValueError(f"Missing schema_version: {path}")
    return data


def resolve_schema(schema: dict[str, Any], root: dict[str, Any]) -> dict[str, Any]:
    reference = schema.get("$ref")
    if not reference:
        return schema
    if not reference.startswith("#/$defs/"):
        raise ValueError(f"Unsupported schema reference: {reference}")
    return root["$defs"][reference.removeprefix("#/$defs/")]


def validate_value(
    value: Any,
    schema: dict[str, Any],
    root: dict[str, Any],
    path: str = "$",
) -> list[str]:
    schema = resolve_schema(schema, root)
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
                errors.extend(validate_value(item, properties[key], root, f"{path}.{key}"))
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


def validate_settings_data(
    data: dict[str, object],
    schema: dict[str, Any],
    complete: bool = False,
) -> list[str]:
    errors = validate_value(data, schema, schema)
    if complete:
        errors.extend(
            f"$.{key}: missing required base setting"
            for key in schema["properties"]
            if key not in data
        )
    return errors


def load_settings(root: Path, user: str | None = None) -> dict[str, object]:
    paths = settings_paths(root, user)
    schema_path = root / "standards" / "settings.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    settings = read_settings(paths[0])
    errors = validate_settings_data(settings, schema, complete=True)
    if errors:
        raise ValueError(f"{paths[0]}: {'; '.join(errors)}")
    allowed = set(settings)
    version = settings["schema_version"]

    for path in paths[1:]:
        overrides = read_settings(path)
        errors = validate_settings_data(overrides, schema)
        if errors:
            raise ValueError(f"{path}: {'; '.join(errors)}")
        if overrides["schema_version"] != version:
            raise ValueError(
                f"Incompatible schema_version in {path}: "
                f"{overrides['schema_version']!r} != {version!r}"
            )
        unknown = set(overrides) - allowed
        if unknown:
            raise ValueError(f"Unknown setting(s) in {path}: {', '.join(sorted(unknown))}")
        settings.update(
            {key: value for key, value in overrides.items() if key != "schema_version"}
        )
    return settings
