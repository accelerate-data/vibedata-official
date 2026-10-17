# Fabric onboarding fit: local change report

Source: `handoff-onboarding-vibedata-fabric-fit.md` supplied by the operator.
Base: `main@e9b27d5`. Branch: `fix/onboarding-vibedata-fabric-fit`.
Scope: the published onboarding plugin and its regression tests. The initial
implementation was local-only, with no Fabric repository edit, notebook execution
or production operation. The operator subsequently authorized committing the
reviewed changes, raising a PR, and approving/merging it after CI passes.

## System requirements and decisions

| ID | Observable behavior | Decision |
| --- | --- | --- |
| D1 | Fabric notebook inventory succeeds and detects Python/dlt imports after magics without running code. Malformed ordinary Python and `.ipynb` still fail without disclosing source. | Require `*.Notebook/notebook-content.py` and the exact Fabric source header before normalizing syntax-invalid magic lines. Preserve Python strings. Treat whole cell-magic bodies as opaque. Keep string paths in `code_files` and add `notebook_files`; `.platform` adds the Fabric stack marker. |
| D2 | Existing notebook/single-file ADR collections retain their location, identifiers and history. | Support literal `artifact_paths.adr`. Keep a native container checker when one exists; otherwise omit the per-Markdown-file ADR checker and record the named ADR-link gap. No container parser or history rewrite. |
| D3 | YAML/notebook registrations do not need invented TOML sections; existing TOML validation remains strict. | Validate every TOML-backed source before reporting non-TOML/embedded registration skips. Missing files/sections and non-TOML `config_section` declarations still fail. Preserve repeated YAML/`SOURCES` conventions and record the uncovered parity gap. |
| D4 | Missing local profiles do not crash selector checks or launch dbt. Existing mapped profiles retain their target selection. | Skip with a named dbt-selector gap only when the profile role is absent. A missing mapped file fails. Remove the hardcoded `dev` target and use dbt's profile/environment selection. Document Fabric/SQLFluff execution limits without selecting Studio. |

## Implementation

1. Add regression tests for D1, D3 and D4 before their fixes.
2. Update the inventory helper and emitted native-map check, preserving existing callers and checks.
3. Update artifact, brownfield and compatibility references, plus the ADR/dlt convention templates.
4. Bump both child plugin manifests from `1.1.0` to `1.1.1`; bump the root plugin from `1.4.0` to `1.4.1` for the existing CI version gate. No marketplace-entry or catalog-metadata version change is needed.
5. Run package/repository checks and a fresh independent review. The initial changes were left uncommitted for operator review; the operator then authorized the PR/merge phase.

## Verification

All checks use a task-owned Python 3.11.17 environment because the workstation's
default Python has no pytest/Ruff. It contains the repository's development tools
plus pytest; no runtime dependency is added to the plugin or customer repository.
The environment is disposable, and all test fixture directories use existing
`TemporaryDirectory` cleanup. Pytest commands also set
`-o tmp_path_retention_count=0 -o tmp_path_retention_policy=failed`.

| Requirement/check | Observed result |
| --- | --- |
| D1/D3/D4 regression baseline | Before implementation, the focused run failed at Fabric `%pip`, missing non-TOML sections, missing dbt profile mapping, and hardcoded `--target dev`. |
| D1 string preservation | An additional test failed when magic-like lines inside a Python multiline string were stripped; syntax-error-directed normalization then passed. |
| D1 real repository repro | `python3 plugins/vibedata-repo-skills/skills/onboarding-vibedata/scripts/inspect_repo.py --root /Users/shwetanksheel/scratch/vibedata-showcase/nyc-taxi-fabric` exits 0; stacks are `dbt`, `dlt`, `fabric`, `python`; seven notebook paths are identified. The repository is read-only throughout. |
| D1 focused context suite | Included in the passing focused run below; malformed `.ipynb`, malformed ordinary/Fabric Python, non-disclosure, read-only discovery and strict Fabric recognition are covered. |
| D3/D4 emitted checks | Tests execute rendered check templates against bounded temporary maps. They cover YAML and embedded gaps, mixed TOML validation before skip, missing TOML sections, absent versus missing mapped profiles, and target selection without `--target dev`. |
| Focused pytest | `python3 -m pytest tests/test_onboarding_context.py tests/test_onboarding_scaffold.py tests/test_onboarding_package.py -q` passes: 61 passed, one opt-in integration skip. |
| CI test suite | `python3 -m coverage run -m unittest discover -s tests`: 176 tests, OK, one opt-in integration skip. |
| Coverage gate | `python3 -m coverage report --fail-under=70`: 90%. |
| CI lint and format | Both exact CI Ruff checks pass. Emitted map-check template is also formatted. |
| CI compilation | The exact `py_compile` command from `.github/workflows/ci.yml` passes. |
| Claude package | `claude plugin validate ./plugins/vibedata-repo-skills` passes. |
| Codex marketplace | Required local check `codex plugin marketplace add .` succeeds and registers this checkout as a local marketplace source; no plugin installation test runs. |
| Marketplace and versions | `python3 scripts/validate-marketplace.py` and `python3 scripts/check-plugin-version-bump.py --base-ref HEAD` pass. Child manifests match at `1.1.1`. |
| Catalog freshness | Initially unavailable because both submodules were uninitialized. Initialize their existing pinned SHAs over SSH port 443; `python3 scripts/build_catalog.py --check` then passes without regeneration or pointer changes. |
| Whitespace | `git diff --check` passes. |

At the initial local checkpoint, release gates also passed against `origin/main`.
There were no staged changes, and the feature branch still pointed to `e9b27d5`.
Both submodule pointers were unchanged, and the Fabric repository remained clean.
Generated catalogs and README blocks needed no update. The task-owned 38 MiB test
environment was removed after verification. PR checks and merge status are tracked
on GitHub during the separately authorized release phase.

## Reference behavior and review

A fresh baseline reader identified missing explicit guidance for container ADR
checks, YAML/notebook parity and notebook-generated profiles. A separate fresh
reader of the updated references selected all three named gaps, retained the
native formats and production boundaries, and separated context readiness from
execution verification. Its remaining questions concern repository inputs
(existing validators, schema adoption, selected runtime, registered selectors),
which the skill must discover from each customer repository.

Independent code review: **no findings**. The reviewer inspected the complete
12-file implementation diff, connected inspector callers, emitted checks and
tests. It confirmed fail-closed parsing, metadata-only inventory, conditional
checks, target selection and reference/template consistency. The report itself
was added afterward; it changes no executable input. The reviewer is complete.

## Limits

No generic YAML-to-notebook parity parser or notebook ADR-link parser is added.
Those remain explicit native-check gaps. Cell-magic bodies do not contribute
dependency imports. No Fabric pipeline, dbt warehouse execution, SQLFluff runtime,
Studio-on-Fabric trial or remote GitHub CI run is claimed. The separate optional
DuckDB/dlt integration remains skipped because the scaffold execution code is
unchanged.
