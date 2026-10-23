# Onboarding reference refresh implementation plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task by task. The user authorized unattended execution through PR creation.

**Goal:** Bring reusable onboarding and subsequent maintenance to the current reference repository contract.

**Architecture:** Reuse the existing portable workflow and checks. Seed the proven semantic authoring/review bundle only when applicable; retain native customer contracts. Extend the shared map checks and conditional Studio assessment.

**Tech Stack:** Python standard library, existing unittest/JSON Schema/PyYAML checks, reference Typer CLI and pinned Apache Ossie schema.

**Spec:** [Full audit and R1–R7](../../reviews/onboarding-reference-audit-2026-10-23.md).

## Global constraints

- Worktree: `/Users/shwetanksheel/.codex/worktrees/c80f/vibedata-official`, branch `feat/onboarding-ossie-reference-refresh`.
- Reference and consumer repositories are read-only; no warehouse execution or production mutation.
- Keep one marketplace onboarding skill; use non-discoverable seed entrypoints to avoid discovery before installation.
- Preserve customer instructions, map extensions, native validators, unknown business meaning and explicit invocation.
- Never hand-edit generated catalog or README blocks. No merge, force-push or branch deletion.

## Review focus

1. Existing human-modified semantic skills and non-default paths survive refresh.
2. A model glob or runner path cannot escape through a symlink; empty matches fail.
3. Two sources share a schema, an external runner has no local file, or a custom builder has no default test module.
4. A structurally green aggregate can still represent the wrong population or metric.
5. A successful sandbox build cannot erase the inherited-view finding or certify the persistent Domain.

## Task 1: Audit and baseline

**Files:** Audit above; this plan; validation evidence below.
**Interfaces:** Consumes pinned reference/package. Produces R1–R7 and dispositions A01–A15.

- [x] Inspect all package categories and corresponding reference behavior; identify conflicts and source-only consumer support.
- [x] Run baseline onboarding suite: 62 passed, one optional integration skipped.
- [x] Capture fresh-agent current-package retrieval/application baseline before skill edits.
- [x] Record failed regression tests before implementation.

## Task 2: Maps and inventory (R3, R4, R6)

**Files:** `scripts/{inspect_repo,validate_context}.py`, `templates/{repo-map.json,repo-map.schema.json,checks/test_maps.py}`, `tests/test_onboarding_{context,scaffold,package}.py` under existing package/root test paths.
**Interfaces:** Consumes existing map; adds optional `orchestrators` entries (`kind`, `runs`, `path` or `location`) and `sources.*.produces`; keeps `validate_context(root, consumer=...)` signature.

- [x] Add failing tests for inventory of Ossie files; confined existing globs and missing/escaped globs; local/external runners; unknown/orphan members; shared producers and custom builders.
- [x] Extend existing functions and schema; keep checks free of application execution.
- [x] Exercise generated native map checks with those cases, then the existing context/scaffold suite.

## Task 3: Semantic delivery and maintenance (R1, R2, R6)

**Files:** `references/semantic-model.md`; `templates/semantic/{semantic-model,validating-semantic-model}/`; selected existing convention/report templates; `tests/test_onboarding_semantic.py`; dependency declarations and provenance.
**Interfaces:** Consumes confirmed marts and `artifact_paths.logical_model`; emits the two repository skills, CLI dependencies and mapped test commands. Existing custom skills remain owned by the customer.

- [x] Add failing delivery tests for complete seeds, valid generic model, malformed model, cross-document identity drift and stale generated level checks.
- [x] Copy reference tools/schema/examples with upstream licensing; resolve the audit's contradictory prose. Generalize paths and examples; do not copy customer canonical data.
- [x] Add creation, refresh, custom-path, no-gold and later-mart routing; register commands and tests without blank model artifacts.
- [x] Run CLI on emitted disposable skills and examples; mutate invalid fixtures and require failures; check data tests remain reported separately.

## Task 4: Complete audit corrections (R5, R6)

**Files:** Main skill; `references/{artifact-contract,brownfield,greenfield,studio-duckdb}.md`; `templates/skills/{dlt,dbt-models,design-records}.md`; report; scenario fixtures.
**Interfaces:** Consumes source inventory and semantic bundle. Produces complete onboarding/maintenance routes and inherited-view assessment.

- [x] Add explicit hidden-rule inventory, map/runner maintenance, population ownership and inherited-before-write assessment.
- [x] Update current source capability observation while keeping historical evidence labelled.
- [x] Run fresh-agent application scenarios with treatment; inspect each answer and correct omissions. Keep retrieval probes distinct from actual runtime/warehouse evidence.

## Task 5: Release and PR (R7)

**Files:** Dual child manifests, root plugin manifest, generated catalog as needed, this plan and validation record.
**Interfaces:** Consumes final diff/evidence. Produces one open PR from new branch with exact checks and limitations.

- [x] Bump child to 1.2.0 and root to 1.5.0; no marketplace entry change.
- [x] Run catalog generation/check, marketplace/version gates, lint/format, compile, full coverage suite and whitespace check. Run supported optional integration if its dependencies are available in a disposable environment.
- [x] Obtain independent whole-change review; fix important findings with RED/GREEN evidence.
- [ ] Commit named files, push branch via SSH/443, create PR, inspect head and CI, resolve in-scope CI failures.
- [ ] Send completion notification and leave self-contained audit, plan, validation and PR links.

## Verification mapping and execution ledger

| Requirement | Concrete gate |
| --- | --- |
| R1, R2 | Emitted semantic CLI tests plus fresh-agent application scenarios and source-content review |
| R3 | Context and generated map negative/positive tests |
| R4 | Inventory and glob path security regression tests |
| R5 | Baseline/treatment scenario and explicit ordered contract review; live sandbox unverified without target |
| R6 | Existing 62-test regression suite, preservation scenarios, source checkout status |
| R7 | CI-equivalent local commands, independent review, remote PR head and checks |

Execution evidence: `docs/reviews/onboarding-reference-validation-2026-10-23.md`.
