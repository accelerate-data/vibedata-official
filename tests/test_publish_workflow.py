"""Shape tests for the Studio release publish pipeline (.github/workflows/publish.yml).

The publish pipeline is triggered by a `studio-release` repository_dispatch from
accelerate-data/vd-studio's deploy.yml AFTER that workflow has already promoted
the images (crane copy, signatures preserved) into the public studio-* packages.
This workflow therefore must NOT re-promote the images; it downloads the
studio-built release artifacts, creates the GitHub Release, and publishes the
operator documentation as a VitePress site rendered from the same dispatch
payload. See vd-studio docs/design/devops/03-release-promotion.md for the
canonical contract.
"""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml

WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "publish.yml"


def load() -> tuple[str, dict]:
    raw = WORKFLOW.read_text()
    data = yaml.safe_load(raw)
    # YAML 1.1 parses a bare `on:` key as boolean True; re-key for assertions.
    if True in data and "on" not in data:
        data["on"] = data[True]
    return raw, data


class PublishWorkflowShape(unittest.TestCase):
    def setUp(self) -> None:
        self.raw, self.wf = load()

    def test_triggered_by_studio_release_dispatch(self) -> None:
        types = self.wf["on"]["repository_dispatch"]["types"]
        self.assertIn("studio-release", types)

    def test_consumes_the_aligned_payload(self) -> None:
        # Contract from deploy.yml: candidate_tag / version / candidate_sha /
        # source_workflow_run_id / release_notes_body.
        self.assertIn("candidate_tag", self.raw)
        self.assertIn("candidate_sha", self.raw)
        self.assertIn("source_workflow_run_id", self.raw)
        self.assertIn("release_notes_body", self.raw)

    def test_does_not_use_the_retired_payload_shape(self) -> None:
        # The old PR expected frontend/backend objects + an embedded release_manifest.
        self.assertNotIn("private_image", self.raw)
        self.assertNotIn("release_manifest", self.raw)

    def test_does_not_re_promote_images(self) -> None:
        # Promotion (crane copy, referrers preserved) happens on the studio side.
        # docker tag/push here would drop the cosign/SBOM/SLSA referrers.
        self.assertNotIn("docker push", self.raw)
        self.assertNotIn("docker tag", self.raw)

    def test_public_packages_match_design_naming(self) -> None:
        self.assertIn("studio-backend", self.raw)
        self.assertIn("studio-frontend", self.raw)
        self.assertNotIn("vibedata-studio-backend", self.raw)
        self.assertNotIn("vibedata-studio-frontend", self.raw)

    def test_downloads_studio_run_artifacts(self) -> None:
        self.assertIn("gh run download", self.raw)
        self.assertIn("accelerate-data/studio", self.raw)

    def test_attaches_cli_binaries_and_install_script(self) -> None:
        self.assertIn("vibedata-", self.raw)  # the 4 platform binaries
        self.assertIn("install.sh", self.raw)

    def test_no_longer_requires_a_wiki_tarball(self) -> None:
        # Studio stopped producing wiki-<tag>.tar.gz and the operator wiki is
        # retired to a pointer; the documentation publishes as a site (VD-5700).
        # Assert the specific retired artifact name (its required-artifact list
        # entry), not the bare word "wiki", so a future comment mentioning
        # "wiki" does not break this test.
        self.assertNotIn("wiki-${TAG}.tar.gz", self.raw)

    def test_creates_release_without_a_separate_image_manifest(self) -> None:
        self.assertIn("gh release create", self.raw)
        self.assertNotIn("release-manifest.json", self.raw)
        self.assertNotIn("THIRD_PARTY_APP_DB", self.raw)
        self.assertNotIn("push origin HEAD:main", self.raw)

    def test_verifies_public_images_offline_no_rekor_hang(self) -> None:
        # Sanity-verify the promoted public images; --offline avoids the online
        # Rekor lookup that hung the nightly self-verify (vd-studio cc217782).
        self.assertIn("cosign verify", self.raw)
        self.assertIn("--offline", self.raw)
        self.assertIn("cosign-release: v2.5.2", self.raw)

    def test_uses_app_token_not_personal_pat(self) -> None:
        # Cross-repo read of vd-studio's run artifacts uses a minted GitHub App
        # token (vibedata-gha-app), not a personal PAT.
        self.assertIn("create-github-app-token", self.raw)
        self.assertIn("VIBEDATA_GHA_APP_ID", self.raw)
        self.assertNotIn("STUDIO_ARTIFACTS_TOKEN", self.raw)

    def test_payload_gate_requires_the_released_build_identity(self) -> None:
        # A release cannot publish documentation that does not name its own
        # build: candidate_tag, candidate_sha and release_notes_body are all
        # required and non-blank, and the publish fails otherwise.
        self.assertIn("missing candidate_sha", self.raw)
        self.assertIn("missing release_notes_body", self.raw)
        self.assertIn("missing source_workflow_run_id", self.raw)

    def test_publishes_operator_documentation_to_pages(self) -> None:
        # The docs job writes the generated release page, builds VitePress, and
        # deploys the artifact to GitHub Pages.
        self.assertIn("docs/release.md", self.raw)
        self.assertIn("npm ci", self.raw)
        self.assertIn("npm run docs:build", self.raw)
        self.assertIn("actions/upload-pages-artifact", self.raw)
        self.assertIn("actions/deploy-pages", self.raw)

    def _docs_release_step_run(self) -> str:
        docs = self.wf["jobs"]["docs"]
        for step in docs["steps"]:
            if step.get("name") == "Generate the release identity and notes":
                return step["run"]
        self.fail("docs job has no 'Generate the release identity and notes' step")

    def test_docs_release_page_interpolates_the_released_identity_and_notes(
        self,
    ) -> None:
        # The generated release page must actually carry the released version,
        # the studio commit, and the release notes. These are the exact shell
        # tokens in the docs step's heredoc; deleting any interpolation fails.
        run = self._docs_release_step_run()
        self.assertIn('echo "# Release ${TAG}"', run)
        self.assertIn("built from studio commit \\`${SHA}\\`.", run)
        self.assertIn("printf '%s\\n' \"$NOTES\"", run)

    def test_docs_job_is_gated_on_the_publish_job(self) -> None:
        # The docs job only runs after the GitHub Release (and its payload gate)
        # succeeded, and it consumes the identity the publish job validated.
        self.assertEqual(self.wf["jobs"]["docs"]["needs"], "publish")

    def test_docs_job_has_pages_permissions_and_environment(self) -> None:
        docs = self.wf["jobs"]["docs"]
        self.assertEqual(docs["permissions"].get("pages"), "write")
        self.assertEqual(docs["permissions"].get("id-token"), "write")
        self.assertEqual(docs["environment"]["name"], "github-pages")

    def test_minimal_permissions(self) -> None:
        perms = self.wf["permissions"]
        self.assertEqual(perms.get("contents"), "write")


if __name__ == "__main__":
    unittest.main()
