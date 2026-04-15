<p align="left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/accelerate-data-logo-light.svg">
    <img src="./assets/accelerate-data-logo-dark.svg" alt="Accelerate Data" height="48">
  </picture>
</p>

Official curated Claude plugins from Accelerate Data

> AI needs good data. Good data needs AI.

Accelerate Data publishes Claude plugins for governed, AI-ready data platforms. This marketplace focuses on practical workflows for modernization, Microsoft Fabric, analytics engineering, and AI-assisted delivery, not generic prompt packs or thin tool wrappers.

The emphasis is repeatable execution: clear workflows, reviewable outputs, and plugins that help teams move from fragile one-off efforts to governed delivery on modern data platforms.

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

The result is a cleaner, agent-ready foundation for Vibedata workflows and more predictable AI outcomes.

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

## Coming Soon

| Plugin | Planned focus |
|---|---|
| `fabric-semantic-models` | Guided workflows for designing and iterating Fabric semantic models |
| `fabric-ontology` | Business ontology and semantic layer design workflows for governed analytics platforms |

## About This Marketplace

This repository is the official Accelerate Data marketplace for Claude plugins focused on data platform work. The catalog is opinionated: plugins are selected for governed, repeatable delivery across modernization, Fabric, analytics engineering, and adjacent workflow automation.

Plugins in this marketplace may bundle commands, agents, and skills, but the unit of distribution is the plugin.

## Contributing

Contributions are welcome, but this repository is curated. If you want to contribute a plugin or improve an existing one:

1. Open an issue or pull request with the proposed change.
2. Keep the README and marketplace entry aligned with the plugin's actual purpose.
3. Follow the repository conventions in [CLAUDE.md](./CLAUDE.md).

## License

Elastic License 2.0. See [LICENSE](./LICENSE).
