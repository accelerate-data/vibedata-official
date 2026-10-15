# dbt testing

Scope: {{confirmed_dbt_paths}}.
Use the mapped tests and existing YAML key/style. Add checks for the actual model/source contract. Update test-map.json when tests or selectors change. Resolve selectors with the selected dbt runtime when available. A parse or empty build is a scaffold check, not evidence that data tests ran. Record missing profiles, source tables and execution targets as gaps.
