@AGENTS.md

## Plugins

This repository publishes the `vibedata` plugin registry for VibeData.
Plugin updates must follow the marketplace rules in AGENTS.md and pass:

```bash
claude plugin validate ./plugins/<plugin-name>
codex plugin marketplace add .
python3 scripts/validate-marketplace.py
```
