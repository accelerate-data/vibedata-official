# onboarding-vibedata implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` for native execution or `superpowers:subagent-driven-development` if the user selects delegated execution. Execute task by task only after this plan is approved. Steps use checkbox syntax for tracking.

**Goal:** Ship one shared `onboarding-vibedata` skill that prepares existing or blank data-engineering repositories for reliable VibeData work with less repeated discovery.
**Architecture:** Package the shared skill, conditional references, templates, and two small portable helpers in `plugins/vibedata-repo-skills/`. Generated instructions route later sessions through repository maps and applicable rules; custom-path compatibility is handled by an explicit tested workaround, with no upstream VibeData edits in this change.
**Tech stack:** Markdown, JSON, Python standard library for customer-facing helpers, existing repository `unittest`/Ruff/coverage/jsonschema tooling, and real Codex/Claude behavioral sessions. The generated greenfield target is dbt/dlt.
**Spec:** [onboarding-vibedata design](onboarding-vibedata-design.md). Read both documents before executing.
**Status:** The original execution is recorded below; the user subsequently authorized draft PR #48, explicit-only invocation, and simpler reporting/verification. The current contract is in design requirements R17–R19. See [validation evidence](onboarding-vibedata-validation.md) for those follow-ups and retained limits: Codex sandbox restrictions leave full onboarding partial, the real VibeData consumer lane is unverified by user direction, and two inherited wiki tests fail; one Codex A16 trial timed out.

**2026-10-16 follow-up:** Execute the approved [source-alignment plan](../docs/superpowers/plans/2026-10-16-onboarding-vibedata-source-alignment.md), with current task states in the [run ledger](onboarding-vibedata-source-alignment-run.md). Its canonical convention skills, generated checks and selected scaffold supersede original template/rules paths below. The original checked tasks/history are retained; they do not establish completion of the new acceptance or Studio lifecycle.

## Contents

- [Global constraints](#global-constraints)
- [Review focus](#review-focus)
- [File responsibilities](#file-responsibilities)
- [Task 1: Establish fixtures and behavioral baselines](#task-1-establish-fixtures-and-behavioral-baselines)
- [Task 2: Implement context inventory and validation](#task-2-implement-context-inventory-and-validation)
- [Task 3: Author the shared skill and templates](#task-3-author-the-shared-skill-and-templates)
- [Task 4: Package for both runtimes](#task-4-package-for-both-runtimes)
- [Task 5: Verify behavior and discovery cost](#task-5-verify-behavior-and-discovery-cost)
- [Task 6: Complete repository verification and handoff](#task-6-complete-repository-verification-and-handoff)
- [Requirement coverage](#requirement-coverage)

## Global constraints

- The skill name and directory name are exactly `onboarding-vibedata`.
- All implementation changes stay in `vibedata-official`; `sample-nyctaxi-comp` and `vibedata-data-engineering` remain read-only references.
- The approved handoff authorizes native implementation and model evaluations in this isolated worktree. Settled design decisions remain unchanged.
- Existing Python scripts/notebooks are discovery inputs. Greenfield creates dbt/dlt, and onboarding does not silently migrate existing application logic.
- Resolve artifact roles through `repo-map.json`; preserve customer names, case, paths, format, numbering, and existing map extensions.
- Preserve every existing instruction or its explicit user-approved replacement. Both-file and only-CLAUDE onboarding consolidate all unique instructions into canonical `AGENTS.md` and replace `CLAUDE.md` with only `@AGENTS.md`.
- Triage conflicts with the user before dependent writes. Apply approved compatibility diffs and verify them; record declined/pending changes and their readiness effect.
- Read application files without executing them during discovery. Never expose secrets, retain notebook outputs, run production loads, or implicitly publish.
- Run behavioral baselines before skill authoring, then use `writing-for-agents` for creation and `writing-skills` for verification.
- Installed platform/library facts must be verified through the approved documentation routes before generating SDK-dependent scaffolds. Auth failures stop the affected operation; do not change data source or model to bypass them.
- Use tiny synthetic fixtures and `tempfile.TemporaryDirectory`/explicit cleanup. Do not copy the reference warehouse or data. If pytest is introduced into a generated project, set `tmp_path_retention_count = 0` and `tmp_path_retention_policy = "failed"`.
- Preserve unrelated work and submodule pointers. Generate catalog/README blocks using the existing generator. No direct-main commits, pushes, PRs, installs into the user's normal runtime, or publication without the applicable authorization.
- Native execution is recommended for this tightly coupled skill change. If delegated execution is selected, implementation agents use `gpt-6-luna` at `high`, reviewers use `gpt-6.1-sol` at `medium`; unavailable selections are reported rather than substituted.

## Review focus

1. Both instruction files contain different mandatory rules, scoped references, imports, and exact duplicates: A06 must prove semantic preservation and prevent a cycle, including symlink aliases and relative-link relocation.
2. A customer chooses `docs/glossary.md` and non-default ADR numbering while an upstream skill names `CONTEXT.md`: A07 must prove actual downstream reads/writes/checks, not merely a valid map.
3. A partial repo has no executable warehouse target or has an unapproved compatibility change: A03/A09 must produce useful context while leaving execution explicitly unverified or blocked.
4. Human-edited artifacts are rerun after a plugin upgrade: A11 must preserve edits and custom extensions and must not rewrite files solely to refresh a timestamp or reorder keys.
5. Installed plugin paths, caller working directories, or filename casing differ: A05/A13/A14 must prove bootstrap loading, skill-relative helper resolution, containment, and a clear failure instead of writing to the wrong directory.

## File responsibilities

Paths below are relative to the implementation worktree; listed files are proposed unless already present.
Use `P = plugins/vibedata-repo-skills` and `S = plugins/vibedata-repo-skills/skills/onboarding-vibedata` only as abbreviations in this plan, not literal shell variables.

| Files | Responsibility |
| --- | --- |
| `S/SKILL.md` | Shared invocation conditions, workflow, approvals, routing, and completion criteria. |
| `S/references/{brownfield,greenfield,artifact-contract,compatibility,studio-duckdb}.md` | Branch-specific discovery/setup, artifact/preservation requirements, conditional runtime/path workarounds and selected Studio/DuckDB readiness. |
| `S/templates/{agents,glossary,adr-index,onboarding-report,review,proposal}.md` | Minimal documents and evidence tables; existing documents are reconciled rather than overwritten from these. Review/proposal outputs require actual findings or decisions. |
| `S/templates/rules/{dbt-models,sql-style,dbt-testing,dlt,python,context,adr,design-records,git-and-prs,workarounds}.md` | Scoped defaults; emit only applicable content, using selected paths and confirmed overrides. |
| `S/templates/{repo-map.schema,repo-map,test-map}.json` | Shared structural contract and honest empty-scaffold examples. |
| `S/templates/greenfield/README.md` | Exact selected-platform scaffold recipe and template placement; records source/model templates as templates, not active assets. |
| `S/scripts/inspect_repo.py` | Read-only mechanical inventory in one call. |
| `S/scripts/validate_context.py` | Portable read-only structural checker, also usable in a generated repo's `.agents/checks/`. |
| `tests/test_onboarding_context.py`, `tests/test_onboarding_package.py` | Deterministic fixture/helper/template and packaging regression tests. |
| `tests/fixtures/onboarding/` | Tiny human-style dbt/dlt, Python/notebook, blank, custom-path, and conflicting-instruction estates. |
| `tests/onboarding/cases.json` | Behavioral scenario contracts A01–A16; no hidden implementation-specific answer key is installed in a customer fixture. |
| `tests/onboarding/reference-refresh.json` | Read-only reference-refresh probes for native contracts, Studio readiness and a non-Studio counterexample; separate from live consumer acceptance. |
| `context/onboarding-vibedata-validation.md` | Baseline and final evidence, commands/settings, preservation results, efficiency comparison, and blockers. Created only during implementation. |
| `P/.claude-plugin/plugin.json`, `P/.codex-plugin/plugin.json` | Runtime packaging for the single shared source. |
| Existing marketplace manifests, root plugin manifest, `AGENTS.md`, and `.github/workflows/ci.yml` | Registration/versioning, correction of the Codex manifest convention, and helper checks. |
| Existing `catalog/` and generated README blocks | Generator-owned distribution inventory. |

## Task 1: Establish fixtures and behavioral baselines

**Requirements:** R01–R16 through cases A01–A16; this task establishes evidence, not implementation.
**Files:** Create `tests/onboarding/cases.json`, `tests/fixtures/onboarding/`, and `context/onboarding-vibedata-validation.md`.
**Interfaces:** Each case has `id`, `requirements`, `fixture`, `prompt`, `allowed_writes`, and `assertions`. Results record case/arm/trial, runtime/version/model/settings, fixture revision, artifact diff, observed behavior, tool counts, and readiness outcome.

- [x] Verify the implementation checkout is isolated and on the intended non-default branch; record its base revision and clean/dirty state without touching unrelated files.
- [x] Read the named authoring skills and their relevant mechanics/testing references. Obtain the installed Claude/Codex invocation and isolated-session options from current approved docs and CLI help; record the exact commands before using them.
- [x] Create minimal fixture files for dbt/dlt, Python plus one `.ipynb`, and a blank repository, with no credentials, data downloads, notebook outputs, or production targets.
- [x] Add variants for all four instruction-file states, custom glossary/ADR locations, conflicting rules, partial onboarding, and a human edit after onboarding; include unique behavioral instructions so losing one can be observed.
- [x] Define the A01–A16 prompts and outcome assertions from the design, including both approval outcomes and a pending decision. Define the exact follow-on prompts used for efficiency comparisons.
- [x] Run the same onboarding/task prompts without the new skill in fresh Codex and Claude contexts. Keep the normal supported tooling but ensure the skill is absent; do not inject the reference skill's instructions into the control prompt.
- [x] Record observed failures and successful baseline behavior verbatim where needed, with artifact effects and counts. Do not invent a failure when the control already succeeds; identify which parts actually require guidance before authoring them.
- [x] Preserve matched controls for A15's five trials per task/runtime and establish the small evidence-retention policy. Auth/runtime failure blocks that lane and is not a substituted-runtime pass.

**Gate:** Each required case has a runnable scenario, explicit outcome checks, and baseline evidence or a named environment blocker. No skill body has been authored yet. Confirm the baseline contains meaningful failures before adding guidance aimed at those failures.

## Task 2: Implement context inventory and validation

**Requirements:** R02, R04, R05, R10–R12; cases A01/A02/A05/A06/A11/A13/A16.
**Files:** Create the two `S/scripts/` helpers and `tests/test_onboarding_context.py`; extend the fixtures from Task 1.
**Interfaces:**

- `inspect_repository(root: Path) -> dict[str, object]` in `inspect_repo.py`; keys are `mode` (`brownfield`, `greenfield`, or `ambiguous`), `instruction_files`, `config_files`, `code_files`, and `existing_artifacts`. Return paths and structural facts only, not secret contents or notebook cells/outputs.
- CLI: `python3 S/scripts/inspect_repo.py --root <repository>` writes one JSON object to stdout, exits zero on a complete inventory, and exits nonzero with an actionable error on malformed/unreadable inputs. The notation `S` must be replaced with the installed absolute skill path in actual commands.
- `validate_context(root: Path) -> list[str]` in `validate_context.py`; an empty list means structural success. CLI `python3 S/scripts/validate_context.py --root <repository>` prints findings and exits nonzero when any check fails. It does not execute commands from either map.

- [x] Write `test_inspection_does_not_execute_or_disclose` using a script that would leave a marker, a notebook with an output sentinel, and secret-bearing files; assert the marker is absent and the returned JSON contains none of their contents.
- [x] Write `test_inspection_preserves_python_estate` and `test_instruction_only_repo_is_greenfield`; assert existing Python paths are inventoried without a fake dlt classification, and an instructions-only repo remains greenfield.
- [x] Write `test_context_resolves_custom_paths_and_patterns`, `test_context_rejects_missing_registered_artifact`, and `test_empty_inventory_has_no_fake_coverage`; assert custom ADR numbering is preserved, future patterns may have absent directories, and valid empty inventories pass while actual missing artifacts fail.
- [x] Write `test_context_rejects_escape_and_cycles` with path traversal, external symlink, cyclic instruction imports, and same-file aliases; assert actionable findings without reading or writing outside the fixture.
- [x] Write `test_wrapper_and_moved_links_preserve_targets` and `test_validation_is_read_only`; assert resolved targets and hashes remain correct and all fixture bytes are unchanged after validation.
- [x] Run `python3 -m unittest discover -s tests -p 'test_onboarding_context.py' -v` and record the meaningful red result before implementing the helpers.
- [x] Implement the interfaces using the standard library and the repository's tracked/unignored file inventory. Exclude generated/vendor/data trees; parse notebooks only as JSON metadata for detection, never execute them.
- [x] Run the same focused test command and record green. Run `python3 -m ruff check plugins/vibedata-repo-skills/skills/onboarding-vibedata/scripts tests/test_onboarding_context.py` and the corresponding `ruff format --check` command.

**Gate:** Helpers are portable, bounded, read-only, and pass the focused tests. Schema conformance tests may reuse the repository's installed `jsonschema`; copied customer checks must not require it. Structural success must not be reported as runtime instruction-loading success.

## Task 3: Author the shared skill and templates

**Requirements:** R01–R11, R13, R16; all artifact/approval cases.
**Files:** Create `S/SKILL.md`, its four references, and the templates in the responsibility table. Extend `tests/test_onboarding_context.py` and create `tests/test_onboarding_package.py`.
**Interfaces:** The skill consumes Task 2's inventory and helper results, produces the design's mapped artifacts plus onboarding report, and routes every vocabulary/ADR operation through the custom-path workaround when necessary.

- [x] Add failing template/package tests for the exact skill name, resolvable supporting references, valid map examples, conditional template selection, and absence of NYC Taxi-specific paths/schema/key names in generic defaults.
- [x] Run `python3 -m unittest discover -s tests -p 'test_onboarding_*.py' -v` and record red before creating the missing deliverables.
- [x] Author the shared steps with `writing-for-agents`: inspect, reconcile, propose, apply, verify. Give every step a checkable completion criterion and use explicit pointers for the branches that need extra reference material.
- [x] Author brownfield rules for evidence, Python/notebook discovery, preservation, partial onboarding, and three-state compatibility decisions (`approved`, `declined`, `pending`). Specify the lossless instruction ledger and conflict table in the onboarding-report template.
- [x] Author the artifact schema/templates and routing rules, including custom path overrides in emitted validation commands and the removal condition for each workaround. Keep unknown existing map fields and already established formats; generate review/proposal documents only for real findings or substantive decisions.
- [x] Author the greenfield recipe for dbt/dlt. Verify current package/adapter initialization from approved documentation, parameterize by the confirmed platform, and use the proposed folder/package defaults only when the user has no existing convention.
- [x] Supply starter source/pipeline/model templates through the recipe without registering fictitious live sources. Register only actual scaffold checks; explain unmet environment requirements instead of asserting an empty build is execution proof.
- [x] Register the copied context checker or preserve a suitable existing one, and define the maintenance trigger for each map/rule/vocabulary artifact. Include the standard pytest retention configuration when generating a pytest project.
- [x] Run the focused tests and review the resulting skill with the `writing-for-agents` criteria. Check that the main skill loads only the selected branch and that preservation instructions retain scope and working links.

**Gate:** Authoring is complete, templates validate, and every R01–R13 requirement has an explicit procedure or conditional reference. Baseline failures have corresponding guidance; unrelated generic instructions have not been added merely to enlarge the skill.

## Task 4: Package for both runtimes

**Requirements:** R01, R15; A14.
**Files:** Create both `P` plugin manifests; modify `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`, `.claude-plugin/plugin.json`, `AGENTS.md`, `.github/workflows/ci.yml`, and `tests/test_onboarding_package.py`. Regenerate `catalog/` and the README generated blocks.
**Interfaces:** Both manifests name `vibedata-repo-skills`, share the same initial plugin version, and resolve the one `skills/` tree. The catalog contains exactly one `onboarding-vibedata` skill entry associated with that plugin.

- [x] Add failing tests for manifest identity/version parity, registered local paths, allowed license, one skill source, and catalog discovery. Reuse the existing marketplace/catalog tests and helpers rather than creating another registry validator.
- [x] Run `python3 -m unittest discover -s tests -p 'test_onboarding_package.py' -v` and record red.
- [x] Verify current official Claude/Codex packaging and choose the supported existing dual-manifest layout. Correct only the target's inaccurate blanket prohibition on the Codex `skills` field; avoid a wider format migration.
- [x] Add the manifests and alphabetically ordered entries with `Elastic-2.0`; preserve all existing plugins and submodule pointers. Increase the marketplace catalog version for the new entry and the root plugin version as required by the existing gate, based on current values rather than a stale planned number.
- [x] Extend existing CI Ruff/format/compile checks to the two new shipped helpers and any maintained Python template code; retain existing tests and coverage requirements.
- [x] Initialize the pinned catalog submodules in the isolated worktree if necessary, without updating their revisions, then run `python3 scripts/build_catalog.py`.
- [x] Run `python3 scripts/build_catalog.py --check`, `python3 scripts/validate-marketplace.py --base-ref origin/main`, and `python3 scripts/check-plugin-version-bump.py --base-ref origin/main` after the new files are tracked in the implementation branch; untracked files alone are not valid version-gate evidence.
- [x] Run `claude plugin validate ./plugins/vibedata-repo-skills` and test discovery in disposable runtime settings using the verified Codex installation mechanism. Do not install into the operator's normal profile merely to test packaging.

**Gate:** Both installed runtimes discover the same skill and relative references, all deterministic packaging checks pass, and no generated catalog content was hand-edited.

## Task 5: Verify behavior and discovery cost

**Requirements:** R01–R16; A01–A16.
**Files:** Update `context/onboarding-vibedata-validation.md` and only the skill/helper/template/test files needed to correct observed failures.
**Interfaces:** Reuse Task 1's case and evidence fields. The comparison has matched baseline and skill-enabled arms; no case passes solely because the expected filename appears in a transcript.

- [x] Run the `writing-skills` verification pass in fresh Codex and Claude sessions with the packaged skill. Hold fixture, prompt, runtime/model/settings, and allowed tools constant between matched arms.
- [x] Exercise all instruction ownership cases, including only-CLAUDE migration into canonical `AGENTS.md` with a reference-only `CLAUDE.md` containing `@AGENTS.md`. Let the runtime load instructions normally; do not paste canonical content into the prompt or tell the task to open a particular hidden file to manufacture success.
- [x] Check semantic preservation against the original instruction ledger and the resulting behavior. Test both conflicting and compatible scoped rules; verify the original content is secured before the placeholder replaces it.
- [x] Exercise approved, declined, and pending compatibility changes. Confirm declined/pending diffs are absent, follow-ups retain evidence and readiness effects, and independent artifact work can still complete.
- [ ] Run A07 with a real VibeData consumer in a disposable environment, using the mapped glossary/ADR locations and applicable workaround. Record actual file reads/writes and emitted checks. If a tool hardcodes a path or the environment is unavailable, record the failure/blocker and follow-up; do not edit the upstream consumer repository or claim full compatibility.
- [x] Exercise reruns after human edits and an unchanged rerun; compare complete artifact diffs and confirm no timestamp-only churn or duplicate default documents.
- [x] Run five matched A15 trials per selected follow-on task and runtime; calculate median discovery tool calls and content read when measurable. Preserve the correctness verdict per run, then report improvements, ties, regressions, and unavailable metrics separately.
- [x] Inspect every failed outcome, correct the owning instruction/helper/template, and rerun affected cases. Follow `writing-skills` micro-testing guidance for ambiguous behavior-shaping wording before repeating expensive full scenarios.

**Gate:** Every claimed capability has behavioral evidence on its relevant runtime. Unavailable or failed lanes remain visibly unverified. Report repository context readiness and execution verification separately; do not label the whole integration complete if A07's VibeData lane is still unverified.

## Task 6: Complete repository verification and handoff

**Requirements:** R12–R16 and scope boundaries.
**Files:** Finalize the validation report and review only changes already in scope.
**Interfaces:** Deliver the plugin diff, requirement-to-evidence results, remaining follow-ups, and exact unrun checks.

- [x] Run `python3 -m unittest discover -s tests -v` and the existing coverage command `python3 -m coverage run -m unittest discover -s tests`, followed by `python3 -m coverage report --fail-under=70`.
- [x] Run `python3 -m ruff check scripts tests plugins/vibedata-repo-skills/skills/onboarding-vibedata/scripts` and `python3 -m ruff format --check scripts tests plugins/vibedata-repo-skills/skills/onboarding-vibedata/scripts`.
- [x] Run the existing marketplace/version/catalog checks at the final tracked revision and inspect `git diff --check`. Reuse prior gate results only when their covered inputs have not changed.
- [x] Verify that both reference checkouts remain unchanged by this work and that target submodule pointers and unrelated files are unchanged.
- [x] Review the complete diff for requirement coverage and scope. Record any live CI-only checks that require external credentials instead of presenting local checks as remote CI evidence.
- [x] Present the local implementation, validation report, and follow-ups. Do not push, publish, or open a PR unless the user has authorized that next boundary.

**Gate:** The user can review exactly what was built, why it is correct, and what remains unverified. This plan does not authorize its own execution or publication.

## Requirement coverage

| Requirement | Implementing task(s) | Acceptance evidence |
| --- | --- | --- |
| R01 | 3, 4, 5 | A05, A14 and the Codex/Claude matrix. |
| R02 | 2, 3, 5 | A01, A02, A16. |
| R03 | 3, 5 | A03 and selected-platform scaffold checks. |
| R04 | 2, 3, 5 | A07, A13. |
| R05 | 2, 3, 5 | A04, A05, A06, A13. |
| R06 | 3, 5 | A05, A06, A08. |
| R07 | 3, 5 | A09, A16. |
| R08 | 3, 5 | A07, A12. |
| R09 | 3, 5 | A03, A10. |
| R10 | 2, 3, 5 | A11. |
| R11 | 2, 3, 5 | A02, A16. |
| R12 | 2, 3, 6 | A01, A03, A13 and structural/CI gates. |
| R13 | 3, 5, 6 | A09 and explicit context/execution readiness results. |
| R14 | 1, 5 | A15's matched fresh-session evidence. |
| R15 | 4, 6 | A14 and marketplace/version/catalog gates. |
| R16 | 1, 3, 5 | Baseline record, authoring review, and `writing-skills` verification. |

The user has requested execution in a new session with the revised instruction-ownership rule. Use native execution unless the user selects delegated execution.
Execution produced the local plugin diff and validation report. Checked steps mean the action ran and its outcome is recorded, not that every runtime assertion passed. The A07 consumer step remains unchecked because the user confirmed no test environment and requested an unverified result. R16 has a chronology deviation: Claude controls preceded authoring; Codex controls followed initial authoring after correction of the login-status diagnosis. Full Codex onboarding remains partial under the test sandbox. The final full suite retains two inherited wiki failures.
