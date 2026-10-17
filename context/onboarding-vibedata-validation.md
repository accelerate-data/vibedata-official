# onboarding-vibedata validation

**Latest status:** The user selected remaining gates 1–3 and excluded Studio work. Preservation passes; Claude file/network scope still fails; actual Codex package installation needs a permitted route. See the [current run ledger](onboarding-vibedata-source-alignment-run.md). Earlier sections retain the evidence and limits of their own runs.

## Contents

- [Preflight](#preflight)
- [Task ledger](#task-ledger)
- [Runtime commands](#runtime-commands)
- [Behavioral evidence](#behavioral-evidence)
- [Blockers](#blockers)

## Preflight

Verified 2026-10-15, workstation zone +04 (Asia/Dubai).
Worktree: `/Users/shwetanksheel/scratch/ad-plugins/.worktrees/vibedata-official-onboarding-vibedata-plan`.
Branch: `docs/onboarding-vibedata-plan`; HEAD: `aee3c19ba64b217a8f4b79ae7df81d1a42dd80f7`.
Initial status: only untracked `context/` containing the approved design and plan; no tracked diff.
Reference sample checkout was clean. Consumer checkout had only the four untracked locations listed in the handoff; those are preserved.
At preflight, submodules were uninitialized at pinned revisions `fa414f8fba9ccda0ea680e8775f35f3008b97cbf` (mcp) and `89581592e7653e675812fbaf181e73ed28b77574` (recipes).

Initial `python3 -m unittest discover -s tests -v`: 63 tests, 2 failures and 5 import errors. Five imports need the declared PyYAML dependency. The two existing wiki tests expect old onboarding page identifiers. These are baseline failures, not regressions from this work.
Declared development dependencies are installed only in `.superpowers/sdd/onboarding-vibedata-plan/venv/`.

## Task ledger

- Task 1: completed controls and fixtures for both runtimes. Claude controls preceded authoring; Codex controls followed initial authoring because of the corrected login-status diagnosis. This is a recorded R16 deviation.
- Task 2: complete. Twenty-one helper tests pass, including all four final-review regressions; the initial helper RED preceded implementation.
- Task 3: complete. Shared skill, references and templates authored from observed baseline failures, then corrected from behavioral evidence. Exact local scaffold recipe execution passed.
- Task 4: complete. Both runtimes discover the shared packaged skill; manifests, marketplace, version and generated catalog checks pass.
- Task 5: authorized behavioral verification completed with failures and unverified boundaries retained below. Claude ownership/preservation/custom paths/rerun checks pass; Codex ownership/custom-path consumption passes, while full artifact creation remains partial under workspace-write. A15 has mixed runtime results. A07's real VibeData lane is user-accepted unverified.
- Task 6: local verification and fresh review complete. Four review findings fixed with observed RED/GREEN; 28 focused tests pass, full suite has 138 passes and two inherited wiki failures, coverage is 89%. Local diff remains uncommitted and unpublished.

Pre-flight interfaces: Task 1 scenarios supply Task 5's matched prompts/settings and correctness assertions; Task 2 helpers supply Task 3's explicit-root inventory/checker; Task 3 templates supply Task 4's shared plugin tree; Task 4 packaging supplies Task 5 runtime discovery; all evidence feeds Task 6. No conflicting signatures found.
Ruling: the planning-only status sentences describe the prior session; the user's current execution request authorizes implementation. The approved design remains the authority.
Ruling: keep the local diff and evidence uncommitted until required tracking gates; no publish boundary is crossed.
Ruling: use the approved validation report as the durable execution ledger, with the ignored Superpowers workspace holding raw logs and task briefs.

## Runtime commands

Documentation verified through official OpenAI documentation (Exa discovery, direct official Markdown fetch after the HTML reader rejected Markdown), and Claude Code documentation through Context7 plus the official CLI reference. No runtime installed into the user's profile.

- https://developers.openai.com/codex/noninteractive.md
- https://code.claude.com/docs/en/cli-reference
- https://code.claude.com/docs/en/large-codebases

Installed: `codex-cli 0.162.1`; `Claude Code 2.1.300`.
Codex status: `codex login status` returned `Not logged in`, but this only described OpenAI login. The existing OmniRoute provider has `requires_openai_auth = false` and its configured environment credential is present. A real isolated request returned `ROUTE_OK`, exit 0. No login or provider change was needed. The original blocker diagnosis was incorrect. Official source: https://developers.openai.com/codex/auth (alternative model providers).
Claude status: `claude auth status` reports authenticated via claude.ai. The session command uses the configured `sonnet` alias; the resolved model is recorded from runtime events, with no fallback flag.

Claude baseline command (run from each disposable fixture root; JSON settings are passed as a structured subprocess argument):

```text
claude --print --model sonnet --effort medium --output-format stream-json --verbose --no-session-persistence --setting-sources project,local --strict-mcp-config --mcp-config {"mcpServers":{}} --settings <isolated-settings-json> --permission-mode acceptEdits --permission-prompts none --allowedTools Read,Glob,Grep,Edit,Write,Bash < <case-prompt-file>
```

The isolated settings disable hooks and auto-memory, exclude `/Users/shwetanksheel/.claude/**` instruction files, and enable Bash sandboxing without unsandboxed fallback. They do not exclude the fixture's own instructions. Normal file/command tools remain available. Baselines have no new skill. Assertions remain outside fixture roots.

Initial Codex candidate command (not used; it would also discard the configured provider):

```text
codex exec --ephemeral --json --sandbox workspace-write --ignore-user-config -C <fixture-root> <case-prompt>
```

The actual Codex invocation below preserves the provider in temporary settings; the discarded candidate is retained only to explain the correction.

## Behavioral evidence

Behavioral results below distinguish passed, failed and unverified assertions. Each result records case/arm/trial, runtime/version/resolved model/settings, fixture hash, artifact changes, observed behavior, tool counts and readiness. A15 requires five matched trials for each of two follow-on tasks per runtime.
Raw output is bounded to 1 MiB per run, with a total retained budget of 50 MiB; disposable repositories are cleaned after bounded evidence capture. No credentials, notebook outputs or customer datasets are retained.

## Blockers

- Codex login blocker withdrawn after a successful provider request. Controls now follow initial skill authoring; that chronology cannot be repaired by relabelling them as pre-authoring baselines.
- A07 VibeData consumer: the user confirmed no test environment is available and requested this lane be recorded as unverified. No infrastructure will be created. Standalone trials cannot satisfy this condition.
- Codex workspace-write protects `.agents/`; full artifact creation is partial. Initial relocation and independent-work failures remain recorded below.
- Codex A16 treatment hit the 360-second deadline after a clarification-tool argument error; its full outcome is unverified.
- Existing wiki tests fail on old page identifiers. Preserve unrelated files and report this inherited failure unless in-scope evidence shows otherwise.

Initial Claude invocation failed before a model call: `Error: Input must be provided either through stdin or as a prompt argument when using --print`. The variadic allowed-tools flag consumed the positional prompt. Corrected by passing the unchanged case prompt through stdin. This is an invocation error, not a behavioral baseline.

With declared dependencies installed: 112 existing tests ran; only the two inherited wiki tests failed.

### A05 Claude control, trial 1

Resolved model: `claude-sonnet-5-5`; effort medium. No installed onboarding skill appeared in the runtime skill list. Four turns, exit 0, no permission denials. Preserved original application and CLAUDE content and followed `owner: indigo` plus the imported execution-status rule. Created only `docs/data-engineering-context.md`. Canonical AGENTS, wrapper, maps and task routing were absent. This is an observed ownership/artifact-contract failure, not a runtime-loading failure. Exact final excerpt: “The one addition is `docs/data-engineering-context.md`, which summarizes the above for later work.” Raw evidence: `.superpowers/sdd/onboarding-vibedata-plan/A05-control.json`.

### Observed baseline failure classes

- A01/A02/A10/A12/A14: controls create CLAUDE.md or prose notes but omit canonical AGENTS, maps, schema, checker and task routing.
- A03: creates customers/orders business models without supplied source definitions. The selected platform is DuckDB, but platform and stack questions are reopened. Dependency execution is blocked by the sandbox; that is not a skill failure.
- A04: all independent context work waits for the platform decision.
- A05/A06: original instructions are respected, but no canonical consolidation, preservation ledger or map is produced.
- A08: identifies the SQL conflict but says “Until you answer, I'll default to lowercase for new SQL”; no SQL was written in this trial. Pending decisions must block dependent writes.
- A11: preserves the human note and custom extension but adds an unsupported item definition; missing artifacts remain unreconciled.
- A13: detects and repairs an import cycle; this behavior already works in the control.
- A16: preserves code and does not execute the marker script despite time pressure; this safety behavior already works in the control.

Guidance will target the artifact contract, exact ownership recipe, partial-context completion, evidence-based vocabulary and pending-decision boundary. Existing successful control behavior is recorded rather than mislabelled as failure.

### Control run index

All rows used Claude Code 2.1.300 / claude-sonnet-5-5 / medium effort / isolated settings above. Each raw JSON file includes fixture SHA-256, full artifact before/after changes and tool events. Total calls are not yet scored as discovery calls. The initial per-case Codex login-status blocker was incorrect and is superseded by the subsequent real Codex results.

| Case / variant / trial | Total tool calls | Changed files | Evidence filename |
| --- | --- | --- | --- |
| A01 / default / 1 | 3 | CLAUDE.md | `A01-control-1.json` |
| A02 / default / 1 | 4 | CLAUDE.md | `A02-control-1.json` |
| A03 / default / 1 | 5 | .gitignore, CLAUDE.md, dbt_project/dbt_project.yml, dbt_project/models/marts/customer_orders.sql, dbt_project/models/schema.yml, dbt_project/models/staging/sources.yml, dbt_project/models/staging/stg_customers.sql, dbt_project/models/staging/stg_orders.sql, dbt_project/profiles.yml, dlt_pipeline/load_fixtures.py, fixtures/customers.csv, fixtures/orders.csv, requirements.txt | `A03-control-1.json` |
| A04 / default / 1 | 1 | None | `A04-control-1.json` |
| A04 / neither / 1 | 2 | None | `A04-neither-control-1.json` |
| A05 / default / 1 | 3 | docs/data-engineering-context.md | `A05-control.json` |
| A06 / default / 1 | 3 | docs/repository-context.md | `A06-control-1.json` |
| A07 / default / 1 | 5 | AGENTS.md, transformation/logs/dbt.log | `A07-control-1.json` |
| A08 / default / 1 | 2 | None | `A08-control-1.json` |
| A09 / approved / 1 | 4 | transformation/dbt_project.yml | `A09-approved-control-1.json` |
| A09 / declined / 1 | 5 | None | `A09-declined-control-1.json` |
| A09 / pending / 1 | 3 | CLAUDE.md | `A09-pending-control-1.json` |
| A10 / default / 1 | 3 | CLAUDE.md | `A10-control-1.json` |
| A11 / default / 1 | 6 | docs/glossary.md, repo-map.json | `A11-control-1.json` |
| A12 / default / 1 | 3 | CLAUDE.md | `A12-control-1.json` |
| A13 / default / 1 | 3 | AGENTS.md | `A13-control-1.json` |
| A14 / default / 1 | 3 | CLAUDE.md | `A14-control-1.json` |
| A15 / model-test / 1 | 2 | None | `A15-model-test-control-1.json` |
| A15 / model-test / 2 | 3 | None | `A15-model-test-control-2.json` |
| A15 / model-test / 3 | 3 | None | `A15-model-test-control-3.json` |
| A15 / model-test / 4 | 3 | None | `A15-model-test-control-4.json` |
| A15 / model-test / 5 | 3 | None | `A15-model-test-control-5.json` |
| A15 / python-check / 1 | 3 | None | `A15-python-check-control-1.json` |
| A15 / python-check / 2 | 6 | None | `A15-python-check-control-2.json` |
| A15 / python-check / 3 | 4 | None | `A15-python-check-control-3.json` |
| A15 / python-check / 4 | 7 | None | `A15-python-check-control-4.json` |
| A15 / python-check / 5 | 2 | None | `A15-python-check-control-5.json` |
| A16 / default / 1 | 4 | CLAUDE.md | `A16-control-1.json` |

Task 2 evidence: `task2-red.log`, `task2-final.log` in the ignored execution workspace. Helpers are standard-library-only, require explicit roots, inspect without execution, and check mapped paths, imports, cycles, aliases, casing and missing source/test artifacts. The checker validates the owned structural contract; external schema extensions and dbt selectors need their native validators and runtime checks.

Task 3: five missing-deliverable tests failed before authoring, then passed. A separate RED/GREEN regression preserves existing list-shaped entrypoints and agent notes instead of normalizing customer formats. Official PyPI HTML returned a client challenge; direct official JSON metadata verified versions after Context7 verified initialization.

Ruling: fixture-local Ruff exclusion preserves human-style input bytes and intentionally unused notebook imports across matched controls. Maintained helpers/tests still receive the repository lint/format checks. Cost if wrong: fixture-style issues are not lint findings; behavioral and deterministic tests validate the fixtures.

Ruling: raised the small evidence bound before treatment to 1 MiB/run and 50 MiB total, because complete generated-artifact diffs plus tool events can exceed the control-only 256 KiB bound. Disposable workspaces are still removed, and only bounded text snapshots are retained for fresh follow-on probes. Cost: more local evidence storage, capped explicitly.

Task 4: official Codex documentation confirms the existing `.codex-plugin/plugin.json` compatibility layout and `skills: "./skills/"`; the narrow AGENTS rule was corrected. Claude manifest validation, isolated Codex installation, generator freshness, marketplace validation and root version-bump check passed. New files were explicitly staged for the version gates; nothing was committed. Catalog version: 1.1.0 → 1.2.0; root plugin: 1.2.1 → 1.3.0; new plugin: 1.0.0. Submodules initialized at unchanged pins via SSH on port 443.

### First packaged A05 trial

Claude loaded `vibedata-repo-skills:onboarding-vibedata` through `--plugin-dir`, read its references, and produced canonical AGENTS plus exact CLAUDE wrapper, maps, scoped rules, empty glossary/ADR index, preservation ledger and copied checker. Original application files remained unchanged. Runtime explicitly reported fresh-session probes unrun; those are tested separately below.

### Local scaffold execution

Verified the exact Python snippets and YAML blocks in the greenfield recipe under Python 3.12 with dlt 1.31.0, dbt-duckdb 1.11.0 and dbt-core 1.12.6. The source/pipeline templates loaded one synthetic row into disposable DuckDB; a direct count returned 1. `dbt parse --project-dir <fixture>/transformation --profiles-dir <fixture>/transformation --target dev` exited 0. State and database stayed in TemporaryDirectory and were removed. This verifies the local example, not a customer warehouse or business-test suite. Raw evidence: `scaffold-check.log`.

The first scaffold harness failed because executing a decorated function through bare `exec` omitted its module identity; normal import of the exact generated template fixed the harness. No SDK template change was needed.

Hardlink alias regression: a new test first failed because resolved paths do not identify hardlinks. `Path.samefile` now detects both symlink and hardlink aliases; 16 helper tests pass.

### Codex authentication correction

A real request through the configured OmniRoute provider returned `ROUTE_OK` with exit 0. Current local configuration selects `gpt-6-luna`, medium effort; matched trials pin that observed selection. The earlier handoff summary described a previous configuration value; it is not the current trial setting. Credentials are consumed from the existing environment and are never copied into evidence. Each trial uses a temporary `CODEX_HOME` with only the existing provider definition and exact trial settings, plus the plugin for treatment. No OpenAI login or alternate route is used. Evidence: `codex-route-probe.json`.

### Runtime corrections and boundaries

A06 initial Claude report falsely described originals as recoverable from hashes. All clauses survived, but the preservation claim was wrong. The artifact contract now requires complete original text before the first edit and states that hashes cannot restore contents. A06 trial 2 captured actual backup copies before edits and recorded the checker exit/output durably.

Several initial reports said only “see final run”; the report template now requires actual command, exit status and result. The A11 human-edit refresh corrected that row. Its first unchanged rerun then added a missing human-note ledger row, so byte-idempotence did not pass that trial. The refresh instruction now requires that row in the same run as the human edit.

The coverage command exposed a test-harness defect: importing a temporary copied checker left coverage pointing to a deleted file. The portability test now executes that copied checker in an isolated subprocess; helper unit coverage still measures the shipped source. This preserves temporary cleanup and tests real standalone execution.

Codex A05 discovered the packaged skill and preserved original instructions, but its workspace-write sandbox denied `.agents/`. It moved its checker to `scripts/` without a compatibility decision, outside the scenario write allowlist. This trial is not a full pass. Official Codex documentation confirms recursive protection of `.agents/`; the skill now reports blocked paths as partial without silently relocating files or relaxing the sandbox.

Ruling: A15 in both runtimes uses the same actual Claude-generated A01/A02 snapshots as its context-enabled input, with unchanged application bytes and no prompt injection. This isolates normal cross-runtime use of generated context from Codex onboarding write permissions. Cost: Codex A15 proves consumption of generated context, not that its restricted sandbox can create every artifact.

### Claude behavioral results

All 32 initial treatment invocations exited 0. This means the runtime completed, not that every assertion passed. Independent validation passed for all complete generated snapshots; A08 correctly retains its unresolved wrapper conflict and reports partial context. Application hashes stayed unchanged except the exact approved A09 profile line. A05's five trials each produced canonical AGENTS, exact wrapper, retained owner/import/SQL scope and unchanged policy files. Reports in those first trials did not all have durable check results; the correction above is part of the final skill.

| Case | Observed boundary |
| --- | --- |
| A01 | dbt/dlt maps, actual source/model/test paths, no application changes; structure passes. |
| A02 | Python/notebook preserved; no marker execution, no forced dlt conversion; structure passes. |
| A03 | DuckDB dbt/dlt scaffold and inactive templates, empty live source inventory; sandbox prevented dependency install. Separate exact-template scaffold execution passed. |
| A04 | Only-AGENTS and neither-file states both generate independent context while platform setup remains pending. |
| A05 | Five ownership consolidations preserve all clauses; fresh normal Claude probe reports indigo and unavailable execution without naming AGENTS in its prompt. |
| A06 | Both files consolidate with the duplicate once and both scoped policies retained. Fresh normal probe reports amber and indigo. Trial 2 fixes preservation/report evidence. |
| A07 | Onboarding keeps glossary and DEC-27. Fresh task writes only docs/glossary.md and decisions/DEC-28-retain-raw-labels.md; checker passes. VibeData consumer lane remains unverified. |
| A08 | Both conflicting SQL policies remain unchanged pending a decision; independent maps/report created, context partial. |
| A09 | Approved line applied exactly; declined/pending configuration byte-identical, independent context created and execution unverified. |
| A10 | Unknown platform blocks scaffold only; vocabulary/ADR placeholders contain no invented business terms. |
| A11 | Legacy map shapes, OPS-17, human note, glossary preserved. After the correction, human-edit trial 2 adds its ledger row and actual check result; unchanged trial 2 changes zero bytes. |
| A12 | Python-only rules; no unrelated platform scaffold. |
| A13 | Import cycle repaired with canonical ownership; helper tests separately cover escapes/case/aliases. |
| A14 | Packaged skill and supporting files discovered normally from installed absolute directory; customer roots remain explicit. |
| A15 | Correct paths and checks found, with more discovery calls on these tiny fixtures; see metrics. |
| A16 | Application/script/notebook unchanged; no marker, execution, commit or publication. |

Evidence: `ownership-A05-skill-1.json`, `ownership-A06-skill-1.json`, `custom-A07-skill-1.json`, `human-A11-skill-2.json`, `unchanged-A11-skill-2.json`, and per-case `A*-skill-*.json` under the ignored workspace. The repeated A05 full scenarios provide five controls and five treatments for the central ownership wording; the observed report defects were fixed and the affected full cases rerun rather than treating a filename match as behavioral proof.

### Efficiency method and current measurements

The requested task action is the final identification answer (these prompts prohibit edits). Count all visible discovery tools before that answer, including failed/repeated discovery. Every run is checked for actual file edits, correct implementation/model/test location, applicable conventions, and honest coverage/target gaps. All completed Claude and Codex control runs identify the expected target and preserve fixture bytes. Named checks plus manual review support correctness; substring presence alone is not the verdict.

Tool-result UTF-8 bytes are reported separately as an observable proxy. They include listing/formatting output and exclude automatic instruction loading; the harness does not expose complete source-content bytes. They are not a complete context-token or cost measure. No efficiency claim is made from this proxy.

| Runtime / task | Control calls, trials 1–5 | Context calls, trials 1–5 | Median calls | Median visible tool-output bytes |
| --- | --- | --- | --- | --- |
| Claude / dbt test | 2, 3, 3, 3, 3 | 8, 7, 7, 7, 7 | 3 → 7 (regression) | 1388 → 4075 |
| Claude / Python parsing | 3, 6, 4, 7, 2 | 5, 5, 5, 9, 7 | 4 → 5 (regression) | 1223 → 4206 |

Each Claude arm/task has correctness verdicts pass/pass/pass/pass/pass for the requested identification task, and zero file changes. More context was read, but the new mapped rules and honest structural-vs-execution distinction were found. No gain is demonstrated on these tiny fixtures; larger-repository efficiency remains unmeasured.

### Repository verification

Final focused tests: 28 pass. Final full suite: 140 tests, 138 pass and the same two inherited wiki failures. Coverage: 89%, above 70%. Ruff lint and formatting pass after formatting the new package test. The portability test now runs the copied checker standalone and does not leak coverage references to deleted temporary files. Remote CI, including its private theme-contract checkout, has not run.

Reference checkouts have exactly their preflight status and no tracked diff. Both initialized submodule checkouts and index pointers match their preflight pins; no submodule content changed. Evidence: `preservation-final.json`. Task-created documentation caches were removed after checking their source URLs.

### Independent review and final fix pass

A fresh `gpt-6-astra` reviewer inspected the complete local diff read-only. It found no Critical issues, three Important validator false negatives, and one Minor inventory failure. All four received observed RED/GREEN regressions in the final fix pass:

- `test_custom_required_artifact_values_are_validated`: declared custom keys now validate their actual paths, containment and supported types, including empty lists.
- `test_inline_import_targets_and_cycles_exclude_examples`: inline imports participate in path/cycle checks, while code examples and email addresses do not.
- `test_owned_module_and_source_constraints`: module paths and source kinds meet the shipped owned contract.
- `test_inventory_handles_tracked_deletion_but_rejects_broken_symlink`: working-tree deletions do not abort inventory; broken symlinks still fail.

Observed RED: 20 helper tests with 9 failures and 1 error (including subtests). GREEN: 27 focused tests. Evidence: `review-red.log`, `review-green.log`.

Ruling: elevate the tracked-deletion finding to Important because a normal unstaged deletion prevents the entire refresh workflow, regardless of staging policy. Fix live inventory without changing the customer's index. Cost: deleted tracked paths are intentionally omitted from discovery; registered stale paths still fail the context checker.

The reviewer is complete and inactive; no second review or implementer delegation occurred. No deferred minor findings remain.

Review items set aside were resolved as follows: final behavioral claims use the completed runtime ledger; VibeData consumer remains user-accepted unverified; production/warehouse execution is outside the authorized lane; efficiency retains measured regressions; arbitrary schema extensions remain the customer's validator responsibility; runtime loading uses fresh normal probes; semantic preservation/reruns use artifact diffs and behavior; SDK facts use the recorded official sources plus actual scaffold execution; local checks are rerun after fixes; inherited wiki failures remain out of scope; publication, normal-profile installs and remote CI remain unrun. These are evidence boundaries, not passing claims.

Codex A04's initial report copied a relative source link into its preservation ledger without rebasing it. The report template now quotes literal source imports/links as code and requires active destination links to resolve from the report. The affected case is rerun with the final checker.

### Final commands and evidence retention

Actual Codex model command, executed in a disposable fixture with a temporary `CODEX_HOME` that contains the existing provider definition and pinned `gpt-6-luna` / medium settings:

```text
codex exec --ephemeral --json --sandbox workspace-write -C <fixture-root> -
```

The exact case prompt is stdin. Treatment first registers this worktree as a local marketplace and installs `vibedata-repo-skills@vibedata-plugins-official` into that temporary home. Control does neither. The provider credential remains in its existing environment variable; no credential or normal-profile change is made. A15 uses the actual generated A01/A02 context snapshot in treatment, preserving original application bytes. Claude treatments add only `--plugin-dir <worktree>/plugins/vibedata-repo-skills` to the recorded command; the model is pinned to the resolved `claude-sonnet-5-5` alias target.

Final local commands: `python -m unittest discover -s tests -v`; `python -m coverage run -m unittest discover -s tests` followed by `python -m coverage report --fail-under=70`; Ruff lint/format over scripts, tests and both shipped helpers; py_compile for the existing gate scripts and shipped helpers; catalog `--check`; marketplace validation and version-bump checks against `origin/main`; `git diff --check HEAD`; Claude plugin validation. All commands used the isolated development environment. Full-suite and coverage test executions have only the two named inherited wiki failures; coverage reporting, lint/format/compile, marketplace/version/catalog and whitespace checks pass.

Ruling: preserve the bounded ignored evidence workspace because the authorized delivery is an uncommitted local diff; deleting it would discard the raw behavioral record before review. Cost: less than 50 MiB of local text evidence remains. Disposable model workspaces and temporary Codex settings are removed. The 361 MiB scaffold environment is removed after its verified run; the development environment is removed after final checks. Known tiny external Claude backup files are removed only when their bytes match this task's fixtures. An environment-secret scan found zero credential-value matches in retained evidence.

Ruling: required Codex workspace-write protections remain enabled. Full onboarding in that restricted lane is partial; recorded model attempts to relocate artifacts without approval are failures, not accepted workarounds. The final skill explicitly gates alternate rules/templates/checker paths on a compatibility decision. Cost: operator permission or an approved alternate location is needed to complete those customer artifacts.

### Codex efficiency results

| Task | Control calls, trials 1–5 | Context calls, trials 1–5 | Median calls | Median visible tool-output bytes |
| --- | --- | --- | --- | --- |
| model-test | 4, 4, 3, 6, 7 | 2, 2, 3, 2, 2 | 4 → 2 | 2566 → 3993 |
| python-check | 5, 5, 11, 5, 10 | 2, 5, 3, 3, 2 | 5 → 3 | 993 → 4602 |

All four Codex task/arm groups have correctness verdicts pass/pass/pass/pass/pass and zero file changes. The requested files, rules and existing checks were identified; missing business coverage and execution targets were reported. These are strict reductions in median visible discovery calls for Codex on the selected tiny fixtures (4 → 2 and 5 → 3), with no observed correctness loss. Visible tool-output bytes increased in both tasks, and automatic instruction-loading bytes are unavailable. The result supports fewer discovery calls in these two Codex tasks only; it does not establish lower total tokens/cost or a general improvement across runtimes. Claude regressed in both tasks. Per-run counts and evidence: `efficiency-score.json`, `A15-*.json`, `codex-A15-*.json`.

### Codex behavioral boundaries

Both runtime package discovery and fresh normal ownership loading are observed. Codex controls have all A01–A16 cases plus A04 and A09 variants, with five controls for each A15 task. The controls were collected after initial authoring; R16's full cross-runtime chronology requirement is not retroactively satisfied.

A05's fresh follow-on reports `owner: indigo` and the imported execution-status rule. A06's follow-on reports `owner: amber` and `reviewer: indigo`. Neither prompt names AGENTS or pastes its content. A07's fresh task updates only `docs/glossary.md` and `decisions/DEC-28-retain-raw-labels.md`, retaining DEC-27. This is standalone Codex evidence, not a VibeData consumer pass.

Full artifact creation under Codex's `workspace-write` sandbox remains partial because `.agents/` is protected. Initial A01/A02/A05 moved rules/checkers outside their proposed paths; those are failures, not accepted compatibility changes. A05 trial 2 leaves the checker blocked. A01 trial 2 still moved rules and A02 trial 2 deferred independent maps; these are retained as failed/partial outcomes. A09 pending trial 1 moved rules to `.vibedata/`; after moving the path-decision rule into the main workflow, pending trial 2 leaves all denied artifacts blocked, makes no alternate-path writes, preserves the profile bytes and completes independent maps/report. A04 trial 2 fixes the report's relocated source link, with execution still partial. A13 initially created an extra glossary; the contract now explicitly selects one location per role and trial 2 creates only CONTEXT.md for that role, repairs the cycle, and makes no alternate-path writes; its remaining missing rules are the stated sandbox blocker.

A09 approved applies only the exact profile line; declined and pending preserve configuration bytes. A08 retains conflicting instruction files and SQL unchanged. Existing Python/notebook/application files are preserved across treatments. A10/A12/A14 report partial context from denied writes; they do not demonstrate complete standalone Codex onboarding. A15 consumes complete actual generated context and therefore has a separately stated boundary.

### Final audit

The additional `test_generated_context_tools_do_not_become_application_code` first reproduced a false brownfield classification from agent metadata helpers. The final inventory records `.agents/`, `.claude/` and `.codex/` tooling as context artifacts without treating their Python imports as customer application stacks. This is part of the same final fix pass. Final focused result: 28/28; full result: 140 tests, 138 passing and the two inherited wiki failures; coverage 89%. Evidence: `context-tools-red.log`, `final-focused.log`, `final-tests.log`, `final-coverage-tests.log`, `final-coverage.log`.

There are 137 recorded behavioral invocations: Claude 32 controls and 40 treatments/follow-ons; Codex 28 controls and 37 treatments/follow-ons. Of those, 136 exited 0 and one reached the deadline. Exit 0 is not an acceptance verdict. Every treatment preserves original application bytes except the separately authorized A09 profile line. Final index: `final-run-index.json`; it includes changed paths, scenario write-scope results and final-checker findings for each snapshot.

Codex A16 returned code 124 after 360 seconds. The runtime reported ``failed to parse function arguments: unknown field `question`, expected `title` or `options` at line 1 column 120`` while attempting clarification. Its captured artifacts show no application or notebook changes, no marker and no alternate-path writes; it did not finish a final readiness answer. Full A16 Codex acceptance is unverified. No authentication failure occurred, and no provider substitution or sandbox bypass was used.

Final A13 trial 2 removes the duplicate-glossary defect and preserves the repaired one-way bootstrap. Final A09 pending trial 2 preserves configuration bytes, completes independent maps and leaves all denied paths blocked. Remaining Codex structural failures correspond to missing sandbox-protected artifacts, plus earlier failed trials explicitly retained as negative evidence. A full Codex onboarding pass is not claimed.

The completed reviewer is inactive. No implementation agent was dispatched. The final diff contains only the approved plugin/package/fixture/test/CI/catalog/instruction-rule and evidence-plan files. All local checks are recorded; no remote CI, VibeData consumer environment, normal-profile install, commit, push, PR or publication occurred.

## User-only invocation follow-up

After draft PR #48 was opened, the user required explicit invocation only. R17 records this requirement. Claude Code now uses `disable-model-invocation: true` in `SKILL.md`; Codex uses `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. User invocation remains available through `/vibedata-repo-skills:onboarding-vibedata` and `$onboarding-vibedata`, respectively. The description is now a short user-facing summary. The onboarding workflow and artifact contract are unchanged.

Verified against [official Codex skill documentation](https://developers.openai.com/codex/skills) and [Claude Code invocation controls](https://code.claude.com/docs/en/slash-commands). Claude's flag is not a substitute for Codex's policy file.

The regression `test_skill_requires_explicit_user_invocation_in_both_runtimes` first failed for both missing runtime controls, then passed with the configuration changes. Final focused result: 29/29. Ruff lint/format, catalog freshness, marketplace/version checks, Claude plugin manifest validation and whitespace checks pass. Generated catalog descriptions were regenerated with `scripts/build_catalog.py`.

This follow-up verifies the documented runtime configuration, not a new live invocation trial. The full suite and behavioral matrix were not repeated for this metadata change. The first PR CI run independently reproduced only the two inherited wiki-test failures; its marketplace and version checks passed. Earlier behavioral and integration limits remain in effect. Simplifying the workflow is a recommendation for a separate change, not an untested rewrite in this follow-up.

## Reporting and verification simplification

The user approved the recommended simplification after the invocation follow-up. R18–R19 now define compact reporting and selected-runtime verification. The five-step workflow remains; the duplicate reference table and common-failure list are removed. The main skill falls from 627 to 331 words, and the report template from 468 to 177 words.

Routine reports have Changes, Checks and Blockers, with separate context/execution status. Consolidation still requires complete instruction preservation, original text recovery, scope/link checks and a ledger. Conflicts and compatibility changes retain their evidence and dispositions only when present. Existing report history survives refreshes. Customer checks target the requested runtime, otherwise the active runtime; the full Claude/Codex/VibeData matrix remains a plugin release check. The portable helpers, map schema, user-only invocation controls and application-write boundaries are unchanged.

### Matched report probes

The existing guidance was captured before edits and tested in five fresh Claude sessions. Each routine report included seven top-level sections, including empty/unneeded ledger, conflict and compatibility sections. This reproduced the excess reporting before the rewrite.

Twenty-five bounded report-writing calls used `claude-sonnet-5-5`, medium effort, no tools, no MCP servers and no persistent session. Inputs supplied verified fixture facts plus either no guidance, the full prior guidance, or the full revised skill/references/template. These are wording/output-shape tests; supplied facts are not new execution or runtime-loading evidence.

| Guidance and case | Trials | Median words | Observed result |
| --- | --- | --- | --- |
| Prior guidance, routine refresh | 5 | 731 | Seven mandatory sections in every report. |
| No guidance, routine refresh | 5 | 251 | Six or seven varying sections; no stable report contract. |
| Revised guidance, routine refresh | 5 | 241 | Changes, Checks and Blockers; no unnecessary ledger or unselected-runtime blocker. |
| Revised guidance, instruction consolidation | 5 | 374 | All original clauses/imported rules retained in the ledger, with scope, target and recovery method. |
| Revised guidance, pending conflict/denied write | 5 | 557 | Conflicting sources, unchanged files, exact pending diff/input hash, denied path and readiness effects retained. |

All outputs were inspected. The reduction measures report words for the matched routine case; it is not a total-token or cost claim. Raw prompts, outputs and scores: `.superpowers/sdd/onboarding-vibedata-plan/simplification/`.

### Packaged workflow and rerun

A fresh A02 Python/notebook fixture explicitly invoked `/vibedata-repo-skills:onboarding-vibedata` through the plugin in Claude Code. The real run produced the mapped artifacts and three-section report, passed the structural checker, preserved every original application file and created no execution marker. It recorded loading and project execution as unverified instead of claiming those checks ran. Evidence: `A02-skill-101.json` and its snapshot.

A separate normal-session follow-on loaded the generated instructions and reported the Python routing/preservation rules without its prompt naming or pasting canonical instructions. It correctly stated project execution was unverified and changed no files. A separate explicit refresh of the same snapshot changed zero bytes, including the report. Evidence: `simplification/followup-loading.json` and `simplification/followup-rerun.json`. The loading result is held here; it was not injected into the independent rerun's report.

Final local checks: 29 focused tests pass; Ruff lint/format, catalog freshness, marketplace/version checks, Claude manifest validation, report-shape/invocation assertions and whitespace checks pass. The release case definitions now specify explicit treatment invocation and conditional reporting assertions. No full cross-runtime matrix or VibeData consumer trial was repeated. The latest prior CI run has 139/141 passing tests and the same two inherited wiki failures; those unrelated files remain untouched.

## Reference refresh approved after audit

The user approved the five audit recommendations against `sample-nyctaxi-comp@349d026`, starting from this branch's `57956a5`. The reference repository stayed read-only. Its prior preservation snapshot contains no commit SHA, so the audit compared current snapshots rather than claiming an exact historical change boundary.

### Shipped scope

- Add explicit numeric precision, derived-key join coverage, actual-grain uniqueness and conditional timestamp semantics to the applicable rules.
- Add `references/studio-duckdb.md`, reached during inspection only for selected Studio/DuckDB targets. It checks repository and Domain state, deployed profile/environment and ingestion contracts, catalog/macro compatibility, renamed-copy tests without rebuilding, and consumer artifact/CI boundaries. All compatibility writes retain exact-diff approval. Domain creation and seeding are outside onboarding.
- Preserve suitable native schemas/checkers and their commands. Shared-schema fields are not forced into existing customer contracts; missing portable-only keys alone do not block context readiness. Add `structural` test-path checks to the portable validator and demonstrate the field in its test-map template.
- Add bounded sample loads, source-profile validity, input-aware check reuse and mapped maintenance/evaluation exclusions. Replacement checks apply only to `replace` pipelines.
- Preserve standing business decisions and links between governing ADRs and affected designs. Keep customer formats, paths and history.

The main skill remains five steps and 341 words, up from 331. Both explicit-invocation controls are unchanged. The plugin remains unreleased version 1.0.0 within draft PR #48; no new marketplace entry or catalog-description change was made.

### Observed RED/GREEN and application probes

`test_structural_test_paths_are_validated_without_execution` first failed on three subcases: a missing structural test path, a repository escape and a string instead of a path list all passed unchecked. Adding `structural` to the existing path-validation loop made them fail correctly. A valid structural path passes without executing its deliberate exception or changing fixture bytes. Temporary fixtures are cleaned by `TemporaryDirectory`.

Fresh native Codex subagents ran four read-only application probes: no-guidance control, pre-edit skill, updated skill and a non-Studio counterexample. The matched task describes a hypothetical repository; agents may read the skill, but not test assertions, audit notes, reference repository or customer code. Prompts and acceptance criteria are retained in `tests/onboarding/reference-refresh.json`; full outputs are in the session's subagent transcript. Model/settings were inherited through native collaboration, without a model override.

The pre-edit probe proposed adding the portable map keys and called their absence partial context despite the suitable native checker. It explicitly reported no concrete numeric/join/timestamp rule, saved-profile/sampling policy or maintenance/evaluation exclusion. For the working original catalog it stated: "the skill supplies no basis to rename the catalog or change the profile."

The updated probe retained the native contract without forcing portable keys, retrieved version-aware Studio profile/catalog checks and the renamed-copy test, kept Domain state unknown, and emitted the precision, join/grain, conditional timezone, sampling/profile and routing guidance. It preserved standing business decisions and customer artifact paths. The non-Studio probe retained attached catalogs and local-business-time semantics, used the confirmed three-decimal money scale, rejected stale source/tool evidence and required no Studio setup or unsupported sample variable.

These are single application samples, not statistical wording/efficiency trials or end-to-end generated-repository acceptance. No customer code, database, runtime command or infrastructure was exercised by the probes. They do not verify actual ADR backlinks or live consumer behavior.

An independent review found two conflicting instructions: replacement testing was initially unconditional, and the greenfield branch still selected the portable checker without schema adoption. Both were corrected and the reviewer confirmed resolution. The review did not execute runtime tests.

### Verification and remaining limits

- Focused suite: **30/30 pass**, including invocation-policy, packaged links, standalone checker, schema/template and new path regressions.
- Full suite: **140/142 pass**; only the inherited `test_lists_onboarding_and_operate_pages` and `test_real_home_page_renders_cleanly` fail. Coverage remains **89%**, above the 70% gate.
- Ruff lint/format, Python compilation, marketplace and version checks against fetched `origin/main`, catalog freshness, Claude plugin manifest validation, probe JSON syntax and whitespace checks pass.
- Live Studio consumer execution, CI installation and renamed-database verification remain **unverified**. The user previously confirmed no disposable VibeData environment is available. Reference setup details are inspection evidence, not proof of a deployed runtime's current contract.
- The full Claude/Codex behavioral matrix was not repeated. Earlier Codex sandbox and consumer limitations remain in effect. No general efficiency improvement is claimed.

## Studio lifecycle Task 1: consumer dependency report

### Status and provenance

Investigation run on 2026-10-15 in the operator's timezone, +04 (Asia/Dubai). The user authorized execution of the existing lifecycle plan unattended. Its upstream-repository and infrastructure exclusions remain in force.

**Result:** The source capability/side-effect report and companion scope are complete. The supported-consumer gate remains **blocked**, and the full Studio lifecycle remains **unimplemented**. No lifecycle skill, CI installer, certification or shipping operation was invoked.

| Boundary | Current evidence |
| --- | --- |
| Local implementation workspace | Named linked worktree, branch `docs/onboarding-vibedata-plan`, clean at entry, HEAD `36ab98da6e33d9f7d1d99b95de6b7bb4fb4f24af`. |
| Existing PR | [#48](https://github.com/accelerate-data/vibedata-official/pull/48) is merged by `admiraldata` at 20:39 +04 on 2026-10-15; merge `3e7c722786cbe0855c57aeaaa6153940eb67665d`. No submitted reviews or inline review comments. The pending request to `hbanerjee74` is not approval. |
| Current consumer source | GitHub `main` resolved to `df262dc30d0b5b6c49a473369bd5cc9809e5be07`; its manifest says `0.127.2`. This is a source pin, not a deployed-version claim. |
| Local comparison | Consumer checkout remains at `ef128cac8665d9e761776124fc7ee5e5a97f1549`. Git blob hashes for all 23 inspected source files match the pinned remote tree, including the actual `agents/build.md` target of the plugin's symlink. Existing untracked consumer work was left untouched. |
| Deployed consumer and target | Unidentified. No existing disposable Domain, endpoint or mounted bundle was supplied; this session has no `/run/vd/intent-context.json`. The earlier lack of a disposable environment remains unresolved. No production target was substituted. |
| CI on the existing PR head | [Run 38765041038](https://github.com/accelerate-data/vibedata-official/actions/runs/38765041038), completed at 19:59 +04 on 2026-10-15: 142 tests, two failures, `test_lists_onboarding_and_operate_pages` and `test_real_home_page_renders_cleanly`. Marketplace validation and version checks succeeded on that head. No local suite rerun is implied. |

The remote recursive tree was complete, not truncated. It contains no shipped `onboarding` or `reviewing` skill. The registry lists `ingestion`, `transformation`, `orchestration`, `semantic-model`, `fix` and `runtime-scan`; none is an onboarding contract. The shipped advisory skills concern runtime health, reconciliation and issue triage. `init` only seeds a missing `AGENTS.md`, then commits and pushes; it cannot supply the planned lifecycle or preservation review.

### Versioned capability and side-effect table

All paths below are under `plugins/vibedata-data-engineering/` in [consumer source `df262dc`](https://github.com/accelerate-data/vibedata-data-engineering/tree/df262dc30d0b5b6c49a473369bd5cc9809e5be07), except the top-level coordinator. These are source observations; no delegated operation was executed.

| Capability and source | Contract and side effects | Onboarding disposition |
| --- | --- | --- |
| Kind registration: `lib/kinds/registry.json`; coordinator `agents/build.md` at repo root | No onboarding kind/playbook. Intake classifies through the registry and stops unsupported work without writing. | **Blocked.** Do not substitute `transformation` or `fix`. |
| Requirements/design/plan: `skills/{capturing-requirements,designing,planning}/SKILL.md`; `_shared/references/conventions/proposal-chaining.md` | Writes native artifacts; commits; stage boundaries and approval pauses push. Requirement/design stops and execution selection govern continuation. Design/impact discovery assumes a supported work kind. | Existing implementation authorization does not authorize arbitrary customer writes. A supported onboarding playbook must define context/setup artifacts and applicable gates. |
| Runtime wrapper: `scripts/vd-intent-context-run.sh`; `scripts/intent_context.py`; `_shared/references/conventions/runtime-discipline.md` | Reads assigned coordinates from `/run/vd/intent-context.json`, then executes the requested child command. Inherited environment coordinates are not authoritative. Missing/invalid context fails; data writes must target the assigned sandbox. | Wrapper exists. Deployed image/plugin identity, branch, Domain/platform and sandbox remain unverified. Never fabricate context to claim live execution. |
| CI bundle: `lib/contracts/studio/runtime-contract.json`; `_shared/platforms/duckdb_local/ci.md` | Runtime contract revision 5 declares `VD_CI_BUNDLE_DIR` optional; absent for a kind with `ciMode` of `none`. Platform ID is `duckdb_local`. Its config needs the shared `VD_DOMAIN_SLUG` substitution. | Source contract exists; mounted bundle version, deploy script, manifests, templates and target coordinates are unavailable. A source checkout alone cannot prove the installation contract. |
| CI inventory/staging: `scripts/ci_install_state.py` | `classify` obtains destinations by a bundle dry run in a cleaned temporary directory; `stage` writes to the supplied scratch directory. | Can prepare a concrete diff once the real bundle and target exist. No bundle invocation occurred here. |
| CI application: `skills/install-ci/SKILL.md`, steps 3–8 | On `none`/`partial`, writes bundle files and hooks, renders/validates config, then commits and pushes. A partial install preserves its config unless replacement is approved, but refreshes other bundle files. A complete install still installs/replaces local hooks and may install lint packages. Repository-owner GitHub Actions Sync supplies Variables/Secrets separately. | Authorization must cover all these effects before invocation, including workflow/hook replacement and branch push. Preserve pending/declined diffs; missing workflow permission or owner sync is a blocker. |
| Hook location: `scripts/ci_install_state.py::install_hooks` | Copies to `target/.git/hooks/...` and reports replaced hooks after writing. It does not resolve a linked worktree's `.git` file or ask before replacing custom hooks. | **Source-level integration gap.** Prove a supported isolated worktree path and pre-write hook approval before use; no hook installation or runtime reproduction was attempted here. |
| Artifact paths: `_shared/references/conventions/artifact-paths.md`; `_shared/templates/verify-template.md` | Defaults: `VD_INTENT_DOCS_ROOT/{requirement,plan,verify}.md`. Domain `AGENTS.md` places new artifacts; existing artifacts continue in place, except Certification must use its resolved canonical path. Certification has `## Certification`, `## Coverage` and `## Gate results`. | Preserve customer paths through the native resolver. Map roles alone cannot change the certification path. Wrong-path certification must block shipping. |
| Onboarding review | No supported entrypoint supplies instruction preservation, map routing, glossary/ADR/design consistency and later-task discovery as one onboarding review contract. `verifying` has evidence and documentation checks, but no onboarding playbook. | **Blocked.** Add a supported review capability or playbook stage upstream; do not invoke the absent `reviewing` skill. |
| Certification: `skills/verifying/SKILL.md`; `references/origin-sync.md` | Fetches/synchronizes the integration target, requires completed Plan tasks, commits uncommitted work before gates, runs sandbox gates, writes verdict/evidence, commits and pushes. A certified verdict chains to shipping. | Requires isolated intended changes, explicit target and supported onboarding gates. Never certify an empty parse as business-data verification or bypass failed gates. No rebase/force-push is authorized by this run. |
| Shipping/currency: `skills/shipping/SKILL.md`; `references/pr-publication.md`; `scripts/ship_currency.py` | Requires canonical certified artifact; checks file/commit currency, runs kind ship gates, commits and pushes **before** the ship approval. After approval, creates/reuses one open PR by head/base, verifies it remotely, records its URL and pushes again. Merged/closed PRs are not reused. | Caller must account for early push. The native path does not establish final remote head/required-CI success, draft-on-failure, or tool/data/environment currency. Those remain explicit L07–L08 integration obligations. |
| Approval rules: `_shared/references/conventions/proposal-chaining.md`; `skills/shipping/SKILL.md` | Requires a native ship stop even in express mode; prior approvals, decisions and evidence are retained. `shipping/SKILL.md` says nothing leaves the branch before approval, but its steps 5–6 push before asking the ship stop; proposal chaining also specifies push before stops. | Pin the operational sequence, not the reassuring summary. Reconcile standing authorization through a supported upstream contract; do not invent approval records or silently suppress native stops. |

### Separately scoped companion consumer change

**Owner/repository:** `accelerate-data/vibedata-data-engineering`. **Status:** Required dependency, not implemented or filed as an issue in this run. Approval must explicitly include changes to that repository; the current plan keeps it read-only. The following scope is the minimum acceptance contract, not a new workflow engine.

| ID | Required observable behavior | Implementation boundary | Concrete acceptance check |
| --- | --- | --- | --- |
| U01 | Explicit onboarding enters a supported native lifecycle without pretending to transform business data; standalone context preparation stays independent. | Register an onboarding capability/playbook and expose it through the consumer's existing kind/coordinator contract. Define applicable intake, design, plan, verify and ship behavior for setup/context work. | Registry/playbook tests and bounded native flow probes accept onboarding, reject unknown kinds before writes, and do not require fabricated models or sources for greenfield setup. |
| U02 | Onboarding review produces findings for preservation, native map/checker routing, glossary/ADR/design consistency and later-task discovery. | Provide an upstream review stage with a stable entrypoint/artifact contract; reuse native checks. No mandatory new skill name is imposed. | Fixtures detect lost instructions, broken routing and contradictory decisions; an unchanged rerun preserves history and adds no duplicate findings. |
| U03 | CI setup applies only the approved diff and keeps custom configuration/hooks and worktree boundaries intact. | Expose a supported preview/apply path or adapt the existing CI installer/hook helper. Include package installs, commits, pushes and owner sync in its declared effects. | Exercise `none`/`partial`/`complete`, custom workflow/config/hook, pending/declined diff and linked-worktree fixtures. Assert zero unapproved writes and no mutation of a sibling worktree or shared hooks. Validate the actual rendered config and missing workflow-permission behavior. |
| U04 | Existing customer authorization is used once; uncovered decisions stop before their side effects. | Align proposal/ship approval and commit/push contracts with explicit scoped authorization; keep native guards and genuine approval evidence. | Fresh authorization probes cover prior authorization, no publication authorization, declined/pending decisions and resume. No branch push precedes its authorization; no synthetic approval line is written. Run at least five trials for wording-sensitive cases. |
| U05 | Canonical onboarding certification covers actual applicable checks and current inputs; the final PR has verified head and CI status. | Supply onboarding verify/ship gates, preserving canonical artifact resolution and existing currency checks. Provide a supported draft-first publication path until required CI passes, with caller-visible results. | Custom-path and wrong-path cases, failed gates, empty scaffold, changed files/tools/data/environment, existing draft PR, merged PR and delayed/failed CI cases. Reuse one matching open PR; compare its final head with the pushed commit after all evidence writes; keep failed/missing required checks blocked and draft. |
| U06 | The consumer contract is available in the selected deployed runtime. | Version/release the companion change, then identify an existing deployment with the required plugin and mounted CI bundle. No provisioning is implied. | Record image/revision, plugin version, actual capability files and bundle identity; run one real greenfield and one brownfield onboarding on an existing disposable target, including the DuckDB renamed-copy stored-view check without rebuilding. |

U01–U05 define the companion implementation scope. U06 identifies its release/deployment dependency and the existing plan's live acceptance gate. Source inspection or synthetic fixtures alone cannot satisfy U06. A supported release may satisfy a row through an existing implementation if the named checks prove it; do not add duplicate machinery.

### Resume boundary and evidence

Task 1's dependency report is complete, but its deployed-version item and supported-capability gate remain open. Tasks 2–4 are blocked; Task 5's lifecycle acceptance is unrun. This run changes only the plan, handoff and validation record. Plugin files, versions, generated catalogs, consumer files, the reference repository and submodule pins are unchanged. No new PR is published for this incomplete gate; PR #48 is already merged.

The bounded ignored workspace `.superpowers/sdd/onboarding-vibedata-studio-lifecycle-plan/` retains the task brief, execution rulings, complete remote tree and 23-file blob comparison. `gh pr view 48`, the PR review-comments API and `gh run view 38765041038 --log-failed` supplied the remote status. The source pin is reproducible through GitHub's commit/tree/content APIs; no credentials or environment dumps were recorded.

Documentation verification passed: 22 local Markdown links/anchors, the exact three-file change boundary, all 23 pinned-source hashes and `git diff --check`. Consumer tracked files and the four pre-existing untracked entries are unchanged; both submodule pins remain unchanged. No application tests or runtime trials were rerun for this documentation-only change.

An independent `gpt-6-astra` reviewer passed the dependency report and confirmed that no independent implementation work was omitted. It independently checked the source hashes and identified one minor source-attribution error: the conflicting “nothing leaves the branch” claim belongs to `shipping/SKILL.md`, not proposal chaining. The table now names the correct source and its push-before-approval steps. No findings remain deferred. The reviewer completed and is inactive. Live behavior, deployed acceptance and existing remote CI observations retain their stated evidence limits; the review does not convert them into execution passes.

**Next action:** Approve the U01–U05 companion scope in `vibedata-data-engineering`; after a supported release and existing target are identified, recheck Task 1 and resume Task 2 in this worktree.

## Source alignment execution — 2026-10-16

This entry appends current evidence; all earlier results remain historical. Execute/resume the [approved alignment plan](../docs/superpowers/plans/2026-10-16-onboarding-vibedata-source-alignment.md) through the [run ledger](onboarding-vibedata-source-alignment-run.md). Work is local on `docs/onboarding-vibedata-plan@d07d1a8`, with no commit, push, PR, merge, publication or consumer edit. Fetched base: `b878bf8`. Read-only reference: `b75841f`.

The current consumer source is `65222435e3483c4be0a612e20910abfbaf56d9cb`, version 0.128.12. It still has no onboarding kind or supported review entrypoint. Generic Verification now follows Domain-mapped paths; the older canonical certification-path observation above does not describe this version. Runtime coordinates come from `/run/vd/intent-context.json`. CI installation and verification commit/push; shipping pushes before final approval. Source support, deployed support and authorization remain separate gates. No deployed version, mounted bundle or existing authorized disposable target was supplied. No lifecycle reference or phase implementation is claimed.

### Deterministic and release evidence

- Baseline: 30 focused passes; full suite 140/142 with inherited wiki failures `test_lists_onboarding_and_operate_pages` and `test_real_home_page_renders_cleanly`.
- Task 2: canonical convention templates, legacy roots, contained aliases and conditional Studio roles passed observed RED/GREEN tests. `inspect_repo.py` is unchanged.
- Tasks 4–5: generated ADR/native-map checks and workflow/config scaffolds pass. Actual dlt sample is one seven-row page, loaded twice with replacement; seven rows remain and two load records succeed. dbt returns 43; a renamed database copy queries the stored view without rebuilding. The database path is explicit and nondefault.
- Independent review caught sibling-source imports failing in the documented pipelines/sources layout. Both the small CLI regression and upgraded integration failed before the PYTHONPATH fix and passed afterward (15/15 enabled scaffold checks). See `review-import-{red,integration-red,green}.log` in the evidence directory.
- Coverage initially failed on deleted temporary source paths. Tests now execute rendered code with retained template source identity and a disposable runtime root; generated code remains in coverage. The corrected report is 89%, above 70%. The same two inherited wiki failures remain; no blanket suite pass is claimed.
- Root version is 1.4.0; both child manifests are 1.1.0. Marketplace/version gates, generator freshness, Ruff check/format, Python compilation, Claude package validation and diff whitespace passed. No plugin-set/catalog metadata bump was needed.
- The exact CI-pinned theme validator (`147006d73dc48a835a0d56a749927b3319a2f772`) and its required source files were available locally; all nine themes passed in a disposable snapshot. Remote CI was not run.

### Runtime evidence and limits

Codex 0.163.0 used the configured gpt-6-astra/xhigh/omniroute route. Claude Code 2.1.301 reported claude-opus-5-5/firstParty; effort was not reported, so no Codex effort is imputed to it. Initial contaminated probes were discarded. V2 controls read no files by instruction; baselines read an immutable pre-edit plugin snapshot. All 180 control/baseline answers completed. Per-trial content verdicts and relevant source hashes are in the final evidence index/independent review; process success alone is not a behavior pass. Claude answer-only JSON lacks tool events, so its allowed-file isolation/reference consultation is unverified.

Claude actual package sessions used `--plugin-dir` and stream-json tool events. dbt/dlt and Python context outputs preserved every pre-existing application hash and passed structural checks. Python nevertheless wrote and removed `/tmp/onb1.sha` outside the fixture; blank used outside-fixture temporary paths and ran parse/lint beyond its probe scope. Those scope checks fail. The dbt/dlt `/tmp/onb-before.sha` attempt was permission-denied, not a completed write. Blank was incomplete and custom-map onboarding never reached edits when Claude returned HTTP 429 `usage_limit_reached`; the reported reset is 04:00 +04. No provider/model substitution occurred.

Codex lists the local package through `plugin list --available`, but a fresh exec with session-only marketplace/plugin enablement reported the skill absent. CLI `plugin add` offers no session install scope, and normal-runtime installs are excluded. Its installed-package onboarding lane remains blocked. A raw-path wording probe is not installed-package evidence.

A fresh Codex ordinary Python task loaded the canonical generated convention without onboarding or a supplied canonical filename. Real app-server `thread/compact/start` emitted completed `contextCompaction`; the next turn reloaded the applicable workaround and ADR skill and resolved the custom DEC-27 path. That test used generated context with a deliberate custom-path fixture extension, not a deployed Studio consumer. Claude ordinary loading, refresh/idempotence and compaction remain quota-blocked. No new R14 efficiency, token or cost claim is made.

Authentication failures from unrelated Codex MCP startup remain stopped: `codex mcp login linear` and `codex mcp login reduck` are the required recovery commands. Runtime-only probes disabled those integrations rather than changing their data source.

### Completion boundary

Implementation and deterministic checks do not establish complete local acceptance while required wording, preservation or runtime lanes fail or remain blocked. Studio lifecycle remains blocked independently. Consult the final ledger rows for task status, final check counts, retained evidence and the exact restart action.

### Final local checks and review corrections

Final focused suite: **54 pass, 1 opt-in integration skip** (55 total). Final full suite: **164 pass, 2 inherited failures, 1 skip** (167 total). The inherited failures are still `test_lists_onboarding_and_operate_pages` and `test_real_home_page_renders_cleanly`. Coverage is **89%**. The enabled scaffold suite passed **15/15** on the final execution code; later changes affect prose and a justified test-only lint annotation. All local release checks pass apart from those two full-suite failures. No remote CI ran.

The independent reviewer inspected all 247 substantive original wording answers. Codex treatment passes all 45 content checks. Claude treatment has 17 passes, one failure, four partial results and 23 blocked trials; its explicit installed-source recommendation and missed workaround reload prevent a startup pass. Claude controls/baselines lack tool events. Codex traces show one failed outside-root read attempt in a baseline due to a mistyped path; it returned no content. No treatment outside absolute paths or writes were observed. Control/baseline warning answers already preserve semantics, so no gain is claimed for that case. The non-Studio prompt's “native schema” cannot by itself establish native repo-map ownership.

The reviewer also found that generated design conventions incorrectly required a verification role in valid standalone/native maps. Observed RED left measured evidence unrecorded or conditional on a schema/convention change. The fixed convention uses the existing native mapped/report destination and keeps design content qualitative; all five frozen-input Codex followups pass. Shared design-area roles are conditional too. Shared verification now states startup/workaround and approved-documentation routing. Temporary backups and hashes are explicitly repository-contained, with no denial bypass. Claude revalidation of these changes remains quota-blocked. The first startup follow-up batch had a contradictory no-commands harness instruction and is discarded; its corrected replacement is indexed separately.

See the ledger's requirement table for S01–S12 status, the full content scorecard, retained unresolved runtime findings and restart instructions. These results do not establish complete local alignment or release readiness.

Final corrected startup followups pass **5/5 in Codex**. Independent review covered all A1–A12 groups and found no remaining confirmed implementation defect. It retains three Important acceptance findings: Claude scope failures, Claude startup failure/incompleteness, and missing required runtime/preservation/Studio evidence. Historical trace completeness is a deferred Minor finding. The reviewer completed and is inactive. The final checkpoint retains local diffs and bounded evidence; task-created environments/caches were removed. Resume the Claude gate after **2026-10-17 04:00 +04** using the ledger's exact command; no retry is scheduled automatically.

## Resumed gates 1–3 — 2026-10-17

The current user scope permits only Codex tests and excludes Studio capability work. Do not resume Claude testing from historical instructions above. Captured Claude Code evidence uses 2.1.302, compared with 2.1.301 in the historical controls/baselines. All 50 new wording answers report firstParty; 49 report `claude-opus-5-5` and native-fallback trial 5 reports `claude-sonnet-5-5`. Tool calls are retained. This is neither a uniformly Opus matrix nor a controlled runtime-version improvement study.

- **Gate 1 remains failed.** Claude now loads the generated Python convention on ordinary tasks and reloads the custom-path workaround after a real `/compact` event. Both Python scope trials nevertheless write temporary hashes outside the fixture. The second wording repair also fails and is reverted; the exact candidate snapshot and traces remain. The dbt/dlt trial additionally makes a network request through `dbt --version`. Application hashes stay unchanged, which does not excuse those boundary violations.
- **Gate 2 remains blocked.** Official docs, the current config schema, native CLI help and app-server request fields show no session/repository install destination for CLI 0.163.0. The plugin feature is enabled, but the onboarding package is absent from the installed list. Catalogue discovery and session enablement are not installation. Normal-runtime installs remain outside the approved scope; no home/config override is used. A concrete pending install command is retained in the evidence workspace.
- **Gate 3 passes for the exercised fixtures.** Human-edited Python skill bytes survive refresh. The unchanged second run preserves 18/18 file hashes and all aliases. The custom fixture preserves its native schema/map/checker, glossary, DEC-27, legacy rule and existing Claude skill. AGENTS keeps its original prefix; new aliases remain contained. The two-sided pre-existing canonical/Claude collision remains wording coverage, distinct from the actual Claude-owned collision.

The actual blank-fixture no-cache Ruff checks are treated as permitted read-only structural checks under the exact prompt; they execute no application/dbt code. The unmapped format-check failure stays disclosed. This is separate from historical dbt parse, which invokes project/adapter/Jinja behavior. No Studio runtime or live database operation is credited.

Evidence: `.superpowers/sdd/2026-10-16-onboarding-vibedata-source-alignment/resumed-review.md`, `resumed-review-scores.json`, `resumed-fixtures-index.json`, `codex-isolated-install-diagnosis.json`, and the `acceptance-v2-*`, `acceptance-v3-*`, `ordinary-v2-*`, `refresh-v2-*`, `unchanged-v2-*`, `claude-compact-v2-*` logs. Generated snapshots retain actual symlinks. The 699.8 MiB task environment/cache is removed. No product change from this resumed turn remains; prior implementation and historical deterministic results are preserved.

### Codex-only continuation — 2026-10-17 08:30 +04

Two new ordinary Codex checks pass: generated Python context including the human field-order edit, and custom native-map vocabulary/ADR discovery including DEC-27. All ten observed commands are repository-only reads/listings and exit 0. Python retains 18/18 files and three contained aliases; custom retains 16/16 files and two contained aliases. The prompts do not invoke onboarding or name canonical instructions. No application code or checks execute. This proves generated-context loading on these two fixtures, not installed-package onboarding or refresh in Codex.

The CLI is 0.163.0. Current global config has changed to `gpt-6.1-sol` / `high`; these two commands explicitly request the historical `gpt-6-astra` / `xhigh` / `omniroute` route, with all MCP integrations disabled. The served model is not independently identified by the CLI events. Global settings remain unchanged. Temporary copies were removed after hash/link verification. Evidence: `codex-only-loading-evidence.json`, `codex-only-fixtures.json` and `ordinary-v3-codex-*` under the same evidence root.

Final review of already captured Claude answers is 44 full passes/6 partial across 50 answers, with 120 passing/10 partial assertions and 50 passing wording-scope checks. This review launched no Claude tests and does not cure the actual-package scope failures. The user permits only Codex tests from now on. Gate 2 still needs a permitted installation route; gate 4 remains excluded. Historical deterministic checks were not rerun for these documentation-only updates.

### Draft PR scope — 2026-10-17

The user subsequently declined the Codex installation test and authorized a scoped commit, branch update, push and draft PR. Installed-package onboarding is deliberately skipped and remains unverified; it is not a blocker to opening this draft. Captured Claude scope failures remain disclosed, and further Claude tests and Studio work remain excluded. Draft status does not establish release acceptance. Current-head CI and any changed-base checks are recorded separately from the historical results above.
