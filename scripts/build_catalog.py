"""Validate the vibedata-official storefront and generate its catalog.

Run `python3 scripts/build_catalog.py` to regenerate catalog/ and the README
generated blocks, or `--check` to fail when the committed output is stale. The
contract rules live in schema/*.json and licenses/allowlist.json; this script
applies them.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = Path(".claude-plugin/marketplace.json")
MANIFEST = Path("manifest.json")
CONNECTOR_SOURCES = Path("connectors/sources.json")
ALLOWLIST = Path("licenses/allowlist.json")
CATALOG_DIR = Path("catalog")
CATALOG_JSON = CATALOG_DIR / "catalog.json"
README = Path("README.md")
MARKETPLACE_NAME = "vibedata-plugins-official"
SCHEMAS = {
    "manifest": Path("schema/manifest.schema.json"),
    "catalog": Path("schema/catalog.schema.json"),
    "connectors": Path("schema/connector-sources.schema.json"),
}
DISCLAIMER = (
    "Third-party content is collated from upstream sources, provided as is, and "
    "used at your own risk. VibeData does not review each upstream change."
)


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> Any:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path}: {exc}")


def load_schemas(root: Path) -> dict[str, dict[str, Any]]:
    schemas: dict[str, dict[str, Any]] = {}
    for name, rel in SCHEMAS.items():
        schema = load_json(root / rel)
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            fail(f"{rel}: not a valid JSON Schema: {exc.message}")
        schemas[name] = schema
    return schemas


def validate(schema: dict[str, Any], instance: Any, label: str) -> list[str]:
    return [
        f"{label}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(instance)
    ]


def load_allowlist(root: Path) -> set[str]:
    data = load_json(root / ALLOWLIST)
    return {str(item) for item in data.get("licenses", [])}


def check_license(
    license_id: Any, label: str, allowlist: set[str], errors: list[str]
) -> None:
    if not isinstance(license_id, str) or not license_id:
        errors.append(f"{label}: license is required")
    elif license_id not in allowlist:
        errors.append(f"{label}: license {license_id!r} is not on the allowlist")


def frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        data = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        fail(f"{path}: invalid frontmatter: {exc}")
    return data if isinstance(data, dict) else {}


def one_line(value: Any) -> str:
    return " ".join(str(value or "").split())


def table_cell(value: Any) -> str:
    return one_line(value).replace("|", "\\|")


def read_plugins(
    root: Path, allowlist: set[str], errors: list[str]
) -> list[dict[str, Any]]:
    data = load_json(root / MARKETPLACE)
    entries: list[dict[str, Any]] = []
    for entry in data.get("plugins", []):
        label = f"{MARKETPLACE}: plugins[{entry.get('name')}]"
        check_license(entry.get("license"), label, allowlist, errors)
        source = entry.get("source")
        if isinstance(source, str):
            source_label = "in-repo"
        elif isinstance(source, dict):
            org_repo = (
                source.get("url", "")
                .removeprefix("https://github.com/")
                .removesuffix(".git")
            )
            path = source.get("path")
            source_label = f"{org_repo} ({path})" if path else org_repo
        else:
            source_label = "unknown"
        item = {
            "name": entry.get("name", ""),
            "description": one_line(entry.get("description")),
            "license": entry.get("license", ""),
            "source": source_label,
            "install": f"/plugin install {entry.get('name', '')}@{MARKETPLACE_NAME}",
        }
        author = entry.get("author")
        if isinstance(author, dict) and author.get("name"):
            item["author"] = str(author["name"])
        entries.append(item)
    return sorted(entries, key=lambda item: item["name"])


def read_skill(root: Path, path: Path, plugin: str | None) -> dict[str, Any]:
    meta = frontmatter(path)
    return {
        "name": str(meta.get("name") or path.parent.name),
        "description": one_line(meta.get("description")),
        "plugin": plugin,
        "path": path.parent.relative_to(root).as_posix(),
    }


def read_skills(root: Path) -> list[dict[str, Any]]:
    entries = [
        read_skill(root, p, None) for p in sorted(root.glob("skills/*/SKILL.md"))
    ]
    for plugin_dir in sorted((root / "plugins").glob("*/skills/*/SKILL.md")):
        plugin = plugin_dir.relative_to(root / "plugins").parts[0]
        entries.append(read_skill(root, plugin_dir, plugin))
    return sorted(entries, key=lambda item: (item["plugin"] or "", item["name"]))


def read_recipes(root: Path) -> list[dict[str, Any]]:
    catalog = load_json(root / "recipes/catalog.json")
    entries = []
    for recipe in catalog.get("recipes", []):
        entries.append(
            {
                "id": recipe.get("id", ""),
                "title": one_line(recipe.get("title")),
                "pitch": one_line(recipe.get("pitch") or recipe.get("description")),
                "area": one_line(recipe.get("area")),
                "readiness": one_line(recipe.get("readiness")),
            }
        )
    return sorted(entries, key=lambda item: item["id"])


def read_mcp(root: Path) -> list[dict[str, Any]]:
    entries = []
    globs = (
        "mcp/*.yaml",
        "mcp/remotes/*.yaml",
        "mcp/obot-remotes/*.yaml",
        "mcp/obot-images/*.yaml",
    )
    for path in [p for pattern in globs for p in sorted(root.glob(pattern))]:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            fail(f"{path}: invalid YAML: {exc}")
        if not isinstance(data, dict):
            continue
        entries.append(
            {
                "name": one_line(data.get("name")),
                "description": one_line(data.get("shortDescription")),
                "runtime": one_line(data.get("runtime")),
                "serverUserType": one_line(data.get("serverUserType")),
            }
        )
    return sorted(entries, key=lambda item: item["name"])


def read_connectors(
    root: Path, schema: dict[str, Any], allowlist: set[str], errors: list[str]
) -> list[dict[str, Any]]:
    data = load_json(root / CONNECTOR_SOURCES)
    errors.extend(validate(schema, data, str(CONNECTOR_SOURCES)))
    entries = []
    for source in data.get("sources", []):
        check_license(
            source.get("license"),
            f"{CONNECTOR_SOURCES}: {source.get('name')}",
            allowlist,
            errors,
        )
        entries.append(
            {
                "name": source.get("name", ""),
                "description": one_line(source.get("description")),
                "url": source.get("url", ""),
                "ref": source.get("ref", ""),
                "license": source.get("license", ""),
                "attribution": source.get("attribution", ""),
            }
        )
    return sorted(entries, key=lambda item: item["name"])


def build_catalog(root: Path) -> tuple[dict[str, Any], list[str]]:
    schemas = load_schemas(root)
    allowlist = load_allowlist(root)
    errors: list[str] = []

    manifest = load_json(root / MANIFEST)
    errors.extend(validate(schemas["manifest"], manifest, str(MANIFEST)))
    for name, source in manifest.get("content", {}).items():
        if "license" in source:
            check_license(
                source["license"], f"{MANIFEST}: content.{name}", allowlist, errors
            )
        path = root / source.get("path", "")
        if not path.exists():
            errors.append(
                f"{MANIFEST}: content.{name}.path {source.get('path')!r} does not exist"
            )

    catalog = {
        "schemaVersion": 1,
        "entries": {
            "plugins": read_plugins(root, allowlist, errors),
            "skills": read_skills(root),
            "recipes": read_recipes(root),
            "connectors": read_connectors(
                root, schemas["connectors"], allowlist, errors
            ),
            "mcp": read_mcp(root),
        },
    }
    errors.extend(validate(schemas["catalog"], catalog, str(CATALOG_JSON)))
    return catalog, errors


def page(title: str, columns: list[str], rows: list[list[str]]) -> str:
    return (
        f"# {title}\n\n{DISCLAIMER}\n\n{page_free_table(columns, rows)}\n\n----\n\n"
        "Generated by `scripts/build_catalog.py`. Do not edit by hand.\n"
    )


def render_pages(catalog: dict[str, Any]) -> dict[Path, str]:
    e = catalog["entries"]
    pages = {
        "plugins": page(
            "Plugins",
            ["Plugin", "Description", "Author", "License", "Source"],
            [
                [
                    f"`{p['name']}`",
                    table_cell(p["description"]),
                    table_cell(p.get("author", "")),
                    table_cell(p["license"]),
                    table_cell(p["source"]),
                ]
                for p in e["plugins"]
            ],
        ),
        "skills": page(
            "Skills",
            ["Skill", "Bundle", "Description"],
            [
                [
                    f"`{s['name']}`",
                    table_cell(s["plugin"] or "Skill Library"),
                    table_cell(s["description"]),
                ]
                for s in e["skills"]
            ],
        ),
        "recipes": page(
            "Recipes",
            ["Recipe", "Title", "Area", "Readiness"],
            [
                [
                    f"`{r['id']}`",
                    table_cell(r["title"]),
                    table_cell(r["area"]),
                    table_cell(r["readiness"]),
                ]
                for r in e["recipes"]
            ],
        ),
        "connectors": page(
            "Connector sources",
            ["Source", "Description", "Upstream", "License"],
            [
                [
                    f"`{c['name']}`",
                    table_cell(c["description"]),
                    f"[{table_cell(c['url'])}]({c['url']})",
                    table_cell(c["license"]),
                ]
                for c in e["connectors"]
            ],
        ),
        "mcp": page(
            "MCP servers",
            ["Server", "Description", "Runtime", "Access"],
            [
                [
                    table_cell(m["name"]),
                    table_cell(m["description"]),
                    table_cell(m["runtime"]),
                    table_cell(m["serverUserType"]),
                ]
                for m in e["mcp"]
            ],
        ),
    }
    return {CATALOG_DIR / f"{name}.md": body for name, body in pages.items()}


def render_readme_blocks(catalog: dict[str, Any]) -> dict[str, str]:
    e = catalog["entries"]
    summary_rows = [
        ["Plugins", len(e["plugins"]), "[catalog/plugins.md](catalog/plugins.md)"],
        ["Skills", len(e["skills"]), "[catalog/skills.md](catalog/skills.md)"],
        ["Recipes", len(e["recipes"]), "[catalog/recipes.md](catalog/recipes.md)"],
        [
            "Connector sources",
            len(e["connectors"]),
            "[catalog/connectors.md](catalog/connectors.md)",
        ],
        ["MCP servers", len(e["mcp"]), "[catalog/mcp.md](catalog/mcp.md)"],
    ]
    summary = page_free_table(["Catalog", "Entries", "Browse"], summary_rows)
    plugins = page_free_table(
        ["Plugin", "What it does", "License", "Install"],
        [
            [
                f"`{p['name']}`",
                table_cell(p["description"]),
                table_cell(p["license"]),
                f"`{p['install']}`",
            ]
            for p in e["plugins"]
        ],
    )
    skills = page_free_table(
        ["Skill", "Bundle", "What it encodes"],
        [
            [
                f"`{s['name']}`",
                table_cell(s["plugin"] or "Skill Library"),
                table_cell(s["description"]),
            ]
            for s in e["skills"]
        ],
    )
    return {
        "catalog-summary": summary,
        "available-plugins": plugins,
        "skill-library": skills,
    }


def page_free_table(columns: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    lines.extend("| " + " | ".join(str(cell) for cell in row) + " |" for row in rows)
    return "\n".join(lines)


def replace_block(text: str, name: str, body: str) -> str:
    begin = f"<!-- BEGIN GENERATED: {name} -->"
    end = f"<!-- END GENERATED: {name} -->"
    if begin not in text or end not in text:
        fail(f"{README}: missing generated block markers for {name}")
    before, rest = text.split(begin, 1)
    _, after = rest.split(end, 1)
    return f"{before}{begin}\n{body}\n{end}{after}"


def build_outputs(root: Path) -> dict[Path, str]:
    catalog, errors = build_catalog(root)
    if errors:
        fail(
            "catalog validation failed:\n" + "\n".join(f"- {error}" for error in errors)
        )

    outputs: dict[Path, str] = {CATALOG_JSON: json.dumps(catalog, indent=2) + "\n"}
    outputs.update(render_pages(catalog))

    readme = (root / README).read_text(encoding="utf-8")
    for name, body in render_readme_blocks(catalog).items():
        readme = replace_block(readme, name, body)
    outputs[README] = readme
    return outputs


def stale_paths(root: Path, outputs: dict[Path, str]) -> list[str]:
    stale = []
    for path, expected in outputs.items():
        target = root / path
        actual = target.read_text(encoding="utf-8") if target.exists() else None
        if actual != expected:
            stale.append(str(path))
    return stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="fail when committed output is stale"
    )
    args = parser.parse_args()

    root = ROOT
    outputs = build_outputs(root)

    if args.check:
        stale = stale_paths(root, outputs)
        if stale:
            fail(
                "generated output is stale — run `python3 scripts/build_catalog.py`:\n"
                + "\n".join(f"- {p}" for p in stale)
            )
        print("catalog is up to date")
        return 0

    for path, content in outputs.items():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
