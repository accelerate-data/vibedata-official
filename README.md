<p align="left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/accelerate-data-logo-light.svg">
    <img src="./assets/accelerate-data-logo-dark.svg" alt="Accelerate Data" height="48">
  </picture>
</p>

The official skill library and plugin marketplace for [VibeData](https://acceleratedata.ai) — the agentic coordination layer for data platforms.

> Organizational data engineering standards, encoded and enforced.

## Why This Exists

Data teams lose weeks to coordination tax — intent lost between role switches, fix patterns never captured, institutional knowledge trapped in people's heads. Current tools address individual slices (ingestion, transformation, observability) without connecting them.

This repository is the distribution layer for the standards that customize VibeData data engineering agents. Skills encode organizational rules for ingestion, extraction, source-system handling, platform conventions, and business logic so agents build, deploy, and operate pipelines with your team's accumulated knowledge — not generic defaults.

The same bundles can also be installed directly in Claude Code as standalone skills for practitioners who want those standards available outside VibeData.

## Skills vs Plugins

| | Skills | Plugins |
|---|---|---|
| **What** | Markdown knowledge packages that encode organizational standards, source customization, and business rules | Installable Claude Code packages that bundle skills for VibeData agents or standalone Claude Code use |
| **How they work** | Loaded into VibeData data engineering agents to align behavior with your team's standards | Installed from the marketplace as reusable capabilities |
| **Example** | dbt naming conventions for Fabric, SCD2 snapshot patterns | Skill bundles like `vibedata-dbt-skills`, or workflow plugins like `ad-migration` |

Skills are the behavior-shaping knowledge. Plugins are the distribution unit that makes those standards available to VibeData agents and, when useful, to Claude Code directly.

## Quick Start

Add the marketplace:

```bash
/plugin marketplace add accelerate-data/vibedata-plugins-official
```

Install the flagship plugin:

```bash
/plugin install ad-migration@vibedata-plugins-official
```

Then explore the rest of the catalog from the same marketplace. Skill bundles are intended for VibeData agent customization first, and can also be installed directly in Claude Code.

### Codex

Add the Codex marketplace:

```bash
codex plugin marketplace add accelerate-data/vibedata-plugins-official
```

The Codex marketplace is declared in `.agents/plugins/marketplace.json`, and each bundled plugin exposes a `.codex-plugin/plugin.json` manifest.

## Featured Plugin: ad-migration

`ad-migration` helps teams modernize legacy data warehouses into governed Fabric Lakehouse platforms.

The result is a cleaner, agent-ready foundation for VibeData workflows and more predictable AI outcomes.

It is designed for teams that need to:

- assess and scope legacy SQL Server warehouse assets
- profile source structures and migration candidates
- generate tests and dbt models as part of a repeatable workflow
- move from one-off migration efforts to governed, reviewable delivery

Install:

```bash
/plugin install ad-migration@vibedata-plugins-official
```

## Available Plugins

| Plugin | What it does | Best for | Install |
|---|---|---|---|
| `ad-migration` | Governed migration workflows for stored procedures, warehouse logic, and dbt model generation | Legacy warehouse to Fabric Lakehouse modernization | `/plugin install ad-migration@vibedata-plugins-official` |
| `fabric-cli` | Operational workflows for Fabric workspaces, notebooks, pipelines, and OneLake | Fabric platform operations and environment control | `/plugin install fabric-cli@vibedata-plugins-official` |
| `fabric-semantic-model` | TMDL semantic model design, validation, and DAX measure authoring | Fabric and Power BI semantic model delivery | `/plugin install fabric-semantic-model@vibedata-plugins-official` |
| `vibedata-dbt-skills` | Customizes dbt agents with Fabric modeling, snapshot, semantic layer, and Elementary quality standards | dbt project delivery on Microsoft Fabric | `/plugin install vibedata-dbt-skills@vibedata-plugins-official` |
| `vibedata-dlt-skills` | Customizes ingestion agents with dlt REST API standards for ADLS Gen2, OneLake, and Fabric lakehouses | API ingestion pipelines feeding dbt | `/plugin install vibedata-dlt-skills@vibedata-plugins-official` |
| `vibedata-domain-skills` | Customizes modeling agents with business rules, including revenue recognition | Domain-aware marts and accounting logic | `/plugin install vibedata-domain-skills@vibedata-plugins-official` |
| `vibedata-ingestion-skills` | Customizes extraction agents with source-system standards, including Salesforce extraction | CRM/source-system extraction patterns | `/plugin install vibedata-ingestion-skills@vibedata-plugins-official` |

## Skill Bundle Contents

Skills are distributed through Claude plugins. Install the bundle that matches the VibeData agent behavior you want to customize, or install it directly in Claude Code for standalone use.

### `vibedata-dbt-skills`

| Skill | What it encodes |
|---|---|
| `dbt-fabric-patterns` | Practitioner-level dbt patterns for Microsoft Fabric |
| `dbt-semantic-layer` | Semantic models and MetricFlow metrics in dbt on Microsoft Fabric |
| `dbt-snapshot-scd2` | SCD Type 2 snapshot implementation in dbt on Microsoft Fabric |
| `elementary-data-quality` | Elementary anomaly detection configuration for dbt on Microsoft Fabric |

### `vibedata-dlt-skills`

| Skill | What it encodes |
|---|---|
| `dlt-rest-api-connector` | dlt REST API pipelines to ADLS Gen2 and OneLake |

### `vibedata-domain-skills`

| Skill | What it encodes |
|---|---|
| `modeling-revenue-recognition` | Revenue recognition mapped to dbt medallion architecture on Microsoft Fabric |

### `vibedata-ingestion-skills`

| Skill | What it encodes |
|---|---|
| `salesforce-extraction` | Salesforce data extraction via dlt into dbt on Microsoft Fabric |

## How Skills Work in VibeData

Skills plug into three surfaces of the VibeData agentic workflow:

- **Build** — When a practitioner describes business intent, agents draw on skills to validate domain fit and generate code that follows your team's conventions.
- **Deploy** — When a PR is opened, deploy agents use skills to run context-informed quality gates — checking documentation, code quality, test coverage, and data quality.
- **Operate** — When a production incident is resolved, fix patterns are captured as new skills and tests, preventing recurrence on future deployments.

Every pipeline built and every incident resolved makes the skill library more valuable. This is the improvement flywheel: accumulated domain expertise that compounds over time.

## Coming Soon

| Plugin | Planned focus |
|---|---|
| `fabric-ontology` | Business ontology and semantic layer design workflows for governed analytics platforms |

## Contributing

Contributions are welcome, but this repository is curated. If you want to contribute a skill or plugin, or improve an existing one:

1. Open an issue or pull request with the proposed change.
2. Keep the README and marketplace entry aligned with the actual purpose.
3. Follow the repository conventions in [CLAUDE.md](./CLAUDE.md).

## License

Elastic License 2.0. See [LICENSE](./LICENSE).
