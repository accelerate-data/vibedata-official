# VibeData Studio onboarding handoff

**We have not added VD onboarding.** The `onboarding-vibedata` skill prepares or refreshes repository context; the full VibeData Studio onboarding lifecycle remains unimplemented. Native requirement/design/setup, CI installation, review, certification, shipping and remote CI completion are planned work. End-to-end Studio execution is also unverified.

## Next agent's task

The latest user instruction authorizes the scoped commit, branch update, push and draft PR. The user declined installed-package Codex testing; it stays skipped and unverified, with no installation approval pending. **Run no more Claude tests.** Earlier “do 1–3, not 4” excludes Studio capability work. Gate 3 passes for the exercised fixtures; gate 1 retains captured scope failures. These gate numbers are not the implementation task numbers. Read the latest ledger entry before restarting anything.

Resume the [source-alignment execution ledger](../../context/onboarding-vibedata-source-alignment-run.md) for the approved [2026-10-16 plan](../superpowers/plans/2026-10-16-onboarding-vibedata-source-alignment.md). Preserve completed diffs and evidence; do not restart design. Task 7 remains blocked on a supported companion consumer release and an existing authorized disposable target. The older lifecycle plan remains a requirements record, not the current capability snapshot.

The user's later instruction, “read and execute docs/handoffs/onboarding-vibedata-studio-lifecycle.md unattended overnight,” authorizes executing the existing lifecycle plan. Its consumer dependency gate and scope exclusions still apply. Upstream consumer implementation, a merge and infrastructure creation remain outside scope. No submitted review from Hemanta Banerjee (`hbanerjee74`) was present in GitHub at preflight.

## Workspace and review

- Worktree: `/Users/shwetanksheel/scratch/ad-plugins/.worktrees/vibedata-official-onboarding-vibedata-plan`.
- Branch: `docs/onboarding-vibedata-plan`.
- Remote: `ssh://git@ssh.github.com:443/accelerate-data/vibedata-official.git`.
- Implementation baseline: `f9908cc00580a65f1d05e135710e6111cc3393cd`; this handoff and its plan follow that commit.
- PR: [#48](https://github.com/accelerate-data/vibedata-official/pull/48) was merged by `admiraldata` on 2026-10-15 at 20:39 +04, as `3e7c722786cbe0855c57aeaaa6153940eb67665d`. Its head was `36ab98da6e33d9f7d1d99b95de6b7bb4fb4f24af`. A later lifecycle implementation needs a new PR; do not update this merged PR as if it were open.

This handoff lives under `docs/handoffs/` as requested. The existing plan stays in `context/`; the nested handoff is outside the top-level operator pages published by `scripts/publish_wiki.py`.

## Read these artifacts

| Artifact | Purpose |
| --- | --- |
| [Lifecycle plan](../../context/onboarding-vibedata-studio-lifecycle-plan.md) | Requirements L01–L08, integration gaps, five tasks and acceptance gates. |
| [Current design](../../context/onboarding-vibedata-design.md) | Implemented preparation scope and preservation guarantees. |
| [Original implementation plan](../../context/onboarding-vibedata-plan.md) | Completed work; historical publication and draft instructions are superseded by the latest user instruction. |
| [Validation record](../../context/onboarding-vibedata-validation.md#reference-refresh-approved-after-audit) | Recorded checks, probes, runtime failures and evidence limits. |
| [Shared skill](../../plugins/vibedata-repo-skills/skills/onboarding-vibedata/SKILL.md) | Current five-step, explicitly user-invoked workflow. |

## First actions

1. Read the current alignment ledger and resume its first runnable incomplete gate; preserve completed diffs and evidence.
2. Recheck branch, changed inputs and runtime quota before a retry. Preserve unrelated changes and submodule pins.
3. For native lifecycle work, first resolve the companion consumer capability and identify its deployed release and existing authorized disposable target. Resume alignment Task 7 only then.

The 2026-10-15 investigation checked upstream `main` at `df262dc30d0b5b6c49a473369bd5cc9809e5be07`, manifest version `0.127.2`. All 23 inspected source files match the earlier local `ef128cac` snapshot. At that revision there was no `onboarding` kind or supported onboarding review entrypoint. `install-ci` and `verifying` commit/push; shipping pushes before its final PR approval. Native artifacts use the consumer's path contract, including `VD_INTENT_DOCS_ROOT`. The report records custom-hook replacement, linked-worktree and CI-completion gaps. Source inspection does not identify the deployed runtime or validate a mounted CI bundle.

That consumer checkout has unrelated untracked work and remains read-only. The historical reference `/Users/shwetanksheel/scratch/vibedata-showcase/sample-nyctaxi-comp` at `349d026` is the read-only brownfield reference, not a disposable test target. Its original `.agents/skills/onboarding/` defines the fuller lifecycle, but this session did not independently prove that lifecycle end to end. Read the shared project registry before cross-project inspection.

## Evidence and limits

The implementation baseline records 30/30 focused tests, 140/142 full-suite tests and 89% local coverage. [PR-head CI](https://github.com/accelerate-data/vibedata-official/actions/runs/38765041038), checked during this run, confirms 142 tests with the same two failures: `test_lists_onboarding_and_operate_pages` and `test_real_home_page_renders_cleanly`. Marketplace/version checks passed on that head. These are existing results, not tests of a lifecycle implementation; inspect current-head CI after any new push.

The user confirmed no disposable VibeData environment is available and accepted the earlier consumer check as unverified. That acceptance does not demonstrate the proposed lifecycle. Full Codex onboarding also remains partial under the earlier sandbox restrictions; application probes and structural checks do not establish live Studio execution. Keep all limits in the validation record and PR description.

Preserve explicit-only invocation in both runtimes, native customer map/checker contracts, lossless instructions, custom glossary/ADR paths and the Changes/Checks/Blockers report. Use existing authorization without redundant questions, but inspect delegated commit/push/CI effects before invoking them. No Domain creation, seeding, production loads, automatic merge, destructive Git operations or unrelated repairs are in scope. Real greenfield and brownfield Studio runs are required before claiming end-to-end verification.

## Suggested skills

- `superpowers:executing-plans` for the approved plan using native execution.
- `mattpocock-skills:writing-for-agents` and `superpowers:writing-skills` for the skill changes and behavioral trials.
- `superpowers:verification-before-completion` for evidence before completion claims.
- `superpowers:requesting-code-review` for the independent implementation review.

**Historical lifecycle next step:** Approve the companion consumer scope in the validation record so its missing onboarding capabilities can be implemented and released before lifecycle wiring resumes.

## Current source-alignment handoff

The 2026-10-16 unattended run uses `docs/onboarding-vibedata-plan@d07d1a8`, compares to fetched `origin/main@b878bf8`, and keeps local diffs without commits/push/PR. The read-only source is now `sample-nyctaxi-comp@b75841f12c14ad8e1870d1b1581d6bd59a0fb5bf`.

Current consumer source is `65222435e3483c4be0a612e20910abfbaf56d9cb` (0.128.12). It still has no onboarding kind/review. It now uses Domain-mapped Verification and `/run/vd/intent-context.json`; older artifact/environment claims above remain historical. No deployed release, mounted bundle or disposable Studio target has been established. Do not substitute a generic kind or invoke early-pushing phases.

Read the ledger for per-task outcomes, exact commands, input hashes and bounded evidence. Complete any remaining local gates before requesting expanded scope. The live restart action is to supply a released consumer with supported onboarding/review plus its deployed version and existing authorized disposable target. Native lifecycle composition then resumes at alignment Task 7.

The local checkpoint finished on 2026-10-17 (+04). Tasks 1, 2, 4, 5 and 9 passed their local checkpoints; Tasks 3, 6 and 8 retain failed or partial runtime acceptance; Task 7 is blocked and excluded. Independent review found no remaining confirmed implementation defect after fixes, but release acceptance is incomplete. Historical focused checks: 54 pass/1 skip. Full suite: 164 pass/2 inherited wiki failures/1 skip. Coverage: 89%. Enabled scaffold: 15/15 pass.

The quota-reset restart above is superseded by the 2026-10-17 resumed run. Do not repeat completed v3 trials or the two unsuccessful scope-wording repairs. Read `.superpowers/sdd/2026-10-16-onboarding-vibedata-source-alignment/RESUME.md` for the current failed/blocked gates, retained evidence and exact next action. Ordinary Claude loading, actual compaction and preservation have new evidence; this does not make the workflow safe under prompt-only file/network restrictions. The unproven main-skill addition was reverted, so the plugin still matches the reviewed frozen package. No automatic retry, commit or publication is scheduled.

Codex-only continuation completed at 08:30 +04. Two fresh ordinary-task checks pass on the retained Python/human-edit and native-map/DEC-27 fixtures. All ten commands stay within repository reads, and all 34 file hashes and five contained symlinks stay unchanged. The task-created copies are removed. See `codex-only-loading-evidence.json`; this is generated-context loading, not installed-package onboarding. The user subsequently declined the installation test and authorized a draft PR. Keep this gap and captured Claude failures visible during review. No more Claude tests or Studio work are permitted. Merge and release publication are not authorized.

Draft preparation integrated current `origin/main@b878bf8` into this feature branch at `404d320`, preserving the reviewed plugin inputs. Fresh checks at 08:39 +04 pass **168/169 tests with one opt-in integration skip and zero failures; coverage is 89%**. Main's existing wiki fixes remove the two historical failures. Marketplace/version, catalog and Ruff checks pass. Review the draft PR and current-head CI next; do not restart the declined installation or excluded runtime work. Merging the PR into main and release publication remain outside scope.
