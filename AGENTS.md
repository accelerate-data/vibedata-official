# AGENTS.md

## Repository purpose

Bundled plugin marketplace for [VibeData](https://acceleratedata.ai). Each subdirectory under `plugins/` is a self-contained Claude and Codex plugin package containing skills and optionally agents, commands, and hooks. The root `.claude-plugin/marketplace.json` is the Claude registry index. The root `.agents/plugins/marketplace.json` is the Codex registry index.

No build scripts or test runners. All changes are Markdown or JSON edits.

## marketplace.json rules

- Only plugins get entries — skills are auto-discovered from each plugin's `skills/` directory
- Local plugin entries: `{ "name", "description", "source": "./plugins/<dir>" }`
- External whole-repo plugins: `"source": { "source": "url", "url": "https://github.com/org/repo.git" }`
- External subdirectory plugins: `"source": { "source": "git-subdir", "url": "https://github.com/org/repo", "path": "subdir" }` — only when the plugin lives in a real subpath, never with `path: "."`
- No `$schema` field, no `strict` field, no `version` field in entries — version lives in each plugin's `plugin.json`

## Plugin structure

- Each plugin lives at `plugins/<name>/` with a `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`
- Only `plugin.json` goes inside `.claude-plugin/` — no other files
- Only `plugin.json` goes inside `.codex-plugin/` — no other files
- Skills are auto-discovered from `skills/` — do not add a `skills` field to `plugin.json`
- `plugin.json` required fields: `name`, `version`, `description`

## Codex marketplace rules

- Codex marketplace entries live in `.agents/plugins/marketplace.json`
- Codex entries use `{ "source": { "source": "local", "path": "./plugins/<name>" } }`
- Every Codex entry must include `policy.installation`, `policy.authentication`, and `category`
- Codex local source paths must stay under `./plugins/`
- Every Codex marketplace entry must point to a plugin with `.codex-plugin/plugin.json`
- `.claude-plugin/marketplace.json.metadata.version` is the single marketplace catalog version. Bump it when adding plugin entries to either the Claude or Codex marketplace manifest.

## Anti-patterns

- Files other than `plugin.json` inside `.claude-plugin/`
- Files other than `plugin.json` inside `.codex-plugin/`
- `"skills"` field in `plugin.json` — skills are auto-discovered
- Single-line `plugin.json` — use pretty-printed JSON
- `version` field in marketplace entries — version lives in `plugin.json`
- Bumping `version` in both `plugin.json` and the marketplace entry — manifest always wins
- Entries for individual skills — only plugins get marketplace entries
- `git-subdir` with `path: "."` — use `"source": "url"` with a `.git` URL for whole-repo external plugins
