# Semantic skill seeds

Install only as directed by [the semantic contract](../../references/semantic-model.md).
`convention.md` becomes `SKILL.md` at the destination; the source filename keeps
these seeds out of normal skill discovery. Copy the whole directory for each
skill. Do not copy the examples into a customer's canonical model unchanged.

Reference source (see the audit provenance) at
`0e9fe609796b513e5ee303e809c00281624f5cd5`, `.agents/skills/semantic-model/`
and `.agents/skills/validating-semantic-model/`. Reused tooling implements
Apache Ossie core `0.2.0.dev0` with VIBEDATA `1.4`. The core validator and machine
schema retain upstream pin `c5cb931d72029dc523a5dd18d267f083403786f2` and its
Apache-2.0 LICENSE/NOTICE under `semantic-model/scripts/ossie_vendor/`.

Local adaptations: customer paths resolve through the map; derived ratios have
no column binding; aggregate eligibility depends on the metric/query population;
only ambiguous business meaning needs a ruling; full-directory validation checks
shared identities. The extension schema ID identifies this distribution. Local tool fixes cover coarser dimension level generation without `via`,
dataset-local field suppliers, and rejection of unsupported extension versions.
The schema and checker both pin VIBEDATA 1.4. The standalone example supplies
its two declared metrics, and both examples declare each metric's rollup rule.
These reference defects have regression tests. The generated level-test header
uses the mapped model location; instructions preserve native map and ADR contracts.

The CLI uses Typer's documented `Typer()` / `@app.command()` interface. Dependencies
are in [requirements.txt](requirements.txt); merge them into the customer's
chosen dependency manager rather than create a second environment. `sqlglot`
enables upstream SQL-expression parsing; without it that check emits a warning.
Reference pins are compatibility pins, not automatic upgrades. Official sources:
[Ossie schema](https://github.com/apache/ossie/blob/c5cb931d72029dc523a5dd18d267f083403786f2/core-spec/ossie-schema.json),
[validator](https://github.com/apache/ossie/blob/c5cb931d72029dc523a5dd18d267f083403786f2/validation/validate.py),
[Typer commands](https://typer.tiangolo.com/tutorial/commands/).

To refresh, compare the complete two-skill tree against a new reviewed source
revision, resolve prose/schema conflicts, preserve vendor files byte for byte,
update this record and run `tests/test_onboarding_semantic.py`. Schema migrations
must update every existing document's extension payload in the same change;
never overwrite human edits by copying a new seed over an installed tree.
