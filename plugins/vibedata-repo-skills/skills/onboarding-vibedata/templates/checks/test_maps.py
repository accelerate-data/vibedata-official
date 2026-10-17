"""Native schema, dlt registration and dbt selector checks for a selected scaffold."""

import json
import subprocess
import sys
import tomllib
from pathlib import Path
from unittest import SkipTest

import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def _path(value):
    path = (ROOT / value).resolve()
    assert not Path(value).is_absolute() and path.is_relative_to(ROOT), (
        f"{value}: outside repository"
    )
    assert path.is_file(), f"{value}: missing file"
    assert path.stat().st_size <= 1024 * 1024, f"{value}: exceeds 1 MiB"
    return path


def _json(value):
    return json.loads(_path(value).read_text(encoding="utf-8"))


def test_repo_map_schema():
    repo = _json("repo-map.json")
    schema = repo.get("key_references", {}).get("schema", "repo-map.schema.json")
    jsonschema.validate(repo, _json(schema))


def test_source_config_sections():
    repo = _json("repo-map.json")
    gaps = []
    for name, source in repo["sources"].items():
        if source.get("kind") != "dlt":
            continue
        section = source.get("config_section")
        config_path = source.get("config") or repo["artifact_paths"].get(
            "source_config"
        )
        config_file = _path(config_path) if config_path else None
        if config_file is None or config_file.suffix.lower() != ".toml":
            assert section is None, f"{name}: config_section requires TOML"
            gaps.append(name)
            continue
        assert isinstance(section, str) and section, f"{name}: missing config_section"
        config = tomllib.loads(config_file.read_text(encoding="utf-8"))
        node = config
        for key in section.split("."):
            assert isinstance(node, dict) and key in node, (
                f"{name}: missing {section} in {config_path}"
            )
            node = node[key]
        assert isinstance(node, dict), f"{name}: {section} must name a TOML section"
    if gaps:
        raise SkipTest(
            f"source-registration gap: {', '.join(gaps)} use native non-TOML or embedded registration; retain its native check"
        )


def test_dbt_selectors():
    repo = _json("repo-map.json")
    test_map = _json(repo.get("key_references", {}).get("test_map", "test-map.json"))
    for name, module in test_map["modules"].items():
        for kind, selector in module.get("selectors", {}).items():
            assert kind in {"unit", "data"}, (
                f"{name}: unsupported selector kind {kind}; retain its native check"
            )
            assert isinstance(selector, str) and selector.strip(), (
                f"{name}.{kind}: empty selector"
            )
            roles = repo["artifact_paths"]
            if "dbt_profiles" not in roles:
                raise SkipTest(
                    "dbt-selector gap: no artifact_paths.dbt_profiles; verify selectors in the authorized native runtime"
                )
            project = _path(roles["dbt_project"]).parent
            profiles = _path(roles["dbt_profiles"]).parent
            command = [
                sys.executable,
                "-m",
                "dbt.cli.main",
                "--quiet",
                "ls",
                "--project-dir",
                str(project),
                "--profiles-dir",
                str(profiles),
                "--select",
                selector,
                "--resource-type",
                "unit_test" if kind == "unit" else "test",
                "--output",
                "json",
            ]
            if kind == "data":
                command += ["--exclude", "test_type:unit"]
            result = subprocess.run(
                command,
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
            assert result.returncode == 0, (
                f"{name}.{kind}: dbt ls failed; install declared packages before checks. {result.stderr}"
            )
            nodes = []
            for line in result.stdout.splitlines():
                try:
                    node = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(node, dict) and node.get("unique_id"):
                    nodes.append(node)
            assert nodes, f"{name}.{kind}: {selector!r} selects no tests"
