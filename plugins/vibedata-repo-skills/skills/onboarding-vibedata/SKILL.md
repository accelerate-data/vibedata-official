---
name: onboarding-vibedata
description: Prepare or refresh a data-engineering repository for VibeData while preserving existing code and conventions.
disable-model-invocation: true
---

# Onboarding VibeData

Invoke explicitly with `/vibedata-repo-skills:onboarding-vibedata` in Claude Code or `$onboarding-vibedata` in Codex.

Prepare reusable repository context. Keep customer conventions and application behavior. A normal source/model task uses existing context; it does not start onboarding.

## Workflow

1. **Inspect.** Resolve this installed skill directory as `skill_root` and the customer repository as `repo_root`. Run `python3 "<skill_root>/scripts/inspect_repo.py" --root "<repo_root>"`. Read discovered instructions/imports, scoped rules, maps and representative code as text. For a selected Studio/DuckDB target, check [Domain readiness](references/studio-duckdb.md) before classifying. Use [brownfield](references/brownfield.md) for an existing implementation or partial context, or [greenfield](references/greenfield.md) for an empty implementation. Done when mode, conventions, ownership and evidence gaps are known without executing application code.
2. **Reconcile.** Follow the [artifact contract](references/artifact-contract.md) for canonical instructions, preservation and mapped destinations. Reuse existing conventions before defaults. Require a preservation ledger when merging, moving or replacing existing instructions. Present actual conflicts with sources and effects. Done when retained destinations are known and pending decisions identify their dependent writes.
3. **Propose.** State the context changes. For compatibility changes, custom-path workarounds or runtime limitations, read [compatibility](references/compatibility.md). Done when each compatibility diff has an input revision, an explicit disposition and a readiness effect.
4. **Apply.** Merge independent context and approved changes into live artifacts. Preserve human edits and map extensions. If a write is denied, keep its proposed path blocked; an alternate location requires an explicit compatibility decision. Continue other writable artifacts. Done when the artifact contract is complete or each missing item has a specific blocker.
5. **Verify.** Follow the [verification contract](references/artifact-contract.md#verification) for structural checks, the selected runtime and authorized execution. Write [the report](templates/onboarding-report.md): changes, checks and blockers, with detail only where needed. Done when context readiness and execution verification have separate evidence, preservation is checked, and unchanged reruns leave artifact bytes unchanged.

Onboarding does not authorize production data writes, application conversion, unrelated repair, provisioning, commits, pushes or publication. Authentication failures stop the affected operation; record the login/refresh action without substituting a provider.
