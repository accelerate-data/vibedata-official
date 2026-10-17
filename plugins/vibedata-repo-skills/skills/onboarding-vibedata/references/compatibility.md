# Compatibility decisions

A compatibility change is a concrete edit required for the selected runtime or platform to use the repository. It is separate from context generation.

For Studio on DuckDB, use the conditional [readiness checks](studio-duckdb.md). Every resulting edit follows the decision procedure below.

1. Capture current input revision or file hashes, exact affected files/diff, enabling behavior, proposed check and expected side effects.
2. Use an existing explicit approval for that diff, or obtain a decision. Record `approved`, `declined`, or `pending`; elapsed time is never approval. A materially changed diff requires a new decision.
3. Apply only approved changes, verify that the input is still the reviewed input, then run the understood check against the approved target. If the input changed, reconcile before applying.
4. For declined/pending changes, preserve application bytes and record evidence, proposed action and which outcome is blocked: context readiness, execution verification, both or neither. Complete independent context work.

Review triage (`intent`, `proposal → P-NNNN`, `declined: <reason>`, `deferred`) is independent of edit approval. Preserve review IDs/text while recording a proposed diff's `pending`/`approved`/`declined` decision separately. Do not turn a deferred finding into approval or ask again about established customer decisions.

For dbt warning cleanup, retain before/after test unique IDs and counts, arguments/configuration, and normalized compiled model/test SQL under identical versions and inputs. Normalization may remove generated comments and formatting, never predicates, literals or test arguments. A removed test or changed predicate prevents a behavior-free verdict even when parsing passes. Restore the contract or obtain a decision on the actual behavioral diff.

## Custom vocabulary and ADR locations

Emit the [workaround rule](../templates/skills/workarounds.md) only when a consuming skill names default vocabulary/ADR paths and the customer uses another location. Route vocabulary and ADR tasks through it before invoking that skill.

Resolve `artifact_paths.context` and `artifact_paths.adr` from `repo-map.json` for reads, writes and filename checks. These values override consuming-skill defaults such as `CONTEXT.md` and `docs/adr/`. Preserve existing ADR identifiers and formatting; an ADR pattern describes future filenames, not a renumbering operation. For a tracked glossary, the emitted check is `git ls-files --error-unmatch "<resolved-context-path>"`. For newly created untracked context, verify file existence and report it as untracked; onboarding does not authorize a commit.

Removal condition: the consuming skill and its executable checks resolve the map directly, with a passing fresh consumer trial. Record the consumer/version and observed hardcoded operation. If an executable hardcodes a default, prose cannot change it: record the failing check and follow-up, and leave that integration unverified. This change never patches the upstream consumer.

## Microsoft Fabric

Keep the repository's Fabric Lakehouse, notebook and dbt adapter/runtime conventions. Fabric Git stores notebook content as source files inside `*.Notebook` directories; see [Microsoft's source-control documentation](https://learn.microsoft.com/fabric/data-engineering/notebook-source-control-deployment) and [supported magics](https://learn.microsoft.com/fabric/data-engineering/author-execute-notebook#magic-commands-in-a-notebook). Inventory reads these files without executing cells or installing their packages.

When dbt runs only in a Fabric notebook, retain its profile-generation procedure and actual target (for example `prod`); do not create a local profile, substitute DuckDB or run the notebook to make local selectors pass. Use the [conditional check contract](artifact-contract.md#repository-checks). SQLFluff with a dbt templater also remains unverified without its required profile and runtime. Record exact unavailable checks, environment requirements and an authorized non-production target when one exists. Context/schema validation can pass while selectors, lint or sandbox execution remain unverified.

Fabric does not select Studio. Apply Studio readiness only when Studio is explicitly selected; this guidance establishes no Studio-on-Fabric runtime support. Production pipeline execution and provisioning retain their separate authorization gates.

## Runtime discovery

Keep customer writes under the explicit repository root. Preserve instruction filename casing; report unsupported discovery before renaming. Treat denied context paths, such as Codex workspace-write protection of `.agents/`, as partial context. Record the denied path and required permission without relaxing the sandbox. A proposed alternate location follows the same compatibility-decision procedure above.

Use the [verification contract](artifact-contract.md#verification) for the selected runtime and requested consumer targets.

Preserve data semantics outside the selected platform contract: deliberate attached catalogs, confirmed currency precision (including three-decimal scales), exact identifiers/membership/NULLs and local-business timezone meaning. Sample controls must exist in the selected loader. Source or tool version changes invalidate dependent profile/check evidence. Unknown versions leave an explicit gap.
