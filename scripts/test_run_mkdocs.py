from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import run_mkdocs


class RunMkDocsTests(unittest.TestCase):
    def test_resolves_both_workspace_roots(self) -> None:
        content = (
            'INHERIT: "${ENGINEERING_GOVERNANCE_ROOT}/mkdocs-base.yml"\n'
            'docs_dir: "${ENGINEERING_REPOS_ROOT}/repo/docs"\n'
        )
        resolved = run_mkdocs.resolve_placeholders(
            content,
            {
                "ENGINEERING_REPOS_ROOT": "D:/repos",
                "ENGINEERING_GOVERNANCE_ROOT": "D:/governance",
            },
        )
        self.assertIn("D:/governance/mkdocs-base.yml", resolved)
        self.assertIn("D:/repos/repo/docs", resolved)

    def test_missing_required_variable_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "ENGINEERING_GOVERNANCE_ROOT"):
            run_mkdocs.resolve_placeholders(
                'INHERIT: "${ENGINEERING_GOVERNANCE_ROOT}/mkdocs-base.yml"\n',
                {},
            )

    def test_extracts_relative_config_argument(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config, remaining = run_mkdocs.extract_config(
                ["build", "--strict", "-f", "config/docs.yml"],
                root,
            )
        self.assertEqual(config, root / "config/docs.yml")
        self.assertEqual(remaining, ["build", "--strict"])


if __name__ == "__main__":
    unittest.main()
