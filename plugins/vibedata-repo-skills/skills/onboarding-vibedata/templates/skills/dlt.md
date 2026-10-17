---
name: dlt
description: Use when adding or changing dlt sources, resources, pipelines or sampling.
---

# dlt ingestion

Scope: {{confirmed_dlt_paths}}.
Preserve confirmed source/resource names, keys, write disposition and destination conventions. Read the existing example before adding a source. Register only actual pipelines and their required artifacts. Verify current dlt and destination initialization before SDK changes. Run understood loads only on an authorized target; production mutation needs its separate dry run and approval.

Read mapped source registrations before querying whether a source exists. Mirror an existing source of the same kind, including its artifact footprint. Use bounded samples while developing; use `DLT_INGEST_LIMIT` only when the implementation supports it. For a `replace` pipeline, prove replacement behavior with two sample loads. Run a full load only when the requirement asks for loaded data, once after the pipeline and docs are final; an additional full load needs an explicit reason and authorization.

Profile a remote source once per unchanged input. Save its identity/version, read time, sample scope, actual landed table/count, load IDs/status and results at artifact_paths.verification (or the native mapped evidence/report destination); reuse it for design and verification while those inputs remain valid. Verify loaded data against the landed table and saved profile. Changed or unknown source versions require a fresh profile or an explicit evidence gap.

A nominal sample limit is not an exact row cap. Check the selected loader's actual limit semantics before loading: dlt can count yielded pages, and a whole final page or Parquet row group can exceed a row threshold. Record requested limit, yielded page/row-group size, expected read cost and authorized budget first; unknown or excessive cost blocks that sample pending a supported smaller read or a decision. Report actual landed counts and failed/partial loads after execution. Never treat an attempted or partial sample as a safe completed load.

When adding a resource to an existing source, keep its parent source and pipeline identity. Update the existing source module, resource docs/tests, pipeline design and applicable dbt source/staging registrations together. Create another source/pipeline only when the source contract actually changes that boundary. A loader without `DLT_INGEST_LIMIT` support retains its own sampling mechanism.
