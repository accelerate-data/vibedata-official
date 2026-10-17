---
type: onboarding
date: "{{review_date_with_local_zone}}"
commit: "{{reviewed_commit_and_worktree_hash}}"
source: "{{review_source_and_version}}"
---

# Onboarding review

Create one mapped review per type/run, only for actual findings. Preserve previous runs and customer formats. Each finding starts `open`; its kind is `platform`, `convention`, `bug`, `gap`, or `style`.

| ID | Kind | Finding and evidence | Effect and proposed action | Status |
| --- | --- | --- | --- | --- |
| R-1 | {{kind}} | {{finding_text_and_evidence}} | {{effect_and_bounded_action}} | open |

Triage changes only Status: `intent`, `proposal → P-NNNN`, `declined: <reason>`, or `deferred`. Keep each `R-n` ID and finding text unchanged through triage; append new evidence or a correction separately. A later run does not rewrite history.

Triage is not edit authorization. For any proposed edit, separately record the exact diff/input revision, owner and approval (`pending`, `approved`, or `declined`) under the compatibility contract. A finding routed to an intent or proposal does not authorize its implementation.
