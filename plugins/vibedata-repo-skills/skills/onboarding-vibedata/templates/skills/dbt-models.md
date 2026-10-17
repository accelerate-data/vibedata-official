---
name: dbt-models
description: Use when adding or changing dbt models and their derived keys.
---

# dbt models

Scope: {{confirmed_model_paths}}.
Follow the existing layer and naming conventions: {{confirmed_conventions_and_exceptions}}. Read the mapped module and its existing example before editing. Preserve source identity and established grain. Register actual models and required design artifacts in the same change; a design record needs a non-obvious decision, not a restatement of SQL.

Before deriving a timestamp key, confirm source timezone meaning, landed type and session timezone; use the same representation on both sides of a join. Apply a timezone conversion only when that contract requires it. Record ambiguity or inconsistent conversions as findings, with dependent changes held for a decision.
