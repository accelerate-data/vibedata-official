# Onboarding report

Context: {{ready_partial_or_blocked_with_reason}}
Execution: {{verified_scope_or_unverified_with_reason}}
Selected runtime: {{requested_runtime_or_active_runtime}}

## Changes

- {{changed_paths_and_reason_or_no_changes}}
- {{preservation_result_and_evidence}}

Record new conventions or setup choices here with their sources/verified versions. Link to existing maps and rules instead of duplicating their inventory. Add the preservation ledger defined in the artifact contract only when existing instructions are merged, moved or replaced.

## Checks

| Target and side effects | Command or loading probe | Exit status and observed result |
| --- | --- | --- |
| {{scope}} | {{actual_command_or_probe}} | {{result_or_unrun_reason}} |

Include structural checks, the selected runtime's loading evidence and authorized project checks. Record results here; an ephemeral transcript link alone is insufficient.

## Blockers

{{none_or_each_finding_with_evidence_next_action_and_context_or_execution_effect}}

For an actual conflict, record sources, alternatives, effect, recommendation, decision and blocked writes. For a compatibility change, retain the exact diff, input revision/hash, disposition and verification; put applied changes under Changes and pending/declined changes here.

Keep existing report history, including prior ledgers and decisions. Omit unused optional detail rather than adding empty tables. Preserve this report's bytes when facts and outcomes are unchanged.
