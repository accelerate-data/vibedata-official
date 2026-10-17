"""Inventory repository structure without executing application code or returning contents."""

from __future__ import annotations

import argparse
import ast
import json
import os
import subprocess
import sys
from pathlib import Path

EXCLUDED = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "target",
    "dist",
    "build",
    "dbt_packages",
    "data",
    "warehouse",
    "logs",
    ".superpowers",
}
CONFIG_NAMES = {
    ".platform",
    "dbt_project.yml",
    "profiles.yml",
    "packages.yml",
    "pyproject.toml",
    "requirements.txt",
    "requirements-dev.txt",
    "setup.cfg",
    "pytest.ini",
    "Makefile",
    "uv.lock",
    "poetry.lock",
    "config.toml",
}
ARTIFACT_NAMES = {
    "repo-map.json",
    "repo-map.schema.json",
    "test-map.json",
    "context.md",
    "glossary.md",
    "onboarding.md",
}
MAX_BYTES = 1024 * 1024


def fabric_import_tree(text: str) -> ast.Module:
    """Keep Python for static import discovery; never evaluate notebook magics."""
    lines = text.splitlines()
    while True:
        try:
            return ast.parse("\n".join(lines))
        except SyntaxError as exc:
            index = exc.lineno - 1
            line = lines[index]
            stripped = line.lstrip()
            if not stripped.startswith(("%", "!")):
                raise
            if stripped.startswith("%%"):
                # shortcut: cell-magic bodies are opaque; add language-aware parsing if needed.
                end = index + 1
                while end < len(lines) and not lines[end].startswith(
                    ("# CELL ", "# PARAMETERS CELL ", "# MARKDOWN ")
                ):
                    end += 1
                lines[index:end] = [""] * (end - index)
            else:
                lines[index] = line[: len(line) - len(stripped)] + "pass"


def secret_path(path: Path) -> bool:
    return any(
        p == ".env"
        or p.startswith((".env.", "credentials.", "secrets."))
        or p.endswith((".env", ".key", ".pem"))
        for p in path.parts
    )


def inventory_paths(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0 and Path(result.stdout.strip()).resolve() == root:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-co", "--exclude-standard", "-z"],
            capture_output=True,
            check=False,
        )
        if result.returncode:
            raise ValueError("git inventory failed; check repository permissions")
        paths = [Path(os.fsdecode(p)) for p in result.stdout.split(b"\0") if p]
    else:
        paths = []
        for directory, dirs, files in os.walk(root, followlinks=False):
            dirs[:] = [
                d
                for d in dirs
                if d not in EXCLUDED and not (Path(directory) / d).is_symlink()
            ]
            paths.extend((Path(directory) / f).relative_to(root) for f in files)
            if len(paths) > 10000:
                raise ValueError(
                    "Inventory exceeds 10000 files; select a smaller repository root"
                )
    return sorted(
        {p for p in paths if not set(p.parts) & EXCLUDED and not secret_path(p)}
    )


def inspect_repository(root: Path) -> dict[str, object]:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Repository root must be a directory")
    result: dict[str, object] = {
        "mode": "greenfield",
        "instruction_files": [],
        "config_files": [],
        "code_files": [],
        "notebook_files": [],
        "existing_artifacts": [],
        "stacks": [],
    }
    stacks = set()
    paths = inventory_paths(root)
    if len(paths) > 10000:
        raise ValueError(
            "Inventory exceeds 10000 files; select a smaller repository root"
        )
    for path in paths:
        file = root / path
        # Git's index can still name a file deleted in the working tree.
        try:
            file.lstat()
        except FileNotFoundError:
            continue
        try:
            resolved = file.resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            raise ValueError(f"{path}: unresolved path or symlink cycle") from exc
        if not resolved.is_relative_to(root):
            raise ValueError(f"{path}: symlink resolves outside repository")
        if not file.is_file():
            continue
        name = path.as_posix()
        if path.name.lower() in {"agents.md", "claude.md"}:
            result["instruction_files"].append(name)
        if path.name in CONFIG_NAMES:
            result["config_files"].append(name)
        context_tool = path.parts[0] in {".agents", ".claude", ".codex"}
        if (
            path.name.lower() in ARTIFACT_NAMES
            or context_tool
            or path.parent.name in {"adr", "decisions"}
        ):
            result["existing_artifacts"].append(name)
        if context_tool:
            continue
        if path.name == ".platform":
            stacks.add("fabric")
        if path.suffix in {".py", ".ipynb", ".sql", ".r", ".R", ".scala"}:
            result["code_files"].append(name)
            result["mode"] = "brownfield"
        if path.name == "dbt_project.yml":
            stacks.add("dbt")
            result["mode"] = "brownfield"
        if path.suffix in {".py", ".ipynb"}:
            if file.stat().st_size > MAX_BYTES:
                raise ValueError(
                    f"{path}: exceeds 1 MiB inspection limit; inspect metadata separately"
                )
            try:
                text = file.read_text(encoding="utf-8")
                if path.suffix == ".ipynb":
                    notebook = json.loads(text)
                    if not isinstance(notebook, dict) or not isinstance(
                        notebook.get("cells"), list
                    ):
                        raise ValueError("invalid notebook structure")
                    result["notebook_files"].append(name)
                else:
                    if (
                        path.name == "notebook-content.py"
                        and path.parent.name.endswith(".Notebook")
                        and text.splitlines()[:1] == ["# Fabric notebook source"]
                    ):
                        result["notebook_files"].append(name)
                        tree = fabric_import_tree(text)
                    else:
                        tree = ast.parse(text)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import) and any(
                            n.name.split(".")[0] == "dlt" for n in node.names
                        ):
                            stacks.add("dlt")
                        if (
                            isinstance(node, ast.ImportFrom)
                            and (node.module or "").split(".")[0] == "dlt"
                        ):
                            stacks.add("dlt")
                stacks.add("python")
            except (ValueError, SyntaxError, UnicodeError, OSError) as exc:
                raise ValueError(
                    f"{path}: malformed or unreadable {path.suffix} input"
                ) from exc
    result["stacks"] = sorted(stacks)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(inspect_repository(args.root), indent=2))
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Inventory failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
