from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/vibedata-repo-skills"
SKILL = PLUGIN / "skills/onboarding-vibedata"


class OnboardingTemplateTests(unittest.TestCase):
    def test_skill_identity_and_conditional_references(self):
        self.assertTrue((SKILL / "SKILL.md").is_file(), "Shared skill is missing")
        text = (SKILL / "SKILL.md").read_text()
        self.assertLess(len(text.split()), 400)
        metadata = yaml.safe_load(text.split("---", 2)[1])
        self.assertEqual(metadata["name"], "onboarding-vibedata")
        self.assertTrue(metadata["description"].strip())
        for name in ("brownfield", "greenfield", "artifact-contract", "compatibility"):
            self.assertIn(f"references/{name}.md", text)
            self.assertTrue((SKILL / f"references/{name}.md").is_file())

    def test_review_template_has_typed_run_metadata(self):
        text = (SKILL / "templates/review.md").read_text()
        rendered = re.sub(r"\{\{[a-z_]+\}\}", "confirmed-value", text)
        self.assertTrue(rendered.startswith("---\n"))
        metadata = yaml.safe_load(rendered.split("---", 2)[1])
        self.assertEqual(set(metadata), {"type", "date", "commit", "source"})
        self.assertEqual(metadata["type"], "onboarding")

    def test_skill_requires_explicit_user_invocation_in_both_runtimes(self):
        metadata = yaml.safe_load((SKILL / "SKILL.md").read_text().split("---", 2)[1])
        with self.subTest(runtime="claude"):
            self.assertIs(metadata.get("disable-model-invocation"), True)
            self.assertIs(metadata.get("user-invocable", True), True)
        with self.subTest(runtime="codex"):
            path = SKILL / "agents/openai.yaml"
            self.assertTrue(path.is_file(), "Codex invocation policy is missing")
            config = yaml.safe_load(path.read_text())
            self.assertIs(config["policy"]["allow_implicit_invocation"], False)

    def test_all_local_document_links_resolve(self):
        self.assertTrue((SKILL / "SKILL.md").is_file())
        for path in SKILL.rglob("*.md"):
            if "templates" in path.parts:
                continue
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                self.assertTrue(
                    (path.parent / target.split("#")[0]).exists(),
                    f"{path.name}: {target}",
                )

    def test_empty_map_templates_conform_and_validate(self):
        for name in ("repo-map.schema.json", "repo-map.json", "test-map.json"):
            self.assertTrue((SKILL / "templates" / name).is_file(), f"Missing {name}")
        data = json.loads((SKILL / "templates/repo-map.json").read_text())
        schema = json.loads((SKILL / "templates/repo-map.schema.json").read_text())
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(data, schema)
        self.assertEqual(data["sources"], {})
        with tempfile.TemporaryDirectory(prefix="onboarding-template-") as tmp:
            root = Path(tmp)
            for name in ("repo-map.schema.json", "repo-map.json", "test-map.json"):
                shutil.copy(SKILL / "templates" / name, root / name)
            (root / "AGENTS.md").write_text("Read repo-map.json.\n")
            (root / "CONTEXT.md").write_text(
                "# Vocabulary\nNo domain terms established.\n"
            )
            (root / "docs").mkdir()
            (root / "docs/onboarding.md").write_text(
                "# Status\nExecution unverified.\n"
            )
            (root / ".agents/skills").mkdir(parents=True)
            (root / ".agents/checks").mkdir()
            shutil.copy(
                SKILL / "scripts/validate_context.py",
                root / ".agents/checks/validate_context.py",
            )
            (root / "tests").mkdir()
            for name in ("test_adr_links.py", "test_maps.py"):
                shutil.copy(SKILL / "templates/checks" / name, root / "tests" / name)
            result = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    str(root / ".agents/checks/validate_context.py"),
                    "--root",
                    str(root),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Context structure valid", result.stdout)

    def test_generic_templates_and_rule_set(self):
        templates = SKILL / "templates"
        for name in (
            "agents",
            "glossary",
            "adr-index",
            "onboarding-report",
            "review",
            "proposal",
        ):
            self.assertTrue((templates / f"{name}.md").is_file(), f"Missing {name}")
        expected = {
            "dbt-models",
            "sql-style",
            "dbt-testing",
            "dlt",
            "python",
            "context",
            "adr",
            "design-records",
            "git-and-prs",
            "workarounds",
        }
        self.assertEqual(
            {p.stem for p in (templates / "skills").glob("*.md")}, expected
        )
        for path in templates.rglob("*"):
            if path.is_file():
                self.assertNotRegex(
                    path.read_text(), r"(?i)nyc.?taxi|trip_key|tlc_pipeline|ops_raw"
                )

    def test_convention_templates_render_valid_metadata(self):
        paths = list((SKILL / "templates/skills").glob("*.md"))
        self.assertEqual(len(paths), 10)
        for path in paths:
            with self.subTest(name=path.stem):
                text = re.sub(
                    r"\{\{[a-z_]+\}\}", "confirmed repository value", path.read_text()
                )
                metadata = yaml.safe_load(text.split("---", 2)[1])
                self.assertEqual(metadata["name"], path.stem)
                self.assertIsInstance(metadata["description"], str)
                self.assertTrue(metadata["description"].strip())
                self.assertNotIn("{{", text)
        with self.assertRaises(yaml.YAMLError):
            yaml.safe_load("name: [broken\ndescription: invalid\n")

    def test_greenfield_python_recipe_compiles(self):
        path = SKILL / "templates/greenfield/README.md"
        self.assertTrue(path.is_file(), "Greenfield recipe is missing")
        snippets = re.findall(r"```python\n(.*?)```", path.read_text(), re.DOTALL)
        self.assertTrue(snippets, "Recipe must include a Python starter template")
        for source in snippets:
            ast.parse(source)


class OnboardingDistributionTests(unittest.TestCase):
    def test_dual_manifest_identity_and_single_skill_source(self):
        manifests = []
        for runtime in ("claude", "codex"):
            path = PLUGIN / f".{runtime}-plugin/plugin.json"
            self.assertTrue(path.is_file(), f"Missing {runtime} manifest")
            manifests.append(json.loads(path.read_text()))
        self.assertEqual(manifests[0]["name"], "vibedata-repo-skills")
        for key in ("name", "version", "description", "license"):
            self.assertEqual(manifests[0][key], manifests[1][key])
        self.assertEqual(manifests[0]["license"], "Elastic-2.0")
        self.assertNotIn("skills", manifests[0])
        self.assertEqual(manifests[1]["skills"], "./skills/")
        self.assertEqual(list(PLUGIN.glob("**/SKILL.md")), [SKILL / "SKILL.md"])

    def test_marketplace_and_catalog_discovery(self):
        claude = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        codex = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        for data in (claude, codex):
            self.assertEqual(
                sum(p["name"] == "vibedata-repo-skills" for p in data["plugins"]), 1
            )
        c = next(p for p in claude["plugins"] if p["name"] == "vibedata-repo-skills")
        x = next(p for p in codex["plugins"] if p["name"] == "vibedata-repo-skills")
        self.assertEqual(c["source"], "./plugins/vibedata-repo-skills")
        self.assertEqual(x["source"]["path"], c["source"])
        self.assertEqual(c["license"], "Elastic-2.0")
        catalog = json.loads((ROOT / "catalog/catalog.json").read_text())
        entries = [
            e
            for e in catalog["entries"]["skills"]
            if e["name"] == "onboarding-vibedata"
        ]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["plugin"], "vibedata-repo-skills")
