<p align="left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/accelerate-data-logo-light.svg">
    <img src="./assets/accelerate-data-logo-dark.svg" alt="Accelerate Data" height="48">
  </picture>
</p>

The official skill library and plugin marketplace for [VibeData](https://acceleratedata.ai) — the agentic coordination layer for data platforms.

> Domain expertise, encoded and enforced.

## Why This Exists

Data teams lose weeks to coordination tax — intent lost between role switches, fix patterns never captured, institutional knowledge trapped in people's heads. Current tools address individual slices (ingestion, transformation, observability) without connecting them.

This repository is the distribution layer for the domain expertise that powers VibeData's agentic workflow. Skills encode business rules, source-system patterns, and platform conventions so that agents can build, deploy, and operate pipelines with your team's accumulated knowledge — not generic defaults.

## Skills vs Plugins

| | Skills | Plugins |
|---|---|---|
| **What** | Markdown knowledge packages that encode domain expertise | Full Claude Code plugins with agents, multi-step workflows, and bundled skills |
| **How they work** | Loaded into VibeData agents at runtime to guide decisions | Installed and executed as standalone tools |
| **Example** | dbt naming conventions for Fabric, SCD2 snapshot patterns | Migration workflow that scopes, profiles, generates, and tests dbt models |

Skills are the knowledge. Plugins are the workflows that use that knowledge.

## Quick Start

Add the marketplace:

```bash
/plugin marketplace add accelerate-data/vibedata-plugins-official
```

Install the flagship plugin:

```bash
/plugin install ad-migration@vibedata-plugins-official
```

Then explore the rest of the catalog from the same marketplace.

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

## Available Skills

Skills are organized by type, reflecting where they sit in the data platform lifecycle.

### Platform

| Skill | What it encodes |
|---|---|
| `dbt-fabric-patterns` | Practitioner-level dbt patterns for Microsoft Fabric |
| `dbt-semantic-layer` | Semantic models and MetricFlow metrics in dbt on Microsoft Fabric |
| `elementary-data-quality` | Elementary anomaly detection configuration for dbt on Microsoft Fabric |

### Source

| Skill | What it encodes |
|---|---|
| `dlt-rest-api-connector` | dlt REST API pipelines to ADLS Gen2 and OneLake |
| `salesforce-extraction` | Salesforce data extraction via dlt into dbt on Microsoft Fabric |

### Domain

| Skill | What it encodes |
|---|---|
| `revenue-domain` | Revenue recognition mapped to dbt medallion architecture on Microsoft Fabric |

### Data Engineering

| Skill | What it encodes |
|---|---|
| `dbt-snapshot-scd2` | SCD Type 2 snapshot implementation in dbt on Microsoft Fabric |

### Skill Builder

Skill-builder skills appear in Settings and are active every session. They guide agents on how to create and maintain skills themselves.

| Skill | What it encodes |
|---|---|
| `skill-builder-practices` | Skill structure rules, content principles, quality dimensions, and anti-patterns |

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
