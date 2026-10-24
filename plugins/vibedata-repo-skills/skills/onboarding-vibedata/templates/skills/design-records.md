---
name: design-records
description: Use when recording or changing component or shared-area design decisions.
---

# Design records

Scope: {{confirmed_component_kinds}}.
Resolve the appropriate design_record role in repo-map.json; shared decisions use design_record_area when mapped, otherwise the equivalent native mapped destination. Record non-obvious component decisions with rationale and alternatives when they exist. Keep recoverable implementation detail in code. Update an existing record when its decision changes; a path pattern alone does not require a document.

Cite governing ADRs at their mapped locations and maintain the ADR's affected-design links using the customer's format. Derive consumers from actual model/pipeline lineage. Keep a model's grain consistent with its implemented grouping and uniqueness checks; unresolved disagreements remain findings, not invented rationale.

Use Markdown ADR links in new records and register the reverse links under the ADR's `## Affected designs`. Run the mapped backlink check when either record changes.

Keep design records qualitative: decisions, reasons, alternatives, governing ADRs, affected consumers and history. Put numeric profile results, row counts, timings, measurements and check outcomes at artifact_paths.verification, or the equivalent native mapped/report destination when that role is absent. Link to that evidence from the design; preserve the native schema without adding roles just for evidence. Open data findings in a design name the issue qualitatively and link to evidence; they do not repeat measured counts. Preserve existing paths and history; relocation needs an explicit lossless migration.

A population definition or business threshold belongs in the governing ADR;
SQL owns the implementation. A canonical logical-source note cites the ADR and
its reconciliation test. Link these from a design record instead of copying a
population statement that will drift when a filter or join changes.
