# Existing repositories

1. Read the mechanical inventory, then representative configuration, code and tests as text. Identify package manager, entrypoints, data platform, actual sources, model/test conventions and exceptions. Attach each conclusion to a file location. Imports and notebook metadata are evidence of dependencies; importing a module or executing a notebook is not discovery. Keep notebook cells/outputs, secret contents and data rows out of generated context.
2. Read existing maps, glossary, ADRs, instruction imports and scoped rules. Preserve names, casing, numbering, formats and extension fields. An instructions-only or dependency-only repository has no substantive implementation and follows the greenfield branch. A partly onboarded implementation follows this branch and fills only observed gaps.
3. Map each real source by its current implementation kind (`python`, `notebook`, `dlt`, or the observed kind). List artifacts actually required by its confirmed convention in `required_artifacts`; name their paths in the entry or `artifacts`. Python sources do not need invented dlt pipelines, schemas or selectors. Register real tests and explicit gaps separately.
4. Reconcile instructions using the [artifact contract](artifact-contract.md). Compare existing rules with each other and the onboarding contract. Custom names are valid overrides. A conflict row names the competing sources, practical effect, recommendation and user decision. Pending conflicts block their dependent writes, not unrelated inventory.
5. Record bugs, unknown rationale and compatibility needs as findings. For a proposed change, use [compatibility](compatibility.md). Apply only the approved diff. Preserve declined/pending changes as follow-ups with evidence and readiness effects. A review document needs an actual finding; a proposal needs a substantial unresolved decision.

The completed report must distinguish observed facts from hypotheses. Unknown business meaning stays unknown until the user supplies evidence. Existing documents remain authoritative at their current locations. Human README, source code and notebooks change only under an explicit approved change.

Retain native check ownership. When the shared scaffold needs missing checks, use the [repository-check contract](artifact-contract.md#repository-checks), register actual commands and verify the emitted ADR command and native map checks.

For Fabric Git sources, `*.Notebook/notebook-content.py` with the `# Fabric notebook source` header is a notebook, even when it contains `%pip`, shell commands or cell magics. Inventory lists it in both `code_files` and `notebook_files`; `.platform` files add the `fabric` stack marker. Only static Python imports are inspected. Cell-magic bodies are opaque, so dependencies found only there need manual text inspection; ordinary malformed Python and malformed `.ipynb` still fail without source disclosure.

Preserve single-file ADR collections and notebook Markdown cells at a literal `artifact_paths.adr`, including existing `ADR NNNN` identifiers. Use their native checker or record the named ADR-link gap; do not emit the per-Markdown-file checker for container ADRs. Keep YAML source registration and a repeated notebook `SOURCES` cell when that is the confirmed convention. Map the real files and record any missing parity check as a source-registration gap. A notebook-generated dbt profile needs no invented local file: omit the local `dbt_profiles` role, retain its generation procedure and record the dbt-selector gap. Emit independent map/schema checks even when these native checks are unavailable; skips remain gaps in both the test map and report. These gaps alone do not block context readiness. See [Fabric compatibility](compatibility.md#microsoft-fabric) for execution limits.

## Convention inventory and procedures

Read rules hidden in code as well as file structure: numeric thresholds, caps,
WHERE/HAVING predicates, report windows, inner-join row loss, grain and comments
that explain why. A confirmed standing business rule belongs in an ADR; unknown
rationale is a review finding, not an invented decision. Keep SQL mechanics in
code, rule authority in the ADR and measured evidence in verification.

Inventory canonical models wherever the map places them. Gold marts without a
canonical model select [semantic creation](semantic-model.md); an existing model
selects reconciliation and maintenance. Register runner/source ownership through
the [map contract](artifact-contract.md#source-ownership). Preserve intentional
native formats and report any uncovered check.

Record every observed or moved convention once. Extend the existing preservation ledger with these columns when it already holds the evidence; do not maintain a second inventory of the same facts.

| ID | Convention | Evidence | Exceptions | Destination and scope | Confirmation state |
| --- | --- | --- | --- | --- | --- |
| C-1 | {{observed_convention}} | {{file_line_or_customer_decision}} | {{exceptions_or_none}} | {{retained_path_and_scope}} | {{confirmation_state}} |

Keep stable `C-n` IDs. States are `inferred`, `confirmed`, `changed by user`, and `dropped`. Established customer decisions are confirmed evidence; do not ask for them again. Read code and existing decisions before asking about unknown rationale, inconsistencies or ownership. Account for every moved clause and linked convention, including exceptions. A dropped row keeps its source and the decision that removed it.

An ordered, repository-only repair or operating procedure is a skill candidate, not automatically a convention. Emit its task-triggered skill only after the procedure, scope, side effects and owner are confirmed. Keep unconfirmed candidates as findings while independent context work continues.

## Review and later tasks

Use the [review template](../templates/review.md) for actual findings. Studio reviews have typed run metadata and stable `R-n` findings; preserve existing customer formats elsewhere. Triage does not approve a code edit. Use the separate [proposal contract](../templates/proposal.md) for substantial pending decisions.

Rehearse adding a source, changing a mart, and using the most relevant confirmed procedure; if none is confirmed, rehearse a connected intermediate-model change. Record one route table at mapped verification (or the native mapped/report equivalent): task, files read, files to change/create, applicable skills, and exact mapped commands. Resolve existing paths and legitimate future patterns. Mark commands unrun unless actually authorized and executed on a disposable target. Do not execute production builds for rehearsals. For repositories without marts, record that platform reason and rehearse the equivalent connected transformation.
