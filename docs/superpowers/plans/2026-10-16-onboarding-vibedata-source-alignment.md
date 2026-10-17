# Onboarding VibeData Source Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task by task with the previously selected native execution method, followed by an independent whole-change review. Use `superpowers:subagent-driven-development` only if the user changes the execution method. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align the shared onboarding skill with the audited source, preserve its generic repository guarantees, and report Studio lifecycle readiness from current consumer evidence.

**Architecture:** Keep one explicitly invoked onboarding skill, with conditional references and plain templates. Generate canonical convention skills, extend the existing maps and checker, and adapt the source's small repository checks and selected-platform scaffold. Compose a Studio lifecycle only through supported native capabilities; a missing consumer capability does not block independent repository work.

**Tech Stack:** Markdown skills, JSON maps and JSON Schema, Python standard library helpers, existing unittest/PyYAML/jsonschema/Ruff tooling, and selected dbt/dlt/DuckDB tooling in disposable environments. No new orchestration framework, general template renderer or YAML parser.

**Spec:** [Source alignment audit](../../../context/onboarding-vibedata-source-audit-2026-10-16.md), [preservation requirements R01–R19](../../../context/onboarding-vibedata-design.md), and [conditional lifecycle requirements L01–L08](../../../context/onboarding-vibedata-studio-lifecycle-plan.md). Read the [historical consumer gate](../../../context/onboarding-vibedata-validation.md#studio-lifecycle-task-1-consumer-dependency-report) as prior evidence, not current capability.

## Global Constraints

- This document authorizes no execution by itself. The later user launch authorized unattended local execution; the [run ledger](../../../context/onboarding-vibedata-source-alignment-run.md) records scope and remaining gates.
- Latest user scope: run only Codex tests; do not run more Claude tests. Preserve captured Claude evidence and its failed/partial verdicts. Studio capability work remains excluded by “do 1–3, not 4.” Historical dual-runtime verification steps below are not authority to resume Claude testing.
- The user later declined installed-package Codex testing and authorized the scoped commit, branch update, push and draft PR. Record that test as skipped/unverified, not passed. Draft review may proceed with the disclosed acceptance gaps; merge and release publication remain excluded.
- Worktree: `/Users/shwetanksheel/scratch/ad-plugins/.worktrees/vibedata-official-onboarding-vibedata-plan`; branch: `docs/onboarding-vibedata-plan`; planning baseline: `d07d1a8538cc52826373211110c96df9d3f090b5`.
- Read-only source: `/Users/shwetanksheel/scratch/vibedata-showcase/sample-nyctaxi-comp`, audited at `b75841f12c14ad8e1870d1b1581d6bd59a0fb5bf`; previous refresh: `349d026`. The audited delta is 42 commits and 68 files.
- Preserve unrelated work, customer application behavior, custom map/schema/checker ownership, instruction scope, human edits, historical ADR identifiers and report history. Unchanged reruns produce no substantive diff.
- Keep `AGENTS.md` canonical and `CLAUDE.md` as the losslessly reconciled `@AGENTS.md` wrapper. Keep onboarding explicitly invoked in both runtimes; generated task conventions remain discoverable for ordinary work.
- Keep the main skill under 400 words. Put conditional detail in linked references. Customer checks use the selected runtime; the full runtime matrix belongs to plugin release verification.
- Reference and consumer repositories remain read-only. No production loads, persistent Domain mutation, provisioning, destructive Git operations, merge, push, PR or publication is included by default. Inspect delegated operations for early commit/push effects.
- Preserve all applicable session authorization. Do not ask again for routine actions already authorized. A later launch can authorize local task commits and additional named operations; record that scope before execution.
- Verify SDK versions and initialization through the operator's approved documentation routes before writing SDK-dependent templates. Preserve the selected package manager and configured runtime provider/model. Authentication failures stop affected service operations.
- The portable checker stays standard-library only. Reuse `resolve_path`, `read_text`, `read_object` and `instruction_findings`. Keep `inspect_repo.py` unchanged unless a new regression proves a defect; it already discovers all 11 source project skills.
- Use tiny synthetic fixtures and `TemporaryDirectory`; never copy the source warehouse. Generated pytest configuration uses `tmp_path_retention_count = 0` and `tmp_path_retention_policy = "failed"`.
- Behavioral evidence is limited to 1 MiB per run and 50 MiB retained in total. Keep redacted events, hashes, diffs and verdicts; exclude credentials, notebook outputs and customer data.
- Report timestamps in the workstation zone (`date +%Z`; `+04` at planning). Never commit secret-bearing files.
- Generate catalog/README blocks only through `scripts/build_catalog.py`. Preserve submodule pins, marketplace parity and the private theme-contract CI gate.

## Review Focus

1. Mixed legacy rules, canonical skills and existing Claude skill names must preserve ownership and avoid duplicate or escaped loads. Task 2 tests aliases, collisions, legacy references and inactive templates; Task 8 checks actual discovery.
2. Custom schemas and artifact paths must remain usable without acquiring the shared schema or fabricated documents. Tasks 2 and 4 test custom maps, future patterns, native checks and custom ADR identifiers.
3. A page larger than a sample limit, a partial load, or a stale profile must not become evidence of a safe completed sample. Tasks 3, 5 and 6 check page semantics, early failure, evidence currency and authorization.
4. A runtime environment variable or renamed database must not send ingestion and transformation to different databases or break stored views. Task 5 tests a nondefault absolute path and renamed-copy queries without rebuilding.
5. A resumed native phase must not reuse stale verification, publish before authorization or treat absent runtime capability as success. Tasks 7 and 8 test phase boundaries, shipping effects and unavailable-target outcomes.

---

## Observable requirements and acceptance map

`A1`–`A12` below refer to the numbered audit findings. These requirements describe output behavior, not agent activities.

| ID | Required behavior | Audit / preserved contract | Tasks / verification |
| --- | --- | --- | --- |
| S01 | New conventions live at `.agents/skills/<name>/SKILL.md`, have valid metadata and load through each selected runtime's supported route. Existing rules and customer skills remain usable. | A1; R01, R05, R06, R10, R17, R19 | 2, 8; context tests, metadata validation and fresh runtime discovery |
| S02 | Studio-ready context resolves `requirement`, `plan`, `verification`, `case_record` and `design_record_area`; standalone/native maps retain their own contracts. | A2; R04, R09, R12, L03 | 2, 7; missing-role and custom-schema cases |
| S03 | Active ADR/design links agree in both directions and repository CI runs the actual registered checks. Native schema/config/selector validation is retained. | A3; R07, R12 | 4, 8; broken-link, selector, config and workflow checks |
| S04 | Design records contain decisions and rationale; measurements and check outcomes live in mapped verification with links from the design. | A4; R09, R18 | 3, 8; profile-placement and refresh probes |
| S05 | Ordinary tasks invoke relevant conventions, reload applicable workarounds after compaction, use mapped lint, use explicit dbt unit-test vars, and consult approved docs instead of installed library source. | A5; R08, R14 | 3, 8; routing, compaction and unit-var probes |
| S06 | Samples report actual page/row-group behavior and landed results; new resources retain their parent source identity and registrations. | A6; R02, R08, R11 | 3, 5, 8; large-page and resource-extension cases |
| S07 | Sandbox data state and persistent Domain state are separate. An unauthorized or unavailable load produces a precise blocker/proposal and no load attempt. | A7; R07, R11, R13, L02, L05 | 6, 7, 8; authorization cases and conditional live run |
| S08 | A selected DuckDB scaffold has executable orchestration/configuration/checks and passes ingestion-to-dbt verification against one explicit database. Empty real scaffolds claim no business coverage. | A8; R03, R11, R12 | 5, 8; same-database integration and empty-scaffold checks |
| S09 | Every applicable Studio setup check has evidence or a named gap; non-Studio platforms retain intentional choices. Warning cleanup preserves test inventory and compiled semantics. | A9; R07, R13 | 5, 6, 8; setup matrix and platform counterexample |
| S10 | Inventory records evidence, exceptions and destinations; only confirmed procedures become skills; typed review IDs remain stable through triage; later-task routes are rehearsed. | A10; R02, R06, R09, R10, R18 | 6, 8; inventory, triage, procedure and rehearsal cases |
| S11 | Studio progression uses the current supported consumer contract and authorized side effects; missing support leaves a named dependency without blocking standalone work. | A11; L01–L08 | 1, 7, 8; versioned capability table and live acceptance |
| S12 | Package checks, preservation regressions, runtime evidence and release metadata describe the changed contract accurately. Historical results remain historical. | A12; R15, R16, R18, R19 | 1, 8, 9; baseline, release matrix and independent review |

Keep R14's efficiency scope honest: rerun its existing five-trial comparisons when claiming fewer discovery calls. Do not turn that result into an unsupported token, cost or cross-runtime claim.

## Resolved adaptation decisions

### Convention discovery and validation

- Rename the ten packaged `templates/rules/<name>.md` files to `templates/skills/<name>.md`. They remain ordinary Markdown templates, not nested distributed `SKILL.md` entrypoints. Their rendered destinations are `.agents/skills/<name>/SKILL.md`.
- For selected Claude use, create contained directory symlinks `.claude/skills/<name> -> ../../.agents/skills/<name>` after checking ownership and collisions. Do not duplicate maintained content. Preserve an existing supported route. A collision remains pending until ownership is clear; finish unrelated work.
- For selected Codex use, use canonical `.agents/skills` discovery. Studio discovery needs evidence from its actual consumer; do not infer it from Codex support.
- Shared maps prefer `key_references.conventions`; accept legacy `rules`, and validate both if both exist. Preserve legacy `.agents/rules` content and active references during migration; remove a redundant file only after its content, scope and callers have retained destinations.
- Start skill-tree instruction validation at actual `SKILL.md` files and follow reached Markdown references. Do not recursively validate unused templates as live policy. Retain legacy rules-directory behavior. Apply containment/cycle/case checks to canonical and symlinked entrypoints and deduplicate by resolved identity.
- Add `validate_context(root: Path, *, consumer: str = "standalone") -> list[str]` and CLI `--consumer {standalone,studio}`. `studio` adds the five role requirements to the shared contract; the default preserves existing callers. Unknown API consumer values raise `ValueError`; CLI choices reject them.
- Do not claim that this structural checker validates YAML frontmatter. Validate shipped/rendered metadata with existing PyYAML tests and selected-runtime native validation where available. For customer content, missing metadata-validation capability is a named verification gap, not proof of valid metadata.
- Keep new role values as future patterns. Defaults: `docs/requirement/{intent}.md`, `docs/plans/{intent}.md`, `docs/verify/{intent}.md`, `docs/cases/{intent}.md`, `docs/design/{area}/{subject}.md`. A consumer owns the intent identifier. Existing customer values win; incompatible consumer paths require a supported mapping or a blocker.

Official discovery documentation checked during planning: [Codex skills](https://developers.openai.com/codex/skills) (redirects to [Build skills](https://learn.chatgpt.com/docs/build-skills)) and [Claude skills](https://code.claude.com/docs/en/skills). Codex documents `.agents/skills`; Claude documents `.claude/skills` and symlinked skill folders. Claude can load malformed YAML with empty metadata, so invocation alone is not metadata validation. Recheck selected versions if behavior differs.

### Source contradictions

| Contradiction in source | Decision for this implementation |
| --- | --- |
| “Two dbt_project.yml lines” conflicts with broader setup/document moves. | State the actual reviewed setup scope; do not claim a two-line limit or authorize unrelated repair. |
| “1,000 rows” conflicts with page-based sampling. | Report actual landed rows and page/row-group cost; do not promise an exact row cap. |
| dlt text puts profiles in design while design conventions prohibit measurements. | Store measurements in verification and link them from qualitative decisions. |
| Existing documents must stay in place but other guidance moves them. | Preserve paths by default; relocate only as an explicit lossless migration. |
| Resource-extension guidance is only in the live dlt convention. | Incorporate it into the generic emitted dlt convention and registration checks. |
| Ordering still names an orchestration route removed elsewhere. | Use repository run scripts; do not invent a native orchestration skill. |

## File responsibilities

`K` means `plugins/vibedata-repo-skills/skills/onboarding-vibedata`, relative to the worktree. Brace notation below expands to the named files only. New paths are marked **new**.

| Paths | Responsibility |
| --- | --- |
| `K/SKILL.md`; `K/agents/openai.yaml` (preserve controls) | Explicit invocation, short shared flow and conditional Studio routing. |
| `K/templates/agents.md`; `K/templates/skills/{adr,context,dbt-models,dbt-testing,design-records,dlt,git-and-prs,python,sql-style,workarounds}.md` (**renamed**) | Generated task routes and convention metadata/content. |
| `K/templates/{repo-map.json,repo-map.schema.json,test-map.json}`; `K/scripts/validate_context.py` | Shared map contract, backward-compatible structural checking and actual check registrations. |
| `K/references/{artifact-contract,compatibility,brownfield,greenfield,studio-duckdb}.md` | Preserve ownership, define generation/refresh, sampling, review and platform checks. |
| `K/references/studio-lifecycle.md` (**conditional new**) | Supported native phase composition, side effects and resume rules; only after Task 7's source capability gate. |
| `K/templates/{review,proposal,onboarding-report}.md` | Typed review/triage, real proposals and compact Changes/Checks/Blockers outcomes. |
| `K/templates/checks/{test_adr_links.py,test_maps.py}` (**new**) | Generated ADR backlinks and selected dbt/dlt map checks. |
| `K/templates/repo/{repo-checks.yml,ruff.toml,sqlfluff.cfg,requirements-dev.txt,gitignore-fragment}` (**new**) | Selected repository CI/check configuration and runtime ignores. Preserve customer equivalents. |
| `K/templates/orchestration/{run_ingest.py,run_transform.py}` (**new**) | Minimal executable entrypoints using one explicit database path and fail-fast behavior. |
| `K/templates/dbt/{dbt_project.yml,profiles.yml,packages.yml,relations.sql,generate_schema_name.sql}`; `K/templates/dlt/{config.toml,requirements.txt}` (**new**) | Selected-platform configuration, with Studio-specific macros/packages gated by the chosen contract. |
| `K/templates/greenfield/README.md` | Exact template-to-destination map, inactive starters and database-path/verification contract. |
| `tests/test_onboarding_{context,package}.py` | Extend existing contract, preservation and distribution tests. |
| `tests/test_onboarding_scaffold.py` (**new**) | Generated checks, subprocess behavior and opt-in selected-platform integration using bounded fixtures. |
| `tests/onboarding/{cases,reference-refresh}.json`; `tests/onboarding/studio-lifecycle.json` (**new**) | Existing behavioral matrix extended with source-alignment and lifecycle cases. |
| `context/onboarding-vibedata-source-alignment-run.md` (**new at execution**) | Restartable task ledger, versioned capability results and evidence index. |
| `context/onboarding-vibedata-{design,plan,studio-lifecycle-plan,validation}.md`; `docs/handoffs/onboarding-vibedata-studio-lifecycle.md` | Current contracts/status and append-only historical evidence, with handoff to this plan. |
| `.claude-plugin/plugin.json`; `plugins/vibedata-repo-skills/.{claude,codex}-plugin/plugin.json` | Root release gate and equal child plugin versions. |
| `catalog/`; README generated blocks | Generator output only, if changed. |

Do not add fixtures for every variation. Reuse `mapped_repo`, `write`, `write_json`, `hashes` and existing fixture copies; build small variations in temporary directories. Keep source inspection unchanged, avoid a new production renderer, and do not add a general migration engine.

## Overnight execution contract

### Launch and resume

1. Read this plan, its spec links and current applicable instructions before edits. Preserve the native execution method from the existing handoff.
2. Record the launch scope, actual branch/head, source SHA, interpreter/runtime versions, source/docs references and task statuses in `context/onboarding-vibedata-source-alignment-run.md`.
3. Give each task one status: `pending`, `running`, `passed`, `blocked`, or `failed`. A blocked task names the missing capability/input, affected requirement, next command/action and tasks that can continue.
4. Record each completed task's changed files, commit or diff hashes, exact check commands, exit codes, evidence paths and local timestamps. Check these inputs before reusing evidence after restart.
5. Commit task-scoped files locally only when launch/session authorization permits it. Never use `git add .`; never stage `.cache/`, secrets, raw traces or unrelated work. Otherwise record the bounded diff and continue without asking repeatedly.
6. On restart, resume the first runnable incomplete task. If code, configuration, dependency versions, relevant data or target identity changed, invalidate only the affected checks. Do not repeat valid work or duplicate artifacts.

If the user later selects subagent-driven development, use implementers `gpt-6-luna` with high reasoning and reviewers `gpt-6.1-sol` with medium reasoning, as required by the supplied project instructions. Stop that dispatch if either exact requirement is unavailable; do not substitute. Release agents after their assigned work or expected review-feedback cycle ends. This conditional option does not change the current native execution choice.

| Task | Prerequisites | What may remain blocked without stopping other work |
| --- | --- | --- |
| 1 | None | Current consumer/deployed-target lookup and individual runtime baseline lanes |
| 2 | Task 1 local baseline | A runtime's actual discovery trial |
| 3 | Tasks 1–2 | Facts requiring unavailable approved documentation/authentication |
| 4 | Task 2 | Customer-native custom syntax outside the supported ADR format |
| 5 | Tasks 2, 4 | Dependency installation or selected-platform execution |
| 6 | Tasks 3, 5's defined contracts | Actual sandbox loading and unknown customer decisions |
| 7 | Tasks 1–6 applicable outputs and current consumer capability | Entire native lifecycle if unsupported; live lane if target or authorization is absent |
| 8 | Tasks 2–6; Task 7 only for lifecycle cases | Individual runtime/live lanes; complete all available checks |
| 9 | Results from every runnable task | Release acceptance remains incomplete where required checks are blocked |

### Bounds and notifications

- Default command limits: 10 minutes for unit/static checks, 20 minutes for dependency installation, 30 minutes for synthetic scaffold integration, and 10 minutes per fresh-runtime probe. Use process timeouts that terminate child processes; bound captured output while streaming. No blocking poll exceeds 60 seconds.
- Retry a transient non-auth network failure once. Do not retry authentication failures or substitute identity/provider. After two repair attempts at the same failing gate, record the evidence and blocker and continue independent work. Resume the gate only with a new supported hypothesis or external change.
- Do not invent an overnight deadline. If the launch supplies one, stop starting work that cannot finish within it and checkpoint safely. Never weaken checks to meet the time limit.
- For a future unattended run, read `/Users/shwetanksheel/.claude/references/pushover.md` and use `PUSHOVER_USER` / `PUSHOVER_API` without printing them. Send priority `1` through `https://api.pushover.net/1/messages.json` on each completion: `Task X of 9 complete: <short task description>`.
- Send a separate alert when input is needed, when the run must pause, and when the whole run ends. State completed/blocked task IDs and the required input. A conditional blocker can be reported while independent work continues. Notification failure is recorded; it does not turn failed delivery into a completed alert or discard local progress.
- No alerts are sent while merely preparing this plan in the current interactive session.

## Implementation tasks

### Task 1: Establish current baselines and the execution ledger

**Files:** Create `context/onboarding-vibedata-source-alignment-run.md` and `tests/onboarding/studio-lifecycle.json`; modify `tests/onboarding/{cases,reference-refresh}.json`; append evidence to `context/onboarding-vibedata-validation.md`.

**Interfaces:** Consumes the audited SHAs and existing scenario schema. Produces baseline evidence indexed by case/runtime/arm/trial, plus a capability table with `capability`, `source revision`, `deployed version`, `entrypoint`, `artifact contract`, `side effects`, `authorization`, and `status`. Source support and deployed support are separate columns.

- [x] **Step 1: Record preflight.** Check `git status --short`, `git branch --show-current`, `git rev-parse HEAD`, `git submodule status`, and the source HEAD/status. Preserve the untracked audit and any unrelated `.cache/` contents. If source moved, record the extra delta before using newer facts; do not silently discard the audited baseline.
- [x] **Step 2: Prepare one bounded development environment.** Use the repository manager and a supported Python (the audit used Python 3.12.12), install declared `requirements-dev.txt`, and record actual versions. Use task-scoped variables such as `ONBOARDING_PYTHON` and `ONBOARDING_EVIDENCE_DIR`; do not overwrite global home/config settings. Keep environment and caches disposable.
- [x] **Step 3: Record the current deterministic baseline.** Run `python -m unittest discover -s tests -p 'test_onboarding*.py' -v`, then `python -m unittest discover -s tests -v` using that interpreter. Record each failure. The historical 30 focused passes and two wiki failures are not this run's results.
- [x] **Step 4: Add behavior cases before changing skill prose.** Extend the existing JSON formats with `convention-discovery`, `legacy-custom-preservation`, `measurement-placement`, `startup-and-compaction`, `page-sampling-resource-extension`, `sandbox-state-and-authorization`, `inventory-review-rehearsal`, `warning-cleanup-equivalence`, and `non-studio-preservation`. Put native lifecycle cases in `studio-lifecycle.json`: `unsupported-consumer`, `artifact-path-conflict`, `early-push-denied`, `partial-ci-hooks`, `stale-resume`, `greenfield-live`, `brownfield-live`. Add `.claude/skills/**` to selected-Claude fixture write allowlists and verify symlink destinations stay inside the fixture; do not grant broad `.claude/**` configuration writes.
- [ ] **Step 5: Capture baseline/control behavior.** Run fresh-context controls and the old installed-skill arm before authoring. Use five trials for each wording probe/variant; keep assertions outside prompt/fixture roots and inspect every output. Pin case text, runtime/model/provider and input hashes. Auth/tool failure blocks that lane; do not claim its baseline exists. Structural work can continue, but record any chronology gap for the affected skill validation.
- [x] **Step 6: Refresh current consumer facts read-only.** Identify the supported consumer source/release and, if available, deployed release and existing disposable target. Inspect onboarding kind/review entrypoints, artifact resolution, CI bundle, runtime context, hook install, verification, shipping and early pushes. Record exact source references and missing capabilities. Do not edit the consumer, invent an onboarding kind, provision a target or reuse merged PR #48.
- [x] **Step 7: Close Task 1's local gate.** Baseline failures and unavailable lanes must be named. Mark Task 7 blocked where consumer support is absent, then proceed to Task 2. Save/commit only task files under the launch contract; suggested message: `test: capture onboarding alignment baselines`.

### Task 2: Migrate convention output and the shared map contract

**Files:** Rename the ten `K/templates/rules/*.md` files to `K/templates/skills/*.md`; modify `K/templates/{agents.md,repo-map.json,repo-map.schema.json,test-map.json}`, `K/scripts/validate_context.py`, `K/references/artifact-contract.md`, `tests/test_onboarding_context.py`, `tests/test_onboarding_package.py`.

**Interfaces:** Produces `validate_context(root: Path, *, consumer: str = "standalone") -> list[str]`, CLI `--consumer`, `key_references.conventions`, the five Studio role names and canonical skill destinations defined above. Existing `validate_context(root)` calls and legacy shared maps remain valid. Native customer maps keep their own validator.

- [x] **Step 1: Add failing structural tests.** Add `test_context_accepts_conventions_or_legacy_rules`, `test_context_validates_both_reference_roots`, `test_skill_templates_are_not_active_instructions`, `test_skill_entrypoints_reject_escaped_or_broken_symlinks`, `test_studio_requires_each_artifact_role`, and `test_standalone_preserves_legacy_roles`. Assert no false `{{rule_path}}` finding for an unreferenced inactive template; assert each omitted Studio role is named; assert legacy/custom fixture hashes do not change.
- [x] **Step 2: Add failing package tests.** Add `test_convention_templates_render_valid_metadata` and update existing rule-set/map assertions. Render known path substitutions only in the test fixture; `yaml.safe_load` must yield nonempty string `name`/`description`, name equal to selected convention, and no unresolved generation tokens. A malformed YAML control must fail the metadata check. Keep exactly one distributed `SKILL.md` under the plugin.
- [x] **Step 3: Observe RED.** Run `python -m unittest discover -s tests -p 'test_onboarding_context.py' -v` and `python -m unittest discover -s tests -p 'test_onboarding_package.py' -v`. Retain failures caused by the old contract, not missing dependencies.
- [x] **Step 4: Implement the structural checker changes.** Accept `conventions` or `rules` with schema `anyOf`; require neither new runtime mode nor new fields in native customer schemas. Validate both supplied roots, seed active `SKILL.md` entrypoints, follow their links, and preserve existing path limits, secret-reference rejection and import-cycle checks. Add `--consumer`; keep success output explicit about unverified metadata/runtime/execution.
- [x] **Step 5: Update generated maps and routing.** Add the new role patterns and preferred reference key. Update map maintenance and template paths together. State the single-copy Claude route, collision handling, legacy preservation and lossless link repair in `artifact-contract.md`; no automatic replacement of a customer skill or native checker.
- [x] **Step 6: Verify GREEN and migration preservation.** Rerun the two test files. Add a contained Claude symlink fixture and a mixed legacy/skills fixture; confirm missing references still fail and unchanged validation is read-only. Runtime collision handling and byte-stable refresh are also checked in Task 8.
- [x] **Step 7: Save the task checkpoint.** Record new interfaces and results; suggested local commit: `feat: generate convention skills with compatible map validation`.

### Task 3: Align convention content, sampling and document placement

**Files:** Modify `K/templates/agents.md`, `K/templates/skills/{dbt-testing,design-records,dlt,python,workarounds,context,adr,dbt-models,git-and-prs,sql-style}.md` only as applicable; modify `K/references/{artifact-contract,compatibility}.md`; extend `tests/onboarding/reference-refresh.json`.

**Interfaces:** Consumes Task 2's role and discovery contract. Produces task-triggered conventions with narrow descriptions, a mapped verification destination for measurements and source/resource routing without platform assumptions.

- [x] **Step 1: Pin the behavior assertions.** `measurement-placement` requires qualitative rationale and a verification link in design, with numeric counts/profile results only in verification. `startup-and-compaction` requires relevant skill invocation, applicable workaround reload, mapped Ruff and no installed-package source inspection. `page-sampling-resource-extension` requires actual page/row-group counts, loader-supported limits and unchanged parent source identity. `non-studio-preservation` retains deliberate catalogs, three-decimal money, exact IDs/NULLs, timezone meaning and non-dlt loading.
- [x] **Step 2: Review baseline failures for those assertions.** Use Task 1 evidence; do not generate a new baseline after the edit and label it pre-change. Missing baseline lanes remain explicit.
- [x] **Step 3: Verify the uncertain package facts.** Check current dbt `overrides.vars` behavior and dlt limit/page semantics through Context7, then official docs if needed. Record versions/URLs. Do not repeat the source's unverified universal statement that project vars never apply. Authentication failure stops that fact lookup and dependent SDK claim.
- [x] **Step 4: Update document conventions.** Keep decisions, alternatives, ADR links, affected consumers and history in design. Route measured evidence to `artifact_paths.verification`, shared design to `design_record_area`, and retain existing document paths/content until any approved migration has verified destinations.
- [x] **Step 5: Update startup and test conventions.** Route task → relevant convention → mapped checks; reload emitted applicable workarounds after compaction. Require explicit relevant unit-test vars. Use approved docs/repo examples for library behavior and actual mapped Ruff config/exclusions. Keep maintenance/evaluation material outside normal build routing.
- [x] **Step 6: Update dlt/source conventions.** Explain whole-page/row-group overshoot, actual landed identity/count/load metadata, repeated replacement samples, acceptable cost and source-version-aware profile reuse. A resource addition updates its existing source module, resource docs/tests/design, dbt source and staging artifacts as applicable; it does not automatically create another source/pipeline.
- [ ] **Step 7: Verify treatment behavior.** Repeat the four bounded probes five times per wording variant in available runtimes and inspect every flagged result. Run package metadata/link tests. Wording success is not runtime discovery or executed sample evidence; those gates remain in Tasks 5 and 8.
- [x] **Step 8: Save the task checkpoint.** Suggested local commit: `docs: align onboarding conventions and evidence placement`.

### Task 4: Supply ADR, native map and repository CI checks

**Files:** Create `K/templates/checks/{test_adr_links.py,test_maps.py}`, `K/templates/repo/repo-checks.yml`, `tests/test_onboarding_scaffold.py`; modify `K/templates/test-map.json`, `K/references/{artifact-contract,greenfield,brownfield}.md` and relevant ADR/design templates.

**Interfaces:** Generated ADR check exports `validate_adr_links(root: Path) -> list[str]`, supports `python tests/test_adr_links.py --root .`, and exposes a pytest test. It resolves `artifact_paths.adr` and `design_record_{model,pipeline,area}`. Generated native map tests retain the customer's schema and verify registered dlt config sections and nonempty dbt selectors. The portable checker is not substituted for these tests.

- [x] **Step 1: Add failing generated-check tests.** In `test_onboarding_scaffold.py`, add `test_adr_links_require_both_directions`, `test_adr_links_support_custom_paths_and_linked_ids`, `test_adr_links_reject_missing_or_escaped_targets`, and `test_adr_links_handle_rejected_and_successor_records`. Use tiny mapped files, including `decisions/DEC-alpha.md`; no assumption of four-digit numbering for linked citations. A design citing an ADR without its backlink and an ADR listing a design without its citation must each fail.
- [x] **Step 2: Pin the supported ADR format.** New output uses Markdown links and `## Affected designs`; preserve source-style `ADR NNNN` citations where the mapped filenames make them unambiguous. Rejected historical ADRs do not require active backlink symmetry, but broken links remain findings. A replacement ADR and active design must link to each other; a design left only on the rejected predecessor is a stale-successor finding. Preserve a native checker for other formats and report unsupported syntax instead of rewriting history.
- [x] **Step 3: Add failing native-map and CI tests.** `test_native_map_checks_preserve_schema_config_and_selectors` fails for a JSON Schema violation, a missing registered `config_section`, and a selector resolving to zero nodes; an empty source inventory is valid. `test_repo_checks_workflow_runs_declared_checks` asserts PR triggering, the actual command and one interpreter with declared pytest/dbt dependencies. Use controlled subprocess outputs in unit tests; reserve real dbt resolution for Task 5. Keep emitted map tests as plain assertion-based functions discoverable by pytest, using existing jsonschema/PyYAML dependencies; package unit tests can call them without adding pytest/dbt to this repository's default test environment.
- [x] **Step 4: Observe RED.** Run `python -m unittest discover -s tests -p 'test_onboarding_scaffold.py' -v`; failures must identify the absent checks or behavior.
- [x] **Step 5: Adapt the two small checks.** Start from the audited source tests, replace hardcoded paths with mapped roles, validate containment and bound reads. Verify the selected dbt CLI/selector interface through approved docs before writing its subprocess call; use installed JSON Schema/PyYAML tooling. Keep template code self-contained in destination repositories and avoid importing the plugin at runtime. Install dbt dependencies through the declared setup/CI command before selector tests; tests must not silently download packages.
- [x] **Step 6: Register the actual commands.** Generated destinations are `tests/test_adr_links.py`, `tests/test_maps.py` and `.github/workflows/repo-checks.yml`. Register the decisions/check modules with real paths. Reuse suitable existing CI; only install the fallback workflow where absent and authorized. Preserve custom hooks and the native bundle; never silently bypass `.git/hooks` by setting `core.hooksPath`.
- [x] **Step 7: Verify GREEN.** Rerun scaffold tests and existing package/context tests. Execute the emitted ADR command in the temporary custom-path fixture and check its exit code/messages. Validate workflow configuration locally; remote triggering remains unverified until an authorized PR run.
- [x] **Step 8: Save the task checkpoint.** Suggested local commit: `feat: add mapped repository and ADR validation templates`.

### Task 5: Complete the selected scaffold and prove one-database execution

**Files:** Create the listed `K/templates/orchestration/`, `K/templates/dbt/`, `K/templates/dlt/` and remaining `K/templates/repo/` files; modify `K/templates/greenfield/README.md`, `K/references/{greenfield,studio-duckdb}.md`, map templates, `tests/test_onboarding_scaffold.py` and package assertions.

**Interfaces:** `run_ingest(db_path: Path) -> int` executes registered pipeline files and stops at the first nonzero status. `run_transform(db_path: Path, target: str = "dev") -> int` runs `dbt deps` then `dbt build`, stopping on dependency failure. Starter `load(source, repository_root, db_path)` uses that same explicit database path. The rendered CLI/profile environment variable is `ONBOARDING_DUCKDB_PATH` for standalone local DuckDB, or the verified native variable for Studio (historically `VD_EPHM_DUCKDB_LOCAL_PATH`); never silently fall back to a different database.

- [x] **Step 1: Verify and record SDK/config facts.** Resolve a compatible Python/dlt/dbt-core/dbt-duckdb set, initialization patterns, CLI invocation, profile behavior and selected packages through approved docs and the project manager. Treat prior version notes as historical. Prepare the bounded integration environment with its declared check dependencies; keep ordinary repository test dependencies separate.
- [x] **Step 2: Add failing orchestration tests.** Add `test_pipeline_and_dbt_share_nondefault_database`, `test_ingest_stops_before_next_pipeline`, `test_transform_stops_when_deps_fail`, `test_missing_database_path_fails_before_launch`, and `test_empty_scaffold_does_not_register_example_sources`. Mock subprocess boundaries for failure ordering; assert exact path propagation, interpreter and return codes. Missing/nonabsolute CLI database input fails before work starts.
- [x] **Step 3: Add the integration gate.** Define `test_selected_duckdb_scaffold_round_trip` gated by `ONBOARDING_RUN_SCAFFOLD_INTEGRATION=1`. In one disposable generated fixture, ingest a tiny synthetic row, transform it through dbt and query the expected value from an absolute path outside the default `.local/data.duckdb`. Assert the default file was not created. Skip explicitly in ordinary unit runs; a skipped result never passes this gate.
- [x] **Step 4: Observe RED.** Run `python -m unittest discover -s tests -p 'test_onboarding_scaffold.py' -v`, then the enabled integration command in Step 8, using the resolved selected-platform environment. Record the old fixed-path defect or missing scaffold as the failure; dependency installation failure is a blocker, not a reproduced product bug.
- [x] **Step 5: Implement orchestration and starter path consistency.** Adapt source patterns with explicit `db_path`, the selected environment variable and `sys.executable`; preserve existing customer entrypoints. Remove the fixed database path from the current pipeline example. Keep source registration empty until a real source contract exists.
- [x] **Step 6: Complete the selected configuration.** Map templates to `orchestration/`, `transformation/`, `ingestion/.dlt/`, root check configs and runtime ignores. Include dbt profile/packages/macros, native check dependencies and supported dlt configuration only when required by the chosen platform. For Studio, verify evaluator package need and disabled-by-default models/seeds, dynamic profile selection, Parquet/Arrow metadata, `source()` staging and catalog-free relations. Preserve intentional attached catalogs outside that contract.
- [x] **Step 7: Document exact destination and command registration.** Add applicable `dbt_project`, `dbt_sources`, `source_config`, `resource_docs`, `source_tests`, ingestion/orchestration roles and commands. Literal paths must exist; future source patterns remain patterns. Keep inactive starter files outside active model/source discovery. Include `.user.yml`, dlt previews, scratch/state, dbt outputs and selected package caches in ignores without ignoring customer source files.
- [x] **Step 8: Verify GREEN with actual tools.** Run scaffold unit tests, then `ONBOARDING_RUN_SCAFFOLD_INTEGRATION=1 python -m unittest discover -s tests -p 'test_onboarding_scaffold.py' -k test_selected_duckdb_scaffold_round_trip -v`. In that same bounded fixture, test replacement loading with a page larger than the requested nominal limit and inspect actual landed rows/load metadata. Query stored views after copying to a renamed database without rebuilding. Keep this synthetic database small; clean it and its task-created caches.
- [x] **Step 9: Save the task checkpoint.** Record resolved versions, actual queries/results and any unavailable adapter lane. Suggested local commit: `feat: complete selected onboarding scaffold and shared database path`.

### Task 6: Complete setup outcomes, inventory, review and rehearsals

**Files:** Modify `K/references/{brownfield,greenfield,studio-duckdb,artifact-contract,compatibility}.md`, `K/templates/{review,proposal,onboarding-report}.md`, `K/SKILL.md`, and the existing behavioral scenario files.

**Interfaces:** Inventory rows use `C-n`, convention, evidence, exceptions, destination and confirmation state (`inferred`, `confirmed`, `changed by user`, `dropped`). Studio review frontmatter uses `type`, `date`, `commit`, `source`; finding IDs use `R-n`. Readiness distinguishes `context`, `runtime loading`, `sandbox execution`, `persistent Domain state`, and conditional `Studio lifecycle` without adding mandatory report sections beyond Changes/Checks/Blockers.

- [x] **Step 1: Pin failing behavior assertions.** The inventory probe accounts for every moved convention and preserves established facts without asking again. The procedure probe emits no unconfirmed procedure skill. The review probe preserves finding IDs/text while triage changes only status. The sandbox probe never runs an unauthorized load and never calls a temporary sample a seeded persistent Domain. Use Task 1 baselines.
- [x] **Step 2: Add the compact inventory and procedure contract.** Build evidence before asking about unknown rationale, inconsistency or ownership. Reuse the preservation ledger where possible; do not create duplicate records. Route repository-only ordered procedures into skills only after confirmation; keep unresolved procedures as findings while other work continues.
- [x] **Step 3: Extend review and proposal templates.** Use one review per type/run, kinds `platform`, `convention`, `bug`, `gap`, `style`, initial status `open`, and triage `intent`, `proposal → P-NNNN`, `declined: <reason>`, `deferred`. Keep proposed-edit approval (`pending`/`approved`/`declined`) separate from review triage. Preserve customer formats and previous runs. Create no empty review/proposal just to populate a path.
- [x] **Step 4: Define sandbox outcomes.** On an empty persistent Domain, attempt each source's bounded sample and applicable dbt build only in a confirmed disposable sandbox within authorization. Record actual target, source/sample limits, landed results and failures. Missing/expensive/unavailable execution yields a mapped proposal and exact blocker; persistent state remains empty/unknown as observed. Authentication failure stops the affected service path, with no credential discovery fallback.
- [x] **Step 5: Complete the setup checklist.** Each row records applicability, before-state, proposed change, side effects, authorization, command/evidence and result/gap: baseline commands; evaluator settings; dependency installation; native schema/config/selectors; Arrow metadata; `source()` staging; timestamp/key consistency; SQLFluff profile/project paths; mapped Ruff config/exclusions; renamed-copy behavior. For warning cleanup, compare before/after test unique IDs/counts and normalized compiled SQL; parsing alone cannot establish unchanged behavior. The `warning-cleanup-equivalence` case supplies a passing parse with a removed test and a changed predicate; either difference must prevent a behavior-free verdict. Normalization may remove generated comments/formatting, never predicates or test arguments.
- [x] **Step 6: Define rehearsal outputs.** Brownfield rehearses adding a source, changing a mart, and using the most relevant confirmed procedure or changing a connected intermediate model. Greenfield rehearses the first source. Record files read, files changed/created and commands at mapped verification; confirm current paths or legitimate future patterns. Rehearsal must not execute a production build. Standalone repositories without a verification role retain an equivalent mapped/report destination.
- [ ] **Step 7: Verify behavior and compactness.** Run the inventory/review/sandbox/non-Studio wording probes with five trials per variant, inspect outputs, and run package link/metadata checks. Ensure the main skill remains under 400 words and reports actual commands/results without claiming unavailable runtime success.
- [x] **Step 8: Save the task checkpoint.** Suggested local commit: `docs: complete onboarding setup review and readiness contract`.

### Task 7: Implement only the supported Studio lifecycle

**Files:** Conditionally create `K/references/studio-lifecycle.md`; modify `K/SKILL.md`, `K/references/{artifact-contract,compatibility,studio-duckdb}.md`, `K/templates/skills/git-and-prs.md`, report template, `tests/onboarding/studio-lifecycle.json`, package tests and lifecycle plan/handoff status.

**Interfaces:** Consumes Task 1's current consumer table, Task 2 artifact roles and Tasks 5–6 setup/review outputs. Produces a conditional sequence of supported native Requirement → Design/plan → Build/setup → onboarding review → Verify/certification → authorized shipping. Exact executable entrypoints and certification paths come from the pinned consumer, not invented aliases.

- [x] **Step 1: Evaluate the capability gate.** Supported onboarding kind, supported review, native artifact resolution and understood phase side effects must all be established. Source support permits source-based integration work; actual deployed support and an authorized existing target are additional gates for live acceptance. If source support is missing, record the required companion consumer change and skip dependent implementation; continue Task 8's independent cases.
- [ ] **Step 2: Capture lifecycle baseline failures.** Use `unsupported-consumer`, `artifact-path-conflict`, `early-push-denied`, `partial-ci-hooks`, and `stale-resume`. Assertions: no substitute intent kind, no invented capability, no publication before coverage by authorization, no hook loss, and changed files/tool/data invalidating affected evidence.
- [x] **Step 3: Reconcile this plan with the historical lifecycle plan.** Mark historical capability observations with their date/revision. Use current native artifact paths, including environment-derived roots where required; map/customer conflicts are explicit blockers unless the consumer supports a mapping. Retain L01–L08 and the original standalone path.
- [ ] **Step 4: Add native phase composition.** Keep the shared context workflow small. The conditional reference names the pinned entrypoints, handoff inputs, output artifacts, stop conditions and side effects before each call. Inspect CI installation, verification and shipping for commits/pushes before invoking them. Never invoke a phase that escapes the current authorized scope merely because a later prompt asks for approval.
- [ ] **Step 5: Add resume and result rules.** Reuse valid artifacts only with unchanged covered inputs; preserve review/verification history. A future authorized shipping run creates/reuses one open PR for the current branch/base, verifies remote head and required CI, and keeps failed required CI blocked/draft. No push or PR is performed under this plan's default local scope.
- [ ] **Step 6: Verify available lifecycle gates.** Run bounded treatment probes and package link/invocation checks. Execute real greenfield and brownfield disposable Studio runs only when the consumer/target and every delegated side effect are authorized; capture actual phases, loaded conventions, review, certification, remote SHA/CI if shipping was authorized. Otherwise retain named blocked rows—no simulated result can pass live acceptance.
- [x] **Step 7: Save the task checkpoint or dependency record.** Suggested local commit if implemented: `feat: compose supported Studio onboarding lifecycle`. A blocked Task 7 is not labeled complete; alert with the dependency and continue independent tasks.

### Task 8: Run generated-repository and runtime acceptance

**Files:** Update `tests/onboarding/{cases,reference-refresh,studio-lifecycle}.json`, test expectations only where the contract changed, the execution ledger and `context/onboarding-vibedata-validation.md`.

**Interfaces:** Consumes final task outputs and baseline indexes. Produces per-requirement `pass`, `fail`, `blocked`, or `not applicable` with actual command, input hashes/revision, runtime/dependency versions and reviewed evidence. `not applicable` needs a platform/scope reason; it does not stand in for an unavailable check.

- [x] **Step 1: Run focused deterministic acceptance.** `python -m unittest discover -s tests -p 'test_onboarding*.py' -v` must pass, with integration skips listed separately. Run the enabled Task 5 integration gate once on final affected inputs; rerun only if relevant changes invalidate its evidence.
- [ ] **Step 2: Run actual generated-context cases.** Use fresh disposable copies for dbt/dlt brownfield, Python/notebook brownfield, blank selected-platform greenfield and custom-map/legacy refresh. Run explicit onboarding through installed package routes. Keep app hashes unchanged except authorized scaffold/setup files. Verify the wrapper, metadata, maps, check commands, contained symlinks and lossless ledger.
- [x] **Step 3: Test refresh preservation.** Add a human edit, refresh, verify retained meaning/destination and repaired links, then rerun unchanged and compare all content hashes. Check Claude skill-name collision, custom ADR numbering and native checker ownership. Preserve pending conflicts instead of overwriting files. The 2026-10-17 run retains the human edit, all 18 file hashes on the unchanged rerun, aliases, native ownership and the existing Claude skill; see the run ledger for the exact exercised fixtures.
- [ ] **Step 4: Test ordinary-task loading.** Start new sessions without explicitly invoking onboarding or naming/pasting canonical files. Observe relevant convention loading through `.agents/skills` in Codex and the supported `.claude/skills` route in Claude; verify onboarding itself does not start. Use native metadata validation such as supported `claude plugin validate .claude/skills`, plus PyYAML fixture checks. Record unavailable validation as a gap.
- [ ] **Step 5: Test compaction and later-task routes.** Exercise a supported actual compaction/resume path and observe applicable workaround reload. Run the source/mart/procedure rehearsals from Task 6. A prompt saying “assume compaction happened” is only a wording probe, not this runtime gate. No compaction facility means the runtime gate remains blocked.
- [ ] **Step 6: Complete behavior comparisons.** For each changed wording probe, compare the pinned control/baseline/treatment arms with five trials per variant and inspect every result. Reuse Task 3/6 runs only if their prompt, relevant files and runtime inputs are unchanged. Run existing R14 efficiency comparisons only with correct task outcomes and comparable measurements.
- [x] **Step 7: Record live acceptance separately.** Use Task 7's evidence for supported Studio only. Report context readiness, actual runtime loading, synthetic scaffold execution, live Studio execution and PR/CI outcome as distinct facts. If no target exists, finish all available local acceptance and mark live coverage blocked.
- [x] **Step 8: Save the acceptance checkpoint.** Inspect every failed/flagged result, fix regressions in their owning task with observed RED/GREEN, and keep evidence within budget. Suggested local commit: `test: verify onboarding source alignment and preservation`.

### Task 9: Update release metadata, verify the branch and hand off

**Files:** Modify the three plugin manifests named above; update current design/status documents and append validation evidence; regenerate catalog/README only if changed. Update `docs/handoffs/onboarding-vibedata-studio-lifecycle.md` to point at this plan and actual task state.

**Interfaces:** Consumes Task 8 results and all blockers. Produces a locally reviewable change with matched child versions, a passing root version gate, accurate current/historical evidence, independent review outcome and one restart point for unfinished work.

- [x] **Step 1: Reconcile documentation.** Update R01–R19 terminology/artifact tables to convention skills and the new behavior, preserve their guarantees, and add the S01–S12 acceptance mapping. Keep old command results intact and append current evidence. Reconcile the lifecycle plan/handoff with Task 7's actual status; do not mark the new work complete in the old plan merely because a newer plan exists.
- [x] **Step 2: Select coordinated versions against the current base.** Planning versions are root `1.3.0` and child `1.0.0`; choose the next valid versions after reading current `origin/main`. Bump both child manifests equally and root `.claude-plugin/plugin.json` because `check-plugin-version-bump.py` gates bundled changes through the root version. There is no root Codex manifest to invent. Do not change marketplace catalog metadata version solely for this update; no plugin entry is added.
- [x] **Step 3: Regenerate through the existing tool.** Initialize missing submodules at their existing pins if required for the catalog, with SSH remotes and no pointer changes. Run `python scripts/build_catalog.py`, review its diff, then `python scripts/build_catalog.py --check`. Auth failure blocks the affected operation; do not substitute stale generated content as current.
- [x] **Step 4: Run the local release checks below.** Use the same resolved environment and recorded base SHA. Capture exact failures; do not silently repair unrelated wiki/theme content or relax assertions.

```bash
python scripts/validate-marketplace.py --base-ref origin/main
python scripts/check-plugin-version-bump.py --base-ref origin/main
python scripts/build_catalog.py --check
python -m ruff check scripts tests plugins/vibedata-repo-skills/skills/onboarding-vibedata/scripts
python -m ruff format --check scripts tests plugins/vibedata-repo-skills/skills/onboarding-vibedata/scripts
python -m py_compile scripts/validate-marketplace.py scripts/check-plugin-version-bump.py scripts/build_catalog.py plugins/vibedata-repo-skills/skills/onboarding-vibedata/scripts/inspect_repo.py plugins/vibedata-repo-skills/skills/onboarding-vibedata/scripts/validate_context.py
python -m coverage run -m unittest discover -s tests
python -m coverage report --fail-under=70
git diff --check
```

Generated Python templates must also be rendered, compiled and exercised by `test_onboarding_scaffold.py`; the existing root lint command alone does not cover their rendered output. Run supported Claude plugin validation on `plugins/vibedata-repo-skills` and actual Codex package discovery from Task 8. Preserve the private theme-contract CI check; report it unrun locally if its pinned validator is unavailable. Remote CI has not run without an authorized push.

- [x] **Step 5: Obtain independent whole-change review.** Use `superpowers:requesting-code-review` with the audit, this plan, final diff, current evidence and blockers. Preserve native implementation followed by an independent reviewer. Review preservation, same-database behavior, authorization boundaries, generated CI and all twelve audit groups. Do not review only `SKILL.md` prose. If the required reviewer cannot run, leave that gate blocked rather than call self-review independent review.
- [x] **Step 6: Resolve review findings.** Add a targeted failing check for a real behavior defect, make the smallest fix and rerun affected checks. Do not repeat the whole matrix unless those inputs changed. Record accepted limitations and unresolved findings.
- [x] **Step 7: Finish the local checkpoint.** Check scoped diff/status, source-repository cleanliness relative to preflight, submodule pins and absence of staged secrets/raw evidence. Save/commit allowed files only; suggested message: `chore: finalize onboarding alignment release evidence`.
- [x] **Step 8: Send the overnight handoff.** Report completed/blocked tasks, local commit/diff, current failed/unrun checks, context versus Studio status, retained evidence location and the exact next action. Send the required final Pushover alert. Do not push, open a PR, merge or publish under the default local scope.

## Completion criteria

The local repository alignment is complete only when Tasks 2–6 are implemented, applicable Task 8 local checks pass, Task 9 metadata/documentation checks pass, and independent review findings are resolved or explicitly retained. A current inherited whole-suite failure remains visible and prevents a blanket “all checks pass” statement.

Full Studio parity additionally requires Task 7's supported integration and actual greenfield/brownfield target evidence, including authorized shipping/remote CI where claimed. If that lane is blocked, the correct result is **local alignment complete; Studio lifecycle blocked/unverified**, with the missing consumer release, target or authorization named. Do not mark the whole plan complete while required live acceptance remains outstanding.

## Planning self-review

- All twelve audit groups map to observable requirements, owning tasks and concrete checks.
- R01–R19 preservation requirements and L01–L08 lifecycle conditions remain in force; source-specific contradictions have explicit adaptations.
- Test failures, runtime unavailability and historical evidence are separate. No new API, intent kind or deployed capability is assumed.
- File responsibilities, interfaces, task dependencies, bounded commands, notifications and resume records are defined for unattended execution.
- Execution began on 2026-10-16. Completed steps are checked below; failed or blocked runtime acceptance remains open in the run ledger. The whole plan is not complete.
