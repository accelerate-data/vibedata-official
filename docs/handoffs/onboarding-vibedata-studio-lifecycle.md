# VibeData Studio onboarding handoff

**We have not added VD onboarding.** The `onboarding-vibedata` skill prepares or refreshes repository context; the full VibeData Studio onboarding lifecycle remains unimplemented. Native requirement/design/setup, CI installation, review, certification, shipping and remote CI completion are planned work. End-to-end Studio execution is also unverified.

## Next agent's task

Continue the [Studio lifecycle implementation plan](../../context/onboarding-vibedata-studio-lifecycle-plan.md). Start with preflight and Task 1, which verifies a supported consumer contract. Read-only dependency checks can proceed; implementation follows the plan's approval boundary. Do not restart design or repeat the completed repository-preparation work.

The current user request authorizes this handoff, its plan, commit/push, ready-for-review status and a review request to Hemanta Banerjee (`hbanerjee74`). It does not authorize lifecycle implementation, a merge or infrastructure creation. Review approval has not been recorded in this handoff.

## Workspace and review

- Worktree: `/Users/shwetanksheel/scratch/ad-plugins/.worktrees/vibedata-official-onboarding-vibedata-plan`.
- Branch: `docs/onboarding-vibedata-plan`.
- Remote: `ssh://git@ssh.github.com:443/accelerate-data/vibedata-official.git`.
- Implementation baseline: `f9908cc00580a65f1d05e135710e6111cc3393cd`; this handoff and its plan follow that commit.
- PR: [#48](https://github.com/accelerate-data/vibedata-official/pull/48). The latest user instruction is ready for review, superseding the earlier draft instruction. Confirm live status and review feedback before continuing.

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

1. Verify the worktree, branch, status, PR head and Hemanta Banerjee's review feedback. Preserve unrelated changes and submodule pins.
2. Read the lifecycle plan and repository instructions. Preserve native inline execution; use an independent whole-change review at the implementation gate.
3. Establish Task 1's deployed consumer version and capability/side-effect table before wiring lifecycle calls. If a capability is absent, record a separately scoped upstream dependency.

Prior read-only inspection used `/Users/shwetanksheel/scratch/99_working/vibedata-data-engineering` at `ef128cac`, manifest version `0.127.2`. It found no `onboarding` kind and no `reviewing` skill. `install-ci` and `verifying` commit/push; shipping pushes before its final PR approval. Native artifacts use the consumer's path contract, including `VD_INTENT_DOCS_ROOT`. These are snapshot findings, not proof of the deployed version; the plan identifies the source files to verify.

That consumer checkout has unrelated untracked work and remains read-only. `/Users/shwetanksheel/scratch/vibedata-showcase/sample-nyctaxi-comp` at `349d026` is the read-only brownfield reference, not a disposable test target. Its original `.agents/skills/onboarding/` defines the fuller lifecycle, but this session did not independently prove that lifecycle end to end. Read the shared project registry before cross-project inspection.

## Evidence and limits

The implementation baseline records 30/30 focused tests, 140/142 full-suite tests and 89% local coverage. [Baseline PR CI](https://github.com/accelerate-data/vibedata-official/actions/runs/38742184056) confirms the two failures: `test_lists_onboarding_and_operate_pages` and `test_real_home_page_renders_cleanly`. Marketplace/version checks passed. These are baseline results; inspect current-head CI after any new push.

The user confirmed no disposable VibeData environment is available and accepted the earlier consumer check as unverified. That acceptance does not demonstrate the proposed lifecycle. Full Codex onboarding also remains partial under the earlier sandbox restrictions; application probes and structural checks do not establish live Studio execution. Keep all limits in the validation record and PR description.

Preserve explicit-only invocation in both runtimes, native customer map/checker contracts, lossless instructions, custom glossary/ADR paths and the Changes/Checks/Blockers report. Use existing authorization without redundant questions, but inspect delegated commit/push/CI effects before invoking them. No Domain creation, seeding, production loads, automatic merge, destructive Git operations or unrelated repairs are in scope. Real greenfield and brownfield Studio runs are required before claiming end-to-end verification.

## Suggested skills

- `superpowers:executing-plans` for the approved plan using native execution.
- `mattpocock-skills:writing-for-agents` and `superpowers:writing-skills` for the skill changes and behavioral trials.
- `superpowers:verification-before-completion` for evidence before completion claims.
- `superpowers:requesting-code-review` for the independent implementation review.

**Next step:** Complete Task 1's supported consumer contract and report any missing deployed capability before lifecycle implementation.
