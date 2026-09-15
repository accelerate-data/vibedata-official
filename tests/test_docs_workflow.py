"""Shape tests for the reusable operator-docs workflow (.github/workflows/docs.yml).

The workflow has two triggers over one implementation: `workflow_call` (invoked by
publish.yml on a `studio-release` dispatch, so a release publishes docs that name
its own build) and `workflow_dispatch` (a manual run for the initial bring-up and
docs-only republishes between releases). See ADR 0110 and
docs/design/operator-documentation/README.md.
"""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml

WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "docs.yml"


def load() -> tuple[str, dict]:
    raw = WORKFLOW.read_text()
    data = yaml.safe_load(raw)
    # YAML 1.1 parses a bare `on:` key as boolean True; re-key for assertions.
    if True in data and "on" not in data:
        data["on"] = data[True]
    return raw, data


class DocsWorkflowShape(unittest.TestCase):
    def setUp(self) -> None:
        self.raw, self.wf = load()

    def test_is_dispatchable_by_hand_and_callable_by_the_release_pipeline(self) -> None:
        self.assertIn("workflow_dispatch", self.wf["on"])
        self.assertIn("workflow_call", self.wf["on"])

    def test_exposes_the_released_build_identity_inputs(self) -> None:
        # The release path passes these in; a manual run may omit them.
        for trigger in ("workflow_dispatch", "workflow_call"):
            inputs = self.wf["on"][trigger]["inputs"]
            self.assertIn("candidate_tag", inputs)
            self.assertIn("candidate_sha", inputs)
            self.assertIn("release_notes_body", inputs)
            self.assertFalse(inputs["candidate_tag"]["required"])
            self.assertFalse(inputs["candidate_sha"]["required"])

    def test_has_pages_permissions_and_environment(self) -> None:
        perms = self.wf["permissions"]
        self.assertEqual(perms.get("pages"), "write")
        self.assertEqual(perms.get("id-token"), "write")
        self.assertEqual(
            self.wf["jobs"]["deploy"]["environment"]["name"], "github-pages"
        )

    def _release_step(self) -> dict:
        for step in self.wf["jobs"]["deploy"]["steps"]:
            if step.get("name") == "Generate the release identity and notes":
                return step
        self.fail("no 'Generate the release identity and notes' step")

    def test_release_page_only_written_when_the_build_identity_is_supplied(
        self,
    ) -> None:
        # A manual run with no inputs has no build to name and must still publish.
        step = self._release_step()
        self.assertIn("inputs.candidate_tag != ''", step["if"])
        self.assertIn("inputs.candidate_sha != ''", step["if"])

    def test_release_page_interpolates_the_released_identity_and_notes(self) -> None:
        # Deleting any of these interpolations strips the build identity from the
        # published page, so lock the exact shell tokens.
        run = self._release_step()["run"]
        self.assertIn('echo "# Release ${TAG}"', run)
        self.assertIn("built from studio commit \\`${SHA}\\`.", run)
        self.assertIn("printf '%s\\n' \"$NOTES\"", run)

    def test_builds_and_deploys_the_pages_artifact(self) -> None:
        self.assertIn("npm ci", self.raw)
        self.assertIn("npm run docs:build", self.raw)
        self.assertIn("actions/upload-pages-artifact", self.raw)
        self.assertIn("docs/.vitepress/dist", self.raw)
        self.assertIn("actions/deploy-pages", self.raw)


if __name__ == "__main__":
    unittest.main()
