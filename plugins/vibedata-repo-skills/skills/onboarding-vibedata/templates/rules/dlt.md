# dlt ingestion

Scope: {{confirmed_dlt_paths}}.
Preserve confirmed source/resource names, keys, write disposition and destination conventions. Read the existing example before adding a source. Register only actual pipelines and their required artifacts. Verify current dlt and destination initialization before SDK changes. Run understood loads only on an authorized target; production mutation needs its separate dry run and approval.

Read mapped source registrations before querying whether a source exists. Mirror an existing source of the same kind, including its artifact footprint. Use bounded samples while developing; use `DLT_INGEST_LIMIT` only when the implementation supports it. For a `replace` pipeline, prove replacement behavior with two sample loads. Run a full load only when the requirement asks for loaded data, once after the pipeline and docs are final; an additional full load needs an explicit reason and authorization.

Profile a remote source once per unchanged input. Save its identity/version, read time, sample scope and results at a mapped scratch location; reuse it for design and verification while those inputs remain valid. Verify loaded data against the landed table and saved profile. Changed or unknown source versions require a fresh profile or an explicit evidence gap.
