# onboarding-vibedata validation

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
