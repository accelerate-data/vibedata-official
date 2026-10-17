# Onboarding source alignment execution ledger

Plan: [2026-10-16 source alignment](../docs/superpowers/plans/2026-10-16-onboarding-vibedata-source-alignment.md).

**Current scope:** The user authorized the scoped commit, branch update, push and draft PR. Installed-package Codex testing is deliberately skipped by user decision; do not request installation again. Run no more Claude tests. Studio remains excluded. Earlier failed and unverified results remain evidence; draft publication does not make them pass. This overrides historical restart commands below. Merging the PR into main and release publication are not authorized.

## Launch

- Authorization: execute the approved nine-task plan unattended, locally in the named worktree. No push, PR, merge, publication, production load, persistent Domain mutation or provisioning. Local commits were not separately requested; retain scoped diffs as the plan permits.
- Native inline implementation; one independent whole-change review after available work.
- Worktree/branch verified: `vibedata-official-onboarding-vibedata-plan`, `docs/onboarding-vibedata-plan`.
- HEAD: `d07d1a8538cc52826373211110c96df9d3f090b5` (matches planning baseline).
- Read-only reference: `sample-nyctaxi-comp@b75841f12c14ad8e1870d1b1581d6bd59a0fb5bf`, clean; matches audit.
- Preserve pre-existing untracked `.cache/`, audit and plan. Consumer checkout `ef128cac8665d9e761776124fc7ee5e5a97f1549` has unrelated untracked `.agents/harness.manifest.json`, `.claude/CLAUDE.md`, `.claude/skills/`, `.dork/`.
- Submodule pins: `mcp@fa414f8fba9ccda0ea680e8775f35f3008b97cbf`, `recipes@89581592e7653e675812fbaf181e73ed28b77574`; initially uninitialized.
- Python 3.12.12; uv 0.11.32; Claude Code 2.1.301; Codex CLI 0.163.0. Existing Codex model/provider: `gpt-6-astra`, `xhigh`, `omniroute`; do not substitute.
- Development environment: task-created temporary venv and package cache, indexed by `.superpowers/sdd/2026-10-16-onboarding-vibedata-source-alignment/environment.json`. Declared requirements installed: jsonschema 4.23.0, PyYAML 6.0.3, Ruff 0.17.1, coverage 7.16.2.
- Evidence: `.superpowers/sdd/2026-10-16-onboarding-vibedata-source-alignment/`; maximum 1 MiB per command, 50 MiB total. Each command records exit, timestamp, arguments and bounded log. Child process groups terminate on timeout. All dates use workstation `+04`.

## Pre-flight interfaces

| Producer → consumer | Contract | Result |
| --- | --- | --- |
| 1 → 2–9 | Baseline, cases, runtime/capability gates | Missing live support must not stop independent work. |
| 2 → 3,4,5,7,8 | Canonical conventions, legacy roots, conditional Studio roles | Preserve standalone defaults and native schemas. |
| 3 → 6,8 | Verification placement, startup, sampling | Probe inputs pinned before prose changes. |
| 4 → 5,8 | ADR/map check commands, CI dependencies | Generated checks must run independently of plugin. |
| 5 → 6,8 | Explicit database, empty real inventory, executable fixture | Use one path; no business-coverage claim. |
| 6 → 7,8 | Readiness, authorization, inventory/review | Unknown target or decisions remain named blockers. |
| 7 → 8,9 | Native lifecycle only if supported | Source support and deployed support are separate gates. |
| 8 → 9 | Current per-lane evidence and blockers | Skips and inherited failures are not passes. |

Ruling: retain task-scoped diffs instead of making local commits — the plan permits this without separate commit authorization — cost if wrong: checkpoints require committing later.
Ruling: keep this durable ledger and bounded scratch evidence through handoff — the plan explicitly requires restartable evidence — cost if wrong: less than 50 MiB retained until review.

## Task state

| Task | Status | Result / next action |
| --- | --- | --- |
| 1 | passed | Local baselines, 180 wording answers and current capability gate captured; Claude tool isolation remains unverified. |
| 2 | passed | Canonical templates, legacy-compatible checker, Studio roles; runtime trials in Task 8. |
| 3 | failed | Claude startup revalidation and real compaction now pass; sampling wording still has an incomplete evidence-detail assertion. See the resumed gate record. |
| 4 | passed | ADR/native-map/CI templates exercised; remote CI remains unrun. |
| 5 | passed | Explicit-path synthetic dlt → dbt round trip and renamed-copy query passed. |
| 6 | failed | Template metadata checks pass; Claude inventory/review answers omit required fields. These are output-evidence gaps, not a confirmed template defect. |
| 7 | blocked | Historical consumer capability gate remains open; the latest user scope explicitly excludes Studio work (gate 4). |
| 8 | failed | Preservation, ordinary Claude loading and real compaction now pass. Claude scope still fails; actual Codex package installation remains blocked. |
| 9 | passed | Local release checkpoint, independent review and handoff saved. Release acceptance remains incomplete. |

## Evidence and rulings

Launch checkpoint: 2026-10-16 23:07 +04

### Task 1 current baselines

- Focused: `python -m unittest discover -s tests -p 'test_onboarding*.py' -v` → exit 0, 30/30. Full: `python -m unittest discover -s tests -v` → exit 1, 140/142; inherited `test_lists_onboarding_and_operate_pages` and `test_real_home_page_renders_cleanly` fail. Logs: `baseline-focused.log`, `baseline-full.log`.
- Current remote main: `b878bf81be9301ec1f21729a021846e780e107b1` fetched; consumer remote source: `65222435e3483c4be0a612e20910abfbaf56d9cb`, plugin 0.128.12, inspected in a disposable bare snapshot. No consumer checkout edits.
- Codex model route returned `ONBOARDING_RUNTIME_OK`; unrelated MCP startup reported `invalid_grant` for Linear and reduck. Stop those integration operations. Recovery: `codex mcp login linear` and `codex mcp login reduck`. Runtime-only probes disable MCP startup and preserve configured model/provider; they do not substitute a source for either service.
- Claude initial probe command consumed its prompt as a variadic tools argument; repaired by passing prompt on stdin. This was a harness error, not product evidence.
- Nine alignment wording cases and seven conditional lifecycle cases added before prose edits. Narrow Claude skill write allowlists and containment assertions added. Controls/baseline use five trials per new wording case; outputs retained outside prompt roots.

### Current consumer capability table

All source rows refer to `65222435e3483c4be0a612e20910abfbaf56d9cb`, version 0.128.12. Deployed version and disposable target are unknown.

| Capability | Entrypoint / artifact contract | Side effects / authorization | Source support | Deployed support |
| --- | --- | --- | --- | --- |
| Onboarding kind | `lib/kinds/registry.json` contains transformation, ingestion, orchestration, semantic-model, fix, runtime-scan | Substituting a kind is not authorized. | Missing | Unknown |
| Onboarding review | No `skills/reviewing` or `skills/onboarding` entrypoint | Repository-local source review is not a deployed capability. | Missing | Unknown |
| Requirement / plan / verification | `skills/capturing-requirements`, `planning`, `verifying`; named Requirement reused, Domain-declared paths | Capturing/designing/planning commit; current verifying commits and pushes. | Generic phases present; onboarding absent | Unknown |
| Runtime context | `_shared/references/conventions/runtime-discipline.md`; `/run/vd/intent-context.json` | Coordinates must come from current context reader, not inherited environment. No target supplied. | Present | Unknown |
| CI install | `skills/install-ci/SKILL.md` deploys bundle and `.git/hooks`, commits/pushes | Outside default local scope; custom hook replacement must be resolved. | Present | Bundle/target unknown |
| Shipping | `skills/shipping/SKILL.md:22` pushes before ship approval at line 24 | Push/PR unauthorized; phase cannot be invoked. | Present with early push | Unknown |

Task 7 source capability gate is blocked. Companion change must add supported onboarding and review with compatible paths, preservation, verification and authorization semantics, then release it. Live acceptance also needs a known deployed version and existing authorized disposable target. Tasks 2–6 and available Task 8/9 checks continue.

Task 1: Ruling: initial no-guidance controls were contaminated by global memory and skill discovery; discard those results. Stop batches and rerun with explicit isolation, no control tools, and baseline reads restricted to the immutable pre-edit snapshot. Provider/model are unchanged. Cost: extra probe time; initial results cannot support behavioral claims.

### Structural/scaffold progress

- Task 2 RED: 39 focused tests, expected missing conventions/consumer API/metadata failures. GREEN: 39/39 (`task2-red.log`, `task2-green.log`). Native legacy fixtures remain read-only; `inspect_repo.py` unchanged. Documentation/routing checkpoint pending behavioral baseline inspection.
- Task 4 RED: six generated-check tests failed because templates were absent. GREEN: 45/45 focused (`task4-red.log`, `task4-green.log`). Supports custom linked ADR IDs, numeric source citations, active symmetry, rejected history/successors, native schema/config/selector checks and PR workflow.
- Task 5 RED: missing orchestration/config templates in both ordinary and enabled integration lanes (`task5-red.log`, `task5-integration-red.log`). Enabled integration GREEN: one test, exit 0, actual two dlt replace loads of one seven-row page, dbt build/data test, result 43, seven retained rows, two successful load records, renamed-copy stored-view query and four generated pytest checks (`task5-integration-green.log`). No source warehouse copied.
- First Task 5 unit rerun exposed a test harness path comparison (`/var` versus resolved `/private/var`), not a database mismatch. Normalize the fixture root once. The explicit database input is still propagated unchanged.
- Ruling: run Task 4/5 deterministic work after Task 2 structural gate while frozen pre-edit wording probes finish — it uses independent interfaces and keeps baseline prose unchanged — cost if wrong: later routing wording can require targeted revalidation.
- SDK documentation: Context7 `/dlt-hub/dlt`, `/dbt-labs/docs.getdbt.com`, `/duckdb/dbt-duckdb`; explicit DuckDB destination, dbt overrides.vars, dbt ls JSON selectors, builtins relation inclusion, Parquet/Arrow metadata checked. Official PyPI JSON fetched after read-website-fast rejected non-HTML responses. Resolved Python 3.12.12 / dlt 1.31.0 / dbt-core 1.12.6 / dbt-duckdb 1.11.0 / DuckDB 1.5.6; exact registry URLs in `sdk-versions.json`, full resolved install in `sdk-install-packages.log`.

Task 2: complete — 2026-10-16 23:21 +04; 50 focused tests passed, one explicitly gated integration skipped in `task2-final.log`; enabled integration passed separately. Five baseline convention-discovery outputs per runtime read: every old-skill trial retained rule output and lacked a canonical convention discovery route. Changed files: checker, two existing test modules, ten renamed convention templates, agents/map/schema/test-map templates and artifact-contract/compatibility references. No commit; final scoped hash index follows at Task 9.

Task 3 baseline evidence: all five Claude measurement-placement outputs repeat numeric findings inside design; the old dlt rule sends profiles to scratch. Both runtimes' five convention-discovery baselines retain rule output and no canonical skill route. Case text was pinned before edits. Baseline probes run from a complete immutable pre-edit plugin copy, never current files; remaining queued outputs remain baseline evidence for that exact snapshot, not for the modified tree. Control-v2 reads no files. Task 3 uses verified dbt overrides.vars behavior without the source's false universal project-var claim.

Tasks 4–5 complete — 2026-10-16 23:25 +04; `task4-5-final.log`: 52 pass, 1 integration skip (enabled gate passed separately). Additional ADR regression caught a silently ignored affected-design link outside mapped patterns; observed RED in `task4-unmapped-design-red.log`, fixed to report native-check/mapping gap, GREEN in final run. Changed files: generated check/workflow/scaffold templates, scaffold tests, map registrations and artifact/greenfield/brownfield references. Native customer equivalents and other platforms retain ownership. Remote workflow triggering and Studio adapter execution remain unverified.

Task 6 prose implemented — 2026-10-16 23:30 +04. Metadata RED/GREEN observed in task6-metadata-red.log and task6-package-green.log (10/10). Baseline inventory trials omit C-n/evidence/confirmation and typed review metadata; sandbox trials blur disposable versus persistent target state. Treatments pending. Corrected Claude probe metadata from captured modelUsage (firstParty); Codex provider/effort had been copied by a harness bug, not runtime routing. Raw outputs retained.

### Release and package checkpoint

2026-10-16 23:34 +04: root version 1.3.0 → 1.4.0; both child versions 1.0.0 → 1.1.0, checked against fetched base. Catalog regenerated without hand edits; catalog metadata unchanged. Marketplace, version gate, catalog freshness, Ruff check/format (including Python templates), Claude package validation and diff whitespace passed. Focused: 53 pass, 1 opt-in skip; final enabled scaffold suite: 14/14 pass, including actual seven-row repeated-load/build/renamed-copy gate.

Codex catalogue discovery works with `plugin list --available --marketplace vibedata-plugins-official --json`. Initial probe omitted --available and used an inconsistent marketplace name; that was a harness mistake. However a fresh `codex exec` with the correct local marketplace and `plugins."vibedata-repo-skills@vibedata-plugins-official".enabled=true` reports the skill absent. CLI 0.163.0 offers no session-scoped `plugin add`; normal-runtime installs are excluded by the original approved plan. Actual Codex installed-package onboarding remains blocked, with catalogue evidence distinct from runtime loading. Generated ordinary-task discovery can still run independently. Do not treat a raw path wording probe as package installation.

### Current runtime and review limits

2026-10-16 23:39 +04: Claude first-party returned HTTP 429 `usage_limit_reached`, reset reported as 04:00 +04. Stop that lane without changing model/provider. 45 controls and 45 baseline answers completed; treatment completed only part of the matrix (exact counts in final index). Custom-map onboarding and later refresh/compaction are blocked by quota. Blank fixture generated files but did not finish. Python generated context and checks completed, yet it wrote then deleted `/tmp/onb1.sha` outside its authorized fixture. Blank also used outside-fixture temporary paths and ran parse/lint beyond its probe scope. These are failed scope checks, not clean runtime acceptance. The dbt/dlt attempt to write `/tmp/onb-before.sha` was permission-denied; do not misreport that attempt as a completed write. Application hashes stayed unchanged in both completed brownfield cases.

Claude wording JSON retains the answer and reported model usage but not tool-call events. Content scoring is possible; allowed-file isolation and actual reference consultation cannot be independently proven from these logs. Future wording runs need bounded stream-json events. Codex JSONL retains tool events. No microprobe is installed-package or compaction evidence.

Coverage initially referenced deleted fixture module files (`No source for code`). RED retained in coverage-temp-source-red.log. First filename-only fix was insufficient; coverage also uses module.__file__. Final test helper executes rendered text with retained template source identity, then points module.ROOT at the disposable fixture. This preserves generated-code coverage instead of excluding it. coverage-fixture-root-report.log: 89%, exit 0. Full suite still has exactly the inherited two wiki failures.

Independent review confirmed the documented ingestion/pipelines → ingestion/sources import layout failed with `ModuleNotFoundError: No module named 'sources'`. Added actual CLI regression plus that layout to the enabled integration. Both failed before the fix (review-import-red.log, review-import-integration-red.log). Runner now prepends the ingestion root to child PYTHONPATH while preserving existing entries. GREEN result follows.

2026-10-16 23:44 +04: Real Codex ordinary Python task loaded `.agents/skills/python/SKILL.md` through the generated repository route, without explicitly invoking onboarding or naming/pasting canonical instructions in its prompt. Trace records repository-only reads; no application execution. Claude ordinary task is quota-blocked. Do not claim R14 efficiency: discovery-call comparisons were not rerun.

Real Codex app-server compaction passed: `thread/compact/start` emitted a completed `contextCompaction`, then the continuation re-read `.agents/skills/workarounds/SKILL.md` and ADR conventions, resolved `decisions/DEC-27-history.md`, and preserved `decisions/DEC-{id}-{slug}.md`. Evidence: codex-real-compaction.log and codex-compaction-evidence.json. The fixture was a copy of actual generated Python context with explicit custom-path/workaround additions from the shipped template; this proves that route's compaction recovery, not end-to-end custom-map onboarding or Studio runtime. No files were edited by either turn. Claude compaction remains quota-blocked.

Review checkpoint: the brownfield source/mart/connected-model rehearsal loaded dlt/dbt conventions, preserved source identity and named mapped read/change/check paths. It executed no application code and used no outside reads. The tiny fixture has no mart/intermediate lineage or mapped dbt selector; this proves conditional routing and honest gaps, not completed model execution. Generated brownfield pytest/jsonschema checks depend on harness PATH packages with no fixture dependency declaration; the report names the setup/CI gap.

Final: Ruling: treat the missing native-map measurement fallback as Important — observed runtime output left evidence unrecorded for a valid schema — cost if wrong: a small redundant clarification in the generated design convention. Include it in this review fix pass.

Final review fixes: generated design conventions now permit equivalent native mapped/report evidence and conditional design-area roles; shared verification requires applicable workaround reload and approved docs; temporary backup/hash evidence stays within the authorized repository. Native evidence fallback has observed RED and five GREEN answers using frozen input snapshots. Claude source/scope revalidation remains quota-blocked.

Follow-up harness correction: the first startup follow-up inherited a blanket no-commands restriction intended for the embedded-convention probe. It correctly declined file reads, so its answer is not a treatment result. Discard all green-startup followups from that batch; stop its unfinished work. Keep the five valid native-fallback outputs. The corrected startup batch permits bounded skill-file reads while excluding edits, application/network/service execution and delegation; its separate startup-labelled logs use the frozen fixed input snapshot.

Final release checks: 55 focused tests (54 pass, one opt-in integration skip); 167 full tests (164 pass, the same two inherited wiki failures, one skip); coverage 89%. The final lint run caught S102 on the coverage helper. All three callers execute only locally rendered repository-owned templates; one inline, justified S102 suppression fixes that test-only lint issue. Ruff lint/format then passed. Other release/package/catalog/compile checks passed. Enabled integration remains the unchanged-input 15/15 pass at review-import-green.log.

### Original wording matrix: independent content scores

Each cell is pass / fail / partial / blocked, out of five. These are content scores, not execution, isolation or loading verdicts. The complete nine-case matrix has 270 planned trials: 247 substantive answers, three quota errors and 20 unrun Claude treatments. Every substantive answer was inspected by the independent reviewer. No statistical or R14 efficiency claim follows.

| Case | Claude control | Claude baseline | Claude treatment | Codex control | Codex baseline | Codex treatment |
| --- | --- | --- | --- | --- | --- | --- |
| Convention discovery | 0/0/5/0 | 0/0/5/0 | 5/0/0/0 | 0/0/5/0 | 0/0/5/0 | 5/0/0/0 |
| Legacy/custom | 0/0/5/0 | 5/0/0/0 | 5/0/0/0 | 0/0/5/0 | 5/0/0/0 | 5/0/0/0 |
| Measurement | 2/3/0/0 | 0/5/0/0 | 5/0/0/0 | 3/2/0/0 | 5/0/0/0 | 5/0/0/0 |
| Startup/compaction wording | 0/5/0/0 | 0/5/0/0 | 0/1/4/0 | 0/5/0/0 | 0/5/0/0 | 5/0/0/0 |
| Page/resource | 0/0/5/0 | 0/0/5/0 | 2/0/0/3 | 0/0/5/0 | 0/0/5/0 | 5/0/0/0 |
| Sandbox state | 0/0/5/0 | 0/0/5/0 | 0/0/0/5 | 0/0/5/0 | 0/0/5/0 | 5/0/0/0 |
| Inventory/review | 0/0/5/0 | 0/0/5/0 | 0/0/0/5 | 0/0/5/0 | 0/0/5/0 | 5/0/0/0 |
| Warning equivalence | 5/0/0/0 | 5/0/0/0 | 0/0/0/5 | 5/0/0/0 | 5/0/0/0 | 5/0/0/0 |
| Non-Studio | 5/0/0/0 | 5/0/0/0 | 0/0/0/5 | 5/0/0/0 | 5/0/0/0 | 5/0/0/0 |

Warning controls/baselines already reject removed tests and changed predicates; a full raw compiled-SQL comparison is at least as strict as semantic-safe normalization. There is no measured improvement on that case. The non-Studio prompt's “native schema” is ambiguous; literal passes do not establish repo-map JSON-schema/checker ownership. Treatments name that ownership, but the controls cannot establish its absence.

Codex traces contain 685 completed reads (359 baseline, 326 treatment) and no commands in 45 controls. One baseline page/resource trial attempted a mistyped path outside the allowed root; it failed with file-not-found and returned no outside content. This is an attempted scope violation, not perfect isolation. Fourteen relative reads omit cwd in event metadata; returned content matches the supplied skill. No treatment outside absolute paths or writes were observed. Claude wording traces have no tool events, so isolation is unverified. During the live treatment batch only run_ingest.py and ignored bytecode hashes changed; convention/reference prose stayed fixed. The review followups use frozen snapshots and saved prompts instead.

### Requirement acceptance at handoff

| Requirement | Status | Evidence and open boundary |
| --- | --- | --- |
| S01 | blocked | Canonical/alias structure and Codex ordinary loading pass; actual Claude ordinary loading and Codex installed-package onboarding are blocked. |
| S02 | pass | Standalone/native ownership and conditional Studio roles pass deterministic checks; native evidence fallback passes five corrected wording trials. |
| S03 | pass | ADR/config/selector/check registration and synthetic execution pass. Remote CI remains outside local scope. |
| S04 | blocked | Measurement treatments pass in both runtimes before the final native-fallback clarification; native fallback has observed RED and five Codex GREEN trials. Claude verification of that clarification remains open. |
| S05 | fail | Codex original startup and actual compaction pass. Claude startup has one failure and four partial results; its final-fix revalidation is quota-blocked. |
| S06 | blocked | Actual seven-row page/replacement integration and five Codex wording trials pass; Claude has two passes and three quota-blocked trials. |
| S07 | blocked | Five Codex no-load/state treatments pass; Claude treatments and live Studio target evidence are absent. No load was attempted by this run. |
| S08 | pass | Enabled synthetic scaffold suite passes 15/15 with shared explicit path and renamed-copy query; no empty-scaffold business coverage claim. |
| S09 | blocked | Setup/warning contracts and Codex wording pass; Claude setup/warning lanes and actual selected Studio adapter lane remain blocked. |
| S10 | blocked | Five Codex inventory/review treatments and conditional brownfield rehearsals pass; Claude treatments, refresh/idempotence and complete customer setup remain blocked. |
| S11 | blocked | Versioned consumer gate is current and no unsupported phase runs; missing upstream onboarding/review and deployed disposable target prevent lifecycle acceptance. |
| S12 | fail | Package/version/catalog/local checks pass; runtime scope failures, blocked preservation/loading lanes and two inherited wiki failures prevent release acceptance. |

No requirement marked pass above implies complete cross-runtime or live Studio acceptance. The remaining runtime rows are required gates, not optional omissions.

Final corrected startup followups: five of five Codex answers pass; all use the frozen final plugin and retain bounded read traces. Applicable workarounds, mapped Ruff, explicit overrides.vars and approved documentation are present. These wording results do not close Claude revalidation or replace the separate real Codex compaction evidence.

### Independent review and retained decisions

The independent whole-change reviewer completed all A1–A12 groups and final fix evidence. Verdict: no confirmed implementation defect remains; **release acceptance is open**. The reviewer is completed/inactive. Detailed findings are retained at `.superpowers/sdd/2026-10-16-onboarding-vibedata-source-alignment/independent-review.md`.

Final: fixed pipeline sibling imports — observed unit/integration RED → 15/15 enabled scaffold GREEN. Final: fixed native measurement fallback — observed wording RED → five frozen-input Codex GREEN trials. Final corrected startup wording is five of five Codex passes. No additional fix pass or new reviewer was dispatched.

Final: Ruling: retain failed/unverified final Claude behavior until its original runtime reruns — quota blocks the required evidence and Codex cannot replace it — cost if wrong: scope or startup failures could survive release.
Final: Ruling: leave actual Codex installed-package onboarding blocked — no supported isolated route was established and normal-runtime installation is excluded — cost if wrong: usable package routing may be delayed.
Final: Ruling: leave end-to-end custom-map and unchanged-refresh preservation blocked — the custom fixture did not finish — cost if wrong: a preservation defect remains undetected.
Final: Ruling: leave live Studio, persistent Domain seeding, remote CI, shipping and deployed parity unverified — source capability, target and authorization gates are absent — cost if wrong: lifecycle readiness could be overstated without executed proof.
Final: Ruling: claim only synthetic scaffold correctness — no business-data acceptance ran — cost if wrong: business-specific behavior remains untested.
Final: Ruling: make no R14 efficiency, token, cost or cross-runtime improvement claim — those comparisons were not rerun — cost if wrong: possible benefits remain unmeasured.
Final: Ruling: do not claim perfect wording isolation — original traces have the documented gaps — cost if wrong: content scores could be mistaken for fully isolated trials.
Final: minor (deferred): historical trace completeness cannot be repaired retrospectively; v3 capture is prepared but not executed. Keep original Claude isolation unverified and the Codex failed outside-read attempt visible.

### Final checkpoint and restart

Completed local tasks: **1, 2, 4, 5, 9**. Failed acceptance: **3 and 8**. Blocked: **6 and 7**. This is not complete local alignment or full plan completion.

The final focused/full/coverage and release commands are indexed by `final-*.json`; lint's observed final failure and corrected pass are separate. Theme validation remains the unchanged-input nine-theme pass. Final documentation validation checked 34 local paths. No staged files, secrets or raw evidence; no commits, push, PR, merge or publication. Reference tracked files remain clean at the audited SHA. Consumer tracked files are unchanged, with its four pre-existing untracked entries still present. Submodule pins are unchanged. `inspect_repo.py` has no diff.

Retained evidence and frozen inputs are in `.superpowers/sdd/2026-10-16-onboarding-vibedata-source-alignment/`, below 50 MiB. The task-created venvs, integration environment, package caches and temporary consumer clone were removed after snapshots and dependency freeze files were saved. `environment.json` is historical; its executable paths no longer exist. Recreate only when needed using `RESUME.md`. Original probe paths in traces are historical; `retained-inputs-index.json` maps their saved inputs. `scope-index.json` and `final-scope.patch` record the final local change.

**Exact next action:** at or after **2026-10-17 04:00 +04**, verify runtime/input identities and run `python3 .superpowers/sdd/2026-10-16-onboarding-vibedata-source-alignment/probes_v3.py treatment claude` from this worktree. This prepared harness saves frozen-input prompts and bounded tool events and stops on errors. Inspect results, then resume fresh installed-package scope checks and refresh/loading gates per `RESUME.md`. No automatic retry or provider substitution is scheduled. Studio Task 7 additionally needs the supported companion release and an existing authorized disposable target.

## Gates 1–3 resumed — 2026-10-17

The user authorized the three remaining Claude, Codex and preservation gates, and excluded Studio capability work (gate 4). This numbering refers to the explanation, not implementation Tasks 1–3. Existing local-only and normal-runtime-install exclusions remain. Claude Code is now 2.1.302; its final-input v3 treatments therefore have runtime-version drift from the historical 2.1.301 baseline. All 50 answers report firstParty; 49 report `claude-opus-5-5` and native-fallback trial 5 reports `claude-sonnet-5-5`. The matrix is not uniformly Opus. Disposable pinned development and integration environments were recreated successfully; new paths are in `resume-environment.json`. New package fixtures and logs use `acceptance-v2-*`.

Codex install diagnosis: official plugin authoring docs state local installs write to the user cache and runtime loads that installed copy. CLI 0.163.0 has no scope option; the app-server install schema has no target/scope field; the current official config schema has no plugin-cache override. The plugins feature is enabled, and the native installed list has no onboarding plugin. Enablement/catalog discovery alone cannot establish loading. No normal-runtime install or home/config override was performed. Evidence: `codex-isolated-install-diagnosis.json` and `codex-current-config-schema.json`. The supported next route needs authorization for a normal-runtime install or a separately provided isolated runtime. Independent Claude and preservation verification continues.

2026-10-17 08:06 +04: the final-reference Python rerun still violated scope: `acceptance-v2-claude-python.log:70` writes `/tmp/onb-before-$$.sha`; line 76 performs wildcard cleanup outside the fixture. Its application hashes and structural checks pass, but its scope verdict is failed. The second and final prose repair at this gate promotes the boundary into the main skill before Workflow: resolve each write/cleanup inside `repo_root`, include temporary hashes/backups, and delete only exact task-created paths. Main skill is 385 words. Observed runtime RED precedes this edit; package checks pass 10/10 in `scope-fix-package-check.log`. The new immutable package is `retained-inputs/scope-fixed-plugin`; fresh `acceptance-v3-*` scope trials are in progress. The v3 wording matrix continues on its original frozen final-reference snapshot; no retroactive same-input claim is made for the main-skill addition.

Real Claude compaction now has a completed `compact_boundary`, followed by fresh reads of the workaround, ADR convention, map and `decisions/DEC-27-history.md`; all observed task reads stay in the fixture and fixture content stays unchanged. Evidence: `claude-compact-v2-{start,compact,continue}.log` and `claude-compaction-v2-evidence.json`. This retained custom-route fixture has dereferenced aliases and stale report entries, so the result proves mapped-path recovery only. Fresh alias discovery is assessed separately.

2026-10-17 08:10 +04: scope repair attempt 2 also fails. `acceptance-v3-claude-python.log` writes before/after snapshots to `/tmp/onb_before_$$.txt` and `/tmp/onb_after_$$.txt`, then removes those exact files. The final result admits the boundary violation. Application hashes and local checks still pass, but they do not cure the scope failure. Per the plan’s two-repair limit, no further prose loop is started. The unproven main-skill addition is reverted; the exact candidate package and failed traces are retained. All live plugin files again match `retained-inputs/review-fixed-plugin`, so the ongoing v3 wording results use the final live package. Gate 1 remains failed on file scope, independent of startup/loading/compaction passes. A future attempt needs a new enforcement hypothesis, not the same wording retry.

Gate 3 passes in the exercised fixtures. `refresh-v2-claude-python-hashes.json` retains the human-edited Python skill byte-for-byte, and report history is retained with a new convention row and refresh section. `unchanged-v2-claude-python-hashes.json` has 18/18 identical file hashes; the harness also asserts unchanged aliases. The custom fixture retains all 11 non-instruction originals exactly, including its native map/schema/checker, glossary, DEC-27, legacy rule and existing Claude Python skill. AGENTS retains its exact original prefix; two added aliases remain contained. Evidence snapshots preserve actual symlinks under `retained-inputs/resumed-acceptance`; `resumed-fixtures-index.json` records file hashes and link destinations. A two-sided pre-existing canonical/Claude skill collision remains wording evidence, separate from the actual existing-Claude-skill collision.

Gate 1 has a second boundary failure beyond temporary files: `acceptance-v2-claude-dbt_dlt.log:61` runs `dbt --version`, whose result queries the current release; the final response admits the network request. All seven original files retain their hashes. Its native map test fails on missing `items.config_section`, correctly named as a setup gap; structural success does not mean native checks are green. No application/pipeline load was run. Ordinary Claude loading now passes on the generated Python fixture without an onboarding invocation.

## Codex-only continuation — 2026-10-17 08:30 +04

The user stopped further Claude testing. The completed wording batch returned exit 0; collecting that result and reviewing its saved outputs launched no new test. The independent reviewer completed all 50 saved answers: 44 full content passes, 6 partial; 120/130 assertions pass and 10 are partial. All 50 wording scope checks pass across 235 tool events. Twenty-two answers exceed the requested word cap. Actual-package scope failures remain failed, independently of these wording scores. The reviewer is complete.

Two new Codex ordinary-task checks passed at 08:29 +04 on fresh copies of the retained generated contexts. Neither prompt invoked onboarding or supplied canonical instruction filenames. Every one of the ten tool calls was a repository-only read/list operation; all returned exit 0. The Python task loaded the canonical Python convention, found the preserved human field-order rule, located `load_items` and identified the missing business tests/Ruff command. The custom task loaded canonical vocabulary/ADR conventions, resolved the native map and DEC-27, preserved native schema/checker ownership and correctly refused to invent an authorized next identifier.

All 18 Python file hashes and three contained symlinks, and all 16 custom file hashes and two contained symlinks, remain unchanged. These are generated-context loading passes, not Codex installed-package onboarding or Codex refresh evidence. The source fixtures were created by the earlier Claude runs. No efficiency claim is made. Evidence: `ordinary-v3-codex-{python,custom}.{json,log}`, saved prompts, `codex-only-loading-evidence.json` and `codex-only-fixtures.json`.

CLI remains 0.163.0. The current user config was observed as `gpt-6.1-sol` / `high` / `omniroute`, which differs from preflight. Commands explicitly requested the historical `gpt-6-astra` / `xhigh` / `omniroute` route for this comparison; no global configuration was changed. The CLI event stream does not independently identify the served model. All configured MCP integrations were disabled per session. No HOME/CODEX_HOME override, installation, Claude invocation, application execution or Studio operation occurred. Fresh temporary copies were removed at 08:30 +04 (114,813 bytes); retained inputs remain.

**Remaining gates:** 1 failed with further Claude tests excluded; 2 blocked on installed-package scope; 3 passed for the exercised fixtures; 4 excluded. The live plugin still matches all 47 retained reviewed files. Historical deterministic suites are unchanged and were not rerun. Branch/HEAD and both submodule pins remain unchanged; staging is empty. The current scope/evidence index is `codex-only-scope-index.json`; historical `scope-index.json` remains intact.

**Superseded next action:** the temporary normal-runtime installation in `pending-codex-install.md` was not run. The user subsequently declined this test and authorized draft PR preparation. Installed-package onboarding remains unverified; no installation approval is pending.

## Draft PR preparation — 2026-10-17

The user approved committing the scoped implementation and documentation, checking against current `main`, pushing the branch and opening a draft PR. Include the source audit required by the plan's links. Keep `.cache/` and raw evidence local. No additional Claude tests, installed-package tests, Studio work, merge to main or release publication are included.

Fetched `origin/main` remains `b878bf81be9301ec1f21729a021846e780e107b1`. It includes the earlier onboarding PR #48 as a squash and the separate wiki fixes from PR #47. Integrate that base into this feature branch so the new PR contains only the alignment changes and retained dependency documentation. Recheck the changed CI/wiki boundary after integration; historical two-failure results remain historical.

GitHub confirms PR #48 is merged and explicitly records no associated Linear issue. No issue for this follow-up is identified. The draft will state this tracking gap instead of borrowing the source repository's VD-6914 or inventing a ticket. The previously failed Linear authentication is not retried.

At 08:39 +04, branch integration is complete: implementation commit `97a7011`, followed by merge `404d320` from `origin/main@b878bf8`. Every one of 27 conflict resolutions was checked against an identical historical input from `d07d1a8` or `36ab98d`; the reviewed alignment content was retained. Ten deleted legacy rule templates reintroduced by the squash-history merge were removed again. All 68 scoped input hashes/deletions match the pre-merge checkpoint. The incoming wiki fixes, tests and CI match main exactly and are outside the PR diff. No force-push or history rewrite was used.

Fresh post-integration checks on `404d320`: **169 tests, 168 passed, one opt-in integration skip, zero failures; coverage 89%**. The two historical wiki failures are resolved by main's existing PR #47 changes. Marketplace validation, root version increase `1.3.0 → 1.4.0`, catalog freshness, Ruff lint and formatting all pass. The previously enabled 15/15 scaffold result remains valid for byte-identical plugin inputs and is not reported as a new integration run. No new Claude or installed-package test ran. Evidence: `pr-full-suite`, `pr-coverage`, `pr-marketplace`, `pr-version`, `pr-catalog`, `pr-lint` and `pr-format` JSON/log files in the retained workspace.

The remaining acceptance gaps concern runtime behavior and tracking: captured Claude package-scope violations remain unresolved; Codex installed-package onboarding is skipped/unverified by user decision; Studio is excluded; no Linear issue is linked. Keep the PR draft and report remote CI separately from these local results. Python compilation and 35 local documentation file targets also pass; documentation anchors were not checked. The next step after opening is review of the draft and its CI results.
