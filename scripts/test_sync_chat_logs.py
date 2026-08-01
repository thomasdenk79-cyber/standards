"""Focused tests for sync_chat_logs.py."""

from __future__ import annotations

import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

import sync_chat_logs


class SyncChatLogsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.settings = {
            "chat_private_dir": "user-memory/why/conversations",
            "chat_shared_dir": "standards/why/conversations",
        }
        self.snapshot = sync_chat_logs.SessionSnapshot(
            payload=(
                b'{"type":"session.start","data":{"sessionId":"session-1",'
                b'"api_key":"secret-value"}}\n'
            ),
            extension="jsonl",
            agent="test-agent",
            model="test/model",
            source_location="test",
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_dot_identifiers_are_rejected(self) -> None:
        for value in (".", ".."):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "Invalid"):
                sync_chat_logs.validate_identifier(value, "identifier")

    def test_archive_is_redacted_and_idempotent(self) -> None:
        raw, changed, chat_number = sync_chat_logs.archive(
            self.root,
            self.settings,
            "copilot",
            "session-1",
            self.snapshot,
            "transcript",
            "only_at_user_memory",
            "redact",
        )
        self.assertTrue(changed)
        self.assertEqual(chat_number, 1)
        self.assertEqual(
            raw.name,
            "001-01__original-restricted__test-agent__test-model__topic-pending.jsonl",
        )
        self.assertIn("[REDACTED-SECRET]", raw.read_text(encoding="utf-8"))

        same_raw, changed, same_number = sync_chat_logs.archive(
            self.root,
            self.settings,
            "copilot",
            "session-1",
            self.snapshot,
            "transcript",
            "only_at_user_memory",
            "redact",
            chat_number=1,
        )
        self.assertEqual(raw, same_raw)
        self.assertFalse(changed)
        self.assertEqual(same_number, 1)

    def test_summary_returns_unique_searchable_path(self) -> None:
        body = self.root / "summary.md"
        body.write_text("## Why\n\nA durable decision was needed.", encoding="utf-8")
        target, changed = sync_chat_logs.shared_summary(
            self.root,
            self.settings,
            1,
            "durable-why",
            "Durable WHY",
            body,
            agent="OpenCode 1.18.9",
            model="github-copilot/gpt-5.6-sol",
            classification="public",
            confirm_sanitized=True,
        )
        self.assertTrue(changed)
        self.assertEqual(
            target.name,
            "001__ai-summary-public__opencode-1.18.9__github-copilot-gpt-5.6-sol__durable-why.md",
        )
        self.assertIn("chat_number: 001", target.read_text(encoding="utf-8"))

    def test_private_archive_requires_transcript_permission(self) -> None:
        with self.assertRaises(ValueError):
            sync_chat_logs.archive(
                self.root,
                self.settings,
                "copilot",
                "session-1",
                self.snapshot,
                "summary",
                "only_at_user_memory",
                "redact",
            )

    def test_private_archive_can_preserve_secrets_by_user_choice(self) -> None:
        raw, _, _ = sync_chat_logs.archive(
            self.root,
            self.settings,
            "copilot",
            "session-1",
            self.snapshot,
            "transcript",
            "only_at_user_memory",
            "preserve",
        )
        self.assertIn("secret-value", raw.read_text(encoding="utf-8"))

    def test_sequence_continues_after_legacy_artifact(self) -> None:
        directory = self.root / "user-memory" / "why" / "conversations"
        directory.mkdir(parents=True)
        (directory / "raw-007_legacy.log").write_text("legacy", encoding="utf-8")
        self.assertEqual(sync_chat_logs.resolve_chat_number(self.root, self.settings, None), 8)

    def test_existing_session_reuses_number_when_omitted(self) -> None:
        first, _, first_number = sync_chat_logs.archive(
            self.root,
            self.settings,
            "copilot",
            "session-1",
            self.snapshot,
            "transcript",
            "only_at_user_memory",
            "redact",
        )
        updated = sync_chat_logs.SessionSnapshot(
            payload=self.snapshot.payload + b'{"message":"next"}\n',
            extension="jsonl",
            agent=self.snapshot.agent,
            model=self.snapshot.model,
            source_location=self.snapshot.source_location,
        )
        second, _, second_number = sync_chat_logs.archive(
            self.root,
            self.settings,
            "copilot",
            "session-1",
            updated,
            "transcript",
            "only_at_user_memory",
            "redact",
        )
        self.assertEqual(first_number, second_number)
        self.assertTrue(first.name.startswith("001-01__"))
        self.assertTrue(second.name.startswith("001-02__"))

    def test_chat_number_rejects_different_session_with_other_native_format(self) -> None:
        sync_chat_logs.archive(
            self.root,
            self.settings,
            "copilot",
            "session-1",
            self.snapshot,
            "transcript",
            "only_at_user_memory",
            "redact",
            chat_number=5,
        )
        other = sync_chat_logs.SessionSnapshot(
            payload=b'{"info":{"id":"other-session"}}',
            extension="json",
            agent="OpenCode 1.18.9",
            model="test/model",
            source_location="test",
        )
        with self.assertRaises(ValueError):
            sync_chat_logs.archive(
                self.root,
                self.settings,
                "opencode",
                "other-session",
                other,
                "transcript",
                "only_at_user_memory",
                "redact",
                chat_number=5,
            )

    def test_session_id_is_validated_before_source_lookup(self) -> None:
        with self.assertRaises(ValueError):
            sync_chat_logs.snapshot_from_args(
                Namespace(session_id="../escape", input=None, source="copilot")
            )

    def test_copilot_snapshot_lists_all_models(self) -> None:
        session_id = "session-models"
        session = self.root / "session-state" / session_id
        session.mkdir(parents=True)
        (session / "events.jsonl").write_text(
            "\n".join(
                (
                    '{"type":"session.start","data":{"copilotVersion":"1.0.75"}}',
                    '{"type":"session.model_change","data":{"newModel":"model-a"}}',
                    '{"type":"session.model_change","data":{"newModel":"model-b"}}',
                    '{"type":"session.model_change","data":{"newModel":"model-a"}}',
                )
            ),
            encoding="utf-8",
        )
        snapshot = sync_chat_logs.load_copilot(session_id, home=self.root)
        self.assertEqual(snapshot.model, "model-a and model-b")

    def test_copilot_snapshot_uses_start_model_without_change_event(self) -> None:
        session_id = "session-start-model"
        session = self.root / "session-state" / session_id
        session.mkdir(parents=True)
        (session / "events.jsonl").write_text(
            '{"type":"session.start","data":{"copilotVersion":"1.0.75",'
            '"selectedModel":"model-a"}}\n',
            encoding="utf-8",
        )
        snapshot = sync_chat_logs.load_copilot(session_id, home=self.root)
        self.assertEqual(snapshot.model, "model-a")

    def test_summary_rejects_detected_secret(self) -> None:
        body = self.root / "summary.md"
        body.write_text("api_key: definitely-secret", encoding="utf-8")
        with self.assertRaises(ValueError):
            sync_chat_logs.shared_summary(
                self.root,
                self.settings,
                1,
                "unsafe",
                "Unsafe",
                body,
                agent="OpenCode 1.18.9",
                model="github-copilot/gpt-5.6-sol",
                classification="public",
                confirm_sanitized=True,
            )

    def test_public_target_rejects_internal_summary(self) -> None:
        router = self.root / "standards" / "why" / "AGENTS.md"
        router.parent.mkdir(parents=True)
        router.write_text("- **DATA-CLASSIFICATION:** public\n", encoding="utf-8")
        body = self.root / "summary.md"
        body.write_text("Neutral technical decision.", encoding="utf-8")
        with self.assertRaises(ValueError):
            sync_chat_logs.shared_summary(
                self.root,
                self.settings,
                1,
                "classification",
                "Classification",
                body,
                agent="test-agent",
                model="test-model",
                classification="internal",
                confirm_sanitized=True,
            )

    def test_topic_is_limited_to_thirty_characters(self) -> None:
        body = self.root / "summary.md"
        body.write_text("Neutral technical decision.", encoding="utf-8")
        with self.assertRaises(ValueError):
            sync_chat_logs.shared_summary(
                self.root,
                self.settings,
                1,
                "this-topic-is-definitely-too-long",
                "Long topic",
                body,
                agent="test-agent",
                model="test-model",
                classification="public",
                confirm_sanitized=True,
            )


if __name__ == "__main__":
    unittest.main()
