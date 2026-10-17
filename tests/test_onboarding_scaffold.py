from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import jsonschema
import yaml
from test_onboarding_context import mapped_repo, write, write_json

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "plugins/vibedata-repo-skills/skills/onboarding-vibedata/templates"


def load_module(path, source):
    spec = importlib.util.spec_from_file_location(path.stem, source)
    module = importlib.util.module_from_spec(spec)
    # Attribute rendered execution to retained source so coverage survives cleanup.
    exec(compile(path.read_text(), str(source), "exec"), module.__dict__)  # noqa: S102 -- trusted repository templates
    module.ROOT = path.resolve().parents[1]
    return module


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="onboarding-scaffold-")
        self.addCleanup(self.temp.cleanup)
        self.root = (Path(self.temp.name) / "repo").resolve()
        self.root.mkdir()
        self.repo = mapped_repo(self.root)
        self.repo["artifact_paths"]["adr"] = "decisions/{id}.md"
        write_json(self.root, "repo-map.json", self.repo)

    def template(self, name, destination):
        source = TEMPLATES / name
        self.assertTrue(source.is_file(), f"Missing generated template: {name}")
        text = source.read_text().replace("<project_name>", "data_project")
        write(self.root, destination, text)
        return self.root / destination

    def adr_check(self):
        path = self.template("checks/test_adr_links.py", "tests/test_adr_links.py")
        return load_module(
            path, TEMPLATES / "checks/test_adr_links.py"
        ).validate_adr_links(self.root)

    def decision(
        self, adr="decisions/DEC-alpha.md", design="docs/design/core/items.md"
    ):
        write(
            self.root,
            adr,
            "# Decision\n\n## Affected designs\n[Items](../docs/design/core/items.md)\n",
        )
        write(
            self.root, design, "# Items\n[Decision](../../../decisions/DEC-alpha.md)\n"
        )

    def test_adr_links_require_both_directions(self):
        self.decision()
        self.assertEqual(self.adr_check(), [])
        write(self.root, "decisions/DEC-alpha.md", "# Decision\n")
        self.assertIn("backlink", "\n".join(self.adr_check()).lower())
        self.decision()
        write(self.root, "docs/design/core/items.md", "# Items\n")
        self.assertIn("cite", "\n".join(self.adr_check()).lower())

    def test_adr_links_support_custom_paths_and_linked_ids(self):
        self.decision()
        self.assertEqual(self.adr_check(), [])
        result = subprocess.run(
            [
                sys.executable,
                str(self.root / "tests/test_adr_links.py"),
                "--root",
                str(self.root),
            ],
            cwd=self.root.parent,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / "docs/adr").exists())
        write(
            self.root,
            "decisions/0007-choice.md",
            "# Decision\n## Affected designs\n[Items](../docs/design/core/items.md)\n",
        )
        write(
            self.root,
            "docs/design/core/items.md",
            "ADR 0007\n[Alpha](../../../decisions/DEC-alpha.md)\n",
        )
        self.assertEqual(self.adr_check(), [])

    def test_adr_links_reject_missing_or_escaped_targets(self):
        self.decision()
        for value in ("missing.md", "../../../../outside.md"):
            with self.subTest(value=value):
                write(self.root, "docs/design/core/items.md", f"[Decision]({value})\n")
                self.assertTrue(self.adr_check())
        outside = self.root.parent / "outside.md"
        outside.write_text("SECRET_SENTINEL")
        write(
            self.root,
            "docs/design/core/items.md",
            "[Decision](../../../decisions/escape.md)\n",
        )
        (self.root / "decisions/escape.md").symlink_to(outside)
        findings = "\n".join(self.adr_check())
        self.assertIn("outside", findings)
        self.assertNotIn("SECRET_SENTINEL", findings)

    def test_adr_links_handle_rejected_and_successor_records(self):
        self.decision()
        write(
            self.root,
            "decisions/DEC-alpha.md",
            "---\nstatus: rejected\n---\n# Old\n## Superseded by\n[Beta](DEC-beta.md)\n## Affected designs\n[Items](../docs/design/core/items.md)\n",
        )
        write(
            self.root,
            "decisions/DEC-beta.md",
            "# New\n## Affected designs\n[Items](../docs/design/core/items.md)\n",
        )
        self.assertIn("successor", "\n".join(self.adr_check()).lower())
        write(
            self.root,
            "docs/design/core/items.md",
            "[Beta](../../../decisions/DEC-beta.md)\n",
        )
        self.assertEqual(self.adr_check(), [])
        write(
            self.root,
            "decisions/DEC-alpha.md",
            "---\nstatus: rejected\n---\n[Broken](missing.md)\n",
        )
        self.assertIn("missing", "\n".join(self.adr_check()).lower())

    def test_adr_affected_link_outside_mapped_designs_is_not_silently_ignored(self):
        self.decision()
        write(self.root, "notes/other.md", "# Other design\n")
        write(
            self.root,
            "decisions/DEC-alpha.md",
            "# Decision\n## Affected designs\n[Other](../notes/other.md)\n",
        )
        self.assertIn("notes/other.md", "\n".join(self.adr_check()))

    def test_ingest_rejects_escaped_pipeline_before_launch(self):
        ingest = self.orchestration("run_ingest")
        outside = self.root.parent / "outside.py"
        outside.write_text("raise AssertionError('must not execute')\n")
        self.repo["sources"]["outside"] = {"kind": "dlt", "pipeline": "../outside.py"}
        write_json(self.root, "repo-map.json", self.repo)
        with (
            patch.object(
                ingest.subprocess, "run", side_effect=AssertionError("must not launch")
            ),
            self.assertRaisesRegex(ValueError, "pipeline"),
        ):
            ingest.run_ingest(self.root / "chosen.duckdb")

    def test_native_map_checks_preserve_schema_config_and_selectors(self):
        path = self.template("checks/test_maps.py", "tests/test_maps.py")
        native = load_module(path, TEMPLATES / "checks/test_maps.py")
        native.test_repo_map_schema()
        write_json(
            self.root,
            "repo-map.schema.json",
            {"type": "object", "required": ["customer_contract"]},
        )
        with self.assertRaises(jsonschema.ValidationError):
            native.test_repo_map_schema()
        self.repo["customer_contract"] = "preserved"
        write_json(self.root, "repo-map.json", self.repo)
        native.test_repo_map_schema()
        self.repo["artifact_paths"]["source_config"] = "ingestion/.dlt/config.toml"
        self.repo["sources"]["crm"] = {"kind": "dlt", "config_section": "sources.crm"}
        write_json(self.root, "repo-map.json", self.repo)
        write(self.root, "ingestion/.dlt/config.toml", "[sources.other]\n")
        with self.assertRaisesRegex(AssertionError, "sources.crm"):
            native.test_source_config_sections()
        write(self.root, "ingestion/.dlt/config.toml", "[sources.crm]\n")
        native.test_source_config_sections()
        self.repo["artifact_paths"]["dbt_project"] = "transformation/dbt_project.yml"
        self.repo["artifact_paths"]["dbt_profiles"] = "transformation/profiles.yml"
        write_json(self.root, "repo-map.json", self.repo)
        write(self.root, "transformation/dbt_project.yml", "name: data_project\n")
        write(self.root, "transformation/profiles.yml", "data_project: {}\n")
        write_json(
            self.root,
            "test-map.json",
            {
                "taxonomy": {},
                "modules": {"items": {"sources": [], "selectors": {"data": "items"}}},
            },
        )
        calls = []

        def fake(args, **kwargs):
            calls.append(args)
            return subprocess.CompletedProcess(args, 0, "", "")

        with (
            patch.object(native.subprocess, "run", side_effect=fake),
            self.assertRaisesRegex(AssertionError, "items"),
        ):
            native.test_dbt_selectors()
        self.assertEqual(
            calls[0][:5], [sys.executable, "-m", "dbt.cli.main", "--quiet", "ls"]
        )
        self.assertIn("items", calls[0])
        self.assertNotIn("deps", calls[0])
        with patch.object(
            native.subprocess,
            "run",
            return_value=subprocess.CompletedProcess(
                [], 0, '{"unique_id":"test.data_project.items"}\n', ""
            ),
        ):
            native.test_dbt_selectors()
        self.repo["sources"] = {}
        write_json(self.root, "repo-map.json", self.repo)
        native.test_source_config_sections()

    def test_repo_checks_workflow_runs_declared_checks(self):
        path = self.template(
            "repo/repo-checks.yml", ".github/workflows/repo-checks.yml"
        )
        workflow = yaml.safe_load(path.read_text())
        trigger = workflow.get("on", workflow.get(True))
        self.assertIn("pull_request", trigger)
        commands = "\n".join(
            s.get("run", "") for s in workflow["jobs"]["checks"]["steps"]
        )
        for command in (
            "python -m pip install -r requirements.txt -r requirements-dev.txt",
            "python -m dbt.cli.main deps",
            "python -m pytest tests/test_adr_links.py tests/test_maps.py",
            "python .agents/checks/validate_context.py --root .",
        ):
            self.assertIn(command, commands)

    def orchestration(self, name):
        return load_module(
            self.template(f"orchestration/{name}.py", f"orchestration/{name}.py"),
            TEMPLATES / f"orchestration/{name}.py",
        )

    def test_pipeline_and_dbt_share_nondefault_database(self):
        ingest = self.orchestration("run_ingest")
        transform = self.orchestration("run_transform")
        write(self.root, "ingestion/pipelines/demo.py", "pass\n")
        self.repo["sources"]["demo"] = {
            "kind": "dlt",
            "pipeline": "ingestion/pipelines/demo.py",
        }
        write_json(self.root, "repo-map.json", self.repo)
        (self.root / "transformation").mkdir()
        db = self.root.parent / "separate" / "selected.duckdb"
        calls = []

        def fake(args, **kwargs):
            calls.append((args, kwargs))
            return subprocess.CompletedProcess(args, 0)

        with (
            patch.dict(os.environ, {"ONBOARDING_DUCKDB_PATH": "/wrong/path.duckdb"}),
            patch.object(subprocess, "run", side_effect=fake),
        ):
            self.assertEqual(ingest.run_ingest(db), 0)
            self.assertEqual(transform.run_transform(db), 0)
        self.assertEqual(len(calls), 3)
        self.assertEqual(
            calls[0][0],
            [sys.executable, str(self.root / "ingestion/pipelines/demo.py")],
        )
        self.assertEqual([c[0][3] for c in calls[1:]], ["deps", "build"])
        for args, kwargs in calls:
            self.assertEqual(args[0], sys.executable)
            self.assertEqual(kwargs["env"]["ONBOARDING_DUCKDB_PATH"], str(db))
        self.assertFalse((self.root / ".local/data.duckdb").exists())

    def test_ingest_stops_before_next_pipeline(self):
        ingest = self.orchestration("run_ingest")
        for name in ("first", "second"):
            path = f"ingestion/{name}.py"
            write(self.root, path, "pass\n")
            self.repo["sources"][name] = {"kind": "dlt", "pipeline": path}
        write_json(self.root, "repo-map.json", self.repo)
        calls = []

        def fail(args, **kwargs):
            calls.append(args)
            return subprocess.CompletedProcess(args, 17)

        with patch.object(ingest.subprocess, "run", side_effect=fail):
            self.assertEqual(ingest.run_ingest(self.root / "chosen.duckdb"), 17)
        self.assertEqual(len(calls), 1)
        self.assertTrue(calls[0][1].endswith("first.py"))

    def test_registered_pipeline_can_import_sibling_source(self):
        self.orchestration("run_ingest")
        write(self.root, "ingestion/sources/crm.py", "VALUE = 43\n")
        write(
            self.root,
            "ingestion/pipelines/crm.py",
            "from sources.crm import VALUE\nprint(VALUE)\n",
        )
        self.repo["sources"]["crm"] = {
            "kind": "dlt",
            "source_module": "ingestion/sources/crm.py",
            "pipeline": "ingestion/pipelines/crm.py",
        }
        write_json(self.root, "repo-map.json", self.repo)
        env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
        result = subprocess.run(
            [
                sys.executable,
                str(self.root / "orchestration/run_ingest.py"),
                "--db-path",
                str(self.root / "selected.duckdb"),
            ],
            cwd=self.root,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "43")

    def test_transform_stops_when_deps_fail(self):
        transform = self.orchestration("run_transform")
        calls = []

        def fail(args, **kwargs):
            calls.append(args)
            return subprocess.CompletedProcess(args, 19)

        with patch.object(transform.subprocess, "run", side_effect=fail):
            self.assertEqual(transform.run_transform(self.root / "chosen.duckdb"), 19)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][3], "deps")

    def test_missing_database_path_fails_before_launch(self):
        for name in ("run_ingest", "run_transform"):
            module = self.orchestration(name)
            with (
                patch.object(
                    subprocess, "run", side_effect=AssertionError("must not launch")
                ),
                self.assertRaisesRegex(ValueError, "absolute"),
            ):
                getattr(module, name)(Path("relative.duckdb"))
            for args in ([], ["--db-path", "relative.duckdb"]):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(self.root / f"orchestration/{name}.py"),
                        *args,
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 2, result.stderr)

    def test_empty_scaffold_does_not_register_example_sources(self):
        data = json.loads((TEMPLATES / "repo-map.json").read_text())
        self.assertEqual(data["sources"], {})
        ingest = self.orchestration("run_ingest")
        with patch.object(
            ingest.subprocess,
            "run",
            side_effect=AssertionError("no registered pipeline"),
        ):
            self.assertEqual(ingest.run_ingest(self.root / "selected.duckdb"), 0)
        for p in TEMPLATES.rglob("*.py"):
            compile(p.read_text(), str(p), "exec")

    @unittest.skipUnless(
        os.environ.get("ONBOARDING_RUN_SCAFFOLD_INTEGRATION") == "1",
        "Set ONBOARDING_RUN_SCAFFOLD_INTEGRATION=1 in the selected-platform environment",
    )
    def test_selected_duckdb_scaffold_round_trip(self):
        import re
        import shutil

        import duckdb

        for name in ("run_ingest", "run_transform"):
            self.orchestration(name)
        for name in ("dbt_project.yml", "profiles.yml", "packages.yml"):
            self.template("dbt/" + name, "transformation/" + name)
        for name in ("relations.sql", "generate_schema_name.sql"):
            self.template("dbt/" + name, "transformation/macros/" + name)
        for name in ("test_adr_links.py", "test_maps.py"):
            self.template("checks/" + name, "tests/" + name)
        snippets = re.findall(
            r"```python\n(.*?)```",
            (TEMPLATES / "greenfield/README.md").read_text(),
            re.DOTALL,
        )
        pipeline = next(s for s in snippets if "def load(" in s)
        pipeline = pipeline.replace("{{pipeline_name}}", "demo").replace(
            "{{dataset_name}}", "raw"
        )
        write(
            self.root,
            "ingestion/sources/demo.py",
            """
import dlt
@dlt.resource(name='items', write_disposition='replace')
def items():
    yield [{'id': n, 'value': 42} for n in range(7)]
    yield [{'id': 99, 'value': 0}]
""",
        )
        pipeline += """
import os
from sources.demo import items
if __name__ == '__main__':
    info = load(items().add_limit(1), Path(__file__).resolve().parents[2], Path(os.environ['ONBOARDING_DUCKDB_PATH']))
    assert not info.has_failed_jobs
    assert info.loads_ids
"""
        write(self.root, "ingestion/pipelines/demo.py", pipeline)
        self.repo["sources"]["demo"] = {
            "kind": "dlt",
            "pipeline": "ingestion/pipelines/demo.py",
            "source_module": "ingestion/sources/demo.py",
            "config_section": "sources.demo",
        }
        self.repo["artifact_paths"].update(
            {
                "source_config": "ingestion/.dlt/config.toml",
                "dbt_project": "transformation/dbt_project.yml",
                "dbt_profiles": "transformation/profiles.yml",
            }
        )
        write_json(self.root, "repo-map.json", self.repo)
        write(self.root, "ingestion/.dlt/config.toml", "[sources.demo]\n")
        write(
            self.root,
            "transformation/models/sources.yml",
            "version: 2\nsources:\n  - name: raw\n    schema: raw\n    tables:\n      - name: items\n",
        )
        write(
            self.root,
            "transformation/models/result.sql",
            "{{ config(materialized='view') }}\nselect id, value + 1 as answer from {{ source('raw', 'items') }}\n",
        )
        write(
            self.root,
            "transformation/models/result.yml",
            "version: 2\nmodels:\n  - name: result\n    columns:\n      - name: id\n        data_tests: [not_null]\n",
        )
        write_json(
            self.root,
            "test-map.json",
            {
                "taxonomy": {},
                "modules": {
                    "result": {
                        "sources": ["transformation/models/result.sql"],
                        "selectors": {"data": "result"},
                    }
                },
            },
        )
        db = self.root.parent / "separate" / "selected.duckdb"
        db.parent.mkdir()
        env = {
            **os.environ,
            "ONBOARDING_DUCKDB_PATH": str(db),
            "DBT_SEND_ANONYMOUS_USAGE_STATS": "false",
            "RUNTIME__DLTHUB_TELEMETRY": "false",
        }
        for name in ("run_ingest", "run_ingest", "run_transform"):
            result = subprocess.run(
                [
                    sys.executable,
                    str(self.root / f"orchestration/{name}.py"),
                    "--db-path",
                    str(db),
                ],
                cwd=self.root,
                env=env,
                capture_output=True,
                text=True,
                timeout=240,
                check=False,
            )
            self.assertEqual(
                result.returncode, 0, (result.stdout + result.stderr)[-8000:]
            )
        self.assertFalse((self.root / ".local/data.duckdb").exists())
        with duckdb.connect(str(db), read_only=True) as conn:
            self.assertEqual(
                conn.execute(
                    "select count(*), min(answer), max(answer) from main.result"
                ).fetchone(),
                (7, 43, 43),
            )
            self.assertEqual(
                conn.execute("select count(*) from raw.items").fetchone()[0], 7
            )
            self.assertEqual(
                conn.execute(
                    "select count(*) from raw._dlt_loads where status=0"
                ).fetchone()[0],
                2,
            )
        renamed = db.with_name("renamed.duckdb")
        shutil.copy2(db, renamed)
        with duckdb.connect(str(renamed), read_only=True) as conn:
            self.assertEqual(
                conn.execute("select count(*),min(answer) from main.result").fetchone(),
                (7, 43),
            )
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "tests/test_maps.py",
                "tests/test_adr_links.py",
                "-o",
                "tmp_path_retention_count=0",
                "-o",
                "tmp_path_retention_policy=failed",
            ],
            cwd=self.root,
            env=env,
            capture_output=True,
            text=True,
            timeout=240,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        print(
            "Synthetic evidence: requested 1 yielded page; landed 7 rows; two replace loads keep 7 rows; result 43; renamed stored view resolves; native checks pass."
        )
