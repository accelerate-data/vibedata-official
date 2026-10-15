# Studio on DuckDB

Use only when the selected consumer is Studio and the Domain platform is `duckdb_local`. Other platforms keep their own profiles, catalog semantics and ingestion setup. Inspect first; proposed configuration or macro changes follow [compatibility decisions](compatibility.md).

## Repository and Domain state

Establish Domain state from existing operator evidence or an authorized read-only check. An unknown state stays unknown; inspecting repository files cannot establish database contents.

| Implementation | Domain data | Treatment |
| --- | --- | --- |
| Empty | Empty | Greenfield context and the selected Studio scaffold requirements below. |
| Present | Present | Brownfield context and compatibility checks. |
| Present | Empty | Brownfield context; record missing source data as an execution-readiness finding. Recommend a separately authorized seed/load before build work. |
| Empty | Present | Warehouse migration assessment required; hold dependent scaffolding and preserve existing data. |
| Either | Unknown | Continue independent inventory; leave data-dependent classification and execution readiness unverified. |

Onboarding does not create a Domain or seed its database.

## Runtime compatibility

Confirm the deployed Studio/plugin version and runtime contract before proposing edits. These checks apply to both greenfield and brownfield repositories; a local DuckDB example alone does not establish Studio compatibility.

| Inspect | Required evidence or proposed change |
| --- | --- |
| Runtime dbt profile | Confirm the provided wrapper, `DBT_PROFILES_DIR`, `DBT_PROFILE_NAME` and `dev` target. Where required, propose `profile: "{{ env_var('DBT_PROFILE_NAME', '<existing-profile>') }}"` in `dbt_project.yml`, retaining the local fallback. |
| Local database path | Confirm local run scripts and the local profile use the same database. For the matching Studio contract, resolve it through `VD_EPHM_DUCKDB_LOCAL_PATH`; Studio supplies its own profile inside an intent. |
| Ingestion integration | If the selected integration uses `vibedata-dlt-duckdb-studio`, verify its supported version and initialization before installing or changing code. Its local run environment may require `VD_DOMAIN_DATA_PLATFORM=duckdb_local`, `VD_EPHM_DUCKDB_LOCAL_PATH` and `VD_DOMAIN_SECRET_STORE_KIND=local_toml`; confirm the actual secret-store binding. Preserve other ingestion implementations. |
| Source relations | A renamed Domain copy must resolve source schemas/tables without the original catalog name. Identify `database:` settings, catalog vars and schema expressions; propose only the changes needed for that contract. Preserve intentional attached-database references pending a supported design. |
| Stored views and macros | Inspect existing `ref()`/`source()` overrides. Where supported, `.include(database=False)` renders schema-qualified relations that survive renaming. Preserve existing macro behavior, including versioned refs; verify adapter behavior before merging an override. |
| Timestamp-derived keys | Establish source meaning, landed type and session timezone. Confirm both sides derive keys from the same representation. UTC conversion is conditional on that evidence; timezone rewrites are compatibility diffs, not a universal dlt rule. |
| Native checks | Reuse schema, source-registration, dbt selector, package, Python and lint checks already mapped. Record missing tools or broken CI/profile paths as findings. |

Use the deployed runtime's supported commands against an established, authorized disposable target. After approved changes, test a renamed copy of a representative built database **without rebuilding its views**. Data tests and stored-view queries must resolve there. A local parse or successful build under the original database name does not pass this check. No target means unverified; it does not authorize infrastructure or loads.

## Consumer boundaries

Resolve requirements, plans and verification artifacts through the deployed consumer's contract, including `VD_INTENT_DOCS_ROOT` when provided. Do not relocate them to a preferred layout that executable checks reject. Retain existing CI; installation, replacement and SDK changes require concrete reviewed scope. Check the selected bundle/version before proposing CI installation. Runtime compaction, missing tools and defective bundles remain platform findings; extra repository prose cannot prove they are fixed.

Record consumer/version, input revision, each disposition, checks run and unavailable checks in the onboarding report. Context readiness and Studio execution readiness remain separate.
