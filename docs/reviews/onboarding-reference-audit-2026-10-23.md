# Onboarding reference audit

## Scope and evidence

The requested result is a reusable onboarding skill that can produce and maintain
the context demonstrated by `accelerate-data/sample-nyctaxi-comp`, with a branch
and PR. The reference is read-only. This audit covers the whole onboarding
package: workflow, references, maps and schema, all ten convention templates,
repository checks, dbt/dlt scaffolds, orchestration, inventory, checker, report,
runtime metadata, tests, release manifests and generated catalog.

- Marketplace base: `fbdb5c6a55e9c551794603285223a4b4934c7e2d`.
- Reference: `0e9fe609796b513e5ee303e809c00281624f5cd5` (clean checkout).
- Consumer source, checked from GitHub: `d49c8d54bb6b52fcc905ae598d8738a919bde7fd`,
  `vibedata-data-engineering` 0.133.4. Its kind registry has no `onboarding`;
  canonical semantic-model delivery exists only in the supplied reference,
  not in that plugin's production skill tree. A journey fixture is not delivery.
- Baseline: 62 onboarding tests passed, one optional dbt/dlt integration skipped.
- Apache Ossie core: `0.2.0.dev0`, reference vendor pin
  `c5cb931d72029dc523a5dd18d267f083403786f2`; VIBEDATA extension 1.4.
  These are compatibility pins, not a claim that they are the latest upstream.
- Context7 returned a monthly-quota error. Official documentation was read with
  `read-website-fast`; there was no authentication failure.

Source paths below are relative to the reference. Package paths are relative to
`plugins/vibedata-repo-skills/skills/onboarding-vibedata` unless qualified.

## Findings and disposition

| ID | Reference evidence | Package gap or difference | Action |
| --- | --- | --- | --- |
| A01 | `.agents/skills/onboarding/references/base-setup.md`, Convention skills | Gold marts require both semantic authoring and validation skills; neither is delivered or selected. | Bundle reusable seed skills, tooling, schemas and generic examples with pinned provenance; select only for actual marts or an existing canonical model. |
| A02 | `.agents/skills/semantic-model/SKILL.md`; `references/reverse-engineering.md` | No canonical creation procedure, inventory of every gold table, atomic-star partitioning, suppliers, aggregate content, metric rollup or refusal contract. | Route onboarding through the seeded authoring and review pair. Preserve custom model locations and record unresolved business decisions. |
| A03 | `.agents/skills/semantic-model/references/refactoring.md`; `.agents/skills/workarounds/SKILL.md` | Later mart edits do not trigger canonical maintenance. | Add same-change routing for field/key/grain/population/filter/metric/aggregate changes, full-directory gates and generated level-test freshness. |
| A04 | `.agents/skills/validating-semantic-model/{SKILL.md,references/checks.md}` | Structural success could be mistaken for semantic correctness. | Require separate structure, supplier/coverage/note checks, SQL/ADR content review and authorized data-test evidence. Report unrun data checks. |
| A05 | `repo-map.json`, `tests/test_maps.py` | Shared schema and checker omit `orchestrators`, external `location`, source/run membership and shared-dataset `produces`. | Add optional validated runner metadata, exact membership and unambiguous table ownership. Keep existing native checker/schema ownership. |
| A06 | `artifact_paths.logical_model = logical-model/*.ossie.yaml` | Portable checker treats glob as a missing literal path; inspector does not list canonical models outside hidden context. | Recognize existing canonical files and confined matching artifact globs; reject unmatched or escaping globs. Future artifacts keep brace patterns. |
| A07 | `tests/test_maps.py`, layer coverage and runner-code checks | Reference checks assume literal `PIPELINES` and taxi layer names; portable runner discovers pipelines from map. | Preserve native tests; map-driven scaffold remains map-driven. Add generic graph checks, require native code/list parity where the runner has a separate list, report unavailable parity. Do not copy taxi-specific regex/layer assertions. |
| A08 | `.agents/skills/onboarding/references/base-setup.md`, Inherited DuckDB views | Package verifies a renamed rebuilt copy only; rebuilding can erase pre-existing view failures. | Require read-only all-view binding assessment on untouched sandbox before any write, separate from post-build portability. No available sandbox means unverified. |
| A09 | `.agents/skills/onboarding/references/inventory.md`, Rules hiding in code | Inventory describes conventions generally but misses explicit thresholds, HAVING, join loss and rationale comments. | Add observable business-rule inventory and destinations; no invented ADR rationale. |
| A10 | `.agents/skills/design-records/SKILL.md`, No population statements | Package avoids measurements but does not prevent duplicate population definitions. | Rules stay in ADRs, implementation in SQL, model notes cite holding tests; designs link rather than duplicate. |
| A11 | Reference source onboarding lifecycle and runtime workarounds | Reference declares a native onboarding kind and phase helpers; current production consumer does not ship it. | Preserve capability gate and update dated source observation. No invented native lifecycle or forced intent kind. |
| A12 | `AGENTS.md`, `.agents/skills/{context,adr,git-and-prs,sql-style}/SKILL.md` | Most prior alignment is already present: routing, preservation, evidence destinations, native conventions, scoped loading, explicit invocation. | Retain. Taxi naming, fixed two-decimal money, unconditional UTC conversion, fixed profile and customer ADR numbering are examples, not universal defaults. |
| A13 | `.agents/skills/onboarding/references/{greenfield,existing-docs,domain-skills,dry-run}.md` | Reference is narrower than distributed package: dbt/dlt only, initial onboarding only, automatic CI phases and document moves. | Preserve Python/Fabric/refresh branches, lossless migration, explicit side-effect authorization, existing check ownership and honest runtime gaps. Add first-mart handoff without empty semantic directories. |
| A14 | `tests/test_ossie_validate.py`, semantic tools and schema | Canonical tooling is coupled to schema versions; copying only SKILL.md cannot work. | Seed complete dependencies; exercise emitted CLI with generic models, invalid mutations, directory drift and freshness. Never run the reference warehouse or include customer canonical model/data. |
| A15 | Package distribution and CI | Any added tooling must reach fixtures, link validation, dual manifests, root version and generated catalog. | Bump child manifests together and root plugin version, regenerate catalog, run full CI-equivalent checks and independent review, open PR and inspect remote CI. |

## Source conflicts resolved for reuse

The reference is the target example, but some older prose contradicts its latest
schema, tests and later rules. Port the current executable contract:

1. Semantic S3 says ratios bind their numerator column; S3c, the 1.4 schema and
   `computed-metric-mapped` validation require derived ratios with no binding.
   Retain the latter and remove the contradictory rule in the seed.
2. Refactoring says every population-narrowed table is standalone; current
   validation review allows a filtered aggregate when it supplies the matching
   filtered metric. Use metric/query-relative population compatibility: the query filter and metric
   filter must together imply the source content filter at a supported grain.
   Include all inner-join loss and HAVING; a narrower source cannot answer an
   unrestricted wider query. Preserve that conditional eligibility explicitly.
3. Reverse engineering first says all unmappable tables need a ruling, then
   permits deterministic note-only refusals. Record evidence-backed dispositions
   directly; ask only when multiple honest meanings remain. Pending items remain
   visible findings, not invented model entries or a passing coverage claim.
4. The workarounds file says one large canonical document; current S1 requires
   whole stars and permits several documents. Validate the full directory to
   catch drift in repeated dimension identities.
5. The reference itself uses an unsupported native onboarding lifecycle. Retain
   its artifact conventions without claiming production phase support.

## System requirements

- R1: Existing marts or canonical models select a complete, usable semantic
  authoring/review bundle. An empty or non-mart repo gets no invented model.
- R2: Every model change has structure and content evidence, with data checks
  reported separately; the next mart change routes to model maintenance.
- R3: Map checks reject orphan sources, unknown runner members, invalid local
  runner paths and ambiguous shared table ownership; native formats survive.
- R4: Canonical artifact globs resolve only inside the repository, require a
  match and preserve literal-path and future-pattern behavior.
- R5: An inherited DuckDB assessment precedes writes and cannot be cleared by a
  successful rebuild. Unknown targets and auth failures retain their gates.
- R6: Existing preservation, Fabric, greenfield, refresh and runtime contracts
  continue to work, with no sample-repository mutation.
- R7: Release metadata, catalog, local tests and PR evidence describe the final
  branch accurately. No merge or deployment is part of this task.

## Implementation choice

Use a self-contained, pinned seed bundle inside the onboarding templates, with
entrypoints named `convention.md` until installed as `SKILL.md`. This reuses the proven
tooling and keeps the marketplace's one explicit onboarding skill. A pointer to
a private reference would leave installed users without the tools; rewriting the
language/checker would create a second implementation. Seed only missing skills;
refresh existing copies through a reviewed diff that preserves human edits.

The implementation and verification sequence is in
[`onboarding-reference-refresh`](../superpowers/plans/2026-10-23-onboarding-reference-refresh.md).

## Implementation audit additions

Executing the complete seed exposed reference defects that copying prose alone
would miss: own-level dimension content crashed the level generator; the standalone
example had two unsupplied metrics; four example metrics omitted rollup metadata;
and the supplier CLI borrowed same-named fields from earlier datasets. Each now
has a failing-before/passing-after regression. The checker previously accepted any
consistent extension version; the delivered schema/checker now both require 1.4.

The independent review also reconciled the aggregate query-filter rule across
all entrypoints and removed promises of a reference-only dbt-variable test.
Native dbt-variable parity remains required evidence or an explicit coverage gap.
The star example states an explicit filter without an unproven inner-join
assumption and labels its SQL contract as illustrative, not executed evidence.

See the [validation record](onboarding-reference-validation-2026-10-23.md) for
regressions, application probes, release checks and real acceptance limits.
