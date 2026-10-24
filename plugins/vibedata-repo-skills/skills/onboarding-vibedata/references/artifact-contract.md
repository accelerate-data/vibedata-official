# Artifact contract

## Instructions and preservation

`AGENTS.md` is canonical. Update it in place if it is the only instruction file; create it when neither exists. If CLAUDE contains instructions, consolidate every unique instruction into AGENTS or an appropriately routed rule; CLAUDE ends as only `@AGENTS.md`. An existing valid wrapper needs no reconsolidation.

Before editing instructions, inventory text, imports, links, scoped front matter, casing and filesystem identities. Resolve symlink/hardlink aliases and cycles before replacing an entrypoint. Secure the complete original text in memory or a bounded, unique temporary backup inside the authorized repository until preservation is verified. Keep temporary hash/evidence files inside that boundary with unique task-owned names. Record the method and original hashes; hashes alone cannot restore text. Remove only task-created temporary files after verification. A denied write stays blocked; do not retry through another tool or broader permissions.

When existing instructions are merged, moved or replaced, append this ledger to the report for every original clause or linked rule in the affected instruction files. Exact duplicates may share a destination. For unchanged instructions or additions that retain all original text in place, a preservation check and short report note suffice.

| Original clause or linked rule | Source | Retained destination and scope | Link/import target verified | Approved replacement, if any |
| --- | --- | --- | --- | --- |
| {{clause_or_rule}} | {{file_location}} | {{file_section_and_scope}} | {{target}} | {{decision_or_none}} |

Keep scope, meaning and force. Repair moved relative links/imports and verify their original targets. Quote original imports/links as code in the ledger; active destination links resolve from the report. Preserve customer-owned rules when routing already works. Pending conflicts retain affected files until the user decides. Replace CLAUDE only after every ledger row and destination has been checked.

## Maps

Use [repo-map.json](../templates/repo-map.json), [schema](../templates/repo-map.schema.json), and [test-map.json](../templates/test-map.json) for new maps. For existing maps, retain the customer schema and suitable checker as their contract, including unknown keys and formats. Resolve equivalent instruction and report locations through that contract; record a report location in the onboarding output if the schema has no such role. Missing portable-only keys such as `instructions` or `onboarding_report` do not alone block context readiness. Adopting the shared schema requires an explicit compatibility decision.

| Owner | Content |
| --- | --- |
| `modules` | Real module paths and short responsibilities. |
| `sources` | Actual source identity and implementation kind; existing artifact paths and confirmed `required_artifacts`. |
| `orchestrators` | Actual runners, source membership and local `path` or external `location`; see [source ownership](#source-ownership). |
| `entrypoints` | Named executable/configuration paths that actually exist. |
| `commands` | Existing understood commands; environment-dependent commands remain unverified in the report. |
| `artifact_paths` | Semantic roles mapped to customer-selected repo-relative paths or future filename patterns. |
| `key_references` | Actual bootstrap, canonical instructions, convention skills, optional legacy rules, schema and test map. |
| `notes_for_agents` | Startup/task pointers to conventions, examples and checks; observed maintenance and evaluation paths excluded from normal build-task routing. |
| Optional `layers` | Existing layer taxonomy only. |

For maps using the shared schema, required artifact roles are `context`, `adr`, `design_record_model`, `design_record_pipeline`, `review`, `proposal`, and `onboarding_report`. For `--consumer studio`, also require `requirement`, `plan`, `verification`, `case_record` and `design_record_area`. Default standalone checking retains the earlier role contract; native customer maps use their own checker. New roles are future patterns, not instructions to fabricate documents. The consumer owns the intent identifier; incompatible native paths require a supported mapping or a blocker. Defaults appear in the map template. Select one location per role; do not also create a default or alternate glossary with the same purpose. Preserve existing locations, case, numbering and formats. Literal registered paths must exist. Future patterns use `{identifier}` placeholders and can name directories not yet created. Instantiate paths only for artifacts actually registered; do not manufacture design records to satisfy a pattern.

In the shared schema, `key_references.agents` is the runtime bootstrap; `key_references.instructions` is canonical AGENTS; `conventions` points at the canonical skill tree; legacy `rules` remains supported. Validate both roots when both exist. `schema` and `test_map` point at the actual customer artifacts. The startup sequence is: canonical instructions → repo map → invoke relevant convention skills and read retained legacy rules/examples → relevant checks in the test map. Custom vocabulary/ADR paths also need the conditional [compatibility workaround](compatibility.md).

`test-map.json` has `taxonomy` and `modules`. Each module has existing `sources` paths and optional `unit`, `data`, `structural`, `selectors`, and `commands`. Use `gaps` for missing coverage. A Python module needs no dbt selector. Selector resolution needs native dbt checks when available; path validation does not execute selectors or commands. Empty inventories are valid.

For an existing canonical semantic model, a file glob such as
`semantics/*.ossie.yaml` selects files in one literal repository directory. It
must match at least one file; every match must remain inside the repository,
including symlink targets. Recursive/directory globs are unsupported by the
portable checker. Use brace patterns for future artifacts. Keep the native
checker for customer pattern syntax outside this contract.

## Source ownership

For shared maps, `orchestrators` has one entry per runner: `kind` (`python`,
`airflow`, `fabric`, or the actual kind), `runs` (source names), and exactly one
of `path` (existing local runner file) or `location` (confirmed external owner
and scheduler/job identity). `runs` is membership, not execution order; order
belongs to the runner. Every source is named by a runner and every member names
a source. Empty inventories are valid. Ask about external scheduling only when
the repository and established decisions cannot identify it. A manual command
can be the confirmed external location; unknown ownership is a finding.

`dataset` is the destination schema identity, not the source name. Once two
sources share a dataset, each declares nonempty, distinct `produces` table names;
two producers cannot silently claim the same table. A single source can use its
module's resources as the list. If its producer is outside the repository and
cannot be inspected, obtain its table list and record `produces` too. Preserve
intentional joint ownership in a native contract with its native checks and an
explicit decision, rather than relabel a collision as validated.

Retain actual layer taxonomy. `built_by` names the builder, never the scheduler;
use `custom` with explanatory `notes` when no standard build procedure applies.
Map every applicable layer to its real test module or a named coverage gap;
custom layers do not get invented dbt selectors. A separately maintained runner
list needs its native code/map parity test. The shared scaffold's runner reads
the map directly. The portable graph check does not inspect external scheduling
or prove runner code executes the declared members; record that limit.

Existing native maps retain their schema and checker. Do not add shared keys to
a closed customer schema. Missing runner ownership or table coverage remains a
reported gap, even when native structural checking passes.

## Artifact selection

For gold marts or an existing canonical model, follow the complete
[semantic-model contract](semantic-model.md), including both seeded skills,
their dependencies, mapped artifacts and structure/content/data evidence.

Use the [agents template](../templates/agents.md) as routing, then select only applicable [convention templates](../templates/skills/): dbt/SQL/testing for transformations, dlt for dlt ingestion, Python for existing Python/notebooks, and context/ADR/design/Git rules for their respective tasks. Replace path tokens using the map and confirmed overrides before emitting a convention skill. A task should load its own rules, not the whole library.

Emit selected conventions at `.agents/skills/<name>/SKILL.md` from the ordinary Markdown templates under `templates/skills/`. Each rendered entrypoint needs nonempty YAML `name` and `description`, a name matching its destination, and all generation tokens resolved. Keep its description focused on task triggers so ordinary work can discover it. Onboarding remains explicit-only.

For selected Codex, use native `.agents/skills` discovery. For selected Claude, reuse an existing supported route or create contained directory symlinks `.claude/skills/<name> -> ../../.agents/skills/<name>`. Verify both the link and its resolved target stay inside the repository. Keep one maintained copy. Before each alias or migration, compare existing content, declared skill names, scope, callers and ownership. Preserve a different customer skill and mark that collision pending; continue unrelated work. Never overwrite an existing skill merely because its basename matches a template.

Retain legacy `.agents/rules` files and active references until every clause, scope and caller has a verified retained destination. Repair relative links on migration. Redundant content can be removed only after that preservation check. The checker begins skill validation at actual `SKILL.md` entrypoints and follows their reached Markdown links; unused template Markdown is not active policy. Legacy rule directories retain their existing validation. Canonical and Claude aliases share resolved identities for deduplication.

Metadata checks and discovery are separate: validate rendered YAML with an available parser/native validator and observe selected-runtime loading. The standard-library structural checker does not parse YAML. Missing metadata validation or runtime capability is a named gap, even if the runtime accepts an entrypoint with empty metadata.

Reuse vocabulary and ADR history. When knowledge is absent, use the [glossary](../templates/glossary.md) and [ADR index](../templates/adr-index.md); do not invent a term, numbered decision or rationale. A design record needs an actual non-obvious decision; a procedure skill needs a confirmed local procedure. Design records hold qualitative decisions and a link to measured evidence at `artifact_paths.verification`, or the equivalent native mapped/report destination. Measurements and check outcomes belong there, including numeric findings; retain design history and paths. Shared-area decisions use `design_record_area` when available. Generate [review](../templates/review.md) and [proposal](../templates/proposal.md) documents only for real findings or substantive decisions.

Retain a suitable customer-owned checker and its mapped command. Preserve native JSON Schema, dlt config-section and dbt selector checks; record coverage gaps without replacing them with the weaker portable check. If no suitable check exists and the shared schema is adopted, install the standalone [context checker](../scripts/validate_context.py) at `.agents/checks/validate_context.py` and register `python3 .agents/checks/validate_context.py --root .` in both maps. Upgrading a previous copy is a reviewed change. It checks owned paths/references, not arbitrary schema extensions or runtime behavior. Run additional customer validators where applicable.

## Repository checks

Reuse the native JSON Schema/config/selector bundle and its actual mapped commands. For an adopted shared scaffold with no equivalent checks, emit [ADR links](../templates/checks/test_adr_links.py) and [native maps](../templates/checks/test_maps.py) at `tests/test_adr_links.py` and `tests/test_maps.py`. Register those actual paths/commands in both maps. Keep customer schemas authoritative; generated checks read the mapped schema rather than replacing it. Select the mapped dbt project/profile and target for that repository; unsupported native selector syntax stays with its native check.

New Markdown ADR/design output uses Markdown links and `## Affected designs`. `python tests/test_adr_links.py --root .` and its pytest test check active links in both directions at mapped ADR/model/pipeline/area paths. Linked custom identifiers are valid; source-style `ADR NNNN` citations need one unambiguous mapped filename. Rejected history does not require active symmetry, but broken links still fail. Use `## Superseded by` with a Markdown successor link; active designs cite the replacement.

Single-file ADR collections and notebook Markdown cells are supported native formats. Map `artifact_paths.adr` to their literal file, preserve identifiers such as `ADR NNNN` and append decisions in that format. Do not split or rewrite history. The shared ADR-link checker supports one Markdown file per ADR; omit it for a collection/container unless a suitable native checker exists. Record `ADR-link gap: container decisions and backlinks are not checked` in the test map and report when no native check covers them. File existence checks do not establish cell-level link coverage; independent schema/map checks can still be emitted.

The map checks validate the selected schema, every TOML-backed dlt source's `config_section` and each registered dbt selector's nonempty JSON result. YAML and notebook-embedded registrations are supported native forms; do not invent TOML or `config_section` values. Non-TOML registrations produce a `source-registration gap` skip after all TOML entries have been checked. A declared `config_section` still requires TOML; missing mapped files and missing TOML sections fail. Retain native registration checks and record uncovered YAML/notebook parity in the test map and report. Empty source inventories are valid.

Selector checks use the mapped dbt project and local profile without a target override: the profile's target or dbt's environment selection applies. Do not hardcode `dev`. When selectors exist but no `dbt_profiles` role is mapped, the selector check reports a `dbt-selector gap` skip without launching dbt; a mapped profile that is missing still fails. Record the native runtime/profile-generation procedure and selector gap in the test map and report. Do not generate a profile or run a production notebook just to satisfy a local check. Install declared dbt packages in setup/CI before runnable selector checks; the tests never silently download them. A passing structural checker or skipped check does not establish native execution coverage.

Reuse suitable CI. Only where absent and within setup authorization, adapt [repo-checks.yml](../templates/repo/repo-checks.yml) to `.github/workflows/repo-checks.yml`; its PR job installs declared dependencies and executes the registered checks with one interpreter. Preserve custom hooks and the native bundle. Do not bypass hooks with `core.hooksPath`. Local workflow inspection is not evidence of a remote PR trigger.

## Reruns and maintenance

Compare current artifacts with live facts and human edits. Preserve unmapped content until it has a retained destination or approved replacement. Keep existing ordering and timestamps when facts are unchanged. Do not regenerate whole documents from a template or create default duplicates of custom artifacts.

Update the repo map in the change that adds, moves, renames or removes a source, module, entrypoint, command or artifact. Update the test map with test/selector changes. Update rules when a convention changes, vocabulary when confirmed meaning changes, ADRs when a qualifying decision occurs, and the report when a readiness blocker changes. Verify affected links/checks in that change. If an edited instruction has an existing ledger row, reconcile that row in the same refresh. Retain report history; an unchanged rerun produces no file diff.

## Verification

Use the customer's requested runtime, otherwise the active runtime. Run the mapped context checker from the repository root. Verify normal instruction loading in a fresh session of that runtime without naming or pasting the canonical file in the probe; reuse recorded loading evidence when its instruction inputs are unchanged. If the probe cannot run, mark loading unverified. Rehearse later tasks through maps and applicable conventions. After a real supported compaction/resume, observe applicable workaround reload. A prompt pretending compaction occurred is only a wording probe, not runtime proof.

At task startup and after compaction, invoke the relevant convention skills and reload applicable emitted workarounds before continuing. For uncertain library behavior, consult operator-approved documentation or repository examples; inspecting installed-package source is outside this workflow. Use the mapped lint configuration and exclusions.

Run understood project checks only against an established, authorized target. Report context readiness and execution verification separately, naming the verified scope and unavailable checks. Structural validation does not prove runtime loading, consumer behavior or warehouse execution.

Reuse a recorded check only when its covered files, configuration, tool versions and relevant data/environment are unchanged. Cite the command, input revision and result; changed or unknown inputs require a new authorized check or an unverified status.

The full Claude/Codex/VibeData matrix is plugin release verification, not a customer onboarding prerequisite. Run a real supported VibeData consumer trial only when it is a requested target; if unavailable, mark that target unverified. Unselected runtimes need no report rows and do not block context readiness.
