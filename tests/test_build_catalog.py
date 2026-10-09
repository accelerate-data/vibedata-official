from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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

    def test_build_is_deterministic(self) -> None:
        root = FixtureRoot(self).root
        self.assertEqual(
            build_catalog.build_outputs(root), build_catalog.build_outputs(root)
        )

    def test_reads_every_mcp_catalog_directory(self) -> None:
        root = FixtureRoot(self).root
        for sub in ("remotes", "obot-remotes", "obot-images"):
            directory = root / "mcp" / sub
            directory.mkdir(parents=True)
            (directory / "extra.yaml").write_text(
                f"name: {sub} server\nshortDescription: from {sub}\nruntime: remote\nserverUserType: multiUser\n",
                encoding="utf-8",
            )
        names = {entry["name"] for entry in build_catalog.read_mcp(root)}
        self.assertEqual(
            names,
            {
                "Fabric Core",
                "remotes server",
                "obot-remotes server",
                "obot-images server",
            },
        )

    def test_external_source_labels_and_author(self) -> None:
        root = FixtureRoot(self).root
        path = root / ".claude-plugin" / "marketplace.json"
        write_json(
            path,
            {
                "name": "vibedata-plugins-official",
                "plugins": [
                    {
                        "name": "sub",
                        "description": "Sub",
                        "license": "MIT",
                        "source": {
                            "source": "git-subdir",
                            "url": "https://github.com/acme/plugins",
                            "path": "plugins/sub",
                        },
                        "author": {"name": "Acme"},
                    },
                    {
                        "name": "whole",
                        "description": "Whole",
                        "license": "MIT",
                        "source": {
                            "source": "url",
                            "url": "https://github.com/acme/whole.git",
                        },
                    },
                ],
            },
        )
        plugins = build_catalog.read_plugins(
            root, {"MIT", "Elastic-2.0", "Apache-2.0"}, []
        )
        self.assertEqual(
            [entry["source"] for entry in plugins],
            ["acme/plugins (plugins/sub)", "acme/whole"],
        )
        self.assertEqual(plugins[0]["author"], "Acme")
        self.assertNotIn("author", plugins[1])

    def test_plugin_missing_license_fails(self) -> None:
        root = FixtureRoot(self).root
        path = root / ".claude-plugin" / "marketplace.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        del data["plugins"][0]["license"]
        write_json(path, data)
        _, errors = build_catalog.build_catalog(root)
        self.assertTrue(any("license is required" in error for error in errors), errors)

    def test_skill_without_frontmatter_falls_back_to_directory_name(self) -> None:
        root = FixtureRoot(self).root
        path = root / "skills" / "plain" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text("# no frontmatter\n", encoding="utf-8")
        self.assertEqual(build_catalog.read_skill(root, path, None)["name"], "plain")

    def test_invalid_mcp_yaml_fails(self) -> None:
        root = FixtureRoot(self).root
        (root / "mcp" / "bad.yaml").write_text(
            "name: [unterminated\n", encoding="utf-8"
        )
        with self.assertRaises(SystemExit):
            build_catalog.build_catalog(root)

    def test_build_outputs_aborts_on_validation_error(self) -> None:
        root = FixtureRoot(self).root
        path = root / ".claude-plugin" / "marketplace.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["plugins"][0]["license"] = "GPL-3.0"
        write_json(path, data)
        with self.assertRaises(SystemExit):
            build_catalog.build_outputs(root)

    def run_main(self, root: Path, argv: list[str]) -> None:
        with (
            mock.patch.object(build_catalog, "ROOT", root),
            mock.patch.object(sys, "argv", ["build_catalog.py", *argv]),
        ):
            build_catalog.main()

    def test_main_writes_then_check_passes_then_stale_check_exits(self) -> None:
        root = FixtureRoot(self).root
        self.run_main(root, [])
        self.run_main(root, ["--check"])
        (root / "catalog" / "plugins.md").write_text("hand edited\n", encoding="utf-8")
        with self.assertRaises(SystemExit) as caught:
            self.run_main(root, ["--check"])
        self.assertNotEqual(caught.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
