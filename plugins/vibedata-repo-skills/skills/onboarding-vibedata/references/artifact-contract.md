# Artifact contract

## Instructions and preservation

`AGENTS.md` is canonical in all four ownership states. Update it in place if it is the only instruction file. Create it when neither exists. If only CLAUDE exists, or both exist, merge every unique instruction into AGENTS or an appropriately routed rule; CLAUDE ends as only `@AGENTS.md`.

Before writing, inventory instruction text, imports, links, scoped rule front matter, actual casing, symlink targets and same-file identities. Use filesystem identity as well as path spelling to detect aliases. Secure the complete original text in the in-memory ledger or a bounded local backup before the first instruction edit; keep it until the retained destinations are verified. For a disk backup, use a unique temporary directory and remove only that backup after verified consolidation. A hash detects a change but cannot recover content. Name the actual preservation method in the report and never describe hashes alone as a backup. The report ledger records each original clause or linked rule, its source location, retained destination and scope, or the explicit approved replacement. Exact duplicates may have one destination. Preserve the meaning and force of each instruction; a short index is not permission to drop detail.

Keep scoped instructions scoped. If text moves, repair relative links/imports against the destination and verify their original targets. Preserve customer-owned source rules when routing already works. Resolve cycles and same-file aliases before replacing either entrypoint. Triage conflicting instructions with the user before dependent writes. Replace CLAUDE with the placeholder only after every ledger row and destination has been checked. A normal fresh-session probe must verify the resulting entrypoint for each available runtime.

## Maps

Use [repo-map.json](../templates/repo-map.json), [schema](../templates/repo-map.schema.json), and [test-map.json](../templates/test-map.json) as shapes. Reconcile existing maps in place, retaining unknown keys and customer formats. A legacy shape that differs from the shared contract needs an explicit compatibility decision or a retained suitable checker, not silent normalization.

| Owner | Content |
| --- | --- |
| `modules` | Real module paths and short responsibilities. |
| `sources` | Actual source identity and implementation kind; existing artifact paths and confirmed `required_artifacts`. |
| `entrypoints` | Named executable/configuration paths that actually exist. |
| `commands` | Existing understood commands; environment-dependent commands remain unverified in the report. |
| `artifact_paths` | Semantic roles mapped to customer-selected repo-relative paths or future filename patterns. |
| `key_references` | Actual bootstrap, canonical instructions, rules directory, schema and test map. |
| `notes_for_agents` | Startup order and task-specific pointers to rules, examples/templates and checks. |
| Optional `layers` | Existing layer taxonomy only. |

Required artifact roles are `context`, `adr`, `design_record_model`, `design_record_pipeline`, `review`, `proposal`, and `onboarding_report`. Defaults appear in the map template. Select one location per role; do not also create a default or alternate glossary with the same purpose. Preserve existing locations, case, numbering and formats. Literal registered paths must exist. Future patterns use `{identifier}` placeholders and can name directories not yet created. Instantiate paths only for artifacts actually registered; do not manufacture design records to satisfy a pattern.

`key_references.agents` is the runtime bootstrap; `key_references.instructions` is canonical AGENTS; `rules`, `schema`, and `test_map` point at the actual artifacts. The startup sequence is: canonical instructions → repo map → applicable task rules/examples → relevant checks in the test map. Custom vocabulary/ADR paths also need the conditional [compatibility workaround](compatibility.md).

`test-map.json` has `taxonomy` and `modules`. Each module has existing `sources` paths and optional `unit`, `data`, `selectors`, and `commands`. Use `gaps` for missing coverage. A Python module needs no dbt selector. Selector resolution needs native dbt checks when available; path validation does not execute selectors or commands. Empty inventories are valid.

## Artifact selection

Use the [agents template](../templates/agents.md) as routing, then select only applicable rule templates: dbt/SQL/testing for transformations, dlt for dlt ingestion, Python for existing Python/notebooks, and context/ADR/design/Git rules for their respective tasks. Replace path tokens using the map and confirmed overrides before emitting a rule. A task should load its own rules, not the whole library.

Reuse vocabulary and ADR history. When knowledge is absent, use the [glossary](../templates/glossary.md) and [ADR index](../templates/adr-index.md); do not invent a term, numbered decision or rationale. A design record or repo-specific skill needs an actual non-obvious decision or confirmed local procedure. Generate [review](../templates/review.md) and [proposal](../templates/proposal.md) documents only for real findings or substantive decisions.

Install the standalone [context checker](../scripts/validate_context.py) at `.agents/checks/validate_context.py` only if no suitable existing check exists. Preserve a customer-owned checker; upgrading a previous copy is a reviewed change. Register `python3 .agents/checks/validate_context.py --root .` in both maps where applicable. It checks the owned path/reference contract, not arbitrary JSON Schema extensions or runtime behavior. Run the customer's additional schema validator where applicable.

## Reruns and maintenance

Compare current artifacts with live facts and human edits. Preserve unmapped content until it has a retained destination or approved replacement. Keep existing ordering and timestamps when facts are unchanged. Do not regenerate whole documents from a template or create default duplicates of custom artifacts.

Update the repo map in the change that adds, moves, renames or removes a source, module, entrypoint, command or artifact. Update the test map with test/selector changes. Update rules when a convention changes, vocabulary when confirmed meaning changes, ADRs when a qualifying decision occurs, and the report when a readiness blocker changes. Verify each affected link/check in that same change. When refreshing after a human edit, reconcile its preservation-ledger row in the same run. Do not defer that documentation to a later unchanged run. An unchanged rerun produces no file diff.
