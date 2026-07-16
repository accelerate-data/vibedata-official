"""Shape tests for the Studio release publish pipeline (.github/workflows/publish.yml).

The publish pipeline is triggered by a `studio-release` repository_dispatch from
accelerate-data/vd-studio's deploy.yml AFTER that workflow has already promoted
the images (crane copy, signatures preserved) into the public studio-* packages
and synced the operator wiki. This workflow therefore must NOT re-promote the
images; it downloads the studio-built release artifacts and creates the GitHub
Release. See vd-studio
docs/design/devops/03-release-promotion.md for the canonical contract.
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
        # New contract from deploy.yml: candidate_tag/version/source_workflow_run_id.
        self.assertIn("candidate_tag", self.raw)
        self.assertIn("source_workflow_run_id", self.raw)

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

    def test_attaches_cli_binaries_install_script_and_wiki_tarball(self) -> None:
        self.assertIn("vibedata-", self.raw)  # the 4 platform binaries
        self.assertIn("install.sh", self.raw)
        self.assertIn("wiki-", self.raw)

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

    def test_minimal_permissions(self) -> None:
        perms = self.wf["permissions"]
        self.assertEqual(perms.get("contents"), "write")


if __name__ == "__main__":
    unittest.main()
