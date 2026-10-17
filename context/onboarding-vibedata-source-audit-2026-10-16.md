# Onboarding VibeData: source alignment audit

Date: 2026-10-16, workstation zone +04 (Asia/Dubai).

## Result

The skill needs coordinated changes to its generated convention skills, map contract, validation, documentation rules and conditional Studio workflow. Changing `SKILL.md` alone will leave incompatible generated repositories. The existing generic preservation and non-Studio behavior should remain.

This audit identifies 12 change groups. “Required” means required to match the named reference in the applicable mode. It does not mean the existing standalone context workflow is broken in every environment. Several Studio lifecycle gaps were already recorded before the latest source changes.

No skill, application, source-reference, manifest, test or prior planning file was changed. This report is the only repository addition. No commit, push, PR, data load or deployment was performed.

## Inputs and scope

| Input | Revision / scope |
| --- | --- |
| Target repository (`T`) | `/Users/shwetanksheel/scratch/ad-plugins/.worktrees/vibedata-official-onboarding-vibedata-plan`, branch `docs/onboarding-vibedata-plan`, `d07d1a8538cc52826373211110c96df9d3f090b5` |
| Target skill (`K`) | `T/plugins/vibedata-repo-skills/skills/onboarding-vibedata`, 33 files |
| Source repository (`S`) | `/Users/shwetanksheel/scratch/vibedata-showcase/sample-nyctaxi-comp`, branch `main`, `b75841f12c14ad8e1870d1b1581d6bd59a0fb5bf` |
| Source onboarding (`O`) | `S/.agents/skills/onboarding`, 40 files |
| Last recorded source refresh | `349d026`, explicitly recorded in `T/context/onboarding-vibedata-validation.md:326`; incorporated by target commit `f9908cc` |
| Source delta | 42 commits; 68 files changed, including renames; `git diff --stat 349d026..b75841f` reports 541 insertions and 525 deletions |

Both working trees were clean at the start. The comparison used the complete source delta and current onboarding instructions, references, templates, nine convention skills, the local `reviewing` skill, maps, map/ADR tests, repository checks and relevant setup decisions. It also covered both target helpers, all target templates/references, packaging, focused tests, behavioral scenario definitions and the previous lifecycle handoff.

This is an audit of the supplied local snapshots. It is not a warehouse correctness audit, a check of unpublished source commits, or proof of the deployed Studio consumer. Source issue statuses below are statements in the local source documentation, not freshly queried Linear statuses.

Evidence paths use `T`, `K`, `S` and `O` as defined above. Line numbers refer to these pinned snapshots.

## Required changes

### 1. Generate convention skills and support their actual structure

**Priority: high. New source contract. Applies to generated context.**

The source moved operator conventions from `.agents/rules/<name>.md` to `.agents/skills/<name>/SKILL.md`. Each has `name` and a task-triggering `description`; `AGENTS.md` tells the runtime to invoke the relevant skill. This was shipped in source commits `9f5bee4` and `ac21d2f`, tracked there as VD-6914.

Our map and test-map still point at `.agents/rules/`, our templates have no skill frontmatter, and our routing says to read rules. The difference affects runtime discovery, not just naming.

The helper also needs a bounded update. Its required reference is `rules`, and it recursively treats every Markdown file under that directory as live instruction content. Two audit probes established that a simple migration is insufficient:

- Renaming only the map key to `conventions` produces `key_references: missing rules`.
- Pointing `rules` at a skill directory with a valid `SKILL.md` and an inactive template produces a false error on the template's `{{rule_path}}` placeholder.

**Change:** emit convention skills with narrow descriptions; update bootstrap routing, map references and maintenance wording together. Preserve existing legacy rules and native checker contracts during refresh. Validate active skill metadata and applicable instruction references without treating unused scaffolding templates as live policy. Keep distributed convention templates named `<name>.md`; render `SKILL.md` only in the destination repository, so the plugin does not accidentally publish every template as another installed skill.

Verify each selected runtime's supported discovery path. The source's `.agents/skills/` convention alone does not prove automatic Claude, Codex and Studio discovery. Use a supported route to the single canonical copy where a runtime needs one.

`inspect_repo.py` already discovers the new directory: it found all 11 source project skills as context artifacts. A new inventory framework is unnecessary.

**Evidence:** `O/references/base-setup.md:56`, `O/templates/repo/AGENTS.md:20`, `O/templates/repo/repo-map.json:83`; `K/templates/repo-map.json:22`, `K/templates/test-map.json:11`, `K/templates/rules/`, `K/scripts/validate_context.py:21`, `K/scripts/validate_context.py:295`; `T/tests/test_onboarding_package.py:103` and `:149`.

**Verification:** generated skills appear in fresh selected-runtime discovery; ordinary model/source tasks load the appropriate convention; old rules remain usable; malformed frontmatter is rejected; inactive templates do not cause false failures; migrated links and unchanged reruns preserve content.

### 2. Add the five newly explicit artifact roles

**Priority: high. New source contract. Required for Studio-facing context.**

The source now declares `requirement`, `plan`, `verification`, `case_record` and `design_record_area`. Per-intent filenames use `{intent}`. The map determines location; the consumer determines the intent name. Our template declares none of these five roles and still passes our structural validator.

**Change:** generate the applicable roles and documented filename ownership. Resolve area design and verification destinations from the map. Update the owned schema/checker and Studio readiness checks together. Preserve custom paths, extensions, native schemas and the existing `onboarding_report`; it is a status report, not a replacement for an intent's verification artifact. Require Studio-specific roles when that consumer needs them, without forcing irrelevant intent machinery into a standalone Python repository.

The source also carries adapter-specific roles such as `dbt_project`, `dbt_sources`, `source_config`, `resource_docs` and `source_tests`. Include these when generating the corresponding dbt/dlt scaffold, using actual paths. Do not replace a customer's broader map with our smaller template.

**Evidence:** `O/templates/repo/repo-map.json:25`, `O/references/base-setup.md:87`; `K/templates/repo-map.json:10`, `K/templates/repo-map.schema.json:78`, `K/scripts/validate_context.py:12`, `K/references/artifact-contract.md:32`.

**Verification:** a Studio fixture missing any required role is incomplete; custom role paths survive refresh; pattern paths need no fabricated document; a later task resolves requirement, plan, verification, case and area-design locations without guessing.

### 3. Enforce ADR/design symmetry and run repository checks in CI

**Priority: high. New source delivery. Applies where ADR/design conventions are selected.**

The source added `tests/test_adr_links.py`, a `decisions` test-map module and a separate `repo-checks.yml` workflow. Its citation checker and backlink checker have distinct jobs. Our ADR/design prose already says to maintain links, but no generated check proves that both directions agree, and no workflow ensures repository checks run.

**Change:** preserve a suitable existing check, otherwise add a small backlink check for the confirmed ADR format and mapped design locations. Register its real command in the maps. Reuse existing CI where it runs the checks; otherwise propose/install the repository-owned workflow within the authorized scope. If hooks are selected, preserve the CI bundle's installed hooks: setting `core.hooksPath` can bypass `.git/hooks`.

Do not copy the source test verbatim into a custom-path repository: it hardcodes `docs/adr`, `docs/design`, four-digit identifiers and `## Affected designs`. The generic skill must either adapt to the selected convention or state that the format is unsupported. Preserve the native map tests for JSON Schema, dlt config sections and dbt selectors; the portable path checker is not equivalent.

**Evidence:** `O/templates/tests/test_adr_links.py:5`, `:33`, `:44`; `O/templates/repo/test-map.json:38`, `O/templates/repo/repo-checks.yml:1`, `O/references/base-setup.md:47`, `:54`; `K/templates/rules/adr.md:6`, `K/templates/rules/design-records.md:6`, `K/references/artifact-contract.md:44`.

**Verification:** fail on each one-sided link, missing listed design, and stale successor citation; pass custom paths and preserved numbering. Run the workflow's command in one interpreter with its declared dbt/test dependencies. Verify checks are actually triggered by the configured PR workflow.

### 4. Keep measurements out of design records

**Priority: medium. Explicit source policy change. Applies to document generation.**

The source replaced its `Evidence` section with `No evidence` and removed measurements from existing design records. Counts, profiles, reconciliation figures and check results belong in the intent's verification file. Design records retain decisions, rationale and links to the verification that informed them.

Our template still says “Record non-obvious component decisions with evidence,” and the dlt template says a saved profile is reused “for design and verification.” Those statements do not make the new distinction clear. They can produce the duplication the source just removed.

**Change:** specify decision provenance versus measured results. Keep decisions, alternatives, ADR links, lineage consumers and history in the design record; put measurements and check outcomes in mapped verification. Add the shared area-design route from finding 2. Preserve existing customer documents during a refresh; any movement of content needs retained destinations and repaired links.

**Evidence:** `S/.agents/skills/design-records/SKILL.md:25`, `O/SKILL.md:56`, source commit `f7bf91d`; `K/templates/rules/design-records.md:4`, `K/templates/rules/dlt.md:8`.

**Verification:** a fixture whose decision is informed by profiling produces a qualitative reason and verification link in design, with the numeric evidence only in verification. No redundant record is created when the code already explains the choice.

### 5. Carry the new startup, test-variable and command-routing conventions

**Priority: medium. New and clarified source guidance. Applies conditionally by task/runtime.**

The source now explicitly forbids reading installed library implementation code to infer behavior. It directs agents to repository examples and library documentation. It invokes the relevant convention at task startup and re-invokes `workarounds` after condensation. Python lint must use the mapped Ruff command, rather than a platform tool with different rules. The latest dbt-testing convention makes unit-test vars explicit with `overrides.vars`.

Our bootstrap covers reading the map once and avoiding maintenance/evaluation material. It lacks the library-source restriction and compaction routing. Our dbt-testing template lacks the explicit unit-test-variable convention; our Python template does not explicitly distinguish mapped lint from a platform's default checker.

**Change:** add these narrow task routes, retaining any customer-specific command. Re-invoke a workaround only when one was emitted and remains applicable. Make tests self-contained with explicit relevant vars; verify current dbt documentation before adopting the source's stronger statement that project vars never apply. Keep library-documentation lookup subject to the operator's approved research routes.

**Evidence:** `S/AGENTS.md:9`, `:11`, `:13`, `:57`; `O/references/base-setup.md:84`; `O/templates/skills/dbt-testing.md:73`; `K/templates/agents.md:3`, `K/templates/rules/dbt-testing.md`, `K/templates/rules/python.md`.

**Verification:** a normal source/model task invokes only relevant conventions, uses the mapped checks, and does not inspect installed package source. A post-condensation probe retains applicable workarounds. A dbt unit test using a var states its input explicitly.

### 6. Define sample limits by actual page behavior and distinguish resources from sources

**Priority: high for sample safety; medium for source registration. New source findings.**

The source added a warning that `DLT_INGEST_LIMIT` bounds pages and does not trim the last page. A Parquet row group can therefore exceed a nominal row target by a large factor. Our dlt template says “bounded samples” without saying what bounds a page or how to judge the landed count.

The live source dlt convention also added the distinction between adding a resource/table to an existing source and creating a new source. That addition has not reached the source's own onboarding dlt template, so copying only source templates misses it.

**Change:** describe the selected loader's actual limit semantics, page/row-group size and acceptable sample cost. Validate replacement with repeated samples and actual landed rows/load metadata, not the numerical limit alone. Preserve our existing conditional use of `DLT_INGEST_LIMIT` and source-version-aware profile reuse. Add resource-extension routing: update the existing source module, resource docs, tests, pipeline design, dbt source and staging model where that repository's contract requires them; do not automatically create another source/pipeline.

**Evidence:** `S/.agents/skills/workarounds/SKILL.md:52`, `S/.agents/skills/dlt/SKILL.md:55`, `O/templates/skills/dlt.md:67`; `K/templates/rules/dlt.md:6`.

**Verification:** a page larger than the nominal limit is judged against documented page semantics and the authorized sample budget. Adding a resource keeps its parent source identity. A non-dlt loader is never assigned an unsupported environment variable.

### 7. Separate sandbox sample loading from persistent Domain seeding

**Priority: high for Studio parity. New source behavior; authorization-sensitive.**

The source now attempts a sample load of every source and a dbt build in the current sandbox when the persistent Domain is empty. If this is unavailable or too costly, it writes a seeding proposal and continues without data. It explicitly reports that the persistent Domain remains empty for later intents.

Our Studio table only recommends a separately authorized seed/load, while the following sentence says onboarding does not seed the database. It does not define the new temporary sandbox path or its reporting outcome.

**Change:** distinguish persistent Domain state, disposable sandbox state and authorization to load. When a confirmed Studio sandbox and authorized scope permit it, run the bounded sample path before data-dependent checks. Otherwise record the exact blocker and a mapped proposal. Retain the ban on implied provisioning or persistent data mutation. Missing credentials trigger the existing authentication-stop rule, not attempts to discover credentials elsewhere.

**Evidence:** `O/SKILL.md:20`, `O/references/base-setup.md:5`; `K/references/studio-duckdb.md:9`, `:17`, `:33`; `K/SKILL.md:21`.

**Verification:** an empty-Domain fixture records sandbox-loaded/persistent-empty separately; an unavailable sandbox emits a specific proposal; unauthorized loads never run; successful sandbox tests cannot be reported as a seeded persistent Domain.

### 8. Complete the selected scaffold and use one database path

**Priority: high. Existing gap exposed by a full comparison; includes a concrete local mismatch.**

The source greenfield output includes working orchestration scripts, dbt profiles/macros/packages, dlt config, map/orchestration/ADR checks, lint configuration, development requirements and ignored runtime artifacts. Our recipe creates empty orchestration/tests directories and inactive source/pipeline examples. It verifies parsing and the APIs separately rather than demonstrating an ingestion-to-transformation path.

There is also a concrete mismatch in our local example: dbt reads `ONBOARDING_DUCKDB_PATH`, while the dlt starter always writes `<repository_root>/.local/data.duckdb`. If an operator selects another allowed disposable path, a later model reads a different database from the one ingestion filled.

**Change:** use one explicit database path for both entrypoints. For selected Studio/DuckDB scaffolds, generate the minimal working run scripts and configuration required by that integration, using the reference's existing patterns. Keep a generic standalone path for other platforms. Include applicable runtime ignores, including dlt previews, scratch state and `.user.yml`; do not register inactive templates as sources or invent business models. Preserve a customer's existing orchestration, package manager and lint choices.

**Evidence:** `K/templates/greenfield/README.md:20`, `:41`, `:78`, `:84`, `:115`; `O/references/greenfield.md:24`, `O/templates/orchestration/run_ingest.py:23`, `O/templates/orchestration/run_transform.py:21`, `O/templates/tests/test_run.py:48`, `O/templates/repo/gitignore-fragment:3`.

**Verification:** a tiny temporary example ingests a row and queries/transforms that same row through dbt using a deliberately nondefault database path. Scripts stop on ingestion/dependency failures. The empty real scaffold contains no fabricated source or business-test success. Clean temporary data and package caches after the check.

### 9. Make the Studio base-setup and audit checklist complete

**Priority: high for claimed Studio readiness. Existing gaps plus expanded source guidance.**

Our Studio reference already covers dynamic profiles, database paths, source catalogs, relation macros, timestamp semantics, native checks and the renamed-copy test. Keep that work. The source now gives a more concrete setup/check contract that ours does not fully enumerate.

**Change:** add a conditional checklist for the following, each with exact scope, side effects, evidence and disposition:

- Run understood baseline commands before setup; retain their results and input revision.
- Check whether the selected CI contract needs `dbt_project_evaluator` and its disabled-by-default model/seed configuration.
- For warning cleanup, compare the before/after test inventory and compiled test SQL; do not label a cleanup behavior-free from a successful parse alone.
- Check native source/config/selector coverage and ensure dbt dependencies are installed before builds.
- Check Parquet/Arrow load metadata where the integration requires it, staging access through `source()`, derived timestamp/key consistency, and SQLFluff profile/project paths.
- Capture actual Ruff configuration/exclusions and run the mapped lint command; report findings without auto-fixing unrelated code.

Do not impose these Studio/DuckDB choices on other adapters, attached catalogs or Python-only loaders. Verify SDK/package facts before implementing template code.

**Evidence:** `O/references/base-setup.md:13`, `:23`, `:30`, `:43`, `:90`; `O/templates/dlt/config.toml:5`; `K/references/studio-duckdb.md:23`, `K/references/compatibility.md:7`.

**Verification:** each source checklist item has a result or a named gap; warning cleanups preserve test membership and compiled SQL; stored views work after database renaming without a rebuild; non-Studio fixtures retain their deliberate platform choices.

### 10. Preserve the source's inventory, review, procedure and dry-run outputs

**Priority: medium. Mostly an existing depth gap. Applies to complete onboarding parity.**

Our brownfield workflow records conclusions and conflicts, but the source defines a convention inventory with evidence, exceptions, destination and confirmation state. It separates operator conventions from confirmed repo-only procedures. It produces a typed review with stable finding IDs and triage states, and rehearses three concrete later tasks. Our review template is a single generic finding without the source's run metadata or triage contract; our verification says to rehearse a later task without that coverage.

**Change:** preserve or emit a compact inventory sufficient to account for each convention and destination. Confirm only unknown rationale, inconsistencies and unclear ownership; do not ask again about facts already established. Discover repo-only multi-step procedures, and emit a procedure skill only when confirmed. For Studio onboarding, use one mapped review with `type`, date, reviewed commit, source and `R-n` findings, keeping disposition of proposed edits distinct from review triage. Rehearse source, mart and connected-model/procedure tasks; greenfield needs the first-source rehearsal. Record the route table in verification.

**Evidence:** `O/references/inventory.md:3`, `O/references/grilling.md:5`, `O/references/domain-skills.md:3`, `O/references/dry-run.md:3`; `S/.agents/skills/reviewing/SKILL.md:12`; `K/references/brownfield.md:3`, `K/references/artifact-contract.md:42`, `:54`, `K/templates/review.md:1`.

**Verification:** every moved convention has evidence and a retained destination; an unconfirmed procedure is not emitted; review IDs survive triage; rehearsal paths exist and the commands are appropriate to the selected environment. A report-format probe alone does not pass runtime-loading checks.

### 11. Re-baseline the pending Studio lifecycle against the current consumer

**Priority: high before claiming full Studio onboarding. Previously recorded gap.**

The source promises Requirement → Design → Build/setup → onboarding review → Verify → one PR. Our installed skill deliberately stops at repository context. Its pending lifecycle plan records a consumer gate based on source `df262dc` and the earlier reference `349d026`. The source has since aligned with a simplified loop and map-owned artifact locations, so that historical dependency report cannot establish today's runtime capability.

**Change:** preserve the small shared context workflow and put supported Studio phase composition behind a conditional reference. First identify the current consumer source and deployed release, its actual onboarding/review entrypoints, artifact paths, CI bundle, verification and shipping side effects. Reconcile the existing lifecycle plan with that evidence before building from it. The source repository's local `reviewing` skill is real, but its existence does not prove the deployed consumer ships that skill. A missing native capability remains a separately scoped dependency.

Reuse already granted authorization where it covers the actual operation. Do not treat an audit request as permission to load data, install customer CI, push, or create a PR. Local context changes can be completed while live integration evidence remains unavailable.

**Evidence:** `O/SKILL.md:30`; `K/SKILL.md:15`, `:21`; `T/context/onboarding-vibedata-studio-lifecycle-plan.md:9`, `:41`, `:75`; `T/context/onboarding-vibedata-validation.md:372`, `:377`.

**Verification:** one supported disposable Studio run proves phase progression, actual convention loading, review, verification and authorized shipping at a known consumer version. Remote PR/head/CI evidence must be current. Until then, report context readiness separately from unverified Studio lifecycle execution.

### 12. Update the fixtures and release evidence with the contract

**Priority: high as an acceptance gate. Test coverage gap, not a current test failure.**

All 30 focused tests pass today. They still expect rule-file templates and `.agents/rules/`. The read-only reference-refresh probes cover the last refresh's profile, precision and preservation cases, not the new convention-skill contract, five role additions, ADR symmetry, sandbox loading or design-evidence policy.

**Change:** update existing fixtures and package assertions instead of building another harness. Keep old rules/custom-schema cases as compatibility tests. Add behavioral cases for findings 1–11, including non-Studio and no-authorization counterexamples. Update the prior design/lifecycle documents and validation record without rewriting historical evidence. Keep both plugin manifests at the same bumped release version when implementation is shipped. Regenerate catalog/README output with the existing generator if it changes. No new plugin entry is needed, so this work alone does not require incrementing the marketplace catalog version.

**Evidence:** `T/tests/test_onboarding_package.py:56`, `:103`, `:149`; `T/tests/test_onboarding_context.py:33`; `T/tests/onboarding/reference-refresh.json:1`; `T/context/onboarding-vibedata-validation.md:324`; `T/plugins/vibedata-repo-skills/.claude-plugin/plugin.json:3` and its Codex peer.

**Verification:** focused tests, appropriate behavior probes, manifest parity, marketplace validation, version gate and generated-catalog freshness pass. Existing whole-repository failures must be rechecked or clearly retained as historical evidence rather than described as current results.

## Source inconsistencies to resolve during adaptation

The current source is useful evidence, but it contains contradictions that should not become new generic requirements.

| Source inconsistency | Evidence | Adaptation |
| --- | --- | --- |
| “Two dbt_project.yml lines” understates the permitted existing-file changes and document moves. | `O/SKILL.md:28` versus `O/references/base-setup.md:23` and `O/references/existing-docs.md:5` | Use one explicit setup/migration scope; preserve application behavior and document destinations. |
| Sample guidance still calls the limit “1,000 rows”; the live dlt rule expects the limit's row count after replacement, while the workaround says whole pages land. | `O/templates/skills/dlt.md:67`, `S/.agents/skills/dlt/SKILL.md:32`, `:36` versus `S/.agents/skills/workarounds/SKILL.md:54` | Check actual page/row-group semantics and landed sample identity/count; do not assert an exact row cap. |
| dlt profiling text still says later figures go into a design record, despite the new no-measurements rule. | `O/templates/skills/dlt.md:77` versus `O/templates/skills/design-records.md:31` | Reuse the profile for reasoning; store measurements in verification and link them from decisions. |
| ADR/design documents are both told to stay at existing paths and told to move to mapped standard classes. | `O/references/existing-docs.md:5` and `:6` | Preserve established paths by default. Treat relocation as an explicit reviewed migration with updated citations. |
| Adding a resource is specified in the live convention but absent from the onboarding template. | `S/.agents/skills/dlt/SKILL.md:55` versus `O/templates/skills/dlt.md:79` | Use the live rule's general distinction; retain customer resource-document conventions. |
| The ordering section still requests a DuckDB orchestration route, although the same document says that row was dropped because repo scripts provide orchestration. | `S/docs/setup/skill-changes.md:5` and `:53` | Use the repo scripts; do not invent a new native orchestrator requirement. |

## What already matches and should remain

- Explicit invocation in Claude and Codex; a normal source/model task does not start onboarding.
- Lossless instruction reconciliation, the `@AGENTS.md` wrapper, link repair, alias/cycle checks and preservation ledger.
- Existing customer schema/checker ownership, custom paths, extension keys, historical ADR identifiers and byte-stable reruns.
- Generic Python/notebook and non-DuckDB support. The sample's `dlt`-only schema and naming/style defaults are not universal requirements.
- Numeric comparison precision, exact identity/NULL checks, derived-key join coverage and actual-grain checks added in the previous refresh.
- Conditional timestamp conversion and catalog removal; preserve source meaning and intentional attached databases.
- Standing business answers as ADRs, component-specific decisions in design records, and no invented business facts.
- Existing source-profile freshness and input-aware verification reuse. The source retired its old per-commit workaround; that does not justify discarding our broader evidence-currency checks.
- Runtime loading, structural readiness and execution evidence remain separate. Neither a local parse nor a repository template proves deployed Studio behavior.

## Change footprint

| Area | Files affected when implementing |
| --- | --- |
| Entry and routing | `K/SKILL.md`, `K/templates/agents.md`, all five existing references; a conditional Studio lifecycle reference if current capability is established |
| Convention output | Current `K/templates/rules/*.md`, rendered as destination convention skills; retain the Python-specific template |
| Map contract | `K/templates/repo-map.json`, `repo-map.schema.json`, `test-map.json`; `K/scripts/validate_context.py` |
| Scaffold and checks | `K/templates/greenfield/README.md`; minimal selected-platform templates for orchestration/configuration, ADR links and repo checks |
| Reports | `K/templates/review.md`, `proposal.md`, `onboarding-report.md`, with retained customer formats and historical records |
| Regression coverage | `T/tests/test_onboarding_context.py`, `test_onboarding_package.py`, relevant `tests/fixtures/onboarding/` and `tests/onboarding/` scenarios |
| Release and evidence | Both `plugins/vibedata-repo-skills` manifests; prior context design/plan/validation/handoff records; generated catalog/README only through the generator |
| No structural rewrite needed | `K/scripts/inspect_repo.py`: existing context discovery already handles `.agents/skills/` |

## Recommended order

1. Refresh context output and validation together: findings 1–6, with preserved legacy/custom-schema fixtures.
2. Complete and test the selected scaffold: finding 8, plus the applicable repository checks from findings 3 and 9.
3. Revalidate the current Studio consumer contract: finding 11, then implement the supported setup/loading/review flow from findings 7, 9 and 10.
4. Run the updated acceptance cases and release checks: finding 12. Claim full Studio parity only after its live acceptance evidence exists.

## Verification performed for this audit

| Check | Result |
| --- | --- |
| Git provenance and source delta | Confirmed target/source SHAs, clean starting trees, recorded baseline and the 42-commit / 68-file delta. |
| Existing focused suite | **30/30 passed:** `python -B -m unittest discover -s tests -p 'test_onboarding*.py' -v`. Python 3.12.12, project-declared `jsonschema==4.23.0`, PyYAML 6.0.3 in a temporary environment. |
| Initial system-Python attempt | 22 helper tests passed; package-test import failed with `ModuleNotFoundError: No module named 'jsonschema'`. The temporary declared-dependency environment resolved this; it was not a code failure. |
| Current source inventory | Brownfield, stacks `dbt`, `dlt`, `python`; all 11 project `SKILL.md` files discovered as context artifacts. |
| Owned map probe | Existing default map passes with all five new artifact roles absent. This demonstrates a parity coverage gap, not a violation of the old schema. |
| Convention-key migration probe | Fails with `key_references: missing rules`. |
| Convention metadata probe | A skill-like file with no description passes the current checker; current validation does not establish skill metadata validity. |
| Inactive-template probe | A valid skill directory containing an inactive Markdown template fails on its placeholder after a blind directory migration. |
| Source ADR checks | Both real `S/tests/test_adr_links.py` test functions passed when called directly. No dbt, application ingestion or warehouse operation ran. |
| Temporary artifacts | Synthetic fixtures, temporary test environment and its package cache were bounded by `TemporaryDirectory` and removed. No test dependency was installed globally. |

Not run: the full marketplace suite, a fresh Claude/Codex behavioral matrix, dbt builds, renamed-warehouse checks, customer CI installation, sandbox sample loads, deployed Studio capability checks, remote PR checks or live Linear status queries. The earlier report's full-suite results and consumer blockers remain historical evidence, not new verification.

**Next action:** update the convention-skill generation, map roles and validator as one reviewable change, using findings 1–3 as its acceptance boundary.
