---
name: onboarding-vibedata
description: Use when a user explicitly asks to onboard, initialize, or refresh a data-engineering repository for VibeData, including an existing dbt/dlt or Python/notebook estate, a partly onboarded repository, or a blank project.
---

# Onboarding VibeData

Prepare reusable repository context. Keep customer conventions and application behavior. A normal source/model task uses existing context; it does not start onboarding.

## Workflow

1. **Inspect.** Resolve the installed directory containing this skill as `skill_root` and the explicit customer repository as `repo_root`. Run `python3 "<skill_root>/scripts/inspect_repo.py" --root "<repo_root>"`. Read the discovered instruction files and their imports, applicable scoped rules, maps and representative code as text. Read [brownfield](references/brownfield.md) for an existing implementation or partial context; read [greenfield](references/greenfield.md) for an empty implementation. If mode is unclear, resolve that fact before dependent setup. Done when the inventory identifies mode, conventions, instruction ownership, actual artifacts, and missing evidence without executing application code.
2. **Reconcile.** Read [artifact contract](references/artifact-contract.md). Resolve artifact roles from the existing map and customer documents before selecting defaults. Build the preservation ledger and conflict table from [the report template](templates/onboarding-report.md). Present unresolved conflicts with their sources and effects. Done when every original instruction has a retained destination or explicit approved replacement; pending decisions identify only the writes they block.
3. **Propose.** State artifact destinations and separate compatibility changes from context work. For a compatibility change, read [compatibility](references/compatibility.md), show the exact diff and input revision, and record `approved`, `declined`, or `pending`. Existing authorization for that exact diff is sufficient. Done when each change has a disposition and separate context/execution readiness effect.
4. **Apply.** Write independent context artifacts and approved changes. Use templates as shapes, merging live content instead of replacing it. Canonical instructions are `AGENTS.md`. When `CLAUDE.md` exists, consolidate every unique instruction into AGENTS or a reachable rule with the same scope, verify the ledger and moved links, then replace CLAUDE with only `@AGENTS.md`. Resolve aliases and conflicts before those writes. Emit only applicable rules and evidence-backed vocabulary/decisions. If a write is denied, keep that artifact blocked at its proposed path; an alternate location for rules, templates or checks requires an explicit compatibility decision. Read [compatibility](references/compatibility.md) and complete the other writable artifacts. Done when the artifact contract is complete or each remaining item has a specific blocker; human edits and map extensions survive.
5. **Verify.** Run the mapped context check from the explicit repository root. Run understood project checks only against an established, authorized target. Rehearse a later task through the maps and applicable rules; check both runtimes' normal instruction loading when available. Report **context readiness** and **execution verification** separately, with commands, outcomes and unresolved follow-ups. Done when preservation and structure have evidence and every unavailable runtime/consumer check is marked unverified. An unchanged rerun leaves artifact bytes unchanged.

## Reference selection

| Situation | Read |
| --- | --- |
| Existing code, notebooks or partial onboarding | [Brownfield](references/brownfield.md) |
| No substantive implementation | [Greenfield](references/greenfield.md) |
| Map fields, instruction consolidation, rerun maintenance | [Artifact contract](references/artifact-contract.md) |
| Compatibility diff, custom vocabulary/ADR paths, runtime limitation | [Compatibility](references/compatibility.md) |

## Common failures

- A prose summary alone omits the artifact contract. Produce the maps, canonical routing, applicable rules and checker; list blocked items precisely.
- An unknown platform blocks dependent scaffolding. Independent inventory, vocabulary placeholders and instruction preservation can proceed.
- Example sources remain templates until a real source is confirmed. Empty business inventories and missing coverage are valid facts.
- A pending conflict retains both alternatives for decision. Preserve the affected files until the decision is explicit.
- Structural success does not prove runtime loading, VibeData consumer behavior or warehouse execution. Record each observed boundary.

Onboarding does not authorize production data writes, application conversion, unrelated repair, provisioning, commits, pushes or publication. Authentication failures stop the affected operation; record the login/refresh action without substituting a provider.
