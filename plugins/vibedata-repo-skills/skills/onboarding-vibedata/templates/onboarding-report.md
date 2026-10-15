# Onboarding report

## Readiness

| Outcome | Status: ready / partial / blocked / unverified | Evidence and blockers |
| --- | --- | --- |
| Repository context | {{status}} | {{preservation_and_structure_evidence}} |
| Execution | {{status}} | {{target_commands_results_or_unavailable_reason}} |
| Codex instruction loading | {{status}} | {{fresh_session_evidence}} |
| Claude instruction loading | {{status}} | {{fresh_session_evidence}} |
| VibeData consumer | {{status}} | {{real_consumer_evidence_or_blocker}} |

## Convention inventory

| Convention or exception | Source location | Scope | Retained artifact |
| --- | --- | --- | --- |
| {{observed_fact}} | {{file_line}} | {{applies_to}} | {{mapped_destination}} |

## Instruction preservation ledger

| Original clause or linked rule | Original source | Retained destination | Original and retained scope | Link/import target verified | Approved replacement, if any |
| --- | --- | --- | --- | --- | --- |
| {{exact_clause_or_rule_identity}} | {{file_line}} | {{file_section}} | {{scope}} | {{target}} | {{decision_or_none}} |

Every original instruction needs a row or an identified exact duplicate. Record original hashes and where the complete original text was secured before the first edit; omit secrets. Hashes alone cannot restore content. Replace CLAUDE only after this ledger is complete and destinations are checked.

Quote original imports and Markdown links as code in the ledger so they do not become active references from the report's directory. Any active retained-destination link must resolve relative to this report.

## Conflicts

| Sources | Competing requirements | Effect | Recommendation | Decision | Blocked writes |
| --- | --- | --- | --- | --- | --- |
| {{locations}} | {{alternatives}} | {{effect}} | {{resolution}} | {{pending_or_explicit_choice}} | {{dependent_paths}} |

## Compatibility changes

| Exact diff and input revision/hash | Enables | Disposition | Applied diff | Verification |
| --- | --- | --- | --- | --- |
| {{reviewable_change}} | {{behavior}} | {{approved_declined_pending}} | {{actual_or_none}} | {{command_and_result}} |

## Verification and follow-ups

| Check | Target and side effects | Actual command | Observed result |
| --- | --- | --- | --- |
| {{check}} | {{scope}} | {{command}} | {{observed_or_unrun}} |

After running each check, record its actual exit status and result here. A pointer to an ephemeral session transcript is not a durable result. If the same check has the same outcome on an unchanged rerun, preserve this report's bytes.

| Finding and evidence | Proposed action | Disposition | Blocks context / execution / neither |
| --- | --- | --- | --- |
| {{finding}} | {{action}} | {{decision}} | {{effect}} |

## Setup choices and sources

Record selected platform, package manager, verified versions/URLs, applied conventions and known gaps. Record uncertain meaning as unknown. Review/proposal links exist only for actual findings/decisions. An unchanged rerun leaves this report unchanged.
