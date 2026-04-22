# Agent Guidelines

This file describes how AI agents should interact with this repository. See `CLAUDE.md` for the full specification of repository structure, conventions, and anti-patterns.

## Repository Type

Markdown and JSON only — no build steps, no test runners. All changes are edits to `.md` or `.json` files.

## Key Entry Points

| File | Purpose |
|---|---|
| `CLAUDE.md` | Full agent guidance: structure, conventions, anti-patterns, custom commands |
| `.claude-plugin/marketplace.json` | Marketplace index — plugins only, not individual skills |
| `plugins/<name>/.claude-plugin/plugin.json` | Per-plugin manifest |
| `plugins/<name>/skills/<skill-name>/SKILL.md` | Skill content and frontmatter |

## Making Changes

- Never commit directly to `main` — always use a feature branch and PR
- Branch naming: `feature/VD-XXX-short-desc` or `docs/topic`
- Run `claude plugin validate ./plugins/<name>` after modifying a plugin
- Update `marketplace.json` after adding or moving plugins (use `/update-marketplace`)

## Invariants to Preserve

- Skill directory names must exactly match the `name` field in `SKILL.md` frontmatter
- Only `plugin.json` belongs inside `.claude-plugin/`
- `references/` directories are one level deep — no nesting
- `context/` directories are process artifacts only — never referenced from `SKILL.md`
