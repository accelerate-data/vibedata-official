---
name: validating-semantic-model
description: "Use when checking a canonical semantic model before commit, after a mart change, or when asked to validate it or whether a metric is trustworthy — covering both the structural tool run and the content review that decides whether the model is honest."
---

# Validating a semantic model

Two passes, and the change is not done until both have evidence. The tool proves the document is well-formed; it cannot judge meaning. A green structural run says the file parses — not that a metric computes what it claims.

Resolve all command arguments from repo-map.json, including custom logical-model, mart, singular-test and ADR locations. The scripts live beside the authoring skill: `../semantic-model/scripts/ossie.py`. Tool behaviour — what each check reads, and what it cannot see — is in `references/checks.md`.

## Step 1 — structure

From the repo root, run `python3 .agents/skills/semantic-model/scripts/ossie.py validate <model-dir>` and require exit 0 with zero errors. Then `ossie.py coverage <model-dir> <marts-dir>` and require `0 coverage error(s)`, `ossie.py suppliers <model-dir>` and require an empty list — it is the instrument behind review item 1 — and `ossie.py notes <model-dir> <tests-dir> <adr-dir>` and require none dangling, which is what keeps a note's promises true after a test or ADR is renamed. Record each command with its exit code.

An error means the document is malformed; fix it and re-run before going further. Nothing in step 2 compensates for a document that does not parse.

## Step 2 — content

Work from the mart SQL, never from the model's own prose. Every item's evidence is a file you read and the line that settles it.

1. **Every declared field resolves.** Each field's `column_map` right side must be a column its mart's `SELECT` produces; for a `table_type: ALIAS` handle, check the table it is an alias of. A field with no `column_map` entry in any source is unsupplied — a finding.
2. **Every aggregate metric binding is honest.** The agg column must compute the same aggregation over the metric/query population. A filtered metric bound to an already aggregated unfiltered total fails if the filter cannot still be applied at that source's grain. A narrower source is eligible only when the query filter together with the metric filter implies its content filter; do not treat a mapping as eligibility for every query. Record the confirming sentence in that source's `note` and in your report — a binding whose note does not carry it is itself a finding.
3. **Rates are rebuilt, never averaged.** A rate or ratio metric is a `derived_expression` over its numerator and denominator metrics and binds to no column; `validate` fails a binding (`computed-metric-mapped`). Check the formula against the ADR that defines the rate. A `based_on_dimensions` metric's `rule` and `across` level must match the question its description states, and where a weighted and an unweighted figure both exist, each description names its weighting.
4. **Population matches the bound metric, not the table's name.** A rollup can remain in its star with a report window or billable filter when declared content restricts it to compatible metric/query populations and grains. It cannot answer an unrestricted wider query. A standalone document is needed only when no honest star mapping exists, not merely because one wider query must use detail. Account for truncation, row-dropping joins and different denominators.
5. **Filters, reach and bridges say what the SQL does.** A metric's `filter` restates the `CASE WHEN` or `FILTER (WHERE ...)` in its expression, no more and no less. Every `unrelated_dimensions: total` metric is a separate metric whose description says it repeats; its base still errors. A `weight` names the mart column that allocates, and the test the bridge `note` cites holds the sum of 1. A coarser dimension source maps only fields its level determines. Read `ossie.py dimensionality` for any metric a multi-fact query will mix.
6. **Content is the SQL, not a guess.** Each aggregate's `content_filter` restates its `WHERE` plus every row its inner joins drop, and its `content_levels` match its `GROUP BY` level by level, with the role (`via`) the join actually uses. Run the holding test against a built warehouse, or report it as unrun. Each level's keys come from the dbt metadata (`primary_key`, `unique` tests, constraints) and intent, a repeating name is an attribute not a key, and every aggregate content level names the `key_columns` that carry the level's key. Run the mapped level test after `ossie.py level-tests <model-dir> <test-file> --check` verifies freshness; regenerate with the same command without `--check` when declarations change and list what it reports as data findings; a report is never a reason to weaken a declaration.
7. **Semi-additive measures are not plain sums.** Down-days, balances, snapshots, stock levels: no `SUM` metric, and no aggregate whose grain crosses the forbidden dimension.
8. **Refusals are recorded.** Every declared field or metric an aggregate declines to supply, and every table that cannot be mapped, carries a `note` naming why. Refusing an undeclared physical column needs no note.
9. **Coverage is complete.** `coverage` proves the model set; the notes prove the gaps. A gold table with neither a handle nor a note is a finding.
10. **Datatypes and SCD are honest.** Each field's `datatype` matches the column the staging or ingestion SQL produces, and each `scd` claim matches the ADR that rules it — a Type 2 claim on a Type 1 source is a finding.
11. **Documents hold whole stars.** A dataset that exists only to bridge two documents is a partition error, not a table.
12. **Consumer parity.** When a dbt semantic layer exists, compare metric names and expressions against it. A divergence is a finding, not a curiosity.

## Step 3 — fix, or escalate

You fix what the model can settle without a business decision, and re-run all mapped structure, coverage, suppliers, notes and freshness gates afterwards. That is: a missing confirming sentence, a wrong `datatype` traceable to the staging or ingestion SQL, an unsupplied metric whose column is obvious, a dangling reference, a note that contradicts the SQL.

You escalate as a grilling session — one finding at a time, location → evidence → options → recommendation, waiting for the ruling before raising the next — when business meaning has multiple plausible interpretations, such as contradictory grain, an undefined population or a conflict with an ADR. If SQL and established decisions determine one honest disposition, make the evidence-backed model correction and record it; preserve an undecided mapping pending the ruling.

Never edit mart SQL, a seed or a macro to satisfy the model. If the mart is wrong, it is a finding about the mart, reported — the model records what the lakehouse actually does.

## Step 4 — report

Give the verdict, then each finding as location → evidence → fix, then the checks you could not run and why (no warehouse, no dbt, no catalog). A verdict of "passes" needs a cited file per claim, and every content fix is followed by re-running all mapped gates — a content edit is an edit.

## Red flags — stop and re-check

- "The tool says green." It says the file parses. Step 2 is unstarted.
- "The note says it was checked." Read the SQL; a note is a claim, not evidence.
- "No warehouse, so I'll assume the keys are unique." Report the unknown as unknown; never convert it into a pass.
- "One mapping looked odd but validate passed." That is a finding.
- "The model documents its own intent, so it is consistent." Read the mart and the ADR; a model can be green and wrong.
- "I fixed it while reviewing, so the review is done." Re-run all mapped gates after any fix, or the verdict describes a file that no longer exists.
