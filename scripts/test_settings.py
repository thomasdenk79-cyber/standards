"""Focused tests for portable hierarchical settings resolution."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import settings


class SettingsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.governance = self.root / "engineering-governance"
        self.governance.mkdir()
        (self.root / "user-memory").mkdir()
        (self.root / settings.WORKSPACE_MARKER).write_text(
            "schema_version: 1\n",
            encoding="utf-8",
        )
        self.write(
            self.governance / "settings.yml",
            """
schema_version: 2
load_user_memory: false
load_agent_memory: false
user_chat_lang: en
markdown_lang: en
default_ai_access: read-only
default_ai_execution: safe
""".lstrip(),
        )
        self.write(
            self.governance / "settings.schema.json",
            """
{
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version"],
  "properties": {
    "schema_version": {"type": "integer", "const": 2},
    "load_user_memory": {"type": "boolean"},
    "load_agent_memory": {"type": "boolean"},
    "user_chat_lang": {"type": "string"},
    "markdown_lang": {"type": "string"},
    "default_ai_access": {"enum": ["allowed", "read-only", "denied"]},
    "default_ai_execution": {"enum": ["denied", "safe", "ask", "allowed"]}
  }
}
""".lstrip(),
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    @staticmethod
    def write(target: Path, content: str) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def load(self, user: str | None = None) -> dict[str, object]:
        return settings.load_settings(self.root, user, self.governance)

    def test_global_and_user_settings_override_in_order(self) -> None:
        self.write(
            self.root / "user-memory/settings.yml",
            "schema_version: 2\ndefault_ai_access: allowed\n",
        )
        self.write(
            self.root / "user-memory/alex/settings.yml",
            "schema_version: 2\nuser_chat_lang: de\n",
        )

        effective = self.load("alex")

        self.assertEqual(effective["default_ai_access"], "allowed")
        self.assertEqual(effective["default_ai_execution"], "safe")
        self.assertEqual(effective["user_chat_lang"], "de")

    def test_missing_user_settings_inherits_global_settings(self) -> None:
        self.write(
            self.root / "user-memory/settings.yml",
            "schema_version: 2\nmarkdown_lang: de\n",
        )

        effective = self.load("missing")

        self.assertEqual(effective["markdown_lang"], "de")
        self.assertEqual(effective["user_chat_lang"], "en")
        self.assertIs(effective["load_user_memory"], False)
        self.assertIs(effective["load_agent_memory"], False)

    def test_memory_loading_can_be_enabled_by_user_override(self) -> None:
        self.write(
            self.root / "user-memory/settings.yml",
            "schema_version: 2\nload_user_memory: true\nload_agent_memory: true\n",
        )
        effective = self.load("alex")
        self.assertIs(effective["load_user_memory"], True)
        self.assertIs(effective["load_agent_memory"], True)

    def test_unknown_override_is_rejected(self) -> None:
        self.write(
            self.root / "user-memory/settings.yml",
            "schema_version: 2\nunknown_setting: true\n",
        )
        with self.assertRaisesRegex(ValueError, "unknown_setting"):
            self.load("alex")

    def test_invalid_override_value_is_rejected(self) -> None:
        self.write(
            self.root / "user-memory/settings.yml",
            "schema_version: 2\ndefault_ai_access: unrestricted\n",
        )
        with self.assertRaisesRegex(ValueError, "unrestricted"):
            self.load("alex")

    def test_non_boolean_memory_loading_is_rejected(self) -> None:
        self.write(
            self.root / "user-memory/settings.yml",
            "schema_version: 2\nload_user_memory: disabled\n",
        )
        with self.assertRaisesRegex(ValueError, "expected boolean"):
            self.load("alex")

    def test_invalid_user_identifier_is_rejected(self) -> None:
        for user in ("..\\outside", ".", ".."):
            with self.subTest(user=user), self.assertRaisesRegex(ValueError, "Invalid user"):
                self.load(user)

    def test_environment_roots_are_discovered(self) -> None:
        env = {
            settings.REPOS_ROOT_ENV: str(self.root),
            settings.GOVERNANCE_ROOT_ENV: str(self.governance),
        }
        with patch.dict(os.environ, env, clear=False):
            self.assertEqual(settings.find_workspace_root(self.root / "user-memory"), self.root)
            self.assertEqual(
                settings.find_governance_root(self.root / "user-memory"),
                self.governance,
            )

    def test_workspace_placeholders_resolve(self) -> None:
        self.assertEqual(
            settings.resolve_workspace_path(
                "${ENGINEERING_GOVERNANCE_ROOT}/why/conversations",
                self.root,
                self.governance,
            ),
            self.governance / "why/conversations",
        )


if __name__ == "__main__":
    unittest.main()
