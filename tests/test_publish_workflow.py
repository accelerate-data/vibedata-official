"""Structural tests for .github/workflows/publish.yml (VD-2014).

These tests verify the publish pipeline contract without invoking the
workflow itself — that is, no GitHub state is mutated by running them.
They guard against accidental changes to:

* the trigger (must be repository_dispatch.types: [studio-release])
* permissions (contents:write, packages:write, id-token:write)
* the trust boundary (cosign verify must run BEFORE docker push)
* the public package coordinates
* the smoke-test step (must docker logout before docker pull)
* the manifest commit + GH release creation
"""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLISH_YML = REPO_ROOT / ".github" / "workflows" / "publish.yml"


def _load_workflow() -> dict:
    with PUBLISH_YML.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _job(wf: dict, name: str) -> dict:
    jobs = wf.get("jobs", {})
    assert name in jobs, f"missing job: {name}"
    return jobs[name]


def _step_text(job: dict) -> str:
    parts = []
    for step in job.get("steps", []):
        for field in ("name", "run", "uses"):
            value = step.get(field)
            if value:
                parts.append(str(value))
        env = step.get("env") or {}
        parts.append(" ".join(f"{k}={v}" for k, v in env.items()))
        with_block = step.get("with") or {}
        parts.append(" ".join(f"{k}={v}" for k, v in with_block.items()))
    return "\n".join(parts)


class PublishTriggerTests(unittest.TestCase):
    def test_workflow_file_exists(self) -> None:
        self.assertTrue(PUBLISH_YML.exists(), "publish.yml must exist")

    def test_repository_dispatch_trigger(self) -> None:
        wf = _load_workflow()
        # PyYAML parses YAML key `on` as boolean True; handle both.
        on = wf.get("on") if "on" in wf else wf.get(True)
        self.assertIsNotNone(on, "workflow must declare an 'on' trigger")
        self.assertIn("repository_dispatch", on)
        rd = on["repository_dispatch"]
        self.assertIn("studio-release", rd.get("types", []))

    def test_permissions(self) -> None:
        wf = _load_workflow()
        perms = wf.get("permissions", {})
        # Required to push public packages, commit manifest, and verify cosign signature.
        self.assertEqual(perms.get("contents"), "write")
        self.assertEqual(perms.get("packages"), "write")
        self.assertEqual(perms.get("id-token"), "write")


class PublishJobShapeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.wf = _load_workflow()
        self.job = _job(self.wf, "publish")

    def test_payload_validation_step_exists(self) -> None:
        names = [s.get("name", "") for s in self.job.get("steps", [])]
        self.assertTrue(
            any("Validate" in n and "payload" in n.lower() for n in names),
            "publish job must validate the dispatch payload",
        )

    def test_cosign_install_present(self) -> None:
        uses = [s.get("uses", "") for s in self.job.get("steps", [])]
        self.assertTrue(
            any(u.startswith("sigstore/cosign-installer") for u in uses),
            "cosign-installer is required to verify signatures",
        )

    def test_cosign_verify_runs_before_docker_push(self) -> None:
        """Trust boundary: signature verification gates the public push."""
        steps = self.job.get("steps", [])
        first_verify = None
        first_push = None
        for idx, step in enumerate(steps):
            run = step.get("run", "") or ""
            if "cosign verify" in run and first_verify is None:
                first_verify = idx
            if "docker push" in run and first_push is None:
                first_push = idx
        self.assertIsNotNone(first_verify, "missing cosign verify step")
        self.assertIsNotNone(first_push, "missing docker push step")
        self.assertLess(
            first_verify,
            first_push,
            "cosign verify must run before any docker push",
        )

    def test_pull_by_digest_then_retag(self) -> None:
        """Public push must use the signed digest, not a mutable tag."""
        text = _step_text(self.job)
        self.assertIn("@${{ steps.payload.outputs.fe_digest }}", text)
        self.assertIn("@${{ steps.payload.outputs.be_digest }}", text)
        self.assertIn("docker pull", text)
        self.assertIn("docker tag", text)

    def test_pushes_to_public_coordinates(self) -> None:
        # Public coordinates live in workflow env to keep step bodies short.
        env = self.wf.get("env", {}) or {}
        fe = env.get("PUBLIC_FE_PACKAGE", "")
        be = env.get("PUBLIC_BE_PACKAGE", "")
        self.assertIn("vibedata-studio-frontend", fe)
        self.assertIn("vibedata-studio-backend", be)
        self.assertTrue(fe.startswith("ghcr.io/accelerate-data/"))
        self.assertTrue(be.startswith("ghcr.io/accelerate-data/"))

        text = _step_text(self.job)
        self.assertIn("PUBLIC_FE_PACKAGE", text)
        self.assertIn("PUBLIC_BE_PACKAGE", text)

    def test_commits_release_manifest_under_releases_dir(self) -> None:
        text = _step_text(self.job)
        self.assertIn("releases/v", text)
        self.assertIn("release-manifest.json", text)
        self.assertIn("git commit", text)

    def test_creates_github_release(self) -> None:
        text = _step_text(self.job)
        self.assertIn("gh release create", text)

    def test_smoke_test_runs_anonymous_pull(self) -> None:
        """`docker logout` MUST appear before the smoke-test pull to prove
        anonymous access works — this is the customer-outcome guard."""
        steps = self.job.get("steps", [])
        logout_idx = None
        smoke_pull_idx = None
        for idx, step in enumerate(steps):
            run = step.get("run", "") or ""
            name = (step.get("name") or "").lower()
            if "docker logout" in run:
                logout_idx = idx
            if "smoke" in name and "docker pull" in run:
                smoke_pull_idx = idx
        self.assertIsNotNone(logout_idx, "smoke test must run docker logout first")
        self.assertIsNotNone(smoke_pull_idx, "smoke test must perform docker pull")
        self.assertLessEqual(
            logout_idx,
            smoke_pull_idx,
            "docker logout must precede the smoke-test pull",
        )


class PublishCosignIdentityTests(unittest.TestCase):
    """The cosign verify command must pin Studio's OIDC identity, otherwise
    any signed image could promote itself to the public coordinates."""

    def setUp(self) -> None:
        self.wf = _load_workflow()
        env = self.wf.get("env", {}) or {}
        self.identity_regexp = env.get("COSIGN_IDENTITY_REGEXP", "")
        self.oidc_issuer = env.get("COSIGN_OIDC_ISSUER", "")

    def test_oidc_issuer_is_github_actions(self) -> None:
        self.assertEqual(
            self.oidc_issuer,
            "https://token.actions.githubusercontent.com",
        )

    def test_identity_regexp_pins_studio_release_workflow(self) -> None:
        self.assertIn("accelerate-data/vd-studio", self.identity_regexp)
        # Identity is a regex — dots are escaped. Check normalised form.
        normalised = self.identity_regexp.replace("\\.", ".")
        self.assertIn(".github/workflows/release.yml", normalised)
        self.assertIn("refs/tags/v", normalised)


if __name__ == "__main__":
    unittest.main()
