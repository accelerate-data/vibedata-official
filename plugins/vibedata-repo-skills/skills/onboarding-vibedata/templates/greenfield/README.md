# Selected-platform scaffold recipe

## Select and verify

Use these files only for a confirmed local, single-database DuckDB scaffold. Preserve the repository's layout, package manager, dependency policy and checks. Other platforms need their documented adapter/destination; unknown platforms block only dependent files. Studio requires the separate [current runtime contract](../../references/studio-duckdb.md), never a local environment variable substituted for assigned coordinates.

Verified together on 2026-10-16: Python 3.12.12, dlt 1.31.0, dbt-core 1.12.6, dbt-duckdb 1.11.0 and DuckDB 1.5.6. The requirement templates pin this tested set; recheck compatibility and current versions at onboarding. Sources: [dlt DuckDB](https://dlthub.com/docs/dlt-ecosystem/destinations/duckdb), [dbt-duckdb](https://github.com/duckdb/dbt-duckdb), [dbt builtins](https://docs.getdbt.com/reference/dbt-jinja-functions/builtins), [unit-test overrides](https://docs.getdbt.com/reference/resource-properties/unit-test-overrides), [dlt resource limits](https://dlthub.com/docs/general-usage/resource#sample-from-large-data), and official PyPI metadata for those packages.

## Template destinations

Paths below are relative to the onboarding skill's `templates/`. Replace `<project_name>` with the confirmed dbt identifier. Preserve dbt/GitHub Jinja expressions; replace only explicit generation tokens. Merge with suitable customer files; a path collision is not permission to overwrite.

| Template | Destination | Selection |
| --- | --- | --- |
| `orchestration/run_ingest.py` | `orchestration/run_ingest.py` | Local DuckDB; executes registered pipelines in map order, stopping on failure. |
| `orchestration/run_transform.py` | `orchestration/run_transform.py` | Local DuckDB; runs deps before build, stopping on failure. |
| `dbt/dbt_project.yml`, `dbt/profiles.yml`, `dbt/packages.yml` | Same basenames under `transformation/` | Selected adapter/profile; no packages are needed for the standalone minimum. |
| `dbt/relations.sql` | `transformation/macros/relations.sql` | Confirmed single-database relation policy; preserves versioned ref arguments. Keep intentional attached catalogs. |
| `dbt/generate_schema_name.sql` | `transformation/macros/generate_schema_name.sql` | Only a confirmed verbatim-schema convention; retain other customer naming. |
| `dlt/config.toml` | `ingestion/.dlt/config.toml` | Select Parquet/Arrow load metadata only where required; add source sections with real sources. |
| `dlt/requirements.txt` | `requirements.txt` | Tested standalone dependencies; use an existing manager instead when selected. |
| `repo/requirements-dev.txt` | `requirements-dev.txt` | Declared native/lint dependencies in the same interpreter. |
| `repo/ruff.toml`, `repo/sqlfluff.cfg` | `ruff.toml`, `.sqlfluff` | When equivalent customer configs do not exist; adapt confirmed exclusions/profile paths. |
| `repo/gitignore-fragment` | Merge into `.gitignore` | Ignore runtime state, previews, scratch, `.user.yml`, dbt outputs/caches and secrets; retain source files. |
| `checks/test_adr_links.py`, `checks/test_maps.py` | Same basenames under `tests/` | Missing shared-scaffold checks; retain native customer equivalents. |
| `repo/repo-checks.yml` | `.github/workflows/repo-checks.yml` | Missing CI only, after setup authorization; adapt actual check paths. |

Create `ingestion/`, `transformation/models/`, `transformation/tests/`, `orchestration/` and `tests/`; use a short README to retain necessary empty directories. For selected pytest, merge into `pyproject.toml`:

```toml
[tool.pytest.ini_options]
tmp_path_retention_count = 0
tmp_path_retention_policy = "failed"
```

## One explicit database

Both run scripts require `--db-path /absolute/disposable/file.duckdb`. They pass that exact value through `ONBOARDING_DUCKDB_PATH`; the local profile and pipeline call must consume the same value. Missing or relative input fails before launching work. The starter `load(source, repository_root, db_path)` also requires the explicit path. No component silently selects `.local/data.duckdb`. Use `sys.executable` for all child Python/dbt commands.

Studio-generated artifacts instead use the verified consumer's supported profile and destination initialization. Resolve current sandbox coordinates through its context reader before invoking a phase. The standalone starter is not a replacement for that integration.

## Map registration

Keep `sources: {}` until a real source contract exists; inactive examples are not sources or business coverage. For this selected scaffold, add these existing roles/entrypoints only after emitting their files:

| Key | Value |
| --- | --- |
| `artifact_paths.dbt_project` | `transformation/dbt_project.yml` |
| `artifact_paths.dbt_profiles` | `transformation/profiles.yml` |
| `artifact_paths.source_config` | `ingestion/.dlt/config.toml` |
| `artifact_paths.dbt_sources` | `transformation/models/sources/{source}.yml` (future pattern) |
| `artifact_paths.source_module` | `ingestion/sources/{source}.py` (future pattern) |
| `artifact_paths.pipeline` | `ingestion/pipelines/{pipeline}.py` (future pattern) |
| `artifact_paths.resource_docs` | `docs/sources/{source}/{resource}.md` (future pattern) |
| `artifact_paths.source_tests` | `tests/sources/test_{source}.py` (future pattern) |
| `entrypoints.ingestion` | `orchestration/run_ingest.py` |
| `entrypoints.transformation` | `orchestration/run_transform.py` |

Register the selected ingestion/transformation modules and actual context, ADR, native-map, lint, deps/parse/build commands. Commands requiring a database name the required explicit input; they are unverified until run. The shared test-map template registers only emitted checks. A different native schema keeps equivalent mappings in its own format. Source registration includes its real pipeline, `config_section`, docs/tests/design and staging paths as applicable, with actual required artifacts rather than example placeholders.

## Inactive starter templates

Place these under `.agents/templates/`, outside active source and dbt model paths. Replace all `{{...}}` tokens only after the user supplies a real source contract. These files are templates, not registered sources or models.

`source.py.tmpl`:

```python
import dlt


@dlt.resource(name="{{resource_name}}", write_disposition="{{confirmed_disposition}}")
def resource(rows):
    yield from rows
```

`pipeline.py.tmpl` for local DuckDB:

```python
from pathlib import Path

import dlt


def load(source, repository_root, db_path):
    db_path = Path(db_path)
    if not db_path.is_absolute():
        raise ValueError("db_path must be an absolute database file path")
    root = Path(repository_root).resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    state = root / ".local"
    state.mkdir(exist_ok=True)
    pipeline = dlt.pipeline(
        pipeline_name="{{pipeline_name}}",
        destination=dlt.destinations.duckdb(str(db_path)),
        dataset_name="{{dataset_name}}",
        pipelines_dir=str(state / "pipelines"),
    )
    return pipeline.run(source)
```

`source.yml.tmpl`:

```yaml
version: 2
sources:
  - name: '{{source_name}}'
    schema: '{{confirmed_dataset}}'
    tables:
      - name: '{{table_name}}'
```

`model.sql.tmpl`:

```sql
select {{confirmed_columns}}
from {{ source('source_name', 'table_name') }}
```

Retain dbt's Jinja call when filling the template; replace only its confirmed identifiers. Add required primary keys, merge behavior and actual tests when the source is established, using the selected destination's current documentation. Do not turn a sample customer/orders domain into business requirements.

## Verification

1. Run mapped context, ADR and native schema/config checks. Rendered Python must compile; metadata needs a YAML/native check separately.
2. Use the selected project-local interpreter and resolved dependencies. Install declared dbt packages before selector checks. Failed installation leaves execution blocked.
3. With `ONBOARDING_DUCKDB_PATH` set to the authorized absolute disposable path, run `python -m dbt.cli.main parse --project-dir transformation --profiles-dir transformation --target dev`. An empty parse proves configuration only.
4. In one tiny disposable fixture, instantiate the inactive starters and run `python orchestration/run_ingest.py --db-path <absolute-path>` followed by `python orchestration/run_transform.py --db-path <same-path>`. Query the transformed synthetic value from that file and assert the default database was not created.
5. Repeat a replacement sample with a yielded page larger than the nominal limit; inspect actual landed row counts, load IDs and failures. A successful extraction is not proof of a completed load. Query the built views from a copy with a different basename without rebuilding. Keep these checks synthetic and delete their database/state/cache afterwards.
6. Execute emitted pytest checks after dbt deps, then mapped Ruff/SQLFluff commands. Set `DBT_SEND_ANONYMOUS_USAGE_STATS=false` and `RUNTIME__DLTHUB_TELEMETRY=false` for local synthetic trials. Report actual commands/results and explicit missing customer/runtime evidence.

Rehearse the first-source route at mapped verification: files to read, files to create/change and commands, with current paths or legitimate future patterns. Rehearsal does not execute a production build.

Register the emitted ingestion runner in `orchestrators.run_ingest` with
`kind: python`, its real `path`, and `runs: []`. Add each first real source to
`runs` as it is registered. This runner reads source pipelines from the map in
map order; do not invent a second `PIPELINES` list. Keep a native runner's own
order/list and parity test when it uses one. No gold marts means no canonical
model or semantic test module yet; preserve the first-mart convention handoff.
