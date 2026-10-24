# Canonical semantic model

Read this when inspection finds gold marts or an existing canonical model. A
repository with neither gets no model directory, placeholder model, or semantic
test module. Its dbt convention records the first-mart handoff below.

## Deliver the authoring and review pair

Use the complete [seed bundle](../templates/semantic/README.md), not only its
Markdown entrypoints. It carries Apache Ossie `0.2.0.dev0`, VIBEDATA `1.4`, the
pinned core validator/schema, extension checker, CLI, level-test generator,
references and examples. These are tested compatibility versions. Before an
upgrade, check the approved upstream sources in its provenance; upgrade schema,
checker, every payload and tests together. An installed plugin that demonstrably
provides this same contract can supply the pair instead; a planned delivery or
journey fixture cannot.

For each missing skill, copy `templates/semantic/<name>/` to
`.agents/skills/<name>/`, then rename `convention.md` to `SKILL.md`. The names are
`semantic-model` and `validating-semantic-model`. Keep their relative asset layout.
Merge the bundle's dependency requirements into the selected project manager and
install with the same interpreter used for checks, within setup authorization.
Retain the upstream LICENSE, NOTICE and pin record. Preserve existing skill names,
human edits and ownership; compare current files with the recorded seed revision
before refresh. A collision blocks that replacement, not unrelated context.
Claude aliases follow the artifact contract and point at this one maintained copy.

Register the pair in the task routes. A mart, key, metric, source mapping, grain,
filter or hierarchy change invokes authoring followed by validation. Copying a
bundle does not establish runtime discovery: verify selected-runtime loading
separately. Resolve every path from the customer map before running commands.

## Create or reconcile

1. Read every gold mart, its properties and governing ADRs. Inventory SQL inputs,
   keys, grain, casts, measures, WHERE/HAVING, joins and dropped rows. Read upstream
   staging/ingestion only where needed to establish types or meaning.
2. Invoke `semantic-model` and its reverse-engineering reference. Every gold
   table gets an honest physical handle or an evidence-backed refusal note on
   its handle. Each fact star stays wholly within one document; repeated shared
   dimensions must agree across documents. Preserve an existing canonical format
   until an explicit migration is decided; another semantic format is evidence
   for parity review, not permission to replace it.
3. Preserve `artifact_paths.logical_model` if present. A new canonical uses
   `logical-model/*.ossie.yaml`; create it only when a real model can be written.
   Register its actual directory under `modules.logical_model` and a test-map
   module with actual source/check paths, or their supported native equivalents.
   Preserve closed customer schemas and command ownership; record any missing
   coverage instead of inserting unsupported keys. Do not register a fake passing model to
   make a glob match. Pending meaning or unavailable inputs remain coverage gaps.
4. Use the current rules for aggregate content, keyed levels, metric filters,
   derived ratios, dimension-based and time-series measures, dimension reach and
   weighted bridges. Read actual SQL: a valid column-map string need not name a
   real output column. Reconcile consumer semantic definitions where they exist.
5. Record unknown business meaning as a finding and request only decisions the
   code and existing ADRs cannot settle. Continue independent model work. Never
   alter mart SQL, seeds or macros to make the semantic model pass.

## Checks and evidence

Register concrete commands in `repo-map.json` and `test-map.json`, replacing these
argument labels with the real mapped paths (quote paths containing spaces):

```text
python3 .agents/skills/semantic-model/scripts/ossie.py validate <model-directory>
python3 .agents/skills/semantic-model/scripts/ossie.py coverage <model-directory> <marts-directory>
python3 .agents/skills/semantic-model/scripts/ossie.py suppliers <model-directory>
python3 .agents/skills/semantic-model/scripts/ossie.py notes <model-directory> <tests-directory> <adr-directory>
python3 .agents/skills/semantic-model/scripts/ossie.py level-tests <model-directory> <level-test-file> --check
```

Run the whole model directory, so shared-dimension drift is checked. All gates
must exit 0 with no errors; inspect and report warnings. Generate the level test
without `--check` after a declared-level/key change, then check freshness. This
generated SQL is warn-only data validation, not proof that declared keys hold.
The `notes` tool resolves `held by <test-name>` and `ADR NNNN` in per-file
directories. For a custom ADR identifier or container it cannot resolve, retain
the customer's checker and report the uncovered note-link check explicitly;
do not renumber decisions to satisfy the tool. Verify model `dbt_var` bindings
against the mapped dbt project using its native parity check, or report missing
coverage; these five gates do not read project variables.

Invoke `validating-semantic-model` for its separate SQL/ADR content review. Record
file/line evidence for every mapping, population and metric claim. Run holding,
level and bridge-weight data tests only on an authorized target; record missing
warehouse/dbt access as unrun. Structural success, synthetic fixtures, and a note
claiming a prior check cannot establish content or data correctness. Add these
actual commands to existing CI where setup permits; preserve other hooks/jobs.

## Maintain in the same change

After mart SQL/properties or semantic metadata changes, reconcile physical
handles, aliases/joins, fields and suppliers, grain, content filters/levels and
key columns, metric expressions/filters/rollup, SCD and hierarchy declarations.
Withdraw stale bindings and dependent fields/metrics when a rule changes. Update
reconciliation tests, note citations, mapped commands and affected design/ADR
links. Run all gates again after content fixes; unchanged-input evidence alone
may be reused. Refactors use the seeded split/fold/rename/retirement procedure.

For the **first gold mart**, its normal model task installs this pair, writes
the real canonical model, registers paths and checks, and performs the same
review. This is a model task; it does not rerun all onboarding. If no approved
bundle is available, name that dependency and leave semantic readiness unverified.
