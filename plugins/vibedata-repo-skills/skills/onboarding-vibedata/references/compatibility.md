# Compatibility decisions

A compatibility change is a concrete edit required for the selected runtime or platform to use the repository. It is separate from context generation.

1. Capture current input revision or file hashes, exact affected files/diff, enabling behavior, proposed check and expected side effects.
2. Use an existing explicit approval for that diff, or obtain a decision. Record `approved`, `declined`, or `pending`; elapsed time is never approval. A materially changed diff requires a new decision.
3. Apply only approved changes, verify that the input is still the reviewed input, then run the understood check against the approved target. If the input changed, reconcile before applying.
4. For declined/pending changes, preserve application bytes and record evidence, proposed action and which outcome is blocked: context readiness, execution verification, both or neither. Complete independent context work.

## Custom vocabulary and ADR locations

Emit the [workaround rule](../templates/rules/workarounds.md) only when a consuming skill names default vocabulary/ADR paths and the customer uses another location. Route vocabulary and ADR tasks through it before invoking that skill.

Resolve `artifact_paths.context` and `artifact_paths.adr` from `repo-map.json` for reads, writes and filename checks. These values override consuming-skill defaults such as `CONTEXT.md` and `docs/adr/`. Preserve existing ADR identifiers and formatting; an ADR pattern describes future filenames, not a renumbering operation. For a tracked glossary, the emitted check is `git ls-files --error-unmatch "<resolved-context-path>"`. For newly created untracked context, verify file existence and report it as untracked; onboarding does not authorize a commit.

Removal condition: the consuming skill and its executable checks resolve the map directly, with a passing fresh consumer trial. Record the consumer/version and observed hardcoded operation. If an executable hardcodes a default, prose cannot change it: record the failing check and follow-up, and leave that integration unverified. This change never patches the upstream consumer.

## Runtime discovery

Keep customer writes under the explicit repository root. Preserve instruction filename casing; report unsupported discovery before renaming. Treat denied context paths, such as Codex workspace-write protection of `.agents/`, as partial context. Record the denied path and required permission without relaxing the sandbox. A proposed alternate location follows the same compatibility-decision procedure above.

Use the [verification contract](artifact-contract.md#verification) for the selected runtime and requested consumer targets.
