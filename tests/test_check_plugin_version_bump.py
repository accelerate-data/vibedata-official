from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "scripts" / "check-plugin-version-bump.py"
)
SPEC = importlib.util.spec_from_file_location("check_plugin_version_bump", MODULE_PATH)
assert SPEC is not None
check_plugin_version_bump = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(check_plugin_version_bump)


class PluginVersionBumpTests(unittest.TestCase):
    def test_detects_plugin_dir_changes(self) -> None:
        self.assertTrue(
            check_plugin_version_bump.bundled_plugin_changed(
                ["plugins/vibedata-dbt-skills/skills/dbt-fabric-patterns/SKILL.md"]
            )
        )

    def test_detects_plugin_json_changes(self) -> None:
        self.assertTrue(
            check_plugin_version_bump.bundled_plugin_changed(
                [".claude-plugin/plugin.json"]
            )
        )

    def test_ignores_marketplace_only_changes(self) -> None:
        self.assertFalse(
            check_plugin_version_bump.bundled_plugin_changed(
                [".claude-plugin/marketplace.json", "README.md"]
            )
        )

    def test_parses_strict_semver(self) -> None:
        self.assertEqual(
            check_plugin_version_bump.version_tuple("1.2.3", "test"),
            (1, 2, 3),
        )

    def test_rejects_non_string_version(self) -> None:
        with self.assertRaises(SystemExit):
            check_plugin_version_bump.version_tuple(123, "test")

    def test_rejects_invalid_semver(self) -> None:
        with self.assertRaises(SystemExit):
            check_plugin_version_bump.version_tuple("1.2", "test")

    def test_formats_version_tuple(self) -> None:
        self.assertEqual(
            check_plugin_version_bump.format_version((1, 2, 3)),
            "1.2.3",
        )

    def test_fail_exits(self) -> None:
        with self.assertRaises(SystemExit):
            check_plugin_version_bump.fail("boom")

    def test_changed_files_combines_committed_staged_and_unstaged(self) -> None:
        with patch.object(
            check_plugin_version_bump,
            "git_output",
            side_effect=[
                "README.md\n",
                "plugins/vibedata-dbt-skills/skills/dbt-fabric-patterns/SKILL.md\n",
                "README.md\n.claude-plugin/plugin.json\n",
            ],
        ):
            self.assertEqual(
                check_plugin_version_bump.changed_files("origin/main"),
                [
                    ".claude-plugin/plugin.json",
                    "README.md",
                    "plugins/vibedata-dbt-skills/skills/dbt-fabric-patterns/SKILL.md",
                ],
            )

    def test_loads_plugin_json_from_worktree(self) -> None:
        data = check_plugin_version_bump.load_plugin_json_from_worktree()

        self.assertEqual(data["name"], "vibedata")

    def test_main_skips_when_no_bundled_files_changed(self) -> None:
        with (
            patch(
                "sys.argv",
                ["check-plugin-version-bump.py", "--base-ref", "origin/main"],
            ),
            patch.object(
                check_plugin_version_bump, "changed_files", return_value=["README.md"]
            ),
        ):
            self.assertEqual(check_plugin_version_bump.main(), 0)

    def test_main_skips_when_base_plugin_json_missing(self) -> None:
        with (
            patch(
                "sys.argv",
                ["check-plugin-version-bump.py", "--base-ref", "origin/main"],
            ),
            patch.object(
                check_plugin_version_bump,
                "changed_files",
                return_value=[
                    "plugins/vibedata-dbt-skills/skills/dbt-fabric-patterns/SKILL.md"
                ],
            ),
            patch.object(
                check_plugin_version_bump,
                "load_plugin_json_from_worktree",
                return_value={"version": "1.1.1"},
            ),
            patch.object(
                check_plugin_version_bump,
                "load_plugin_json_from_git",
                return_value=None,
            ),
        ):
            self.assertEqual(check_plugin_version_bump.main(), 0)

    def test_main_passes_when_plugin_version_increases(self) -> None:
        with (
            patch(
                "sys.argv",
                ["check-plugin-version-bump.py", "--base-ref", "origin/main"],
            ),
            patch.object(
                check_plugin_version_bump,
                "changed_files",
                return_value=[
                    "plugins/vibedata-dbt-skills/skills/dbt-fabric-patterns/SKILL.md"
                ],
            ),
            patch.object(
                check_plugin_version_bump,
                "load_plugin_json_from_worktree",
                return_value={"version": "1.1.1"},
            ),
            patch.object(
                check_plugin_version_bump,
                "load_plugin_json_from_git",
                return_value={"version": "1.1.0"},
            ),
        ):
            self.assertEqual(check_plugin_version_bump.main(), 0)

    def test_main_fails_when_plugin_version_does_not_increase(self) -> None:
        with (
            patch(
                "sys.argv",
                ["check-plugin-version-bump.py", "--base-ref", "origin/main"],
            ),
            patch.object(
                check_plugin_version_bump,
                "changed_files",
                return_value=[
                    "plugins/vibedata-dbt-skills/skills/dbt-fabric-patterns/SKILL.md"
                ],
            ),
            patch.object(
                check_plugin_version_bump,
                "load_plugin_json_from_worktree",
                return_value={"version": "1.1.0"},
            ),
            patch.object(
                check_plugin_version_bump,
                "load_plugin_json_from_git",
                return_value={"version": "1.1.0"},
            ),
            self.assertRaises(SystemExit),
        ):
            check_plugin_version_bump.main()


if __name__ == "__main__":
    unittest.main()
