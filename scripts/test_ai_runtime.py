from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ai_runtime


class AiRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.policy_path = self.root / "policy.json"
        self.state_dir = self.root / "state"
        self.policy_path.write_text(
            json.dumps(
                {
                    "context": {
                        "target_input_tokens": 32_768,
                        "warn_input_tokens": 65_536,
                        "new_session_input_tokens": 98_304,
                        "max_output_tokens": 8_192,
                    },
                    "local": {"game_processes": ["TL.exe"]},
                    "routing": {"default_provider": "siemens"},
                }
            ),
            encoding="utf-8",
        )
        self.policy = ai_runtime.load_policy(self.policy_path)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_context_thresholds_warn_then_block(self) -> None:
        self.assertEqual(ai_runtime.projected_context(self.policy, 60_000, 1_000), "allow")
        self.assertEqual(ai_runtime.projected_context(self.policy, 65_000, 1_000), "warn")
        self.assertEqual(ai_runtime.projected_context(self.policy, 90_000, 9_000), "block")

    def test_game_process_blocks_local_work(self) -> None:
        self.assertEqual(
            ai_runtime.local_block_reason(self.policy, self.state_dir, lambda: {"tl.exe"}),
            "game:tl.exe",
        )

    def test_manual_blocker_is_persistent_and_clearable(self) -> None:
        ai_runtime.set_manual_blocker(self.state_dir, "gaming")
        self.assertEqual(
            ai_runtime.active_blockers(self.policy, self.state_dir, lambda: set()),
            ["manual:gaming"],
        )
        ai_runtime.clear_manual_blocker(self.state_dir, "gaming")
        self.assertEqual(ai_runtime.active_blockers(self.policy, self.state_dir, lambda: set()), [])

    def test_lease_refuses_a_blocked_runtime(self) -> None:
        manager = ai_runtime.lease.LeaseManager(
            self.root / "leases",
            availability_check=lambda: "game:tl.exe",
        )
        with self.assertRaises(ai_runtime.lease.LeaseBlockedError):
            manager.acquire("local-llm", "test", "ollama/test", wait_seconds=0)

    def test_usage_ledger_has_no_prompt_column(self) -> None:
        ai_runtime.record_event(
            self.state_dir,
            event="usage",
            runtime="opencode",
            provider="siemens",
            model="qwen-3.6-27b",
            input_tokens=123,
        )
        import sqlite3

        connection = sqlite3.connect(self.state_dir / ai_runtime.LEDGER_FILENAME)
        try:
            columns = [row[1] for row in connection.execute("PRAGMA table_info(runtime_events)")]
        finally:
            connection.close()
        self.assertNotIn("prompt", columns)
        self.assertIn("input_tokens", columns)

    def test_opencode_cap_preserves_credentials_and_caps_limits(self) -> None:
        config = self.root / "opencode.json"
        config.write_text(
            json.dumps(
                {
                    "provider": {
                        "siemens": {
                            "options": {"apiKey": "keep"},
                            "models": {
                                "qwen": {"limit": {"context": 1_048_576, "output": 32_768}}
                            },
                        }
                    }
                }
            ),
            encoding="utf-8",
        )

        self.assertTrue(ai_runtime.cap_opencode_config(config, self.policy))
        updated = json.loads(config.read_text(encoding="utf-8"))

        self.assertEqual(updated["provider"]["siemens"]["options"]["apiKey"], "keep")
        self.assertEqual(
            updated["provider"]["siemens"]["models"]["qwen"]["limit"]["context"],
            98_304,
        )
        self.assertEqual(
            updated["provider"]["siemens"]["models"]["qwen"]["limit"]["output"],
            8_192,
        )
        self.assertTrue(config.with_name("opencode.json.runtime-guard.bak").is_file())


if __name__ == "__main__":
    unittest.main()
