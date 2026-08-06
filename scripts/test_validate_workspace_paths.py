from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import validate_workspace_paths


class ValidateWorkspacePathsTests(unittest.TestCase):
    def test_active_hardcode_fails_and_history_is_separate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "repo").mkdir()
            (root / "repo/AGENTS.md").write_text(
                r"Read C:\GIT\standards\AGENTS.md",
                encoding="utf-8",
            )
            (root / "repo/docs").mkdir()
            (root / "repo/docs/changelog.md").write_text(
                r"Previously used C:\GIT\standards",
                encoding="utf-8",
            )
            active, historical = validate_workspace_paths.findings(root)
        self.assertEqual(len(active), 1)
        self.assertEqual(len(historical), 1)

    def test_environment_placeholders_are_portable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "AGENTS.md").write_text(
                "Read ${ENGINEERING_GOVERNANCE_ROOT}/AGENTS.md",
                encoding="utf-8",
            )
            active, historical = validate_workspace_paths.findings(root)
        self.assertEqual(active, [])
        self.assertEqual(historical, [])

    def test_bare_workspace_root_is_not_portable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                r"Workspace: C:\GIT",
                encoding="utf-8",
            )
            active, historical = validate_workspace_paths.findings(root)
        self.assertEqual(len(active), 1)
        self.assertEqual(historical, [])

    def test_generated_directories_are_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("bin", "obj", "vscode-chat-backup"):
                target = root / "repo" / name
                target.mkdir(parents=True)
                (target / "generated.md").write_text(
                    r"Read C:\GIT\standards\AGENTS.md",
                    encoding="utf-8",
                )
            active, historical = validate_workspace_paths.findings(root)
        self.assertEqual(active, [])
        self.assertEqual(historical, [])

    def test_repository_local_standards_are_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / "repo"
            (repo / "standards").mkdir(parents=True)
            (repo / "AGENTS.md").write_text(
                "python standards/scripts/test_docs.py",
                encoding="utf-8",
            )
            active, historical = validate_workspace_paths.findings(root)
        self.assertEqual(active, [])
        self.assertEqual(historical, [])

    def test_parent_standards_reference_is_not_local(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / "repo"
            (repo / "standards").mkdir(parents=True)
            (repo / "AGENTS.md").write_text(
                "Read ../standards/AGENTS.md",
                encoding="utf-8",
            )
            active, historical = validate_workspace_paths.findings(root)
        self.assertEqual(len(active), 1)
        self.assertEqual(historical, [])


if __name__ == "__main__":
    unittest.main()
