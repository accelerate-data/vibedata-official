# dbt testing

Scope: {{confirmed_dbt_paths}}.
Use the mapped tests and existing YAML key/style. Add checks for the actual model/source contract. Update test-map.json when tests or selectors change. Resolve selectors with the selected dbt runtime when available. A parse or empty build is a scaffold check, not evidence that data tests ran. Record missing profiles, source tables and execution targets as gaps.

Comparisons of rebuilt measures name their precision in the acceptance criteria: the confirmed currency/business scale for money, an explicit absolute or relative tolerance for floating measures. DuckDB floating aggregates can differ in their last bits; compare matched values at the agreed precision, not hashes of raw doubles. Check identifiers, row membership and NULL semantics exactly.

A left join on a derived key needs a coverage assertion: every required left row matches, or unmatched rows are the documented exceptions. State the full grain from grouping keys and test uniqueness at that grain. Report disagreements between documented and implemented grain before changing either.
