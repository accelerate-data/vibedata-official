---
name: adr
description: Use when recording, superseding or checking architecture or standing business decisions.
---

# Architecture decisions

Scope: durable decision tasks.
Resolve artifact_paths.adr from repo-map.json. Preserve numbering, history and format. Record an actual hard-to-reverse or surprising trade-off, with named alternatives, rationale and source. A user-supplied requirement alone is not an agent decision. Unknown historical rationale stays unknown. Use an index when no decisions exist; create a numbered ADR only when a decision qualifies.

Confirmed standing business definitions also qualify: measure, population, grain, week boundary or NULL handling. Cite the customer decision or evidence; reuse an existing answer before asking again. A reversible choice confined to one model or pipeline belongs in its design record. Keep links between governing ADRs and affected designs current; when an ADR is superseded, update affected records to cite its successor without deleting history.

For new Markdown records, use Markdown links and `## Affected designs`; a rejected predecessor keeps history and links its successor under `## Superseded by`. Update each active design to cite that successor. A literal ADR path can hold a collection or notebook Markdown cells: append in that native format with existing identifiers, without splitting history. Use the mapped native ADR command to check both directions; if none supports the container, record an ADR-link gap instead of claiming the per-file checker covers it.
