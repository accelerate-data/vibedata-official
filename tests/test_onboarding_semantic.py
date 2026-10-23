"""Run the delivered semantic CLI from a disposable emitted skill tree."""

from __future__ import annotations

import ast
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SEEDS = (
    ROOT / "plugins/vibedata-repo-skills/skills/onboarding-vibedata/templates/semantic"
)


class SemanticDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="onboarding-semantic-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("semantic-model", "validating-semantic-model"):
            seed = SEEDS / name
            self.assertTrue((seed / "convention.md").is_file(), f"Missing {name} seed")
            dest = self.root / ".agents/skills" / name
            shutil.copytree(
                seed, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc")
            )
            (dest / "convention.md").rename(dest / "SKILL.md")
        self.skill = self.root / ".agents/skills/semantic-model"
        self.tool = self.skill / "scripts/ossie.py"
        self.models = self.root / "custom-semantics"
        self.models.mkdir()
        self.model = self.models / "orders.ossie.yaml"
        shutil.copy(self.skill / "examples/star.ossie.yaml", self.model)

    def run_cli(self, *args, expected=0):
        result = subprocess.run(
            [sys.executable, str(self.tool), *map(str, args)],
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_seed_examples_validate_and_suppliers_are_complete(self):
        self.run_cli("validate", self.models)
        self.run_cli("suppliers", self.models)
        self.run_cli("validate", self.skill / "examples/standalone.ossie.yaml")
        self.run_cli("suppliers", self.skill / "examples/standalone.ossie.yaml")
        version = json.loads(self.run_cli("version").stdout)
        self.assertEqual(version["spec"], "0.2.0.dev0")

    def test_examples_declare_rollup_for_every_metric(self):
        for path in (self.skill / "examples").glob("*.ossie.yaml"):
            for metric in yaml.safe_load(path.read_text())["metrics"]:
                with self.subTest(example=path.name, metric=metric["name"]):
                    payload = next(
                        (
                            json.loads(ext["data"])
                            for ext in metric.get("custom_extensions", [])
                            if ext["vendor_name"] == "VIBEDATA"
                        ),
                        {},
                    )
                    self.assertIn("aggregation", payload)

    def test_suppliers_does_not_borrow_a_same_named_field_from_another_dataset(self):
        model = yaml.safe_load(self.model.read_text())
        customer = next(d for d in model["datasets"] if d["name"] == "customer")
        extension = customer["custom_extensions"][0]
        payload = json.loads(extension["data"])
        del payload["logical_sources"][0]["column_map"]["customer_key"]
        extension["data"] = json.dumps(payload)
        self.model.write_text(yaml.safe_dump(model))
        self.run_cli("validate", self.models)
        result = self.run_cli("suppliers", self.models, expected=1)
        self.assertIn("customer.customer_key", result.stdout)

    def test_validation_rejects_a_consistent_unsupported_extension_version(self):
        self.model.write_text(self.model.read_text().replace('"1.4"', '"0.0"'))
        result = self.run_cli("validate", self.models, expected=1)
        self.assertIn("vibedata/unsupported-version", result.stdout)

    def test_extension_checker_key_sets_match_schema(self):
        scripts = self.skill / "scripts"
        syntax = ast.parse((scripts / "ossie_vibedata.py").read_text())
        constants = {
            node.targets[0].id: ast.literal_eval(node.value)
            for node in syntax.body
            if isinstance(node, ast.Assign)
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Set)
        }
        definitions = json.loads((scripts / "vibedata-schema.json").read_text())[
            "$defs"
        ]
        pairs = {
            "MODEL_KEYS": "modelPayload",
            "DATASET_KEYS": "datasetPayload",
            "RELATIONSHIP_KEYS": "relationshipPayload",
            "PHYSICAL_TABLE_KEYS": "physicalTable",
            "PHYSICAL_JOIN_KEYS": "physicalJoin",
            "LTS_KEYS": "logicalSource",
            "HIERARCHY_KEYS": "hierarchy",
            "SCD_KEYS": "scd",
            "VARIABLE_KEYS": "variable",
            "LEVEL_KEYS": "level",
            "LEVEL_REF_KEYS": "levelRef",
            "METRIC_KEYS": "metricPayload",
            "TIME_SERIES_KEYS": "timeSeries",
            "BASED_ON_KEYS": "basedOnDimensions",
            "LEVEL_KEY_KEYS": "levelKey",
            "ROW_LEVEL_KEYS": "rowLevel",
        }
        for constant, definition in pairs.items():
            with self.subTest(definition=definition):
                self.assertEqual(
                    constants[constant], set(definitions[definition]["properties"])
                )

    def test_malformed_model_and_directory_identity_drift_fail(self):
        twin = yaml.safe_load(self.model.read_text())
        twin["name"] = "other_star"
        twin["datasets"][0]["fields"][0]["datatype"] = "Integer"
        (self.models / "twin.ossie.yaml").write_text(yaml.safe_dump(twin))
        self.run_cli("validate", self.models, expected=1)
        (self.models / "twin.ossie.yaml").unlink()
        self.model.write_text("version: 'wrong'\nname: broken\n")
        self.run_cli("validate", self.models, expected=1)

    def test_coverage_rejects_unregistered_mart_and_notes_resolve(self):
        model = yaml.safe_load(self.model.read_text())
        payload = json.loads(model["custom_extensions"][0]["data"])
        marts = self.root / "models/marts"
        marts.mkdir(parents=True)
        for table in payload["physical_tables"]:
            if table.get("dbt_model"):
                (marts / f"{table['dbt_model']}.sql").write_text("select 1\n")
        self.run_cli("coverage", self.models, marts)
        (marts / "unregistered.sql").write_text("select 1\n")
        self.run_cli("coverage", self.models, marts, expected=1)
        tests, adrs = self.root / "sql-tests", self.root / "decisions"
        tests.mkdir()
        adrs.mkdir()
        self.run_cli("notes", self.models, tests, adrs, expected=1)
        (tests / "assert_order_daily_matches_its_content_filter.sql").write_text(
            "select 1\n"
        )
        self.run_cli("notes", self.models, tests, adrs)

    def test_level_test_freshness_rejects_stale_output(self):
        target = self.root / "assert_levels.sql"
        self.run_cli("level-tests", self.models, target)
        self.assertIn(
            "date.LTS2_month_table: date month key is no member", target.read_text()
        )
        self.run_cli("level-tests", self.models, target, "--check")
        target.write_text("select 1\n")
        self.run_cli("level-tests", self.models, target, "--check", expected=1)


if __name__ == "__main__":
    unittest.main()
