"""Check context paths and instruction references; never execute registered commands."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

ROLES = {
    "context",
    "adr",
    "design_record_model",
    "design_record_pipeline",
    "review",
    "proposal",
    "onboarding_report",
}
STUDIO_ROLES = {
    "requirement",
    "plan",
    "verification",
    "case_record",
    "design_record_area",
}
REFERENCES = {"agents", "instructions", "schema", "test_map"}
PATH_FIELDS = {"path", "module", "pipeline", "docs", "tests", "design_record", "config"}
PATTERN = re.compile(r"\{[a-zA-Z_][a-zA-Z_0-9]*\}")
MAX_BYTES = 1024 * 1024


def resolve_path(
    root: Path, value: object, *, pattern: bool = False, base: Path | None = None
) -> Path:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise ValueError(f"invalid repository path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or urlsplit(value).scheme:
        raise ValueError(f"{value}: path must be repository-relative")
    expanded = PATTERN.sub("placeholder", value) if pattern else value
    if "{" in expanded or "}" in expanded:
        raise ValueError(f"{value}: invalid or unexpected placeholder pattern")
    if base is None and ".." in path.parts:
        raise ValueError(f"{value}: path escapes repository convention")
    if pattern and any(c in value for c in "*?["):
        if (
            PATTERN.search(value)
            or "**" in value
            or any(c in path.parent.as_posix() for c in "*?[")
        ):
            raise ValueError(
                f"{value}: glob must select files in one literal directory"
            )
        directory = resolve_path(root, path.parent.as_posix(), base=base)
        matches = sorted(directory.glob(path.name))
        if not matches:
            raise ValueError(f"{value}: artifact glob matches no files")
        for match in matches:
            checked = resolve_path(root, match.relative_to(root).as_posix())
            if not checked.is_file():
                raise ValueError(f"{value}: artifact glob must match files")
        return directory
    candidate = (base or root) / expanded
    try:
        resolved = candidate.resolve()
    except (OSError, RuntimeError) as exc:
        raise ValueError(f"{value}: symlink cycle or unresolved path") from exc
    if not resolved.is_relative_to(root):
        raise ValueError(f"{value}: path resolves outside repository")
    current = base or root
    for part in PurePosixPath(expanded).parts:
        if part == "..":
            current = current.parent
            continue
        if current.is_dir():
            names = [p.name for p in current.iterdir()]
            matches = [n for n in names if n.casefold() == part.casefold()]
            if matches and (part not in names or len(matches) > 1):
                raise ValueError(
                    f"{value}: filename case mismatch or ambiguity at {part}"
                )
        current = current / part
    if not (pattern and PATTERN.search(value)) and not candidate.exists():
        raise ValueError(f"{value}: registered path is missing")
    return candidate


def read_text(path: Path) -> str:
    if path.stat().st_size > MAX_BYTES:
        raise ValueError(f"{path.name}: exceeds 1 MiB context limit")
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValueError(f"{path.name}: cannot read UTF-8 context") from exc


def read_object(path: Path) -> dict:
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path.name}: malformed JSON at line {exc.lineno}") from exc
    if not isinstance(data, dict):
        raise TypeError(f"{path.name}: expected a JSON object")
    return data


def source_routing_findings(root: Path, repo: dict) -> list[str]:
    """Check declared ownership; never execute a runner or inspect remote state."""
    errors = []
    sources = repo.get("sources", {})
    if not isinstance(sources, dict):
        return ["sources must be an object"]
    if "orchestrators" in repo:
        runners = repo["orchestrators"]
        if not isinstance(runners, dict):
            return ["orchestrators must be an object"]
        runs = set()
        for name, runner in runners.items():
            label = f"orchestrators.{name}"
            if not isinstance(runner, dict):
                errors.append(f"{label}: expected an object")
                continue
            if not isinstance(runner.get("kind"), str) or not runner["kind"].strip():
                errors.append(f"{label}: kind is required")
            if ("path" in runner) == ("location" in runner):
                errors.append(f"{label}: supply exactly one of path or location")
            if "path" in runner:
                try:
                    path = resolve_path(root, runner["path"])
                    if not path.is_file():
                        errors.append(f"{label}: runner path must name a file")
                except (OSError, ValueError) as exc:
                    errors.append(f"{label}: {exc}")
            elif (
                not isinstance(runner.get("location"), str)
                or not runner["location"].strip()
            ):
                errors.append(f"{label}: external location is required")
            members = runner.get("runs")
            if not isinstance(members, list) or any(
                not isinstance(member, str) or not member.strip() for member in members
            ):
                errors.append(f"{label}: runs must list source names")
            else:
                if len(set(members)) != len(members):
                    errors.append(f"{label}: duplicate source in runs")
                runs.update(members)
        if runs - sources.keys():
            errors.append(
                f"orchestrators run unknown sources: {sorted(runs - sources.keys())}"
            )
        if sources.keys() - runs:
            errors.append(
                f"sources with no orchestrator: {sorted(sources.keys() - runs)}"
            )
    datasets = {}
    for name, source in sources.items():
        if not isinstance(source, dict):
            continue
        dataset = source.get("dataset")
        if dataset is not None:
            if not isinstance(dataset, str) or not dataset.strip():
                errors.append(f"sources.{name}: dataset must be a nonempty string")
                continue
            datasets.setdefault(dataset, []).append((name, source))
        if "produces" in source:
            tables = source["produces"]
            if (
                not isinstance(tables, list)
                or not tables
                or any(not isinstance(t, str) or not t.strip() for t in tables)
            ):
                errors.append(
                    f"sources.{name}: produces must list nonempty table names"
                )
            elif len(set(tables)) != len(tables):
                errors.append(f"sources.{name}: duplicate table in produces")
    for dataset, owners in datasets.items():
        if len(owners) < 2:
            continue
        claimed = set()
        for name, source in owners:
            tables = source.get("produces")
            if not isinstance(tables, list) or not tables:
                errors.append(
                    f"sources.{name}: shared dataset {dataset} requires produces"
                )
                continue
            for table in tables:
                if not isinstance(table, str) or not table.strip():
                    continue
                if table in claimed:
                    errors.append(f"sources on {dataset} claim the same table: {table}")
                claimed.add(table)
    return errors


def instruction_findings(root: Path, starts: list[Path]) -> list[str]:
    errors = []
    visited = set()
    imports: dict[Path, list[Path]] = {}
    pending = list(starts)
    while pending:
        file = pending.pop().resolve()
        if file.resolve() in visited or file.suffix.lower() != ".md":
            continue
        if len(visited) >= 1000:
            errors.append("Instruction references exceed 1000 documents")
            break
        visited.add(file.resolve())
        try:
            # Examples are not active imports or links.
            content = re.sub(
                r"^\s*(```|~~~).*?^\s*\1\s*$",
                "",
                read_text(file),
                flags=re.MULTILINE | re.DOTALL,
            )
            content = re.sub(r"(`+).*?\1", "", content, flags=re.DOTALL)
            references = [
                (m.rstrip(".:"), True)
                for m in re.findall(r"(?<![\w@/])@([^\s`<>()[\],;!?\"']+)", content)
            ]
            references += [
                (m, False)
                for m in re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', content)
            ]
            for raw, is_import in references:
                value = unquote(raw.strip("<>").split("#")[0])
                if not value or (
                    not is_import
                    and urlsplit(value).scheme in {"http", "https", "mailto"}
                ):
                    continue
                try:
                    if any(
                        p.startswith((".env", "secrets.", "credentials."))
                        or p.endswith((".key", ".pem"))
                        for p in PurePosixPath(value).parts
                    ):
                        raise ValueError("secret-bearing reference must not be loaded")
                    target = resolve_path(root, value, base=file.parent)
                    if is_import:
                        imports.setdefault(file.resolve(), []).append(target.resolve())
                    if target.is_file() and target.suffix.lower() == ".md":
                        pending.append(target)
                except (ValueError, TypeError, OSError) as exc:
                    errors.append(f"{file.relative_to(root)}: {exc}")
        except (ValueError, TypeError, OSError) as exc:
            errors.append(str(exc))
    complete = set()

    def visit(file, chain):
        if file in chain:
            errors.append(
                "Instruction import cycle: "
                + " -> ".join(str(p.relative_to(root)) for p in [*chain, file])
            )
            return
        if file in complete:
            return
        for target in imports.get(file, []):
            visit(target, [*chain, file])
        complete.add(file)

    for file in imports:
        visit(file, [])
    return errors


def validate_context(root: Path, *, consumer: str = "standalone") -> list[str]:
    if consumer not in {"standalone", "studio"}:
        raise ValueError(f"Unknown consumer: {consumer}")
    errors = []
    try:
        root = root.resolve(strict=True)
        if not root.is_dir():
            return ["Repository root must be a directory"]
        repo = read_object(resolve_path(root, "repo-map.json"))
    except (OSError, ValueError, TypeError, RuntimeError) as exc:
        return [str(exc)]

    def check_path(value, label, pattern=False):
        try:
            return resolve_path(root, value, pattern=pattern)
        except (OSError, ValueError) as exc:
            errors.append(f"{label}: {exc}")
            return None

    for key in (
        "modules",
        "sources",
        "commands",
        "artifact_paths",
        "key_references",
    ):
        if not isinstance(repo.get(key), dict):
            errors.append(f"repo-map.json: {key} must be an object")
    for key in ("entrypoints", "notes_for_agents"):
        if not isinstance(repo.get(key), (dict, list)):
            errors.append(f"repo-map.json: {key} must be an object or list")
    errors.extend(source_routing_findings(root, repo))
    roles = repo.get("artifact_paths", {})
    if isinstance(roles, dict):
        required_roles = ROLES | STUDIO_ROLES if consumer == "studio" else ROLES
        for key in sorted(required_roles - roles.keys()):
            errors.append(f"artifact_paths: missing role {key}")
        for key, value in roles.items():
            check_path(value, f"artifact_paths.{key}", pattern=True)
    refs = repo.get("key_references", {})
    resolved_refs = {}
    if isinstance(refs, dict):
        if not {"conventions", "rules"} & refs.keys():
            errors.append("key_references: missing conventions or legacy rules")
        for key in sorted(REFERENCES - refs.keys()):
            errors.append(f"key_references: missing {key}")
        for key, value in refs.items():
            path = check_path(value, f"key_references.{key}")
            if path:
                resolved_refs[key] = path
        if refs.get("instructions") != "AGENTS.md":
            errors.append(
                "Canonical instructions must resolve to AGENTS.md; verify runtime discovery before changing casing"
            )
    for section in ("modules", "sources", "layers"):
        entries = repo.get(section, {})
        if not isinstance(entries, dict):
            continue
        for name, entry in entries.items():
            if not isinstance(entry, dict):
                errors.append(f"{section}.{name}: expected an object")
                continue
            if section == "modules" and (
                not isinstance(entry.get("path"), str) or not entry["path"]
            ):
                errors.append(f"modules.{name}: path must be a nonempty string")
            if section == "sources" and (
                not isinstance(entry.get("kind"), str) or not entry["kind"]
            ):
                errors.append(f"sources.{name}: implementation kind is required")
            for key in PATH_FIELDS & entry.keys():
                values = entry[key] if isinstance(entry[key], list) else [entry[key]]
                for value in values:
                    check_path(value, f"{section}.{name}.{key}")
            artifacts = entry.get("artifacts", {})
            if not isinstance(artifacts, dict):
                errors.append(f"{section}.{name}.artifacts: expected an object")
                artifacts = {}
            for key, value in artifacts.items():
                check_path(value, f"{section}.{name}.artifacts.{key}")
            required = entry.get("required_artifacts", [])
            if not isinstance(required, list) or any(
                not isinstance(k, str) for k in required
            ):
                errors.append(
                    f"{section}.{name}.required_artifacts: expected a list of keys"
                )
            else:
                for key in required:
                    if key not in entry and key not in artifacts:
                        errors.append(
                            f"{section}.{name}: missing required artifact {key}"
                        )
                    elif key in entry:
                        values = (
                            entry[key] if isinstance(entry[key], list) else [entry[key]]
                        )
                        if not values:
                            errors.append(
                                f"{section}.{name}.{key}: required artifact is empty"
                            )
                        for value in values:
                            check_path(value, f"{section}.{name}.{key}")
    if isinstance(repo.get("entrypoints"), dict):
        for key, value in repo["entrypoints"].items():
            check_path(value, f"entrypoints.{key}")
    if isinstance(repo.get("entrypoints"), list):
        for value in repo["entrypoints"]:
            check_path(value, "entrypoints")
    for key in ("schema", "test_map"):
        path = resolved_refs.get(key)
        if not path:
            continue
        try:
            data = read_object(path)
            if key == "schema":
                continue
            if not isinstance(data.get("taxonomy"), dict) or not isinstance(
                data.get("modules"), dict
            ):
                errors.append("test-map.json: taxonomy and modules must be objects")
                continue
            for name, entry in data["modules"].items():
                if not isinstance(entry, dict) or not isinstance(
                    entry.get("sources"), list
                ):
                    errors.append(f"test-map.modules.{name}: sources must be a list")
                    continue
                for field in ("sources", "unit", "data", "structural"):
                    paths = entry.get(field, [])
                    if not isinstance(paths, list):
                        errors.append(
                            f"test-map.modules.{name}.{field}: expected a list"
                        )
                        continue
                    for value in paths:
                        check_path(value, f"test-map.modules.{name}.{field}")
        except (ValueError, TypeError, OSError) as exc:
            errors.append(str(exc))
    starts = [
        p
        for k, p in resolved_refs.items()
        if k in {"agents", "instructions"} and p.is_file()
    ]
    rules = resolved_refs.get("rules")
    if rules and rules.is_dir():
        for p in rules.rglob("*.md"):
            checked = check_path(p.relative_to(root).as_posix(), "rules")
            if checked:
                starts.append(checked)
    skill_roots = [
        resolved_refs.get("conventions"),
        root / ".agents/skills",
        root / ".claude/skills",
    ]
    pending = [
        p for p in skill_roots if p is not None and (p.exists() or p.is_symlink())
    ]
    visited = set()
    while pending:
        directory = pending.pop()
        checked = check_path(directory.relative_to(root).as_posix(), "conventions")
        if checked is None or checked.resolve() in visited:
            continue
        if not checked.is_dir():
            errors.append(
                f"conventions: {directory.relative_to(root)} must be a directory"
            )
            continue
        if len(visited) >= 1000:
            errors.append("Convention discovery exceeds 1000 directories")
            break
        visited.add(checked.resolve())
        for entry in checked.iterdir():
            if entry.is_symlink() or entry.is_dir() or entry.name == "SKILL.md":
                target = check_path(entry.relative_to(root).as_posix(), "conventions")
                if target is None:
                    continue
                if target.is_dir():
                    pending.append(target)
                elif target.name == "SKILL.md":
                    starts.append(target)
    claude = root / "CLAUDE.md"
    if claude.exists() or claude.is_symlink():
        checked = check_path("CLAUDE.md", "bootstrap")
        if checked:
            starts.append(checked)
            if (root / "AGENTS.md").exists() and checked.samefile(root / "AGENTS.md"):
                errors.append(
                    "CLAUDE.md and AGENTS.md are same-file aliases; resolve ownership before writing"
                )
            elif read_text(checked).strip() != "@AGENTS.md":
                errors.append(
                    "CLAUDE.md must contain only @AGENTS.md after lossless consolidation"
                )
    errors.extend(instruction_findings(root, starts))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument(
        "--consumer", choices=("standalone", "studio"), default="standalone"
    )
    args = parser.parse_args()
    try:
        findings = validate_context(args.root, consumer=args.consumer)
    except (OSError, ValueError, TypeError, RuntimeError) as exc:
        findings = [str(exc)]
    if findings:
        print("\n".join(findings), file=sys.stderr)
        return 1
    print(
        "Context structure valid; metadata, runtime instruction loading and execution remain unverified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
