# Selected-platform scaffold recipe

## Contents

- [Select and verify](#select-and-verify)
- [Local DuckDB example](#local-duckdb-example)
- [Inactive starter templates](#inactive-starter-templates)
- [Verification](#verification)

## Select and verify

Use this recipe only after the platform is confirmed. Preserve the selected package manager. For a platform other than local DuckDB, verify its dbt adapter and dlt destination using the operator's approved documentation route, replace the platform-dependent configuration below, and record the versions and URLs. Do not infer a warehouse from the example.

Verified package facts on 2026-10-15: dlt 1.31.0 supports Python >=3.10,<3.15; dbt-duckdb 1.11.0 and dbt-core 1.12.6 declare Python >=3.10. These are independent current releases, not a tested combined lockfile. Resolve a compatible environment with the project's package manager and record its actual installed versions before claiming execution.

Sources: [dlt DuckDB documentation](https://dlthub.com/docs/dlt-ecosystem/destinations/duckdb), [dbt-duckdb official README](https://github.com/duckdb/dbt-duckdb), and official [dlt](https://pypi.org/pypi/dlt/json), [dbt-duckdb](https://pypi.org/pypi/dbt-duckdb/json), [dbt-core](https://pypi.org/pypi/dbt-core/json) registry metadata. Refresh these facts when onboarding; they are not perpetual version pins.

## Local DuckDB example

When local DuckDB is selected and no layout exists, create `ingestion/`, `transformation/models/`, `orchestration/` and `tests/`. Preserve empty directories with a short README if they must survive Git. Use `requirements.txt` containing `dlt[duckdb]` and `dbt-duckdb`; resolve and pin compatible versions with the chosen manager. `requirements-dev.txt` contains only the selected check tools. Keep virtual environments, `.local/`, dbt `target/` and logs ignored. Keep credentials outside tracked files.

`transformation/dbt_project.yml` (replace the project/profile identifier with the confirmed name):

```yaml
name: data_project
version: '1.0'
config-version: 2
profile: data_project
model-paths: [models]
test-paths: [tests]
```

`transformation/profiles.yml` for the confirmed local target:

```yaml
data_project:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: "{{ env_var('ONBOARDING_DUCKDB_PATH') }}"
      threads: 1
```

Select an absolute disposable local database path for verification. The explicit environment variable keeps the database location independent of the caller's working directory. Set it for each command; an unset value is an actionable configuration failure. A repository may use its existing environment-variable convention instead.

If pytest is selected, include this in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
tmp_path_retention_count = 0
tmp_path_retention_policy = "failed"
```

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


def load(source, repository_root):
    root = Path(repository_root).resolve()
    state = root / ".local"
    state.mkdir(exist_ok=True)
    pipeline = dlt.pipeline(
        pipeline_name="{{pipeline_name}}",
        destination=dlt.destinations.duckdb(str(state / "data.duckdb")),
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

1. Run the mapped context check from the customer root. When the bundled checker was installed, its command is `python3 .agents/checks/validate_context.py --root .`; retain an existing suitable checker and its command.
2. Use a supported Python interpreter and a project-local virtual environment. Install the resolved dependencies only when network/install scope permits. Preserve the resolved versions as evidence; an install error blocks execution verification.
3. With `ONBOARDING_DUCKDB_PATH` set to a disposable absolute path, run `dbt parse --project-dir transformation --profiles-dir transformation --target dev`. Disable dbt telemetry for the local trial with `DBT_SEND_ANONYMOUS_USAGE_STATS=false`. An empty parse verifies configuration only.
4. To verify the starter APIs, instantiate them with tiny synthetic rows in a disposable fixture, keeping pipeline state and the database there. Record the actual run and clean it afterwards. Keep that synthetic fixture out of the customer's source inventory.
5. Register only actual scaffold commands in the maps. Report business tests, customer credentials and warehouse execution as absent/unverified until they exist and run.
