# VibeData Studio onboarding handoff

**We have not added VD onboarding.** The `onboarding-vibedata` skill prepares or refreshes repository context; the full VibeData Studio onboarding lifecycle remains unimplemented. Native requirement/design/setup, CI installation, review, certification, shipping and remote CI completion are planned work. End-to-end Studio execution is also unverified.

## Next agent's task

Continue the [Studio lifecycle implementation plan](../../context/onboarding-vibedata-studio-lifecycle-plan.md) from its blocked Task 1 gate. Preflight and the source/dependency investigation have run; read the [consumer dependency report](../../context/onboarding-vibedata-validation.md#studio-lifecycle-task-1-consumer-dependency-report) before resuming. Do not restart design or repeat the completed repository-preparation work.

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

1. Resolve the separately scoped consumer dependency in the validation record, then identify the supported release deployed to an existing disposable target.
2. Recheck the worktree, branch, status and release capabilities. Preserve unrelated changes and submodule pins.
3. Resume Task 2 only after Task 1's gate passes. Preserve native inline execution and the independent whole-change review.

The 2026-10-15 investigation checked upstream `main` at `df262dc30d0b5b6c49a473369bd5cc9809e5be07`, manifest version `0.127.2`. All 23 inspected source files match the earlier local `ef128cac` snapshot. There is still no `onboarding` kind or supported onboarding review entrypoint. `install-ci` and `verifying` commit/push; shipping pushes before its final PR approval. Native artifacts use the consumer's path contract, including `VD_INTENT_DOCS_ROOT`. The report records custom-hook replacement, linked-worktree and CI-completion gaps. Source inspection does not identify the deployed runtime or validate a mounted CI bundle.

That consumer checkout has unrelated untracked work and remains read-only. `/Users/shwetanksheel/scratch/vibedata-showcase/sample-nyctaxi-comp` at `349d026` is the read-only brownfield reference, not a disposable test target. Its original `.agents/skills/onboarding/` defines the fuller lifecycle, but this session did not independently prove that lifecycle end to end. Read the shared project registry before cross-project inspection.

## Evidence and limits

The implementation baseline records 30/30 focused tests, 140/142 full-suite tests and 89% local coverage. [PR-head CI](https://github.com/accelerate-data/vibedata-official/actions/runs/38765041038), checked during this run, confirms 142 tests with the same two failures: `test_lists_onboarding_and_operate_pages` and `test_real_home_page_renders_cleanly`. Marketplace/version checks passed on that head. These are existing results, not tests of a lifecycle implementation; inspect current-head CI after any new push.

The user confirmed no disposable VibeData environment is available and accepted the earlier consumer check as unverified. That acceptance does not demonstrate the proposed lifecycle. Full Codex onboarding also remains partial under the earlier sandbox restrictions; application probes and structural checks do not establish live Studio execution. Keep all limits in the validation record and PR description.

Preserve explicit-only invocation in both runtimes, native customer map/checker contracts, lossless instructions, custom glossary/ADR paths and the Changes/Checks/Blockers report. Use existing authorization without redundant questions, but inspect delegated commit/push/CI effects before invoking them. No Domain creation, seeding, production loads, automatic merge, destructive Git operations or unrelated repairs are in scope. Real greenfield and brownfield Studio runs are required before claiming end-to-end verification.

## Suggested skills

- `superpowers:executing-plans` for the approved plan using native execution.
- `mattpocock-skills:writing-for-agents` and `superpowers:writing-skills` for the skill changes and behavioral trials.
- `superpowers:verification-before-completion` for evidence before completion claims.
- `superpowers:requesting-code-review` for the independent implementation review.

**Next step:** Approve the companion consumer scope in the validation record so its missing onboarding capabilities can be implemented and released before lifecycle wiring resumes.
