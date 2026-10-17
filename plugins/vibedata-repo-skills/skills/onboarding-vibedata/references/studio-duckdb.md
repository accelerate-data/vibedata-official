# Studio on DuckDB

Use only when the selected consumer is Studio and the Domain platform is `duckdb_local`. Other platforms keep their own profiles, catalog semantics and ingestion setup. Inspect first; proposed configuration or macro changes follow [compatibility decisions](compatibility.md).

## Repository and Domain state

Establish Domain state from existing operator evidence or an authorized read-only check. An unknown state stays unknown; inspecting repository files cannot establish database contents.

| Implementation | Domain data | Treatment |
| --- | --- | --- |
| Empty | Empty | Greenfield context and the selected Studio scaffold requirements below. |
| Present | Present | Brownfield context and compatibility checks. |
| Present | Empty | Brownfield context; use only an authorized disposable sandbox sample as below. Persistent Domain remains empty. |
| Empty | Present | Warehouse migration assessment required; hold dependent scaffolding and preserve existing data. |
| Either | Unknown | Continue independent inventory; leave data-dependent classification and execution readiness unverified. |

Onboarding does not create a Domain or seed its persistent database. Sandbox state and persistent Domain state are separate observations.

## Bounded sandbox outcomes

With an empty persistent Domain, attempt each registered source's bounded sample and applicable dbt build only when an existing disposable target, source access, cost and side effects are authorized. Resolve the database from the current runtime contract; record its actual identity, source/version, supported limit, possible whole-page/row-group overshoot, landed rows and load metadata. A nominal row limit is not an exact cap. Stop dependent builds after failed/partial loads and report what landed. Use the dlt convention's repeated small sample to verify replacement.

If the target, authorization, affordable sample mechanism or execution capability is missing, do not attempt the load. Create a real proposal at the mapped location naming sources/size evidence, exact missing input, bounded steps and acceptance. Continue independent context work. Authentication failure stops that service path; report the login/refresh action without credential searches, retries or alternate providers. A successful sandbox sample never seeds the persistent Domain for later Intents. Report its state as empty/present/unknown from separate evidence.

## Runtime compatibility

Confirm the deployed Studio/plugin version and runtime contract before proposing edits. These checks apply to both greenfield and brownfield repositories; a local DuckDB example alone does not establish Studio compatibility.

For **every applicable row**, record applicability, before-state, proposed change, side effects, authorization, command/input revision and result or named gap in verification. Preserve suitable native configuration. A setup checklist is not permission to repair unrelated application code.

| Inspect | Required evidence or proposed change |
| --- | --- |
| Runtime dbt profile | Confirm the provided wrapper, `DBT_PROFILES_DIR`, `DBT_PROFILE_NAME` and `dev` target. Where required, propose `profile: "{{ env_var('DBT_PROFILE_NAME', '<existing-profile>') }}"` in `dbt_project.yml`, retaining the local fallback. |
| Local database path | Confirm local run scripts and the local profile use the same database. For the matching Studio contract, resolve it through `VD_EPHM_DUCKDB_LOCAL_PATH`; Studio supplies its own profile inside an intent. |
| Ingestion integration | If the selected integration uses `vibedata-dlt-duckdb-studio`, verify its supported version and initialization before installing or changing code. Its local run environment may require `VD_DOMAIN_DATA_PLATFORM=duckdb_local`, `VD_EPHM_DUCKDB_LOCAL_PATH` and `VD_DOMAIN_SECRET_STORE_KIND=local_toml`; confirm the actual secret-store binding. Preserve other ingestion implementations. |
| Source relations | A renamed Domain copy must resolve source schemas/tables without the original catalog name. Identify `database:` settings, catalog vars and schema expressions; propose only the changes needed for that contract. Preserve intentional attached-database references pending a supported design. |
| Stored views and macros | Inspect existing `ref()`/`source()` overrides. Where supported, `.include(database=False)` renders schema-qualified relations that survive renaming. Preserve existing macro behavior, including versioned refs; verify adapter behavior before merging an override. |
| Timestamp-derived keys | Establish source meaning, landed type and session timezone. Confirm both sides derive keys from the same representation. UTC conversion is conditional on that evidence; timezone rewrites are compatibility diffs, not a universal dlt rule. |
| Native checks | Reuse schema, source-registration, dbt selector, package, Python and lint checks already mapped. Record missing tools or broken CI/profile paths as findings. |
| Baseline commands | Run understood mapped dependency, parse, build, tests and lint commands once on the authorized sandbox, with the runtime wrapper/target it supplies. Record failures before edits. No target means an explicit execution gap. |
| Dependencies and evaluator | Confirm the selected CI bundle/version. Install declared packages before build/selector checks only within setup scope. Where that bundle requires `dbt_project_evaluator`, verify its supported package version; gate both its models and seeds with `var('dbt_project_evaluator_enabled', false)`. Confirm the bundle enables it for quality checks. Do not add it to other platforms by default. |
| Warning cleanup | Compare before/after test unique IDs and counts plus normalized compiled model/test SQL under unchanged inputs. Remove only generated comments/formatting when normalizing; preserve predicates, literals and test arguments. A removed test or changed predicate prevents a behavior-free verdict even if parse passes. See [compatibility](compatibility.md). |
| Arrow/Parquet metadata | Where the integration requires `_dlt_load_id` and `_dlt_id`, verify selected normalizer configuration and actual landed columns/load identity. Configuration alone is not landed-data evidence. |
| Staging access | Confirm bronze staging uses registered `source()` relations where required by the selected contract. Preserve intentional cross-catalog designs pending a supported mapping. |
| SQL lint | Check SQLFluff's selected dialect, templater, project and profile paths against actual commands and the runtime profile; never copy a credential-bearing profile into evidence. |
| Python lint | Use the mapped Ruff config and existing exclusions, including CLI exclusions. Report lint failures as findings unless their repair is in scope. |

Use the deployed runtime's supported commands against an established, authorized disposable target. After approved changes, test a renamed copy of a representative built database **without rebuilding its views**. Data tests and stored-view queries must resolve there. A local parse or successful build under the original database name does not pass this check. No target means unverified; it does not authorize infrastructure or loads.

## Consumer boundaries

Resolve requirements, plans and verification artifacts through the deployed consumer's current context reader and Domain-declared artifact paths. The inspected 0.128.12 source reads coordinates from `/run/vd/intent-context.json`; inherited environment variables are not proof of runtime identity. Do not relocate artifacts to a preferred layout that executable checks reject. Retain existing CI; installation, replacement and SDK changes require concrete reviewed scope. Check the selected bundle/version before proposing CI installation. Runtime compaction, missing tools and defective bundles remain platform findings; extra repository prose cannot prove they are fixed.

Before any native lifecycle call, verify supported onboarding kind, onboarding review, artifact resolution and phase side effects in the selected source and deployed version. Consumer 0.128.12 source (`65222435e3483c4be0a612e20910abfbaf56d9cb`) has no supported onboarding kind or review entrypoint; generic phases are not substitutes. Its CI installation and verification commit/push, and shipping pushes before final approval. Do not invoke those phases under local-only authorization. A companion consumer release and deployed target evidence are required; continue standalone context work and report Studio lifecycle blocked.

Record consumer/version, input revision, each disposition, checks run and unavailable checks in the onboarding report. Separate context, runtime loading, sandbox execution, persistent Domain state and conditional Studio lifecycle evidence.
