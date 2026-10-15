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

Load the packaged skill normally. Resolve helpers from its installed directory, pass `--root` explicitly, and keep customer writes under that root. Preserve instruction filename casing; report unsupported discovery before renaming. Consolidate only after checking symlink/hardlink aliases, import cycles and relocated references. Prove wrapper loading with a fresh normal session whose prompt does not name or paste the canonical file.

If the runtime denies a required context path (for example, Codex workspace-write protects `.agents/`), leave that artifact blocked and report context readiness as partial. Do not relax the sandbox or silently move the checker into application directories. Record the denied path and required permission; alternate artifact locations need an explicit compatibility decision. Independent allowed context work can proceed.

Standalone Codex/Claude success is separate from a VibeData build-session trial. Use a disposable supported consumer environment; an unavailable environment is a blocker, not a simulated pass. Stop the affected lane on authentication failure and report the exact login/refresh action. Continue independent authorized checks.
