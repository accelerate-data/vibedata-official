#!/usr/bin/env python3
"""Require plugin.json version bumps when bundled plugin content changes."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

PLUGIN_JSON = Path(".claude-plugin/plugin.json")
BUNDLED_PLUGIN_PATHS = (
    ".claude-plugin/plugin.json",
    "plugins/",
)
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def git_output(args: list[str]) -> str:
    result = subprocess.run(args, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    return result.stdout


def changed_files(base_ref: str) -> list[str]:
    outputs = [
        git_output(["git", "diff", "--name-only", f"{base_ref}...HEAD"]),
        git_output(["git", "diff", "--name-only", "--cached"]),
        git_output(["git", "diff", "--name-only"]),
    ]
    files = {line for output in outputs for line in output.splitlines() if line}
    return sorted(files)


def load_plugin_json_from_worktree() -> dict:
    with PLUGIN_JSON.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        fail(f"{PLUGIN_JSON}: top-level value must be an object")
    return data


def load_plugin_json_from_git(ref: str) -> dict | None:
    result = subprocess.run(
        ["git", "show", f"{ref}:{PLUGIN_JSON.as_posix()}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    data = json.loads(result.stdout)
    if not isinstance(data, dict):
        fail(f"{ref}:{PLUGIN_JSON}: top-level value must be an object")
    return data


def version_tuple(version: object, location: str) -> tuple[int, int, int]:
    if not isinstance(version, str):
        fail(f"{location}: version must be a string")
    match = SEMVER_RE.fullmatch(version)
    if not match:
        fail(f"{location}: version must be strict semver, e.g. 1.2.3")
    return tuple(int(part) for part in match.groups())


def format_version(version: tuple[int, int, int]) -> str:
    return ".".join(str(part) for part in version)


def bundled_plugin_changed(files: list[str]) -> bool:
    return any(
        file == BUNDLED_PLUGIN_PATHS[0] or file.startswith(BUNDLED_PLUGIN_PATHS[1])
        for file in files
    )


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-ref", required=True)
    args = parser.parse_args()

    files = changed_files(args.base_ref)
    if not bundled_plugin_changed(files):
        print("No bundled plugin files changed; plugin.json version bump not required")
        return 0

    current = load_plugin_json_from_worktree()
    base = load_plugin_json_from_git(args.base_ref)
    if base is None:
        print(
            f"Skipping plugin version comparison: {args.base_ref}:{PLUGIN_JSON} was not found"
        )
        return 0

    current_version = version_tuple(current.get("version"), "current plugin.json")
    base_version = version_tuple(base.get("version"), f"{args.base_ref} plugin.json")
    if current_version <= base_version:
        fail(
            "plugin.json version must increase when bundled plugin files change "
            f"({args.base_ref}: {format_version(base_version)}, "
            f"current: {format_version(current_version)})"
        )

    print(
        "plugin.json version bumped: "
        f"{format_version(base_version)} -> {format_version(current_version)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
