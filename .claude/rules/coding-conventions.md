# Coding Conventions

This is the canonical source for naming, markdown, JSON, and error-handling conventions.

## Markdown

- Keep `SKILL.md` concise. Move long supporting material into `references/`.
- Use sentence-style prose with no hard wrapping at a fixed column.
- Prefer forward-slash paths in examples and references.
- When a file exceeds 100 lines, add a table of contents.
- Keep process artifacts out of published `references/`; use `context/` instead.

## JSON

- Format JSON as pretty-printed JSON with 2-space indentation.
- Keep keys stable and deterministic where ordering matters for reviewability.
- Do not add unsupported fields to `plugin.json` or `.claude-plugin/marketplace.json`.

## Repository Content

- Directory names for standalone skills must match the `name` field in `SKILL.md` front matter exactly.
- Only `plugin.json` belongs inside a plugin's `.claude-plugin/` directory.
- Do not create marketplace entries for individual skills; only plugins belong in `.claude-plugin/marketplace.json`.

## Error Handling

- Validate structural assumptions at the repository boundary before writing files.
- Stop on malformed JSON, missing required manifest fields, or invalid marketplace structure.
- Prefer explicit failures over silent repair when a repo contract is violated.
