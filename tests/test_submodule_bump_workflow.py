"""Shape tests for the daily submodule bump (.github/workflows/submodule-bump.yml).

The workflow bumps every submodule to its tracked branch, regenerates the
storefront catalog so the ci.yml freshness check stays green, and opens a PR the
App token created (so the pull_request checks run) that auto-merges on green.
See the VD-6698 plan.
"""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml

WORKFLOW = (
    Path(__file__).resolve().parents[1] / ".github" / "workflows" / "submodule-bump.yml"
)


def load() -> tuple[str, dict]:
    raw = WORKFLOW.read_text()
    data = yaml.safe_load(raw)
    # YAML 1.1 parses a bare `on:` key as boolean True; re-key for assertions.
    if True in data and "on" not in data:
        data["on"] = data[True]
    return raw, data


class SubmoduleBumpWorkflowShape(unittest.TestCase):
    def setUp(self) -> None:
        self.raw, self.wf = load()

    def test_runs_daily_and_can_be_dispatched(self) -> None:
        self.assertIn("schedule", self.wf["on"])
        self.assertIn("workflow_dispatch", self.wf["on"])
        self.assertTrue(self.wf["on"]["schedule"][0]["cron"])

    def test_has_write_permissions_for_branch_and_pr(self) -> None:
        self.assertEqual(self.wf["permissions"].get("contents"), "write")
        self.assertEqual(self.wf["permissions"].get("pull-requests"), "write")

    def test_mints_an_app_token_so_the_pr_triggers_ci(self) -> None:
        self.assertIn("actions/create-github-app-token", self.raw)
        self.assertIn("VIBEDATA_GHA_APP_ID", self.raw)
        self.assertIn("repositories: vibedata-official", self.raw)

    def test_checks_out_with_submodules(self) -> None:
        self.assertIn("submodules: recursive", self.raw)

    def test_bumps_submodules_and_regenerates_the_catalog(self) -> None:
        self.assertIn("git submodule update --remote --recursive", self.raw)
        self.assertIn("python3 scripts/build_catalog.py", self.raw)

    def test_opens_and_auto_merges_the_bump_pr(self) -> None:
        self.assertIn("gh pr create", self.raw)
        self.assertIn("gh pr merge --auto --squash", self.raw)

    def test_does_nothing_when_already_current(self) -> None:
        self.assertIn("git diff --cached --quiet", self.raw)


if __name__ == "__main__":
    unittest.main()
