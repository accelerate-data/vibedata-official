---
name: workarounds
description: Use when a vocabulary or ADR task encounters the recorded consumer custom-path mismatch.
---

# Custom-path compatibility workaround

Scope: vocabulary and ADR reads, writes, updates and filename checks when the consuming skill uses hardcoded defaults.
Action: resolve artifact_paths.context and artifact_paths.adr from repo-map.json before invoking that skill. Use the mapped values in every operation and emitted check, overriding CONTEXT.md and docs/adr/ defaults. Preserve customer numbering and formats.
Reason: {{observed_consumer_version_and_hardcoded_operation}}.
Removal condition: the consumer and its executable checks resolve the map directly and a fresh consumer trial passes.
Verification: {{actual_consumer_evidence_or_unverified_blocker}}.

If an executable hardcodes the default, record its failure and follow-up. Prose cannot repair executable path handling. Emit this convention only when the mismatch exists. Reload it at task startup and after compaction whenever its recorded scope applies.
