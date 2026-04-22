@AGENTS.md

## Plugins

This repository publishes the `vibedata` plugin registry for VibeData.

Current plugins:

- `fabric-cli`
- `vibedata-dbt-skills`
- `vibedata-dlt-skills`
- `vibedata-domain-skills`
- `vibedata-ingestion-skills`
- `ad-migration` (external — `accelerate-data/migration-utility`, subpath `plugin`)
- `fabric-semantic-model` (external — `accelerate-data/fabric-semantic-model`)

Plugin updates must follow the `marketplace.json` rules in AGENTS.md and pass:

```bash
claude plugin validate ./plugins/<plugin-name>
```
