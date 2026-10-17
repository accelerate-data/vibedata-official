# Studio onboarding lifecycle implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` for native execution, then an independent whole-change review. The user's 2026-10-15 instruction to execute the handoff unattended authorizes this plan within its stated scope. Task 1's consumer capability gate still applies. Steps use checkbox syntax.

**Goal:** Explicit Studio onboarding proceeds from repository discovery through supported setup, sandbox verification, certification and one remotely verified PR, with failures reported at their actual stage.
**Architecture:** Keep the shared user-invoked skill and its short core workflow. Add one conditional `references/studio-lifecycle.md` that composes supported consumer capabilities; reuse `studio-duckdb.md` for platform checks and the existing artifact/report contracts. Do not create another workflow engine or copy the upstream skills.
**Tech stack:** Existing Markdown/JSON skill package, Python structural checks, repository unittest/Ruff tooling, native Claude/Codex trials and the deployed Studio consumer.
**Spec:** User-requested lifecycle extension and requirements below, extending [the current design](onboarding-vibedata-design.md). The existing preparation-only publication boundary changes only for an explicitly requested Studio lifecycle.
**Status:** Execution authorized; blocked at Task 1's supported-consumer gate. **We have not added VD onboarding: the full VibeData Studio lifecycle is not implemented.** The existing skill prepares and refreshes repository context. PR #48 was merged by `admiraldata` on 2026-10-15 at 20:39 +04; GitHub records no submitted review. The [Task 1 dependency report](onboarding-vibedata-validation.md#studio-lifecycle-task-1-consumer-dependency-report) pins historical upstream source, its side effects and the separately scoped work needed to continue. Implementation baseline: `f9908cc`; execution baseline: `36ab98d`; reference: `sample-nyctaxi-comp@349d026`. Continue from the [agent handoff](../docs/handoffs/onboarding-vibedata-studio-lifecycle.md).

**Current gate, 2026-10-16 23:07 +04:** Refreshed upstream source `65222435e3483c4be0a612e20910abfbaf56d9cb`, plugin 0.128.12, still lacks onboarding kind and supported onboarding review. Generic verification now writes Domain-mapped Verification; do not apply the older certification-path observation to this version. Runtime coordinates come from `/run/vd/intent-context.json`. CI installation/verification commit and push; shipping pushes before final approval. Deployed version, bundle and authorized disposable target are unknown. The [alignment plan](../docs/superpowers/plans/2026-10-16-onboarding-vibedata-source-alignment.md) Task 7 stays blocked; independent Tasks 2–6/8–9 continue. No lifecycle reference is created. See the [current capability table](onboarding-vibedata-source-alignment-run.md#current-consumer-capability-table).

## Contents

- [Requirements](#requirements)
- [Constraints and integration findings](#constraints-and-integration-findings)
- [Review focus](#review-focus)
- [File responsibilities](#file-responsibilities)
- [Implementation tasks](#implementation-tasks)
- [Verification and release gate](#verification-and-release-gate)

## Requirements

| ID | Observable behavior |
| --- | --- |
| L01 | Explicit onboarding into Studio selects the complete lifecycle. Standalone repository preparation and refresh remain available without Studio dependencies. Both runtime controls continue to disable implicit invocation. |
| L02 | Before lifecycle side effects, the skill identifies the selected Domain/platform, runtime/plugin version, intent branch, artifact paths, capabilities, CI bundle, authorization and disposable execution target. Missing prerequisites produce named blockers. |
| L03 | Requirement, plan and certification artifacts use paths and formats accepted by the deployed consumer. Existing customer maps, instructions, glossary and ADR history retain their preservation guarantees. |
| L04 | The agent prepares concrete setup/CI diffs, applies changes within the user's existing authorization, and asks only for uncovered decisions. Business logic repairs, production loads and infrastructure creation remain outside onboarding. |
| L05 | The selected sandbox executes applicable dependency, parse, build, native map, Python, lint and data checks. On DuckDB, existing views also resolve in a renamed database copy without rebuilding. Greenfield empty parses are labeled as scaffold evidence. |
| L06 | Onboarding review records findings and verifies instruction preservation, map routing, ADR/design consistency and later-task discovery. Certification is complete only when required checks have current evidence. |
| L07 | The supported shipping path commits/pushes within authorization and creates or reuses one PR. The remote PR, head SHA and CI results are verified. No merge or production publication occurs. Failed required CI leaves completion blocked and the PR draft. |
| L08 | The report distinguishes context readiness, Studio verification and PR/CI outcome. Missing runtime evidence cannot become a completed Studio onboarding. Resume preserves decisions and history and avoids duplicate PRs or repeated valid work. |

## Constraints and integration findings

- Keep implementation in the named worktree and branch. Preserve unrelated work and submodule pins. PR #48 is merged and cannot serve as the active implementation PR. A later implementation needs a new PR; its merge does not establish lifecycle completion. L07's draft rule applies to PRs produced by the future customer workflow.
- Preserve one skill, explicit-only invocation, bounded discovery, native map/checker contracts and the three-section report. Put Studio orchestration behind one conditional link; target a main skill under 400 words.
- Source/SDK/runtime facts must be checked against the selected deployed version before commands or scaffolds are authored. Authentication failures stop the affected operation.
- No provisioning, Domain creation, seeding, production writes, destructive Git operations or automatic merge. Use small synthetic fixtures and bounded temporary storage; never copy the reference warehouse.
- The existing acceptance of an unverified consumer lane remains recorded. It does not establish acceptance of the new end-to-end lifecycle. Implementation and local tests can finish without a live environment; the new release gate cannot.

Historical 2026-10-15 read-only inspection found a concrete dependency gap in local `vibedata-data-engineering@ef128cac`, manifest version `0.127.2`:

1. `lib/kinds/registry.json` has no `onboarding` kind.
2. The reference calls a `reviewing` skill that is absent from this checkout.
3. `install-ci` deploys files/hooks and commits/pushes; `verifying` also commits/pushes. Shipping's PR approval occurs after an earlier branch push. Wrapping these calls in prose does not remove their side effects.
4. Requirements/plans/certification follow the consumer's artifact-path contract, including `VD_INTENT_DOCS_ROOT`; arbitrary map paths alone cannot override executable checks.

This checkout is not proof of the deployed runtime version. Task 1 must find a supported release or identify a required companion consumer change. Do not pretend onboarding is another kind, invoke a missing skill, or bypass native certification/shipping checks. The consumer repository remains read-only under the current scope; a required upstream implementation is a separately scoped dependency, not a hidden edit in PR #48.

## Review focus

1. A standalone refresh must not acquire Studio dependencies or publication side effects: Task 2's standalone probe.
2. A partial CI installation with custom configuration/hooks must preserve ownership and worktree boundaries: Task 3's partial-install scenario.
3. Custom artifact locations must remain compatible with executable certification/shipping checks: Tasks 1 and 4's consumer-contract and wrong-path checks.
4. A delegated skill that commits/pushes before its final approval must not escape the requested authorization: Tasks 1 and 4's side-effect and authorization cases.
5. A resumed run with changed code, data or tool versions must invalidate stale evidence without duplicating the PR: Task 4's stale-evidence and resume cases.

## File responsibilities

Let `S` denote `plugins/vibedata-repo-skills/skills/onboarding-vibedata` in this document only.

| File | Planned responsibility |
| --- | --- |
| `S/SKILL.md` | Select complete Studio lifecycle versus standalone preparation and replace the blanket publication prohibition with the scoped authorization contract. |
| `S/references/studio-lifecycle.md` (new) | Preflight, native phase handoffs, setup/CI side effects, review, certification, shipping and resume conditions. |
| `S/references/studio-duckdb.md` | Keep one source for platform-specific setup and renamed-copy checks. |
| `S/references/{artifact-contract,compatibility,greenfield,brownfield}.md` | Align branch behavior, selected-runtime execution and native consumer artifact requirements. |
| `S/templates/{onboarding-report.md,rules/git-and-prs.md,greenfield/README.md}` | Record lifecycle outcome without new mandatory report sections; align publication and Studio scaffold behavior. |
| `tests/onboarding/studio-lifecycle.json` (new) | Baseline/treatment scenarios, negative cases and real consumer acceptance criteria. |
| `tests/test_onboarding_package.py` | Existing invocation, link, artifact and packaging checks extended only where the new contract has a mechanical assertion. |
| `context/onboarding-vibedata-{design,plan,validation}.md` | Current approved scope, implementation status, pinned consumer contract and evidence. |

## Implementation tasks

### Task 1: Establish a supported consumer contract

**Deliverable:** A versioned capability/side-effect table in the validation record, with a runnable native path or an explicit upstream dependency. This task gates downstream lifecycle wiring.

- [ ] Identify the deployed consumer version and supported onboarding entrypoints; compare with the inspected local snapshot.
- [x] Verify kind registration, the actual review capability, runtime wrapper, CI bundle contract, artifact paths and certification/shipping checks in pinned upstream source. Source anchors include consumer `lib/kinds/registry.json`, `skills/{install-ci,verifying,shipping}/SKILL.md` and `_shared/references/conventions/artifact-paths.md`. Deployed bundle contents and execution remain unverified.
- [x] Record which operations write files, alter hooks, commit, push, publish a PR or require native approval; map them to the requested Studio scope before invoking anything.
- [x] If onboarding support is absent, define the minimal companion consumer change and its acceptance tests before proceeding. Use an onboarding playbook/registered capability where required; do not disguise onboarding as transformation. Resolve the missing review stage through a supported implementation before wiring it here.

**2026-10-15 result:** Dependency report complete; Task 1's gate remains blocked. Upstream `df262dc` still carries plugin `0.127.2`, no onboarding kind and no supported onboarding review entrypoint. No deployed runtime or disposable Domain is identified. Tasks 2–4 cannot consume a supported phase contract; Task 5's live acceptance cannot run. See the validation record for companion scope and concrete acceptance checks. No upstream implementation or provisioning is authorized.

**Gate:** Every delegated operation exists and accepts the intended artifacts. Any upstream change needs its own approved scope and supported release; a missing capability blocks the full path while independent context work remains possible.

### Task 2: Add the conditional lifecycle workflow

**Deliverable:** `studio-lifecycle.md` plus a short core pointer and aligned design/authorization boundaries. Consumes Task 1's supported capability table; produces the phase contract used by Tasks 3–4.

- [ ] Add baseline scenarios for requested Studio onboarding, standalone refresh, missing capability and existing publication authorization; run them against the current skill before editing.
- [ ] Define the sequence: preflight → requirement/design/plan → context/setup → onboarding review → verification/certification → shipping → remote CI outcome. Reuse existing consumer phase artifacts and guards.
- [ ] Route explicit Studio onboarding through that sequence; retain standalone preparation without extra runtime requirements. Keep both explicit-invocation controls unchanged.
- [ ] Align `SKILL.md`, branch references, compatibility rules and `git-and-prs.md`. Preserve exact-diff approval for uncovered compatibility changes and existing authorization; do not add duplicate shipping questions or assume a downstream commit/push is harmless.

**Gate:** Fresh treatment probes follow the complete requested path, stop at unsupported dependencies before side effects, and leave standalone behavior intact.

### Task 3: Integrate setup, CI and sandbox checks

**Deliverable:** The lifecycle performs supported setup and checks instead of stopping at recommendations. Consumes the approved target, capability contract and exact setup diff.

- [ ] Add scenarios for CI absent/partial/complete, customized configuration/hooks, pending or declined setup diffs, unknown Domain state and unavailable sandbox.
- [ ] Inventory and run permitted baseline checks before setup changes. Apply approved profile/macro/source changes using `studio-duckdb.md`; preserve business behavior and native validators.
- [ ] Invoke the supported CI path with its actual file/hook/commit/push scope. Preserve custom configuration and worktree boundaries; report required repository-owner synchronization or missing permissions without inventing values.
- [ ] Run mapped dependency, parse/build, map/schema, selector, Python, lint and applicable data checks in the selected sandbox. Require the DuckDB renamed-copy check where applicable; keep sample/production boundaries.
- [ ] Add only the missing Studio greenfield scaffold pieces required by the pinned contract, using supported templates/packages. Do not register fictional sources/models or claim an empty build tested business data.

**Gate:** A failed check is recorded with its scope and effect; unavailable targets stay blocked/unverified. Approved setup is exercised, and existing customer configuration or application logic is not silently replaced.

### Task 4: Complete review, certification and PR publication

**Deliverable:** One remote PR with current evidence, or a precise blocked stage. Consumes Task 3's outputs and checks; uses the deployed certification and shipping formats.

- [ ] Add scenarios for review findings, failed gates, stale evidence, wrong certification path, publication not authorized, existing authorization and resuming an existing PR.
- [ ] Run the supported onboarding review: instruction preservation, native maps/checks, glossary/ADR/design consistency and source/model/domain-task routing. Record genuine findings; do not fix unrelated bugs.
- [ ] Produce native certification from actual command results, commit/input identity and target data. Keep the onboarding report's Changes, Checks and Blockers sections; add Studio/PR status only when selected.
- [ ] Follow native shipping approval and side-effect rules, create or reuse one PR, verify its remote head, and inspect CI for that head. Preserve a draft/blocker when required checks fail; do not merge.
- [ ] Resume from existing artifacts and decisions. Reuse checks only when covered files, tools and relevant data/environment remain unchanged, with native currency checks still applied.

**Gate:** Successful completion has a remote PR URL, matching head and required passing checks. Missing or stale evidence cannot be certified, and retries do not create a duplicate PR or repeat approved decisions.

### Task 5: Verify and update the implementation PR

**Deliverable:** Local regression results plus real consumer evidence for the complete lifecycle, with limitations stated separately.

- [ ] Run fresh baseline/treatment skill trials and inspect actual actions against `studio-lifecycle.json`; test at least five fresh trials for wording-sensitive authorization/resume boundaries. Use bounded disposable repositories, keeping assertions outside the agent's fixture.
- [ ] Run the focused suite, full suite, Ruff, compilation, marketplace/version checks, generated-catalog freshness and manifest checks. Reuse existing commands from the validation record; baseline remains 30 focused tests and two inherited wiki failures in the full suite.
- [ ] Run one real greenfield and one real brownfield Studio onboarding using an existing disposable Domain or supported harness and a test repository. Verify actual loading, sandbox commands, CI installation where needed, certification consumption and one remote PR. For brownfield DuckDB, include stored views in a renamed copy without rebuilding.
- [ ] Independently review the final change, record both implementation and live-test evidence, and update the implementation PR. Check PR #48's current state before continuing; retain its user-requested ready status if it remains the active PR. Keep plugin/root versions consistent with repository release rules and regenerate catalogs only through the generator.

## Verification and release gate

| Requirements | Concrete check |
| --- | --- |
| L01–L02 | Invocation-policy regressions; Studio/standalone and missing-capability probes; runtime capability inspection. |
| L03–L04 | Custom-path/native-schema scenarios; CI none/partial/complete cases; declined/pending diff preservation; observed commit/push authorization boundaries. |
| L05 | Real sandbox command results; native validator/selector results; renamed-copy data tests; honest empty-scaffold case. |
| L06 | Review findings, ADR/design consistency and later-task routing; native certification reads actual evidence. |
| L07–L08 | Remote PR URL/head/CI verification; failed/stale/unauthorized shipping cases; resumed run reuses one PR and valid evidence. |

No live environment is currently available. Do not provision one as an implied plan step. The complete implementation may be reviewable with that lane blocked, but neither the skill nor PR may claim demonstrated end-to-end Studio onboarding until the live acceptance runs pass. The two inherited wiki failures remain separate from lifecycle evidence and must still be reported in PR status.
