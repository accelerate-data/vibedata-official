from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "build_catalog.py"
SPEC = importlib.util.spec_from_file_location("build_catalog", MODULE_PATH)
assert SPEC is not None
build_catalog = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(build_catalog)

MARKER_PAIRS = ("catalog-summary", "available-plugins", "skill-library")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def write_skill(path: Path, name: str, description: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n",
        encoding="utf-8",
    )


def readme_text() -> str:
    blocks = "\n".join(
        f"<!-- BEGIN GENERATED: {name} -->\n<!-- END GENERATED: {name} -->"
        for name in MARKER_PAIRS
    )
    return f"# Demo\n\n{blocks}\n"


class FixtureRoot:
    """A minimal storefront tree; mutate a file after building to probe failures."""

    def __init__(self, case: unittest.TestCase) -> None:
        self.root = Path(tempfile.mkdtemp())
        case.addCleanup(shutil.rmtree, self.root)
        (self.root / "schema").mkdir()
        for schema in (
            "manifest.schema.json",
            "catalog.schema.json",
            "connector-sources.schema.json",
        ):
            shutil.copy(REPO_ROOT / "schema" / schema, self.root / "schema" / schema)
        write_json(
            self.root / "licenses" / "allowlist.json",
            {"schemaVersion": 1, "licenses": ["MIT", "Apache-2.0", "Elastic-2.0"]},
        )
        write_json(
            self.root / ".claude-plugin" / "marketplace.json",
            {
                "name": "vibedata-plugins-official",
                "plugins": [
                    {
                        "name": "demo-plugin",
                        "description": "A demo plugin",
                        "license": "MIT",
                        "source": "./plugins/demo-plugin",
                    }
                ],
            },
        )
        write_skill(
            self.root / "skills" / "demo-skill" / "SKILL.md",
            "demo-skill",
            "A library skill",
        )
        write_skill(
            self.root
            / "plugins"
            / "demo-plugin"
            / "skills"
            / "demo-bundled"
            / "SKILL.md",
            "demo-bundled",
            "A bundled skill",
        )
        write_json(
            self.root / "recipes" / "catalog.json",
            {
                "recipes": [
                    {
                        "id": "demo-recipe",
                        "title": "Demo recipe",
                        "area": "ingestion",
                        "readiness": "supported",
                        "pitch": "Do a thing",
                    }
                ]
            },
        )
        (self.root / "mcp").mkdir()
        (self.root / "mcp" / "fabric-core.yaml").write_text(
            "name: Fabric Core\nshortDescription: Manage Fabric\nruntime: remote\nserverUserType: multiUser\n",
            encoding="utf-8",
        )
        write_json(
            self.root / "connectors" / "sources.json",
            {
                "schemaVersion": 1,
                "sources": [
                    {
                        "name": "verified-sources",
                        "description": "dlt sources",
                        "url": "https://github.com/dlt-hub/verified-sources",
                        "ref": "abc123",
                        "license": "Apache-2.0",
                        "attribution": "dltHub",
                    }
                ],
            },
        )
        (self.root / "releases").mkdir()
        (self.root / "releases" / "README.md").write_text(
            "release notes\n", encoding="utf-8"
        )
        write_json(
            self.root / "manifest.json",
            {
                "schemaVersion": 1,
                "content": {
                    "plugins": {
                        "path": ".claude-plugin/marketplace.json",
                        "fetchedBy": "studio",
                        "adminOverride": "additive",
                    },
                    "skills": {
                        "path": "skills/",
                        "fetchedBy": "studio",
                        "adminOverride": "none",
                        "license": "Elastic-2.0",
                    },
                    "recipes": {
                        "path": "recipes/catalog.json",
                        "fetchedBy": "studio",
                        "adminOverride": "pointer",
                        "license": "Elastic-2.0",
                    },
                    "connectors": {
                        "path": "connectors/sources.json",
                        "fetchedBy": "studio",
                        "adminOverride": "additive",
                        "license": "Apache-2.0",
                    },
                    "releases": {
                        "path": "releases/",
                        "fetchedBy": "studio",
                        "adminOverride": "none",
                        "license": "Elastic-2.0",
                    },
                    "mcp": {
                        "path": "mcp/",
                        "fetchedBy": "obot",
                        "adminOverride": "none",
                    },
                },
            },
        )
        (self.root / "README.md").write_text(readme_text(), encoding="utf-8")


class BuildCatalogTests(unittest.TestCase):
    def test_valid_fixture_builds_without_errors(self) -> None:
        root = FixtureRoot(self).root
        catalog, errors = build_catalog.build_catalog(root)
        self.assertEqual(errors, [])
        self.assertEqual(len(catalog["entries"]["plugins"]), 1)
        self.assertEqual(len(catalog["entries"]["skills"]), 2)
        self.assertEqual(len(catalog["entries"]["recipes"]), 1)
        self.assertEqual(len(catalog["entries"]["connectors"]), 1)
        self.assertEqual(len(catalog["entries"]["mcp"]), 1)

    def test_plugin_license_off_allowlist_fails(self) -> None:
        root = FixtureRoot(self).root
        path = root / ".claude-plugin" / "marketplace.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["plugins"][0]["license"] = "GPL-3.0"
        write_json(path, data)
        _, errors = build_catalog.build_catalog(root)
        self.assertTrue(
            any("not on the allowlist" in error for error in errors), errors
        )

    def test_connector_license_off_allowlist_fails(self) -> None:
        root = FixtureRoot(self).root
        path = root / "connectors" / "sources.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["sources"][0]["license"] = "Proprietary"
        write_json(path, data)
        _, errors = build_catalog.build_catalog(root)
        self.assertTrue(
            any("not on the allowlist" in error for error in errors), errors
        )

    def test_manifest_missing_source_fails_schema(self) -> None:
        root = FixtureRoot(self).root
        path = root / "manifest.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        del data["content"]["mcp"]
        write_json(path, data)
        _, errors = build_catalog.build_catalog(root)
        self.assertTrue(any("mcp" in error for error in errors), errors)

    def test_manifest_path_missing_fails(self) -> None:
        root = FixtureRoot(self).root
        path = root / "manifest.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["content"]["recipes"]["path"] = "recipes/absent.json"
        write_json(path, data)
        _, errors = build_catalog.build_catalog(root)
        self.assertTrue(any("does not exist" in error for error in errors), errors)

    def test_generated_pages_carry_disclaimer(self) -> None:
        root = FixtureRoot(self).root
        outputs = build_catalog.build_outputs(root)
        page_names = [
            path
            for path in outputs
            if path.suffix == ".md" and path.parent.name == "catalog"
        ]
        self.assertGreater(len(page_names), 0)
        for path in page_names:
            self.assertIn(build_catalog.DISCLAIMER, outputs[path], path)

    def test_outputs_are_deterministic_and_fresh(self) -> None:
        root = FixtureRoot(self).root
        outputs = build_catalog.build_outputs(root)
        self.assertEqual(
            set(build_catalog.stale_paths(root, outputs)), {str(p) for p in outputs}
        )
        for path, content in outputs.items():
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        self.assertEqual(build_catalog.stale_paths(root, outputs), [])

    def test_stale_detection_after_manual_edit(self) -> None:
        root = FixtureRoot(self).root
        outputs = build_catalog.build_outputs(root)
        for path, content in outputs.items():
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        (root / "catalog" / "plugins.md").write_text("hand edited\n", encoding="utf-8")
        self.assertIn("catalog/plugins.md", build_catalog.stale_paths(root, outputs))

    def test_replace_block_missing_marker_fails(self) -> None:
        with self.assertRaises(SystemExit):
            build_catalog.replace_block("no markers here", "catalog-summary", "body")

    def test_table_cell_escapes_pipes_and_newlines(self) -> None:
        self.assertEqual(build_catalog.table_cell("a | b\nc"), "a \\| b c")


if __name__ == "__main__":
    unittest.main()
