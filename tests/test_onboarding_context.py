from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "plugins/vibedata-repo-skills/skills/onboarding-vibedata/scripts"
FIXTURES = ROOT / "tests/fixtures/onboarding"


def write(root, path, content):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def write_json(root, path, value):
    write(root, path, json.dumps(value, indent=2) + "\n")


def mapped_repo(root):
    files = {
        "AGENTS.md": "Read repo-map.json.\n",
        "docs/glossary.md": "# Vocabulary\nNo domain terms established.\n",
        "docs/onboarding.md": "# Status\nExecution unverified.\n",
        ".agents/rules/python.md": "# Python\nPreserve CSV compatibility.\n",
        "repo-map.schema.json": '{"type":"object"}\n',
    }
    for path, text in files.items():
        write(root, path, text)
    data = {
        "modules": {},
        "sources": {},
        "entrypoints": {},
        "commands": {},
        "key_references": {
            "agents": "AGENTS.md",
            "instructions": "AGENTS.md",
            "rules": ".agents/rules",
            "schema": "repo-map.schema.json",
            "test_map": "test-map.json",
        },
        "artifact_paths": {
            "context": "docs/glossary.md",
            "adr": "decisions/DEC-{id}-{slug}.md",
            "design_record_model": "docs/design/{layer}/{model}.md",
            "design_record_pipeline": "docs/pipelines/{pipeline}.md",
            "review": "docs/review/{date}-{slug}.md",
            "proposal": "docs/proposal/{id}-{slug}.md",
            "onboarding_report": "docs/onboarding.md",
        },
        "notes_for_agents": {"startup": "Read mapped rules before edits."},
        "customer_extension": {"keep": True},
    }
    write_json(root, "repo-map.json", data)
    write_json(
        root,
        "test-map.json",
        {"taxonomy": {}, "modules": {}, "gaps": ["No business tests."]},
    )
    return data


def hashes(root):
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in root.rglob("*")
        if p.is_file() and not p.is_symlink()
    }


class OnboardingContextTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="onboarding-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()

    def helper(self, name):
        path = SCRIPTS / f"{name}.py"
        self.assertTrue(path.is_file(), f"Missing required helper: {path.name}")
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def inspect(self):
        return self.helper("inspect_repo").inspect_repository(self.root)

    def validate(self):
        return self.helper("validate_context").validate_context(self.root)

    def test_inspection_does_not_execute_or_disclose(self):
        shutil.copytree(FIXTURES / "python", self.root, dirs_exist_ok=True)
        write(self.root, ".env", "TOKEN=SECRET_SENTINEL\n")
        notebook = json.loads((self.root / "analysis.ipynb").read_text())
        notebook["cells"][0]["outputs"] = [
            {"output_type": "stream", "text": "OUTPUT_SENTINEL"}
        ]
        write_json(self.root, "analysis.ipynb", notebook)
        before = hashes(self.root)
        result = json.dumps(self.inspect())
        self.assertNotIn("SECRET_SENTINEL", result)
        self.assertNotIn("OUTPUT_SENTINEL", result)
        self.assertNotIn("load_items", result)
        self.assertNotIn(".env", result)
        self.assertFalse((self.root / "EXECUTED_MARKER").exists())
        self.assertEqual(before, hashes(self.root))

    def test_inspection_preserves_python_estate(self):
        shutil.copytree(FIXTURES / "python", self.root, dirs_exist_ok=True)
        result = self.inspect()
        self.assertEqual(result["mode"], "brownfield")
        self.assertIn("scripts/clean_items.py", result["code_files"])
        self.assertIn("analysis.ipynb", result["code_files"])
        self.assertNotIn("dlt", result.get("stacks", []))

    def test_instruction_only_repo_is_greenfield(self):
        shutil.copytree(FIXTURES / "only_claude", self.root, dirs_exist_ok=True)
        write(self.root, "requirements.txt", "dlt\n")
        result = self.inspect()
        self.assertEqual(result["mode"], "greenfield")
        self.assertIn("CLAUDE.md", result["instruction_files"])

    def test_generated_context_tools_do_not_become_application_code(self):
        for path in (
            ".agents/checks/validate_context.py",
            ".claude/skills/example/helper.py",
            ".codex/tools/example.py",
        ):
            write(self.root, path, "import dlt\n")
        result = self.inspect()
        self.assertEqual(result["mode"], "greenfield")
        self.assertEqual(result["code_files"], [])
        self.assertEqual(result["stacks"], [])
        self.assertEqual(len(result["existing_artifacts"]), 3)

    def test_inventory_respects_git_ignores_and_generated_trees(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        write(self.root, ".gitignore", "private/\n")
        for path in [
            "private/ignore.py",
            "target/ignore.py",
            "data/ignore.py",
            "src/keep.py",
        ]:
            write(self.root, path, "pass\n")
        self.assertEqual(self.inspect()["code_files"], ["src/keep.py"])

    def test_inventory_handles_tracked_deletion_but_rejects_broken_symlink(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        write(self.root, "removed.py", "pass\n")
        subprocess.run(["git", "-C", str(self.root), "add", "removed.py"], check=True)
        (self.root / "removed.py").unlink()
        write(self.root, "live.py", "pass\n")
        self.assertEqual(self.inspect()["code_files"], ["live.py"])
        (self.root / "broken.py").symlink_to("missing.py")
        with self.assertRaisesRegex(ValueError, "broken.py"):
            self.inspect()

    def test_malformed_notebook_fails_without_source_disclosure(self):
        write(self.root, "bad.ipynb", "{SECRET_SENTINEL")
        with self.assertRaisesRegex(ValueError, "bad.ipynb") as caught:
            self.inspect()
        self.assertNotIn("SECRET_SENTINEL", str(caught.exception))

    def test_context_resolves_custom_paths_and_patterns(self):
        data = mapped_repo(self.root)
        before = hashes(self.root)
        self.assertEqual(self.validate(), [])
        self.assertEqual(before, hashes(self.root))
        self.assertFalse((self.root / "decisions").exists())
        self.assertEqual(data["artifact_paths"]["adr"], "decisions/DEC-{id}-{slug}.md")

    def test_context_rejects_missing_registered_artifact(self):
        data = mapped_repo(self.root)
        data["sources"]["items"] = {
            "kind": "python",
            "module": "missing.py",
            "required_artifacts": ["module", "tests"],
        }
        write_json(self.root, "repo-map.json", data)
        findings = "\n".join(self.validate())
        self.assertIn("missing.py", findings)
        self.assertIn("tests", findings)

    def test_custom_required_artifact_values_are_validated(self):
        for value in ("missing/schema.yml", "../outside.yml", {}, [], ["absent.yml"]):
            with self.subTest(value=value):
                data = mapped_repo(self.root)
                data["sources"]["items"] = {
                    "kind": "python",
                    "required_artifacts": ["schema"],
                    "schema": value,
                }
                write_json(self.root, "repo-map.json", data)
                self.assertIn("schema", "\n".join(self.validate()))
        data["sources"]["items"]["schema"] = "docs/glossary.md"
        write_json(self.root, "repo-map.json", data)
        self.assertEqual(self.validate(), [])

    def test_owned_module_and_source_constraints(self):
        for entry in ({}, {"path": ""}, {"path": ["docs/glossary.md"]}):
            with self.subTest(entry=entry):
                data = mapped_repo(self.root)
                data["modules"]["broken"] = entry
                write_json(self.root, "repo-map.json", data)
                self.assertIn("modules.broken", "\n".join(self.validate()))
        data = mapped_repo(self.root)
        data["sources"]["broken"] = {"kind": ""}
        write_json(self.root, "repo-map.json", data)
        self.assertIn("sources.broken", "\n".join(self.validate()))

    def test_inline_import_targets_and_cycles_exclude_examples(self):
        mapped_repo(self.root)
        write(self.root, "AGENTS.md", "Follow @missing.md for policy.\n")
        self.assertIn("missing.md", "\n".join(self.validate()))
        write(self.root, "AGENTS.md", "Follow @docs/policy.md for policy.\n")
        write(self.root, "docs/policy.md", "Also follow @../AGENTS.md.\n")
        self.assertIn("cycle", "\n".join(self.validate()).lower())
        write(
            self.root,
            "AGENTS.md",
            "Example `@missing.md`; contact reader@example.com.\n"
            "```text\n@another-missing.md\n```\n"
            "Follow @docs/glossary.md, then stop.\n",
        )
        self.assertEqual(self.validate(), [])

    def test_empty_inventory_has_no_fake_coverage(self):
        mapped_repo(self.root)
        self.assertEqual(self.validate(), [])
        write_json(
            self.root,
            "test-map.json",
            {
                "taxonomy": {},
                "modules": {
                    "python": {"sources": ["missing.py"], "unit": ["tests/missing.py"]}
                },
            },
        )
        findings = "\n".join(self.validate())
        self.assertIn("missing.py", findings)
        self.assertIn("tests/missing.py", findings)

    def test_structural_test_paths_are_validated_without_execution(self):
        mapped_repo(self.root)
        write(self.root, "tests/check_maps.py", "raise RuntimeError('must not run')\n")
        module = {"sources": ["repo-map.json"]}
        for paths, expected in (
            (["tests/check_maps.py"], None),
            (["tests/missing.py"], "registered path is missing"),
            (["../outside.py"], "path escapes"),
            ("tests/check_maps.py", "expected a list"),
        ):
            with self.subTest(paths=paths):
                module["structural"] = paths
                write_json(
                    self.root,
                    "test-map.json",
                    {"taxonomy": {}, "modules": {"maps": module}},
                )
                before = hashes(self.root)
                findings = self.validate()
                if expected is None:
                    self.assertEqual(findings, [])
                else:
                    self.assertIn(
                        "test-map.modules.maps.structural", "\n".join(findings)
                    )
                    self.assertIn(expected, "\n".join(findings))
                self.assertEqual(before, hashes(self.root))

    def test_context_rejects_escape_and_cycles(self):
        for unsafe in (
            "../outside.md",
            "/tmp/outside.md",
            "C:\\outside.md",
            "docs/{bad-name}.md",
        ):
            with self.subTest(unsafe=unsafe):
                data = mapped_repo(self.root)
                data["artifact_paths"]["context"] = unsafe
                write_json(self.root, "repo-map.json", data)
                self.assertTrue(self.validate())
        mapped_repo(self.root)
        write(self.root, "AGENTS.md", "@CLAUDE.md\n")
        write(self.root, "CLAUDE.md", "@AGENTS.md\n")
        self.assertIn("cycle", "\n".join(self.validate()).lower())

    def test_external_symlink_and_same_file_alias(self):
        mapped_repo(self.root)
        outside = self.root.parent / "outside.md"
        outside.write_text("EXTERNAL_SENTINEL\n")
        (self.root / "AGENTS.md").unlink()
        (self.root / "AGENTS.md").symlink_to(outside)
        findings = "\n".join(self.validate())
        self.assertIn("outside", findings.lower())
        self.assertNotIn("EXTERNAL_SENTINEL", findings)
        (self.root / "AGENTS.md").unlink()
        write(self.root, "AGENTS.md", "# Instructions\n")
        (self.root / "CLAUDE.md").symlink_to("AGENTS.md")
        self.assertIn("alias", "\n".join(self.validate()).lower())
        self.assertEqual(outside.read_text(), "EXTERNAL_SENTINEL\n")

    def test_hardlink_instruction_alias_is_reported(self):
        mapped_repo(self.root)
        (self.root / "CLAUDE.md").hardlink_to(self.root / "AGENTS.md")
        self.assertIn("alias", "\n".join(self.validate()).lower())

    def test_wrapper_and_moved_links_preserve_targets(self):
        mapped_repo(self.root)
        write(
            self.root,
            "AGENTS.md",
            "For Python, read [policy](.agents/rules/python.md).\n",
        )
        write(self.root, "CLAUDE.md", "@AGENTS.md\n")
        write(
            self.root,
            ".agents/rules/python.md",
            "Read [vocabulary](../../docs/glossary.md).\n",
        )
        self.assertEqual(self.validate(), [])
        write(
            self.root,
            ".agents/rules/python.md",
            "Read [vocabulary](docs/glossary.md).\n",
        )
        self.assertIn("glossary.md", "\n".join(self.validate()))

    def test_validation_is_read_only(self):
        data = mapped_repo(self.root)
        data["commands"] = {"danger": "touch EXECUTED_MARKER"}
        write_json(self.root, "repo-map.json", data)
        before = hashes(self.root)
        self.assertEqual(self.validate(), [])
        self.assertEqual(before, hashes(self.root))

    def test_validation_checks_types_and_exact_case(self):
        data = mapped_repo(self.root)
        data["sources"] = []
        write_json(self.root, "repo-map.json", data)
        self.assertIn("sources", "\n".join(self.validate()))
        mapped_repo(self.root)
        (self.root / "AGENTS.md").rename(self.root / "agents.md")
        self.assertIn("case", "\n".join(self.validate()).lower())

    def test_legacy_notes_and_entrypoint_lists_remain_valid(self):
        data = mapped_repo(self.root)
        data["notes_for_agents"] = ["Keep the human note."]
        data["entrypoints"] = ["AGENTS.md"]
        write_json(self.root, "repo-map.json", data)
        self.assertEqual(self.validate(), [])

    def test_helpers_use_explicit_root_from_another_cwd(self):
        mapped_repo(self.root)
        for name in ("inspect_repo", "validate_context"):
            self.helper(name)
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / f"{name}.py"), "--root", str(self.root)],
                cwd=self.root.parent,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertFalse((self.root.parent / "repo-map.json").exists())
