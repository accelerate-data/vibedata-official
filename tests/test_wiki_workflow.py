"""Shape tests for the reusable operator-wiki workflow (.github/workflows/wiki.yml).

The workflow has two triggers over one implementation: `workflow_call` (invoked by
publish.yml on a `studio-release` dispatch, so a release publishes docs that name
its own build) and `workflow_dispatch` (a manual run for the initial bring-up and
docs-only republishes between releases). It mints an app token and pushes the
canonical pages to the wiki with scripts/publish_wiki.py. See ADR 0111 and
docs/design/operator-documentation/README.md.
"""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml

WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "wiki.yml"


def load() -> tuple[str, dict]:
    raw = WORKFLOW.read_text()
    data = yaml.safe_load(raw)
    # YAML 1.1 parses a bare `on:` key as boolean True; re-key for assertions.
    if True in data and "on" not in data:
        data["on"] = data[True]
    return raw, data


class WikiWorkflowShape(unittest.TestCase):
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

    def test_has_read_only_contents_permission(self) -> None:
        self.assertEqual(self.wf["permissions"].get("contents"), "read")
        self.assertNotIn("pages", self.wf["permissions"])
        self.assertNotIn("id-token", self.wf["permissions"])

    def test_serializes_publishes(self) -> None:
        # A manual dispatch must not race the release call; publish.yml's
        # concurrency is keyed by candidate_tag, which a manual run lacks.
        self.assertEqual(
            self.wf["concurrency"],
            {"group": "operator-wiki", "cancel-in-progress": False},
        )

    def test_mints_a_scoped_app_token_for_the_wiki_repo(self) -> None:
        self.assertIn("actions/create-github-app-token", self.raw)
        self.assertIn("VIBEDATA_GHA_APP_ID", self.raw)
        self.assertIn("repositories: vibedata-official", self.raw)
        self.assertIn("github.repository_owner", self.raw)

    def test_runs_the_wiki_publisher_with_the_validated_identity(self) -> None:
        self.assertIn("python3 scripts/publish_wiki.py", self.raw)
        self.assertIn("WIKI_REMOTE:", self.raw)
        self.assertIn("TAG: ${{ inputs.candidate_tag }}", self.raw)
        self.assertIn("SHA: ${{ inputs.candidate_sha }}", self.raw)
        self.assertIn("NOTES: ${{ inputs.release_notes_body }}", self.raw)

    def test_does_not_reference_the_retired_pages_surface(self) -> None:
        self.assertNotIn("actions/deploy-pages", self.raw)
        self.assertNotIn("actions/upload-pages-artifact", self.raw)
        self.assertNotIn("github-pages", self.raw)


if __name__ == "__main__":
    unittest.main()
