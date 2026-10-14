"""The catalogue gates every published theme with the pinned DS contract."""

import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class ThemeCIWorkflowTests(unittest.TestCase):
    def test_ci_runs_the_pinned_ds_validator_on_all_theme_files(self) -> None:
        workflow = yaml.safe_load((ROOT / ".github/workflows/ci.yml").read_text())
        steps = workflow["jobs"]["ci"]["steps"]
        checkout = next(
            step
            for step in steps
            if step.get("with", {}).get("repository")
            == "accelerate-data/vd-design-system"
        )
        self.assertEqual(checkout["uses"], "actions/checkout@v7")
        self.assertEqual(
            checkout["with"]["ref"], "147006d73dc48a835a0d56a749927b3319a2f772"
        )
        token = next(step for step in steps if step.get("id") == "theme-contract-token")
        self.assertEqual(token["uses"], "actions/create-github-app-token@v3")
        self.assertEqual(token["with"]["owner"], "accelerate-data")
        self.assertEqual(token["with"]["repositories"], "vd-design-system")
        self.assertEqual(token["with"]["permission-contents"], "read")
        self.assertEqual(
            checkout["with"]["token"], "${{ steps.theme-contract-token.outputs.token }}"
        )
        self.assertFalse(checkout["with"]["persist-credentials"])
        self.assertLess(steps.index(token), steps.index(checkout))
        path = checkout["with"]["path"]
        validator = next(
            step
            for step in steps
            if step.get("run") == f"python3 {path}/scripts/check_theme.py themes/*.json"
        )
        self.assertLess(steps.index(checkout), steps.index(validator))
        for step in (token, checkout, validator):
            self.assertNotIn("if", step)
            self.assertFalse(step.get("continue-on-error", False))


if __name__ == "__main__":
    unittest.main()
