---
name: semantic-model
description: "Use when creating, editing or validating the canonical semantic model (Ossie, lakehouse logical model) — reverse-engineering it from dbt marts during onboarding, adding or refactoring a star, deciding which source supplies a field or measure, or explaining why a table is unmapped."
---

# Semantic model

The canonical model is Apache Ossie `0.2.0.dev0` — canonical definition in the upstream repo (exact links and pinned commit live beside the vendored machine schema, which is never edited) — flat document, one model per file, plus `VIBEDATA` extensions for the Oracle-style mappings Ossie core has no room for (aliases, multi-source LTS with content levels and filters, hierarchies, SCD, partitioning, metric aggregation rules, level-based and time-series metrics). Resolve model, mart, test and ADR locations through the repository map; paths in examples are illustrative. Preserve existing locations and skill ownership. Consumer formats (MetricFlow, Tableau, PowerBI) export from canonical on the fly and are never committed. Before commit, run the `validating-semantic-model` skill for the content review. Open `references/refactoring.md` for split, fold, rename, grain-change, rule-change, aggregate-lifecycle and star-retirement work; `references/reverse-engineering.md` when onboarding a lakehouse or adding a mart; `references/vibedata-fields.md` for what a payload field means; `examples/standalone.ossie.yaml` beside this file is the shape for a table with no star; `examples/star.ossie.yaml` is the shape to copy for a star: one document, one fact, a role-playing dimension reached by two relationships, a date dimension with a keyed time hierarchy, one aggregate source with its content levels and filter, a derived rate, and the VIBEDATA payloads (one at model level for `physical_tables`/`physical_joins`/`variables`, one per dataset, per relationship and per metric, each `data` a JSON-encoded string).

## Quick reference

| Question | Answer |
| --- | --- |
| Which commands gate a change? | `validate <dir>`, `coverage <dir> <marts>`, `suppliers <dir>`, `notes <dir> <tests-dir> <adr-dir>`, `level-tests <dir> <test-file> --check`; all five must exit 0 |
| Where does a refused column go? | The detail source's `note`, naming each column and why |
| Where does an unmappable table's reason go? | A `note` on its `physical_tables` entry |
| Where does a blocked decision go? | Ask first (`references/reverse-engineering.md`); write the entry plus its `note` only once ruled |
| Where does a business rule go? | The repo's decision record (ADR). The model cites the rule; it never restates it |
| Aggregate source or standalone document? | Metric and query filters plus requested grain decide (`references/refactoring.md`); their combined restriction must fit the source content |
| Detail or aggregate priority? | Detail-class `1` (one per role), aggregate `0` |
| What does an aggregate declare beyond its `column_map`? | `content_levels` from its `GROUP BY`, `content_filter` from its `WHERE` and inner joins, held by a test its `note` names (S3b) |
| A rate or ratio? | A `derived_expression` over its numerator and denominator metrics, bound to no column (S3c) |
| A level? | Declared once on the dimension (`levels[]`) with `keys[]`: exactly one primary, at most one display, every key unique at the level by declaration; a repeating name is an attribute (S5a) |
| A metric's population (billable only)? | `filter` on the base metric, read by its core expression too (S3c) |
| Grouped by a dimension its fact cannot reach? | Error by default; a separate metric with `unrelated_dimensions: total` repeats the value. Check with `ossie.py dimensionality` (S3c) |
| A bridge that fans a zone out to its POIs? | A relationship with `to_level` and `weight`; the weights sum to 1, held by a test (S4) |
| A month table beside the day table? | A `priority_group: 0` source of the same dimension with an own-level `content_levels` entry (S3b) |
| Sum per day, then average? Closing headcount? Mean of zone averages? | A dimension-based aggregation rule: `based_on_dimensions` across the inner level with the right `rule` (S3c) |

## Stars are atomic; documents partition stars (S1)

A fact's star is the set of dimension keys the fact carries as columns: every foreign key on the fact is a relationship into that dimension, whether or not the fact's own SQL joins it. `physical_join` names the equi join a consumer would execute; the fact's own `FROM`/`JOIN` refs only decide which aggregate sources are honest. A fact star — its fact, those dims, its relationships, its metrics, its aggregate sources — lives wholly inside one document. It is never split across documents, and there is no shared-dimension document: Ossie resolves relationships within a document only, and the schema is closed, so a cross-document reference is unexpressible and a "shared dims" file would leave every star broken.

Tables the population rule makes standalone share a document when they share a population: such a document declares no relationships and raises one `table-unjoined` per table, all expected. A dimension no gold fact can reach — an effective-dated reference table joined upstream — gets a one-dataset document whose `physical_tables` note carries the reason; that is not a shared-dimension document. A fact-to-fact key (a trip carrying `shift_id`) stays a degenerate field on the referencing fact unless both facts live in one document; never import another star's fact as a dataset to express the path. Two stars in one document share one copy of a common dimension. Two stars in separate documents each carry their own copy, and the copies must agree on the dimension's identity — `source`, keys, and every field — while the role-specific parts stay local: a role alias (`Pickup_Zone`) and a role logical source exist only in a document whose facts play that role. The validator compares same-named datasets, metrics, and physical tables across a directory and fails any that diverge in identity.

## Curated fields, not a mirror (S2)

`fields` are semantic attributes (keys, grouping/filtering dims, inputs to metric expressions) — a curated subset of the mart, never a column dump. Degenerate non-semantic columns stay out. A field the model drops is a scope decision, recorded in the change, not an oversight. Money types are `Decimal`, other floating values `Float`, integrals `Integer`, and a vendor type outside the enum pairs `Opaque` with a `custom_extensions` note. Establish the type from the source column as the staging or ingestion SQL produces it — never from the column name; where no SQL shows a cast, declare `Opaque` and record the unknown in the source `note`.

## Every field needs a supplying LTS (S3)

`logical_sources[].column_map` names the physical column behind each logical field or metric **per LTS**; an aggregate LTS maps only what its `content_grain` supports. Priority: detail-class `1` (one per role), aggregate `0`. Keep every detail at `1`: a consumer reads any non-zero value as detail supply, so inventing `2, 3, …` for aggregates makes an aggregate-only field look detail-supplied. Order aggregates with the source's own `join_cost` instead. Every declared field and metric needs a supplier; `suppliers` (run by the validating skill) lists any that has none, and nothing supplies an item a mode invents locally. `content_grain` names the grain in the LTS table's own result columns — including a derived one such as `weather_class` — falling back to the logical grain name only where no column expresses it; for a period-grain table name the period key (`shift_month`), never just the entity key, which reads as a false grain. It is a human-readable declaration (list of strings), not a validated reference. Right-side (physical) columns are verified by you against the mart SQL, never assumed identity — `validate` cannot see them, so a map onto a column that does not exist is green.

A join can narrow the population as much as a filter. An aggregate may answer only the metric/query population and grain its SQL proves; record its content filter including join loss. The query filter together with the metric filter must imply the source content filter. A narrower source cannot answer an unrestricted wider query; do not assume a future query restriction. Use `references/refactoring.md` for the disposition.

Metric names are compared across documents, so a name may not mean two populations: a metric answering a narrower population than the star's takes a scope-prefixed name (`billable_zone_day_trip_count`); a measure that also exists on another fact is named `<fact>_<measure>` (`shift_trip_count`); and a star metric name mapped on a filtered source retains its meaning and the source's explicit query eligibility restriction. A ratio is a `derived_expression` over numerator and denominator metrics, datatype `Decimal`, with no physical column binding (S3c).

**Prove the population before binding a metric.** Read the aggregate's `FROM`/`JOIN` clauses, its `WHERE` and its `HAVING` — not only its aggregate columns — and reconcile the result against the ADRs that rule that population (billable, verdicts, unresolved zones). An inner join to a banding seed whose ranges exclude negatives, a spine that covers only some boroughs, a `HAVING` that drops thin groups: each can make the table's rows a subset of the requested metric/query population, making it ineligible for that query however exact the aggregation. A table that contradicts an ADR raises a finding under `references/reverse-engineering.md`; resolve the conflict before binding it. Do not write the population into the document. A rule goes to an ADR, the mechanics stay in the mart SQL, and the reconciliation lives in a singular test — the source `note` points at that test. A prose population is a copy that goes stale the first time a filter moves.

Red-flag trap (seen in testing): mapping a filtered measure onto an unfiltered agg column, e.g. `billable_revenue` onto a monthly `total_revenue` — a monthly total is not billable-filtered revenue. No automated check can see this: treat every aggregate metric binding as guilty until the agg SQL proves it innocent, and record that proof in the source's `note` (the `validating-semantic-model` skill reviews it).

## Content tells an engine when an aggregate may answer (S3b)

`content_grain` is for people; `content_levels` and `content_filter` are for the engine. Every aggregate declares its levels and any population restriction; an omitted filter means all rows, never an unknown or unread restriction. `content_levels` names, per dimension role, the level the source holds and the source's columns that carry that level's key (`key_columns`), so the source can be joined to the dimension at that level: a query grouping by anything finer cannot use it, and a role it omits is summed away. The physical join from the source to the table the role reaches must exist. `content_filter` states every row the source holds as a predicate over the dataset's declared fields — its `WHERE`, and also the rows its **inner joins** drop (a null zone key, a null date key): an inner join is a filter. Report-window bounds read the `:report_start`/`:report_end` model variables, which are bound to the dbt vars the marts use, never a literal date. Write the predicate from the SQL, then hold it with a singular test that rebuilds each bound total from the detail under that predicate (the mapped aggregate-reconciliation test), and point the source `note` at it. A population no row predicate can state — a `HAVING` floor — keeps its filter and sets `navigable: false`, so it answers only when asked by name. The detail source maps every metric too: when no aggregate's content covers a query, the detail is the answer.

A dimension with tables at several grains (a day calendar and a month calendar, a customer table and a segment table) keeps one dataset. The row-level table is its detail source; each coarser table is a `priority_group: 0` source whose `content_levels` names the dataset's own level, with no `via`, and its `key_columns`. It maps only what that level determines: its keys and attributes and those of coarser levels, never a finer field. An aggregate at that level joins the coarser table at the level's key.

## Metrics carry their rollup rule (S3c)

Every metric declares `aggregation`. A ratio or rate is a `derived_expression` over its numerator and denominator metrics and binds to no column, so an engine rebuilds it after aggregation at any grain; a precomputed rate column is refused on every source. A distinct count is `NON_ADDITIVE`. A level-based metric (`at_levels`), a time-series metric (`time_series`) and a dimension-based aggregation rule (`based_on_dimensions`: evaluate at the `across` level, then aggregate across that dimension with `AVG`, `MAX`, `LAST`, …) are consumption measures, in OBIEE terms all of them. Each wraps exactly one other metric and repeats its core `expression`. Add one only when a consumer needs the number, and never one whose meaning depends on a filter the model does not state. Before writing one, decide which ratio or average the question means (weighted ratio of totals, or equal-weight mean of per-group values) from the table in `references/vibedata-fields.md`, and say which in the description. A semi-additive snapshot is `based_on_dimensions` with `rule: LAST` across a day level, not a plain `SUM`. Only members that have rows take part; densifying a calendar is a cube concern this model does not take on. The evaluation order there is normative: a logical-column formula is always applied last, to inputs already shifted or aggregated across a dimension.

A metric that reads a subset of its fact's rows declares that subset as `filter` (`trips.is_billable`), and its core expression reads the same columns: an engine matches the filter against an aggregate's `content_filter` to know whether the aggregate can answer. A metric grouped by a dimension its fact cannot reach fails by default (`unrelated_dimensions: error`). When a repeated total is genuinely wanted, as the denominator of a share across a dimension the fact does not have, declare a **separate** metric with `unrelated_dimensions: total`, and leave the base metric failing. Run `ossie.py dimensionality` to see what each metric reaches. A rolling window is `time_series` `ROLLING` over the calendar; a mart column that rolls over rows is refused, because a missing day stretches it.

## Additivity decides which measure becomes a metric (S3a)

A measure is additive only across the dims it can be summed over. A semi-additive fact — vehicle down-days (sums across vehicles, not across overlapping ranges), a balance, a headcount snapshot, a stock level — never becomes a plain `SUM` metric, because every consumer will then sum it across the dim it forbids. State the additivity limit in the field description and in the fact dataset's `description`, then choose one: supply no metric, and record the refusal in the detail source's `note` with the shape a legal metric would need; define a metric that expands to the legal grain (a daily expansion, an end-of-period pick); or define a per-event mean as ratio-of-sums over the same event count, which never totals the measure and so does not cross the forbidden dimension. An aggregate source whose grain crosses the forbidden dimension cannot supply that measure at all. `validate` cannot tell a plain `SUM` of a semi-additive measure from a legal one, so this is a rule you keep, not a check that keeps you.

## Aliases are physical rows, not flags (S4)

A role-playing dimension is one dataset and N relationships: `zone` stays a single dataset, `trips_to_pickup_zone` and `trips_to_dropoff_zone` both target it with different `from_columns`, and each relationship's `physical_join` names its own `physical_tables` entry with `table_type: ALIAS` and `alias_of` pointing at the base table. Do not clone the dimension into `pickup_zone`/`dropoff_zone` datasets — the endpoints that differ are the relationship's columns and the alias handle, not the dataset. A fan-trap is two or more declared paths into the same table with no distinguishing role; a bridge reached by one path needs no alias. Aggregate LTS tables point their joins at a dimension for reachability; no logical relationship backs them (aggs aren't datasets), and that dangle is structural, not a smell. The core `relationships[]` keep the equi fallback; the real predicate (including SCD as-of clauses) lives in the relationship's `join_expression`. A `physical_join` naming no model-level join fails `validate`.

A bridge that fans a dimension member out to many rows (a zone to its points of interest) lives in the star it serves. Its relationship joins the member, not a version (`to_level`), and carries the `weight` that allocates any measure crossing it from the one side. The weights of one member sum to 1, held by a singular test the bridge source's `note` names. Without a declared weight, no measure crosses that direction.

## Levels are declared from intent, keyed for joins (S5a)

A dimension declares its levels once (`levels[]`), and its hierarchies list them coarsest first; a level shared by two hierarchies (a day in Time and in Week) is one object. Each level carries `keys[]`, and every key identifies one member of its level **by declaration**. Exactly one key is primary: aggregate navigation, a join at the level and blending all use it. At most one is the display key. A field that describes a member without identifying it, such as a name several members share (`zone_name` covers more than one TLC zone; `month_name` repeats every year), is an `attribute`, never a key. `row_level` says which level one row is: when rows are members, the dataset's `primary_key` is one of that level's keys (`date_key` and `calendar_date` both key a day); when rows are versions of members (Type 2), the `scd.natural_key` is the level's primary key and every hierarchy over it states `scd_rollup` (`as_of` or `current`).

Map a dbt model systematically, in this order: (1) the `primary_key` and every `unique` test or constraint in the mart's properties YAML are candidate keys, and the column descriptions say which level each describes; (2) assign each candidate key to the level it identifies, choose the primary, and record readable columns that identify nothing as attributes; (3) write the hierarchies from the business's drill paths, not from what the data happens to satisfy; (4) for each aggregate, name the columns that carry each level's key. Never weaken a declaration because the data breaks it. Run `ossie.py level-tests` to regenerate the mapped level test, which reports a key that repeats, a key that names several members, a member with several parents, and an aggregate key value that is no member, as warnings. A reported row is a data finding for the mart or the consuming tool (`row_number() = 1` and the like), recorded where it belongs, such as the source `note` or an ADR.

## SCD and hierarchies ride the dataset (S5)

Versioned dimensions declare `scd`, their business key in `unique_keys` (`[[natural_key, valid_from]]`), `levels[]`, `row_level` and `hierarchies[]` (S5a; a level of a versioned dimension is keyed by the natural key, so a member survives its versions), and truly partitioned storage in `partitioned_by` — all naming real fields, all shaped per `references/vibedata-fields.md`.

## The model upgrades itself (S6a)

The key set and the spec version move together, and the tool is the authority. When either changes, upgrade every document in the same change rather than leaving old ones behind:

1. Change the schema and the checker together; the parity test that compares the checker's key sets with `scripts/vibedata-schema.json` is what stops the two drifting.
2. Rewrite every document mechanically — a script, never hand edits on payload lines — dropping or adding the affected key and stamping the new `vibedata_version` in every payload, so a document cannot carry two generations.
3. Run all mapped validation gates, including level-test freshness; a document left at the old shape fails `unknown-key` or the version check, which is the point.
4. Record the change in `references/vibedata-fields.md` with what moved and why, so the next upgrade has a precedent.

A `note` cites what backs it and nothing else: `held by <test-name>` for a reconciliation and `ADR NNNN` for a rule. `notes` (run by the validating skill) resolves both against the mapped test and ADR directories, so a renamed test or a superseded ADR leaves a dangling pointer that fails rather than a sentence nobody dares touch.

## Frozen keys (S6)

The `VIBEDATA` key set per level is closed and machine-readable in `scripts/vibedata-schema.json`, with field-by-field meanings in `references/vibedata-fields.md`. An unknown key fails validation (`unknown-key`). New keys arrive with their schema change, validator change, and tests, never by silent addition. `vibedata_version` rides every payload.

## Validate (S7)

Before commit, run the `validating-semantic-model` skill: it executes the structural gate (`validate`, `coverage`) and then reviews whether every mapping is honest. `validate` checks structure only — schema, names, references, payload keys, file naming — so a green run never means the content is right. The tool exits 1 on errors; a warning such as `table-unjoined` is factual (a table no join reaches), expected for standalone documents and aggregate handles.

After any mart change, update the canonical in the same change.

## Common mistakes
- Identity column maps assumed from siblings. Verify every right-side column against the mart definitions.
- New physical table without its `physical_joins` entries. The table exists but no query can reach it; `table-unjoined` warns.
- New key invented inline instead of arriving with its schema, validator, and test change. `unknown-key` fails it.
- `content_filter` copied from the mart's `WHERE` alone. Inner joins can also drop null keys, unmatched non-null keys and rows excluded by join predicates; reconcile the whole population.
- Window bounds written as literal dates. Use the `:report_start`/`:report_end` variables, or the filter goes stale when the dbt var moves.

## Red flags — stop and re-check

- "Validate is green, so the mapping is semantically right." Green proves shape and references, never business correctness.
- "The agg table must carry this column." Check the agg SQL; grain decides, not hope.
- "I haven't read the mart SQL, but the column name is obvious." Block: no mapping without reading the mart definitions. Unreadable mart means unmapped source with a `note`, never an assumed map.
- "One more key won't hurt." It fails. Use the schema file.
- "The aggregate obviously covers the same trips." Write the `content_filter` and run the holding test; an inner join says otherwise more often than not.
