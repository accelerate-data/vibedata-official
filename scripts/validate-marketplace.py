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
GITHUB_URL_RE = re.compile(r"^https://github\.com/[^/\s]+/[^/\s]+(?:\.git)?$")
LOCAL_SOURCE_RE = re.compile(r"^\./plugins/[a-z0-9]+(?:-[a-z0-9]+)*$")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


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


def added_plugin_names(current: dict[str, Any], base: dict[str, Any]) -> list[str]:
    current_names = {
        entry["name"]
        for entry in current.get("plugins", [])
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }
    base_names = {
        entry["name"]
        for entry in base.get("plugins", [])
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }
    return sorted(current_names - base_names)


def validate_version_bump(
    current: dict[str, Any], base: dict[str, Any], base_ref: str
) -> list[str]:
    errors: list[str] = []
    added_names = added_plugin_names(current, base)
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
            "metadata.version must increase when adding marketplace entries "
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
    errors = validate_marketplace(current, str(args.path))

    if args.base_ref:
        base = load_json_from_git(args.base_ref, args.path)
        if base is None:
            print(
                f"Skipping version bump comparison: {args.base_ref}:{args.path} was not found"
            )
        else:
            errors.extend(validate_version_bump(current, base, args.base_ref))

    if errors:
        print("marketplace validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("marketplace validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
