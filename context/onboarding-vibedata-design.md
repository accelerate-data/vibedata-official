# onboarding-vibedata design

**Status:** The shared repository-preparation skill is implemented. The 2026-10-16 source-alignment update is under local acceptance; Studio lifecycle is blocked. Current results and remaining gates are in the [execution ledger](onboarding-vibedata-source-alignment-run.md).
**Scope:** One shared skill distributed from `vibedata-official`, usable in Codex and Claude, preparing repositories for later VibeData build sessions.
**Companion:** [Implementation plan](onboarding-vibedata-plan.md).
**Repository baseline:** Original design `aee3c19`; alignment execution `d07d1a8`, checked against fetched `origin/main@b878bf8`. Historical results remain in the validation record.

## Contents

- [Purpose and scope](#purpose-and-scope)
- [System requirements](#system-requirements)
- [Artifact contract](#artifact-contract)
- [Instruction ownership and conflict triage](#instruction-ownership-and-conflict-triage)
- [Workflow and approval boundaries](#workflow-and-approval-boundaries)
- [Rules and temporary workarounds](#rules-and-temporary-workarounds)
- [Packaging and authoring](#packaging-and-authoring)
- [Verification and acceptance cases](#verification-and-acceptance-cases)
- [Implementation choices and remaining evidence](#implementation-choices-and-remaining-evidence)
- [Sources](#sources)

## Purpose and scope

Onboarding spends discovery effort once so later VibeData sessions can find the relevant files, conventions, examples, decisions, and commands without repeatedly exploring the repository.

Brownfield means a human-engineered data repository with existing code, configuration, documents, or instructions, including Python scripts and notebooks and partly onboarded repositories.
Greenfield means a repository with no substantive data-engineering implementation; a README, license, instruction file, or dependency manifest alone does not make it brownfield.
Existing assets are inventoried in either mode.
The target stack is always dbt/dlt; Python discovery does not authorize conversion of existing Python logic.
Greenfield choices concern the data platform and conventions, not an alternative application stack.

This work reads `sample-nyctaxi-comp` as a reference only.
Implementation is confined to `vibedata-official` and disposable evaluation repositories.
Creating Studio Domains, provisioning infrastructure, loading production data, deploying pipelines, converting Python logic, and changing the upstream VibeData consumer repository are outside V1.
Customer-repository onboarding does not automatically commit, push, create a PR, or publish.

## System requirements

| ID | Observable behavior |
| --- | --- |
| R01 | `onboarding-vibedata` runs in Codex and Claude from the same skill source and produces the same artifact contract. |
| R02 | Brownfield discovery records existing dbt/dlt and Python/notebook structure, conventions, exceptions, and evidence without changing application behavior. |
| R03 | Greenfield creates a minimal dbt/dlt scaffold consistent with the chosen platform and conventions, with templates for later source/model work. |
| R04 | `repo-map.json` resolves semantic artifact roles to customer-selected paths; later work uses those paths, including validation commands. |
| R05 | Existing instruction content is preserved according to the ownership table below; `AGENTS.md` is canonical in every case, and any existing `CLAUDE.md` becomes the reference-only placeholder. |
| R06 | Conflicting existing instructions, referenced rules, and onboarding requirements are presented to the user before dependent changes proceed. |
| R07 | The user sees each proposed compatibility change and its effect; approved changes are applied and verified, while declined or pending changes remain follow-ups. |
| R08 | Discoverable convention skills contain applicable conventions and exceptions; legacy rules remain usable; temporary workarounds specify scope, action, reason, and removal condition. |
| R09 | Existing vocabulary and decisions are reused; uncertain rationale is identified, and absent knowledge produces minimal placeholders rather than invented business facts. |
| R10 | Reruns preserve human edits, reconcile missing/stale information, avoid duplicates, and produce no substantive diff when inputs have not changed. |
| R11 | Discovery does not execute unfamiliar notebooks, ingestion, or arbitrary repository commands; execution checks use an established target and understood side effects. |
| R12 | Structural checks detect broken paths, reference cycles, incomplete source registration, and stale map relationships; missing test coverage is reported honestly. |
| R13 | Results distinguish context, runtime loading, sandbox execution, persistent Domain state and conditional Studio lifecycle; each gap names its next action. |
| R14 | Fresh sessions locate task files, applicable rules, examples/templates, and checks through the generated context; reduced discovery is measured alongside correctness. |
| R15 | Both plugin manifests and marketplace catalogs expose the skill, and the generated catalog is updated through the existing generator. |
| R16 | Baseline scenarios precede authoring; `writing-for-agents` guides creation and `writing-skills` supplies the subsequent behavioral verification pass. |
| R17 | Only explicit user invocation starts the skill; Claude and Codex cannot select it implicitly. |
| R18 | Routine reports contain changes, checks and blockers with separate context/execution status. Instruction consolidation adds a complete preservation ledger; other details appear only for actual findings or decisions. Existing report history survives refreshes. |
| R19 | Customer onboarding verifies the requested runtime, or the active runtime by default. The full Claude/Codex/VibeData matrix is plugin release verification; unselected runtimes do not block customer readiness. |

## Artifact contract

The map is an intentional cache of expensive repository discovery, maintained by the same changes that make it stale.
It contains facts and routing information; convention skills own conventions, the glossary owns vocabulary, and ADRs own qualifying decisions.

| Artifact | Brownfield | Greenfield |
| --- | --- | --- |
| `repo-map.json` | Actual modules, sources, entrypoints, commands, examples, instruction ownership, and artifact locations. | The scaffold that exists, plus explicit patterns for future artifacts. |
| `repo-map.schema.json` | Validate the agreed map shape while preserving existing extensions. | The same schema, permitting an empty source/model inventory. |
| `test-map.json` | Actual checks, their scope and selectors, and explicit coverage gaps. | Scaffold checks and conventions for later tests; no fictitious business coverage. |
| Canonical instruction file | Existing instructions reconciled into a short startup index and appropriately scoped rules. | `AGENTS.md` with startup routing and maintenance obligations. |
| `.agents/skills/<name>/SKILL.md` | Confirmed task conventions, exceptions and applicable workarounds with valid metadata; retain active legacy rules and customer skills. | Selected defaults demonstrated by the scaffold. |
| `.claude/skills/<name>` | Contained aliases to canonical skills after ownership checks; preserve collisions pending resolution. | One maintained copy through contained aliases. |
| Vocabulary, via `artifact_paths.context` | Reuse supported definitions and existing location/format. | Known terms only; otherwise a heading and a statement that no domain terms are established. |
| ADRs, via `artifact_paths.adr` | Preserve location, numbering, decisions, and history. | Record actual qualifying setup decisions; otherwise create an index stating that no ADRs are recorded. No empty numbered ADR. |
| Design records | Qualitative decisions not recoverable from code, with rationale and links to mapped verification; no mandatory record for every trivial artifact. | Templates, and records only for substantive components actually introduced. |
| Repo-specific skills | Only confirmed procedures not already covered by available general skills. | Only procedures that setup actually establishes; no speculative skill library. |
| Onboarding report | Changes, checks and blockers; a preservation ledger for instruction consolidation, and decision details for actual conflicts or compatibility changes. | The same compact report, with actual setup choices and outstanding configuration. |
| Review and proposal documents | Evidence-backed findings at the mapped review location; a proposal only when a substantial finding needs a separate decision. | The same formats are available; no empty finding or proposal is invented to fill a directory. |
| Context checker | Retain a suitable native checker; the portable checker applies when the shared schema is adopted. | Use the same selection rule and register the actual checker command. |
| Project scaffold | Preserve existing application layout and package manager. | Minimal configuration, folders, safe commands, test configuration, and starter templates for dbt/dlt. |

### Map fields

Retain the reference repo's useful top-level concepts: `modules`, `sources`, `entrypoints`, `commands`, `artifact_paths`, and `notes_for_agents`.
`layers` is optional when the existing estate has no such taxonomy; do not impose NYC Taxi schemas or a medallion model on unrelated Python code.
Existing unknown keys survive reconciliation.
`sources` contains only actual sources and records their existing implementation kind and artifact links; it does not require a Python source to have a dlt pipeline.
Each registered source lists the artifacts actually required by its confirmed convention.

Existing maps retain a suitable native schema/checker contract. Portable-only missing fields do not alone block context readiness; equivalent locations are resolved through the customer contract, with the report path stated in onboarding output when no map role exists. Adoption of the shared schema requires an explicit compatibility decision.

For the shared schema, the following role keys are stable, while their values are customer-selected:

| Key under `artifact_paths` | Default for a new repository | Meaning |
| --- | --- | --- |
| `context` | `CONTEXT.md` | Business vocabulary file. |
| `adr` | `docs/adr/{nnnn}-{slug}.md` | ADR path pattern and numbering convention. |
| `design_record_model` | `docs/design/models/{layer}/{model}.md` | New model design records when warranted. |
| `design_record_pipeline` | `docs/design/pipelines/{pipeline}.md` | Pipeline decisions when warranted. |
| `review` | `docs/review/{date}-{type}-{slug}.md` | Findings requiring triage. |
| `proposal` | `docs/proposal/{nnnn}-{slug}.md` | Optional proposals for substantial follow-up work. |
| `onboarding_report` | `docs/onboarding.md` | Durable inventory, decisions, and verification for onboarding. |
| `requirement`, `plan`, `verification`, `case_record` | `docs/{requirement,plans,verify,cases}/{intent}.md` respectively | Future artifacts required by the shared Studio contract; standalone/native maps remain compatible. |
| `design_record_area` | `docs/design/{area}/{subject}.md` | Qualitative cross-component decisions, linked to mapped evidence. |

In the shared schema, `key_references.agents` names the bootstrap file, `key_references.instructions` the canonical instruction file, and `key_references.conventions`, `key_references.schema`, and `key_references.test_map` the canonical skill tree, map schema, and test map. Legacy `rules` remains supported and both roots are checked when present.
`notes_for_agents` states the startup sequence and maps task kinds to rules and suitable existing examples or templates.
Paths are repo-relative and preserve case; placeholder patterns are distinguished from existing instances.
A repository with different ADR identifiers retains them and declares its actual pattern; `{nnnn}` is a default, not a renumbering instruction.
An existing artifact continues at its recorded location instead of moving merely to match a new default.

Checks validate existing literal paths and instantiated paths where an actual source/model is registered.
Declared future artifact patterns are checked for syntax and containment; their directories need not exist until the first artifact is written.
Empty inventories are valid; a missing check is a reported gap, never a fabricated passing test.
Neither the map nor the report includes credentials, notebook outputs, data rows, or secret-file contents.

`test-map.json` retains the reference repo's `taxonomy` and `modules` structure.
Each module has `sources` paths and optional `unit`, `data`, `structural`, `selectors`, and `commands` entries; Python modules need no dbt selector.
An optional `gaps` list records missing coverage explicitly, and existing extra keys are preserved.
Only actual test files and runnable check commands are registered; a command that needs unavailable infrastructure is labeled unverified in the onboarding report.
Selector resolution is checked with the appropriate project/runtime command when available, not by pretending a path-only validator executes dbt.

### Greenfield defaults

The author-selected defaults are `ingestion/`, `transformation/`, `orchestration/`, and `tests/`, with project dependencies in `requirements.txt` and development dependencies in `requirements-dev.txt` when no manager already exists.
Preserve a manager the human has already selected.
Choose the dbt adapter and dlt destination from the declared VibeData data platform, using current approved documentation before generating dependency versions or initialization code.
No default warehouse is inferred from the NYC Taxi example.
If the platform is unknown, ask before writing dependent configuration.

With no real source definition, provide source/pipeline/model templates and a command index for the checks that actually work; do not register a fake source or introduce a fake business model.
Offline structural checks can pass at this point, but warehouse execution remains unverified until it is possible.
Representative fixture runs use small synthetic data solely to exercise the templates.
Human-facing setup notes may explain the generated scaffold; existing human documents are preserved unless an approved change explicitly edits them.

## Instruction ownership and conflict triage

| Files found | Canonical source after onboarding |
| --- | --- |
| Only `AGENTS.md` | Update `AGENTS.md` in place. |
| Only `CLAUDE.md` | Consolidate all unique instructions into `AGENTS.md`; replace `CLAUDE.md` with only `@AGENTS.md`. |
| Both | Consolidate all unique instructions into `AGENTS.md`; replace `CLAUDE.md` with only `@AGENTS.md`. |
| Neither | Create `AGENTS.md`. |

Preserve actual filename casing in references.
Verify that the selected runtime discovers the resulting entrypoint; surface an unsupported casing/discovery case rather than silently renaming customer files. The release suite verifies both runtimes.
Existing import chains and scoped rules are part of the inventory.
Resolve symlink aliases and cycles before writing so a file cannot be overwritten through its own alias.

When existing instructions are merged, moved or replaced, the preservation ledger assigns each original instruction or linked rule in the affected files a source location and retained destination, or an explicit user-approved replacement. Unchanged instructions and in-place additions need a preservation check and a short report note; an already valid CLAUDE wrapper needs no reconsolidation. Existing report history and applicable ledger rows survive refreshes.
Exact duplicates may be stored once.
Move a convention into a rule only when startup routing preserves when it is read; moving a scoped instruction must retain its scope.
Repair relative references when their owning text moves.
Replace the old instruction file with the placeholder only after the consolidated content and ledger have been checked.

Existing content is compared with other existing instructions and with the onboarding contract.
A conflict row contains the source locations, competing requirements, practical effect, recommended resolution, and user decision.
Custom names and permissible convention overrides are not conflicts by themselves.
Pending decisions block affected writes, not independent discovery.
Elapsed time is not approval, and the skill never silently chooses its own default over a customer rule.

## Workflow and approval boundaries

1. **Inspect.** Establish scope and mode; collect mechanical facts and read relevant conventions without running application code.
2. **Reconcile.** Resolve conventions and artifact destinations, using a preservation ledger for instruction consolidation and decision records for actual conflicts; ask only for unresolved facts or decisions that change the result.
3. **Propose changes.** Separate artifact work from compatibility changes; show exact affected files/diffs and the behavior each compatibility change enables.
4. **Apply.** Write independent artifact work, resolve approved conflicts, and apply only approved compatibility changes. Preserve pending/declined items as follow-ups.
5. **Verify and report.** Validate structure and preservation, verify the selected runtime, run understood checks against the approved target, and rehearse a later task. Report changes, checks and blockers with separate context and execution status. Reuse recorded loading evidence only when its instruction inputs are unchanged.

Compatibility approval attaches to the presented change and input revision; a materially different diff needs a new decision.
Each follow-up states evidence, proposed action, disposition, and whether it prevents context readiness, execution verification, or neither.
Existing bugs and style problems are findings, not incidental repairs.
For impactful writes to data, apply the operator's dry-run/confirmation rules separately; onboarding approval does not authorize production mutation.

Reruns compare live facts and human edits with existing artifacts; they do not overwrite from a previous generated snapshot.
Preserve unmapped content until it has a destination or an explicit decision.
An unchanged rerun must not rewrite timestamps or reorder content just to demonstrate activity.

## Rules and temporary workarounds

Task convention skills cover dbt models, SQL, testing, dlt, existing Python/notebook practices, documentation, and Git conventions where applicable. Canonical paths are `.agents/skills/<name>/SKILL.md`; selected Claude uses contained directory aliases after collision checks. Legacy rule scopes remain authoritative until losslessly migrated.
Permanent rules and temporary workarounds remain distinct.
Select runtime/platform workarounds from observed requirements rather than copying all NYC Taxi workarounds into every repository.
An ingestion task reads ingestion rules and applicable workarounds, not the full documentation rule library.

For V1, the custom-path workaround is deliberate:

> Before reading, creating, updating, or validating vocabulary or ADRs, resolve `artifact_paths.context` and `artifact_paths.adr` from `repo-map.json`. These locations override consuming-skill defaults naming `CONTEXT.md` or `docs/adr/`, including emitted filename checks. Remove this workaround when consuming skills resolve the map directly.

The canonical instruction file routes vocabulary and ADR tasks to this workaround before the consuming skill is used.
The root cause is observed in the upstream `domain-modeling` skill, which currently insists on `CONTEXT.md` and checks that literal name.
No upstream edit is required merely because that instruction exists.
If a deterministic executable also hardcodes the path, prose cannot alter it: record the specific failed check and follow-up instead of claiming compatibility.
Successful standalone Codex/Claude tests are not proof that a VibeData build session follows the workaround.

## Packaging and authoring

Use one plugin directory, `plugins/vibedata-repo-skills/`, with Claude and Codex manifests and one shared `skills/onboarding-vibedata/` directory.
The plugin directory name is an author-selected packaging choice; the user-selected skill name is exactly `onboarding-vibedata`.
Register the plugin in both marketplaces; individual skills are not marketplace entries.
The current catalog generator already discovers plugin-contained skills, so no duplicate top-level skill copy is needed.
Use `Elastic-2.0`, consistent with this repository's owned skill content and license allowlist.

`SKILL.md` holds the shared workflow, gates, and completion criteria.
Conditional references hold brownfield discovery, greenfield setup, artifact/preservation rules, and compatibility details.
Templates encode the common artifact shape and selected stack conventions; two small Python helpers collect mechanical inventory and validate context without running project code.
The validator can be copied into a customer repo as `.agents/checks/validate_context.py` when no suitable check exists, so maintenance does not depend on a local plugin-cache path.
Preserve a customer-owned checker; replacement of a previously installed helper is a reviewed change, not an automatic upgrade.

Use `writing-for-agents` to author the skill and generated instructions: explicit completion criteria, conditional context pointers, and a single owner for each instruction.
Use `writing-skills` to define baseline scenarios before authoring and to verify behavior afterward.
Invocation is user-only: `/vibedata-repo-skills:onboarding-vibedata` in Claude Code or `$onboarding-vibedata` in Codex. Set `disable-model-invocation: true` in skill frontmatter and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`; a matching natural-language request alone must not trigger the skill.
Resolve helper paths relative to the installed skill and pass an explicit target repository; never write into the installed plugin as if it were the customer repo.

The target instructions currently prohibit a `skills` manifest field while shipped Codex compatibility manifests declare `"skills": "./skills/"`.
Reconcile that narrow packaging rule against current official documentation during implementation; preserve the shared source layout and test actual discovery in both runtimes.
This is packaging work, not a marketplace-format migration.

## Verification and acceptance cases

This is the plugin release suite. It exercises both Claude and Codex, plus a supported VibeData consumer when available. Customer onboarding runs checks for its selected runtime and explicitly requested consumer target; it does not launch this entire matrix. Unavailable requested checks remain unverified. Report-writing probes can test output shape and preservation detail, but do not establish runtime loading or full onboarding behavior.

All fixture repositories are tiny, offline, and disposable; no warehouse or customer dataset is copied.
Use bounded temporary-directory cleanup, and keep retained evidence small and redacted.
Each case specifies its requirement IDs, fixture state, prompt, expected artifact effects, allowed writes, and checks.

| Case | Requirements | Required result |
| --- | --- | --- |
| A01 Brownfield dbt/dlt | R02, R04, R12 | Preserve code and layout; discover conventions and exceptions; maps point to real artifacts and tests. |
| A02 Existing Python and notebooks | R02, R11 | Inventory imports/configuration/execution assumptions without running notebooks or converting their logic. |
| A03 Greenfield dbt/dlt | R03, R09, R12 | Scaffold and rules agree; no invented sources, domain terms, ADR rationale, or business-test coverage. |
| A04 Only AGENTS / neither file | R05 | Retain the existing canonical content or create one canonical entrypoint, with correct routing. |
| A05 Only CLAUDE | R01, R05, R06, R18 | Consolidate all unique instructions into AGENTS with a complete preservation ledger, preserving scope and links; triage conflicts before dependent changes; replace CLAUDE with only `@AGENTS.md` and prove fresh sessions load the canonical instructions. |
| A06 Both instruction files | R05, R06, R18 | Every unique instruction survives with a consolidation ledger; scope and links survive; conflicts are triaged; CLAUDE becomes the exact placeholder. |
| A07 Custom glossary and ADR paths | R04, R08 | New and updated artifacts and filename checks use the map, including a fresh VibeData consumer session. |
| A08 Existing-rule conflict | R06, R18 | Present competing sources and defer dependent writes until a decision; preserve their decision details in the report; permissible custom naming passes. |
| A09 Compatibility approved / declined / pending | R07, R13 | Apply only the approved diff; document other changes and their readiness effects. |
| A10 Empty vocabulary and decisions | R09 | Minimal glossary and ADR index; no empty numbered ADR or fabricated historical reason. |
| A11 Rerun and partial onboarding | R10, R18, R19 | Preserve human edits and report history; reconcile actual gaps; use a compact routine report without unnecessary ledgers or unselected-runtime blockers; unchanged input produces no substantive diff. |
| A12 Workaround applicability | R08 | Include only relevant platform/runtime rules, with a removal condition and task routing. |
| A13 Path and reference safety | R04, R05, R12 | Detect import cycles, path escapes, symlink aliases, case ambiguity, broken links, and registered-but-missing artifacts. |
| A14 Cross-runtime package discovery | R01, R15, R17, R19 | Both runtimes load the shared installed skill through explicit user invocation; catalogs and versions validate. The matrix is a release check, not a customer onboarding step. |
| A15 Fresh-session efficiency | R14 | Locate correct files/rules/checks with fewer discovery calls or context read, while preserving task correctness. |
| A16 Scope and side effects | R02, R07, R11 | No secret contents, production execution, silent conversion, unrelated repair, or implicit publication. |

Baseline and post-authoring runs use matched fixtures, prompts, runtime/model/settings, and fresh contexts.
Record tool-call counts before the first correct task action, content-read volume where the harness exposes it, wrong paths, repeated discovery, and correctness outcomes.
Use five matched trials per runtime for A15; compare medians per task and runtime, and inspect every correctness failure.
An efficiency claim requires a strict reduction in median discovery calls or measured content read without a reduction in correctness; report ties and regressions.
No universal numerical improvement target is promised in advance.

Structural checks and live behavioral checks are separate evidence.
Auth or unavailable runtime failures are blockers, not passing tests and not authorization to substitute a model or runtime.
A VibeData consumer trial runs on a disposable Domain/sandbox or equivalent supported harness; if unavailable, report A07's VibeData portion unverified.

## Implementation choices and remaining evidence

User decisions are the scope, skill name, dbt/dlt target, customer-path support, ownership table, lossless consolidation, conflict triage, conditional compatibility approval, workarounds, and requested authoring/verification skills.
Author-selected defaults are the plugin container name, report path, minimal helper arrangement, greenfield folders/package files, and five matched efficiency trials.
They are reviewable defaults, not claims of user preference.

Still to prove: wrapper loading in each runtime, custom-path behavior under VibeData, scaffold execution for the selected platform, and discovery reduction.
Current check outcomes and runtime limits are in the execution ledger and append-only validation record; this design is not execution evidence.

## Source-alignment contract (2026-10-16)

The approved [alignment plan](../docs/superpowers/plans/2026-10-16-onboarding-vibedata-source-alignment.md#observable-requirements-and-acceptance-map) maps S01–S12 to the original R01–R19 and conditional L01–L08.

| Requirement | Observable addition and acceptance |
| --- | --- |
| S01 | Canonical convention skills, contained Claude aliases, legacy ownership; metadata/context checks and real loading. |
| S02 | Shared Studio maps require requirement, plan, verification, case_record and design_record_area future patterns; standalone/native contracts remain valid. |
| S03 | ADR/design symmetry and actual native schema/config/selector checks execute through mapped commands and generated PR CI. |
| S04 | Measurements and outcomes stay in mapped verification; qualitative designs link them. |
| S05 | Ordinary tasks load relevant conventions and applicable workarounds after real compaction; mapped lint, explicit unit vars and approved docs guide work. |
| S06 | Samples account for page overshoot, cost, actual landed rows/load metadata, partial failures and parent-source extension registrations. |
| S07 | Authorized disposable samples leave persistent Domain state unchanged; missing targets/approval produce concrete proposals. |
| S08 | Selected DuckDB scaffold uses one explicit database and passes synthetic repeated ingestion, dbt and renamed-copy checks. |
| S09 | Every setup row has evidence/gap; warning cleanup preserves test IDs/counts and compiled semantics. |
| S10 | Stable C-n inventory, confirmed-only procedures and typed R-n review triage; source/mart/procedure-or-connected-model rehearsals. |
| S11 | Current supported consumer capability, artifact paths and side effects gate lifecycle composition; missing support is blocked. |
| S12 | Current package, preservation, runtime and release evidence remain distinct from historical results and skipped lanes. |

A shared `validate_context(root, *, consumer="standalone")` remains standard-library only; `studio` adds the five roles. Metadata parsing, native customer validation and runtime loading are separate checks. New roles are future patterns, not fabricated documents. Customer schemas and historical ADR IDs retain their ownership.

Inventory rows record C-n, convention, evidence, exceptions, destination and confirmation (`inferred`, `confirmed`, `changed by user`, `dropped`). Established facts need no repeated approval. Studio review metadata records type/date/commit/source; R-n text and IDs survive triage. Review status and proposed-edit approval are distinct. Reuse preservation ledgers instead of duplicating inventories.

No new discovery-efficiency claim is made without the required five-trial R14 comparison. Local scaffold success is not live Studio evidence.

## Sources

- [Target repository instructions](../AGENTS.md), [coding conventions](../.claude/rules/coding-conventions.md), and [catalog generator](../scripts/build_catalog.py).
- [Reference onboarding skill](/Users/shwetanksheel/scratch/vibedata-showcase/sample-nyctaxi-comp/.agents/skills/onboarding/SKILL.md), its `references/` and `templates/`, and the reference repo's `.agents/rules/` (read-only).
- [Current consumer domain-modeling skill](/Users/shwetanksheel/scratch/99_working/vibedata-data-engineering/plugins/vibedata-data-engineering/skills/domain-modeling/SKILL.md) and its shared `domain-context-and-adrs.md` (read-only evidence).
- [writing-for-agents](/Users/shwetanksheel/.codex/plugins/cache/ad-internal-marketplace/mattpocock-skills/1.0.0/skills/writing-for-agents/SKILL.md) and [writing-skills](/Users/shwetanksheel/.codex/plugins/cache/ad-internal-marketplace/superpowers/7.0.0/skills/writing-skills/SKILL.md); discover installed paths again before execution rather than treating these versioned locations as runtime dependencies.
