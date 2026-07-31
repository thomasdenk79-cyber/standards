"""Focused tests for hierarchical settings resolution."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import settings


class SettingsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "standards").mkdir()
        (self.root / "user-memory").mkdir()
        self.write(
            "standards/settings.yml",
            """
schema_version: 2
user_chat_lang: en
markdown_lang: en
default_ai_access: read-only
default_ai_execution: safe
""".lstrip(),
        )
        self.write(
            "standards/settings.schema.json",
            """
{
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version"],
  "properties": {
    "schema_version": {"type": "integer", "const": 2},
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

    def write(self, relative: str, content: str) -> None:
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def test_global_and_user_settings_override_in_order(self) -> None:
        self.write(
            "user-memory/settings.yml",
            "schema_version: 2\ndefault_ai_access: allowed\n",
        )
        self.write(
            "user-memory/alex/settings.yml",
            "schema_version: 2\nuser_chat_lang: de\n",
        )

        effective = settings.load_settings(self.root, "alex")

        self.assertEqual(effective["default_ai_access"], "allowed")
        self.assertEqual(effective["default_ai_execution"], "safe")
        self.assertEqual(effective["user_chat_lang"], "de")

    def test_missing_user_settings_inherits_global_settings(self) -> None:
        self.write(
            "user-memory/settings.yml",
            "schema_version: 2\nmarkdown_lang: de\n",
        )

        effective = settings.load_settings(self.root, "missing")

        self.assertEqual(effective["markdown_lang"], "de")
        self.assertEqual(effective["user_chat_lang"], "en")

    def test_unknown_override_is_rejected(self) -> None:
        self.write(
            "user-memory/settings.yml",
            "schema_version: 2\nunknown_setting: true\n",
        )

        with self.assertRaisesRegex(ValueError, "unknown_setting"):
            settings.load_settings(self.root, "alex")

    def test_invalid_override_value_is_rejected(self) -> None:
        self.write(
            "user-memory/settings.yml",
            "schema_version: 2\ndefault_ai_access: unrestricted\n",
        )

        with self.assertRaisesRegex(ValueError, "unrestricted"):
            settings.load_settings(self.root, "alex")

    def test_invalid_user_identifier_is_rejected(self) -> None:
        for user in ("..\\outside", ".", ".."):
            with self.subTest(user=user), self.assertRaisesRegex(ValueError, "Invalid user"):
                settings.load_settings(self.root, user)


if __name__ == "__main__":
    unittest.main()
