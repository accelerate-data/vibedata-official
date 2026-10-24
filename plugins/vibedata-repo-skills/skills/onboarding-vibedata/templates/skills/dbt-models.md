---
name: dbt-models
description: Use when adding or changing dbt models and their derived keys.
---

# dbt models

Scope: {{confirmed_model_paths}}.
Follow the existing layer and naming conventions: {{confirmed_conventions_and_exceptions}}. Read the mapped module and its existing example before editing. Preserve source identity and established grain. Register actual models and required design artifacts in the same change; a design record needs a non-obvious decision, not a restatement of SQL.

Before deriving a timestamp key, confirm source timezone meaning, landed type and session timezone; use the same representation on both sides of a join. Apply a timezone conversion only when that contract requires it. Record ambiguity or inconsistent conversions as findings, with dependent changes held for a decision.

For gold mart SQL, properties, keys, grain, population or metric changes, invoke
the repository's `semantic-model` and then `validating-semantic-model` skills.
Update the canonical at `artifact_paths.logical_model` in the same change:
handles and aliases, fields/suppliers, content filters/levels, keyed hierarchies,
metric rollup and governing note/test links. Regenerate declared-level tests
when their inputs change. Run full-directory structure, coverage, suppliers,
notes and freshness gates plus content review; report unrun data checks.

When adding the first gold mart without this pair, seed it from the approved
installed onboarding bundle, create the real canonical, and register paths and
checks in both maps. Use the normal model task; do not rerun all onboarding.
Missing delivery is an explicit semantic-readiness gap. Preserve existing custom
skill/model formats until a migration is decided.
