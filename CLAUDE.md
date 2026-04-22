# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

A public marketplace for [Vibedata](https://acceleratedata.ai) hosting:

- **Bundled skills** (`plugins/<plugin>/skills/`) — Markdown knowledge packages that customize Vibedata data engineering agent behavior with organizational standards
- **Claude plugins** (`plugins/`) — Installable packages that can contain skills, agents, commands, hooks, or multi-step workflows

No build scripts or test runners. All changes are Markdown or JSON edits.

---

## Bundled skills (`plugins/<plugin>/skills/`)

Skills live inside a plugin bundle. Directory name must **exactly match** the `name` field in `SKILL.md` front matter.

```
plugins/
└── <plugin-name>/
    └── skills/
        └── <skill-name>/
            ├── SKILL.md        # Required
            ├── references/     # Supporting files, one level deep only
            └── context/        # Process artifacts only (never published)
```

### Front matter

```yaml
---
name: dbt-fabric-patterns          # kebab-case, matches directory name. Max 64 chars. No "anthropic" or "claude".
description: >                     # "[What]. Use when [triggers]." Third person. Max 1024 chars. No XML tags.
  ...
tools: Read, Write, Edit, Glob, Grep, Bash
type: platform                     # platform | domain | source | data-engineering | skill-builder
domain: dbt on Microsoft Fabric
version: 1.0.0
---
```

### Structural constraints

- `SKILL.md` under 500 lines — extract long sections to `references/`
- `references/` is one level deep — no subdirectory nesting
- Files over 100 lines need a table of contents
- `context/` is for process artifacts only (clarifications, decisions, research) — never referenced from `SKILL.md`
- No time-sensitive dates or "before/after X date" language — use "legacy" / "current" sections instead
- No Windows-style paths — forward slashes only (`references/guide.md` not `references\guide.md`)

---

## Claude plugins (`plugins/`)

```
plugins/
└── <plugin-name>/
    ├── .claude-plugin/
    │   └── plugin.json     # ONLY this file goes in .claude-plugin/
    ├── agents/
    ├── skills/<skill-name>/SKILL.md
    ├── commands/
    └── hooks/
```

`plugin.json` required fields: `name`, `version`, `description`. Optional: `author`, `homepage`, `repository`, `license`, `keywords`. Full spec: [code.claude.com/docs/en/plugins-reference](https://code.claude.com/docs/en/plugins-reference).

Do not add a `skills` field — skills are auto-discovered from the `skills/` directory.

### Testing

```bash
claude --plugin-dir ./plugins/<plugin-name>      # load without installing
claude plugin validate ./plugins/<plugin-name>   # validate structure
```

---

## `.claude-plugin/marketplace.json`

- Only **plugins** get marketplace entries — skills are auto-discovered via their parent plugin
- Plugin entries: `{ "name", "description", "source": "./plugins/<dir>" }` — no `strict` field needed
- No individual entries for `skills/` directories — they are found automatically
- No `$schema` field, no `skills` field in entries

To sync this file after adding or moving plugins, run `/update-marketplace`.

---

## Anti-patterns

**Skills**
- Nested `references/` subdirectories — one level only
- "When to Use This Skill" body section — triggers belong in `description` frontmatter only
- Process artifacts in `references/` — they go in `context/` only
- `dbt-utils` macros on Fabric — use `tsql-utils` instead
- Mixing `dlt` (dlthub) with Databricks DLT terminology

**Plugins**
- Files other than `plugin.json` inside `.claude-plugin/`
- `"skills"` field in `plugin.json` — not in spec, skills are auto-discovered
- Single-line `plugin.json` — format as pretty-printed JSON
- Bumping `version` in both `plugin.json` and the marketplace entry — manifest always wins

