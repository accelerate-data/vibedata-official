#!/usr/bin/env python3
"""Validate the VibeData plugin marketplace registry."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

MARKETPLACE_PATH = Path(".claude-plugin/marketplace.json")
CODEX_MARKETPLACE_PATH = Path(".agents/plugins/marketplace.json")
GITHUB_URL_RE = re.compile(r"^https://github\.com/[^/\s]+/[^/\s]+(?:\.git)?$")
LOCAL_SOURCE_RE = re.compile(r"^\./plugins/[a-z0-9]+(?:-[a-z0-9]+)*$")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
CODEX_INSTALLATION_POLICIES = {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}
CODEX_AUTHENTICATION_POLICIES = {"ON_INSTALL", "ON_USE"}


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        fail(f"{path}: invalid JSON: {exc}")
    except OSError as exc:
        fail(f"{path}: could not read file: {exc}")

    if not isinstance(data, dict):
        fail(f"{path}: top-level value must be an object")
    return data


def load_json_from_git(ref: str, path: Path) -> dict[str, Any] | None:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path.as_posix()}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        fail(f"{ref}:{path}: invalid JSON: {exc}")

    if not isinstance(data, dict):
        fail(f"{ref}:{path}: top-level value must be an object")
    return data


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def version_tuple(
    version: Any, location: str, errors: list[str]
) -> tuple[int, int, int] | None:
    if not isinstance(version, str):
        errors.append(f"{location}: metadata.version must be a string")
        return None

    match = SEMVER_RE.fullmatch(version)
    if not match:
        errors.append(f"{location}: metadata.version must be strict semver, e.g. 1.2.3")
        return None

    return tuple(int(part) for part in match.groups())


def validate_marketplace(data: dict[str, Any], location: str) -> list[str]:
    errors: list[str] = []

    if not isinstance(data.get("name"), str) or not data["name"]:
        errors.append(f"{location}: top-level name is required")

    owner = data.get("owner")
    if (
        not isinstance(owner, dict)
        or not isinstance(owner.get("name"), str)
        or not owner["name"]
    ):
        errors.append(f"{location}: owner.name is required")

    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        errors.append(f"{location}: metadata object is required")
    else:
        version_tuple(metadata.get("version"), location, errors)

    plugins = data.get("plugins")
    if not isinstance(plugins, list):
        errors.append(f"{location}: plugins must be an array")
        return errors

    names: list[str] = []
    for index, entry in enumerate(plugins):
        entry_location = f"{location}: plugins[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{entry_location}: entry must be an object")
            continue

        name = entry.get("name")
        if not isinstance(name, str) or not name:
            errors.append(f"{entry_location}: name is required")
        elif not NAME_RE.fullmatch(name):
            errors.append(f"{entry_location} ({name}): name must be kebab-case")
        else:
            names.append(name)
            entry_location = f"{entry_location} ({name})"

        description = entry.get("description")
        if not isinstance(description, str) or not description:
            errors.append(f"{entry_location}: description is required")

        if "version" in entry:
            errors.append(
                f"{entry_location}: marketplace entries must not contain version"
            )

        source = entry.get("source")

        # Local path sources: "./plugins/<name>"
        if isinstance(source, str):
            if not LOCAL_SOURCE_RE.fullmatch(source):
                errors.append(
                    f"{entry_location}: local source must be a relative ./plugins/<name> path"
                )
            elif not Path(source).is_dir():
                errors.append(
                    f"{entry_location}: local source path {source!r} does not exist"
                )
            continue

        # External sources: object with source/url fields
        if not isinstance(source, dict):
            errors.append(
                f"{entry_location}: source must be a local ./plugins/ path or an object"
            )
            continue

        source_type = source.get("source")
        url = source.get("url")
        if source_type not in {"url", "git-subdir"}:
            errors.append(f"{entry_location}: source.source must be url or git-subdir")
            continue

        if not isinstance(url, str) or not GITHUB_URL_RE.fullmatch(url):
            errors.append(
                f"{entry_location}: source.url must be a full https://github.com/owner/repo URL"
            )

        if source_type == "url":
            extra_keys = set(source) - {"source", "url"}
            if extra_keys:
                errors.append(
                    f"{entry_location}: url sources may only include source and url"
                )
            if isinstance(url, str) and not url.endswith(".git"):
                errors.append(f"{entry_location}: url source URLs must end in .git")

        if source_type == "git-subdir":
            extra_keys = set(source) - {"source", "url", "path"}
            if extra_keys:
                errors.append(
                    f"{entry_location}: git-subdir sources may only include source, url, and path"
                )

            path = source.get("path")
            if not isinstance(path, str) or not path:
                errors.append(f"{entry_location}: git-subdir source.path is required")
            elif path in {".", "./"}:
                errors.append(
                    f"{entry_location}: use source=url for whole-repo plugins, "
                    f"not git-subdir path={path}"
                )
            elif path.startswith("/") or path.endswith("/"):
                errors.append(
                    f"{entry_location}: source.path must be a relative subpath "
                    "without a trailing slash"
                )

    duplicate_names = sorted({name for name in names if names.count(name) > 1})
    for name in duplicate_names:
        errors.append(f"{location}: duplicate plugin name {name}")

    if names != sorted(names):
        errors.append(f"{location}: plugins must be sorted alphabetically by name")

    return errors


def validate_codex_marketplace(data: dict[str, Any], location: str) -> list[str]:
    errors: list[str] = []

    if not isinstance(data.get("name"), str) or not data["name"]:
        errors.append(f"{location}: top-level name is required")

    interface = data.get("interface")
    if interface is not None and not isinstance(interface, dict):
        errors.append(f"{location}: interface must be an object when present")
    elif isinstance(interface, dict):
        display_name = interface.get("displayName")
        if display_name is not None and not isinstance(display_name, str):
            errors.append(f"{location}: interface.displayName must be a string")

    plugins = data.get("plugins")
    if not isinstance(plugins, list):
        errors.append(f"{location}: plugins must be an array")
        return errors

    names: list[str] = []
    for index, entry in enumerate(plugins):
        entry_location = f"{location}: plugins[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{entry_location}: entry must be an object")
            continue

        name = entry.get("name")
        if not isinstance(name, str) or not name:
            errors.append(f"{entry_location}: name is required")
        elif not NAME_RE.fullmatch(name):
            errors.append(f"{entry_location} ({name}): name must be kebab-case")
        else:
            names.append(name)
            entry_location = f"{entry_location} ({name})"

        source = entry.get("source")
        if not isinstance(source, dict):
            errors.append(f"{entry_location}: source must be an object")
            continue

        source_type = source.get("source")
        if source_type == "local":
            validate_codex_local_source(source, name, entry_location, errors)
        elif source_type in {"url", "git-subdir"}:
            validate_remote_source(source, source_type, entry_location, errors)
        else:
            errors.append(
                f"{entry_location}: source.source must be local, url, or git-subdir"
            )

        policy = entry.get("policy")
        if not isinstance(policy, dict):
            errors.append(f"{entry_location}: policy object is required")
        else:
            installation = policy.get("installation")
            if installation not in CODEX_INSTALLATION_POLICIES:
                errors.append(
                    f"{entry_location}: policy.installation must be one of "
                    f"{sorted(CODEX_INSTALLATION_POLICIES)}"
                )

            authentication = policy.get("authentication")
            if authentication not in CODEX_AUTHENTICATION_POLICIES:
                errors.append(
                    f"{entry_location}: policy.authentication must be one of "
                    f"{sorted(CODEX_AUTHENTICATION_POLICIES)}"
                )

        if not isinstance(entry.get("category"), str) or not entry["category"]:
            errors.append(f"{entry_location}: category is required")

    duplicate_names = sorted({name for name in names if names.count(name) > 1})
    for name in duplicate_names:
        errors.append(f"{location}: duplicate plugin name {name}")

    if names != sorted(names):
        errors.append(f"{location}: plugins must be sorted alphabetically by name")

    return errors


def validate_codex_local_source(
    source: dict[str, Any], name: Any, entry_location: str, errors: list[str]
) -> None:
    source_path = source.get("path")
    if not isinstance(source_path, str) or not LOCAL_SOURCE_RE.fullmatch(source_path):
        errors.append(
            f"{entry_location}: source.path must be a relative ./plugins/<name> path"
        )
        return

    plugin_path = Path(source_path)
    if not plugin_path.is_dir():
        errors.append(f"{entry_location}: source path {source_path!r} does not exist")
        return

    manifest_path = plugin_path / ".codex-plugin" / "plugin.json"
    if not manifest_path.is_file():
        errors.append(f"{entry_location}: {manifest_path} is required")
        return

    manifest = load_json(manifest_path)
    if manifest.get("name") != name:
        errors.append(f"{entry_location}: {manifest_path} name must match entry name")


def validate_remote_source(
    source: dict[str, Any], source_type: str, entry_location: str, errors: list[str]
) -> None:
    url = source.get("url")
    if not isinstance(url, str) or not GITHUB_URL_RE.fullmatch(url):
        errors.append(
            f"{entry_location}: source.url must be a full https://github.com/owner/repo URL"
        )

    if source_type == "url":
        extra_keys = set(source) - {"source", "url"}
        if extra_keys:
            errors.append(
                f"{entry_location}: url sources may only include source and url"
            )
        if isinstance(url, str) and not url.endswith(".git"):
            errors.append(f"{entry_location}: url source URLs must end in .git")

    if source_type == "git-subdir":
        extra_keys = set(source) - {"source", "url", "path"}
        if extra_keys:
            errors.append(
                f"{entry_location}: git-subdir sources may only include source, url, and path"
            )

        path = source.get("path")
        if not isinstance(path, str) or not path:
            errors.append(f"{entry_location}: git-subdir source.path is required")
        elif path in {".", "./"}:
            errors.append(
                f"{entry_location}: use source=url for whole-repo plugins, "
                f"not git-subdir path={path}"
            )
        elif path.startswith("/") or path.endswith("/"):
            errors.append(
                f"{entry_location}: source.path must be a relative subpath without a trailing slash"
            )


def validate_catalog_parity(
    claude_data: dict[str, Any], codex_data: dict[str, Any]
) -> list[str]:
    claude_names = plugin_names(claude_data)
    codex_names = plugin_names(codex_data)
    errors: list[str] = []

    missing_in_codex = sorted(claude_names - codex_names)
    if missing_in_codex:
        errors.append(
            "Codex marketplace is missing Claude marketplace plugins: "
            + ", ".join(missing_in_codex)
        )

    extra_in_codex = sorted(codex_names - claude_names)
    if extra_in_codex:
        errors.append(
            "Codex marketplace has plugins not present in Claude marketplace: "
            + ", ".join(extra_in_codex)
        )

    return errors


def plugin_names(data: dict[str, Any]) -> set[str]:
    return {
        entry["name"]
        for entry in data.get("plugins", [])
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }


def added_plugin_names(current: dict[str, Any], base: dict[str, Any]) -> list[str]:
    return sorted(plugin_names(current) - plugin_names(base))


def validate_version_bump(
    current: dict[str, Any], base: dict[str, Any], base_ref: str
) -> list[str]:
    added_names = added_plugin_names(current, base)
    return validate_added_names_version_bump(
        added_names, current, base, base_ref, "marketplace entries"
    )


def validate_codex_version_bump(
    codex_current: dict[str, Any],
    codex_base: dict[str, Any] | None,
    current: dict[str, Any],
    base: dict[str, Any],
    base_ref: str,
) -> list[str]:
    base_names = plugin_names(codex_base) if codex_base is not None else set()
    added_names = sorted(plugin_names(codex_current) - base_names)
    return validate_added_names_version_bump(
        added_names, current, base, base_ref, "Codex marketplace entries"
    )


def validate_added_names_version_bump(
    added_names: list[str],
    current: dict[str, Any],
    base: dict[str, Any],
    base_ref: str,
    entry_label: str,
) -> list[str]:
    errors: list[str] = []
    if not added_names:
        return errors

    current_version = version_tuple(
        current.get("metadata", {}).get("version"), "current", errors
    )
    base_version = version_tuple(
        base.get("metadata", {}).get("version"), base_ref, errors
    )
    if current_version is None or base_version is None:
        return errors

    if current_version <= base_version:
        errors.append(
            f"metadata.version must increase when adding {entry_label} "
            f"(added: {', '.join(added_names)}; {base_ref}: {format_version(base_version)}, "
            f"current: {format_version(current_version)})"
        )

    return errors


def format_version(version: tuple[int, int, int]) -> str:
    return ".".join(str(part) for part in version)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-ref", help="git ref to compare for new-entry version bump checks"
    )
    parser.add_argument("--path", default=MARKETPLACE_PATH, type=Path)
    args = parser.parse_args()

    current = load_json(args.path)
    if args.path == CODEX_MARKETPLACE_PATH:
        errors = validate_codex_marketplace(current, str(args.path))
    else:
        errors = validate_marketplace(current, str(args.path))

    base: dict[str, Any] | None = None
    if args.base_ref:
        base = load_json_from_git(args.base_ref, args.path)
        if base is None:
            print(
                f"Skipping version bump comparison: {args.base_ref}:{args.path} was not found"
            )
        else:
            errors.extend(validate_version_bump(current, base, args.base_ref))

    if args.path == MARKETPLACE_PATH and CODEX_MARKETPLACE_PATH.exists():
        codex = load_json(CODEX_MARKETPLACE_PATH)
        errors.extend(validate_codex_marketplace(codex, str(CODEX_MARKETPLACE_PATH)))
        errors.extend(validate_catalog_parity(current, codex))
        if args.base_ref and base is not None:
            codex_base = load_json_from_git(args.base_ref, CODEX_MARKETPLACE_PATH)
            errors.extend(
                validate_codex_version_bump(
                    codex, codex_base, current, base, args.base_ref
                )
            )

    if errors:
        print("marketplace validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("marketplace validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
