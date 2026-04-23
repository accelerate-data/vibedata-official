from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "scripts" / "validate-marketplace.py"
)
SPEC = importlib.util.spec_from_file_location("validate_marketplace", MODULE_PATH)
assert SPEC is not None
validate_marketplace = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validate_marketplace)


def valid_marketplace() -> dict:
    return {
        "name": "vibedata-plugins-official",
        "owner": {"name": "accelerate-data"},
        "metadata": {"description": "Plugin marketplace", "version": "1.0.0"},
        "plugins": [
            {
                "name": "alpha-plugin",
                "description": "A whole-repo external plugin",
                "source": {
                    "source": "url",
                    "url": "https://github.com/example/alpha-plugin.git",
                },
            },
            {
                "name": "beta-plugin",
                "description": "A subdirectory external plugin",
                "source": {
                    "source": "git-subdir",
                    "url": "https://github.com/example/plugins",
                    "path": "plugins/beta-plugin",
                },
            },
        ],
    }


def valid_codex_marketplace() -> dict:
    return {
        "name": "vibedata-plugins-official",
        "interface": {"displayName": "VibeData Official"},
        "plugins": [
            {
                "name": "alpha-plugin",
                "source": {"source": "local", "path": "./plugins/alpha-plugin"},
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Data Engineering",
            },
            {
                "name": "beta-plugin",
                "source": {"source": "local", "path": "./plugins/beta-plugin"},
                "policy": {
                    "installation": "INSTALLED_BY_DEFAULT",
                    "authentication": "ON_USE",
                },
                "category": "Data Engineering",
            },
        ],
    }


class MarketplaceValidationTests(unittest.TestCase):
    def test_valid_marketplace_passes(self) -> None:
        errors = validate_marketplace.validate_marketplace(
            valid_marketplace(), "current"
        )
        self.assertEqual(errors, [])

    def test_valid_local_string_source_passes(self) -> None:
        data = valid_marketplace()
        # insert a local source entry in alphabetical order
        data["plugins"].insert(
            0,
            {
                "name": "aaa-local",
                "description": "A local plugin",
                "source": "./plugins/aaa-local",
            },
        )
        errors = validate_marketplace.validate_marketplace(data, "current")
        # only error should be that ./plugins/aaa-local does not exist on disk
        self.assertTrue(all("does not exist" in e for e in errors) or errors == [])

    def test_rejects_invalid_local_source_string(self) -> None:
        data = valid_marketplace()
        data["plugins"].insert(
            0,
            {
                "name": "aaa-local",
                "description": "A local plugin",
                "source": "./wrong/aaa-local",
            },
        )
        errors = validate_marketplace.validate_marketplace(data, "current")
        self.assertTrue(any("./plugins/" in error for error in errors))

    def test_rejects_git_subdir_path_dot(self) -> None:
        data = valid_marketplace()
        data["plugins"][0]["source"] = {
            "source": "git-subdir",
            "url": "https://github.com/example/alpha-plugin",
            "path": ".",
        }

        errors = validate_marketplace.validate_marketplace(data, "current")

        self.assertTrue(any("use source=url" in error for error in errors))

    def test_rejects_url_without_git_suffix(self) -> None:
        data = valid_marketplace()
        data["plugins"][0]["source"]["url"] = "https://github.com/example/alpha-plugin"

        errors = validate_marketplace.validate_marketplace(data, "current")

        self.assertTrue(any("must end in .git" in error for error in errors))

    def test_rejects_unsorted_names(self) -> None:
        data = valid_marketplace()
        data["plugins"].reverse()

        errors = validate_marketplace.validate_marketplace(data, "current")

        self.assertTrue(any("sorted alphabetically" in error for error in errors))

    def test_rejects_duplicate_names(self) -> None:
        data = valid_marketplace()
        data["plugins"][1]["name"] = "alpha-plugin"

        errors = validate_marketplace.validate_marketplace(data, "current")

        self.assertTrue(
            any("duplicate plugin name alpha-plugin" in error for error in errors)
        )

    def test_rejects_entry_version_field(self) -> None:
        data = valid_marketplace()
        data["plugins"][0]["version"] = "1.0.0"

        errors = validate_marketplace.validate_marketplace(data, "current")

        self.assertTrue(any("must not contain version" in error for error in errors))

    def test_rejects_git_subdir_absolute_path(self) -> None:
        data = valid_marketplace()
        data["plugins"][1]["source"]["path"] = "/plugins/beta-plugin"

        errors = validate_marketplace.validate_marketplace(data, "current")

        self.assertTrue(any("relative subpath" in error for error in errors))

    def test_rejects_url_source_extra_keys(self) -> None:
        data = valid_marketplace()
        data["plugins"][0]["source"]["path"] = "plugins/alpha-plugin"

        errors = validate_marketplace.validate_marketplace(data, "current")

        self.assertTrue(
            any(
                "url sources may only include source and url" in error
                for error in errors
            )
        )

    def test_does_not_require_version_bump_without_added_entries(self) -> None:
        base = valid_marketplace()
        current = valid_marketplace()

        errors = validate_marketplace.validate_version_bump(
            current, base, "origin/main"
        )

        self.assertEqual(errors, [])

    def test_requires_version_bump_when_entries_added(self) -> None:
        base = valid_marketplace()
        current = valid_marketplace()
        current["plugins"].append(
            {
                "name": "gamma-plugin",
                "description": "A new plugin",
                "source": {
                    "source": "url",
                    "url": "https://github.com/example/gamma-plugin.git",
                },
            }
        )

        errors = validate_marketplace.validate_version_bump(
            current, base, "origin/main"
        )

        self.assertTrue(
            any("metadata.version must increase" in error for error in errors)
        )

    def test_version_bump_passes_when_entries_added(self) -> None:
        base = valid_marketplace()
        current = valid_marketplace()
        current["metadata"]["version"] = "1.0.1"
        current["plugins"].append(
            {
                "name": "gamma-plugin",
                "description": "A new plugin",
                "source": {
                    "source": "url",
                    "url": "https://github.com/example/gamma-plugin.git",
                },
            }
        )

        errors = validate_marketplace.validate_version_bump(
            current, base, "origin/main"
        )

        self.assertEqual(errors, [])

    def test_same_marketplace_version_must_bump_when_codex_entries_added(self) -> None:
        base = valid_marketplace()
        current = valid_marketplace()
        base_codex = valid_codex_marketplace()
        base_codex["plugins"] = base_codex["plugins"][:1]
        current_codex = valid_codex_marketplace()

        errors = validate_marketplace.validate_codex_version_bump(
            current_codex, base_codex, current, base, "origin/main"
        )

        self.assertTrue(any("Codex marketplace entries" in error for error in errors))

    def test_same_marketplace_version_bump_covers_codex_entries(self) -> None:
        base = valid_marketplace()
        current = valid_marketplace()
        current["metadata"]["version"] = "1.0.1"
        base_codex = valid_codex_marketplace()
        base_codex["plugins"] = base_codex["plugins"][:1]
        current_codex = valid_codex_marketplace()

        errors = validate_marketplace.validate_codex_version_bump(
            current_codex, base_codex, current, base, "origin/main"
        )

        self.assertEqual(errors, [])

    def test_valid_codex_marketplace_shape_passes_except_missing_local_dirs(
        self,
    ) -> None:
        errors = validate_marketplace.validate_codex_marketplace(
            valid_codex_marketplace(), "current"
        )

        self.assertTrue(
            all("does not exist" in error for error in errors) or errors == []
        )

    def test_codex_marketplace_accepts_remote_sources(self) -> None:
        data = valid_codex_marketplace()
        data["plugins"][0]["source"] = {
            "source": "url",
            "url": "https://github.com/example/alpha-plugin.git",
        }

        errors = validate_marketplace.validate_codex_marketplace(data, "current")

        self.assertFalse(
            any("source.source must be local" in error for error in errors)
        )

    def test_codex_marketplace_requires_policy(self) -> None:
        data = valid_codex_marketplace()
        del data["plugins"][0]["policy"]

        errors = validate_marketplace.validate_codex_marketplace(data, "current")

        self.assertTrue(any("policy object is required" in error for error in errors))

    def test_codex_marketplace_rejects_invalid_authentication_policy(self) -> None:
        data = valid_codex_marketplace()
        data["plugins"][0]["policy"]["authentication"] = "ALWAYS"

        errors = validate_marketplace.validate_codex_marketplace(data, "current")

        self.assertTrue(any("policy.authentication" in error for error in errors))

    def test_codex_marketplace_requires_category(self) -> None:
        data = valid_codex_marketplace()
        del data["plugins"][0]["category"]

        errors = validate_marketplace.validate_codex_marketplace(data, "current")

        self.assertTrue(any("category is required" in error for error in errors))

    def test_marketplace_catalog_parity_passes_when_plugin_names_match(self) -> None:
        errors = validate_marketplace.validate_catalog_parity(
            valid_marketplace(), valid_codex_marketplace()
        )

        self.assertEqual(errors, [])

    def test_marketplace_catalog_parity_rejects_missing_codex_plugin(self) -> None:
        codex = valid_codex_marketplace()
        codex["plugins"] = codex["plugins"][1:]

        errors = validate_marketplace.validate_catalog_parity(
            valid_marketplace(), codex
        )

        self.assertTrue(
            any("missing Claude marketplace plugins" in error for error in errors)
        )

    def test_marketplace_catalog_parity_rejects_extra_codex_plugin(self) -> None:
        codex = valid_codex_marketplace()
        codex["plugins"].append(
            {
                "name": "gamma-plugin",
                "source": {
                    "source": "url",
                    "url": "https://github.com/example/gamma-plugin.git",
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Data Engineering",
            }
        )

        errors = validate_marketplace.validate_catalog_parity(
            valid_marketplace(), codex
        )

        self.assertTrue(
            any("not present in Claude marketplace" in error for error in errors)
        )


if __name__ == "__main__":
    unittest.main()
