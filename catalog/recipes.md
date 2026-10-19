# Recipes

Third-party content is collated from upstream sources, provided as is, and used at your own risk. vibedata does not review each upstream change.

| Recipe | Title | Area | Readiness |
| --- | --- | --- | --- |
| `api-to-bronze-incremental-contract` | Land a SaaS or REST API into bronze with an incremental cursor and a schema contract | ingestion | supported |
| `bounded-partition-backfill` | Backfill a bounded date range after a logic change without a full refresh | transformation | supported |
| `business-event-fact` | Build a business-event fact with auditable duplicate handling | transformation | supported |
| `customer-historical-ltv` | Compute historical customer lifetime value with margin | transformation | supported |
| `customer-retention-churn-features` | Build retention cohorts and a churn feature table | transformation | supported |
| `customer-rfm-segmentation` | Score customers with RFM, maintain segments incrementally and explain every move | transformation | supported |
| `database-tables-to-bronze` | Load a database table set into bronze with a bounded incremental strategy and landed-data proof | ingestion | supported |
| `dbt-full-refresh-to-incremental` | Convert a full-refresh dbt model to incremental and show the runtime delta | transformation | supported |
| `dbt-refactor-output-identical` | Refactor dbt models without changing consumer output | transformation | supported |
| `dbt-snapshot-history` | Add dimension history with verified historical fact classification | transformation | supported |
| `effective-dated-business-rules` | Build historical event amounts from effective-dated business rules | transformation | supported |
| `event-resource-attribution` | Build auditable event-to-resource attribution | transformation | supported |
| `fabric-data-pipeline-as-code` | Author a Fabric Data Pipeline that sequences ingestion, dbt, and downstream refresh as committed code | orchestration | supported |
| `fabric-direct-lake-semantic-model` | Author a Direct Lake semantic model as code over governed gold tables | semantic-layer | supported |
| `file-drop-to-bronze` | Load a recurring file drop into bronze with file-completeness and schema controls | ingestion | supported |
| `finance-ap-aging` | Age payables from open items as of any chosen date and reconcile the total | transformation | supported |
| `finance-ar-aging-dso` | Age receivables and compute DSO from open invoices as of any chosen date | transformation | supported |
| `finance-budget-forecast-actual` | Compare budget and forecast to actuals at cost-center grain | transformation | supported |
| `finance-duplicate-invoice-detection` | Detect duplicate invoice candidates from explicit matching rules before payment | data-quality | supported |
| `finance-gl-subledger-tieout` | Tie the general ledger to its subledgers and classify every break | transformation | supported |
| `finance-revenue-recognition` | Generate the revenue-recognition schedule and deferred-revenue roll-forward from contracts | transformation | supported |
| `finance-trial-balance-close` | Produce the trial balance and close pack as code | transformation | supported |
| `finops-cloud-allocation` | Allocate cloud and platform spend to teams and flag untagged cost and daily spikes | governance-cost | supported |
| `finops-saas-license-utilization` | Measure SaaS licence utilisation and shelfware against contracts and invoices | governance-cost | supported |
| `governed-spreadsheet-table` | Promote a spreadsheet or CSV to a governed, tested table | ingestion | supported |
| `identity-golden-record-crosswalk` | Deduplicate customers into a golden record with a source crosswalk | transformation | supported |
| `identity-standardize-names-addresses` | Standardize names and addresses and mint deterministic match keys | transformation | supported |
| `incremental-dbt-model-with-contract` | Author an incremental dbt model with its contract and prove idempotency | transformation | supported |
| `legacy-sql-to-dbt` | Convert a legacy SQL script or view into a dbt model and prove parity | transformation | supported |
| `logistics-fleet-utilization` | Build fleet utilisation against explicit asset availability | transformation | supported |
| `managed-connector-to-dlt` | Replace a Fivetran or Airbyte connector with a dlt pipeline and reconcile the result | ingestion | supported |
| `master-b2b-account-hierarchy` | Resolve B2B account hierarchies and roll measures to the ultimate parent | transformation | supported |
| `master-product-sku-hierarchy` | Conform product and SKU hierarchies across systems | transformation | supported |
| `materialized-view-to-dbt` | Convert a materialized view into a dbt model and preserve its required refresh semantics | transformation | supported |
| `metric-population-and-rollups` | Build a metric with explicit eligibility and reconcilable rollups | transformation | supported |
| `metricflow-semantic-model` | Define governed metrics as a MetricFlow semantic model over a gold mart | semantic-layer | supported |
| `motherduck-flight-scheduling` | Schedule a dlt load and a dbt build on MotherDuck as a committed MotherDuck Flight | orchestration | supported |
| `notebook-transformation-to-dbt` | Convert a notebook transformation into a dbt model and prove parity | transformation | supported |
| `operational-state-duration` | Build state durations by entity, location and reporting period | transformation | supported |
| `ops-inventory-reconciliation` | Reconcile inventory positions across warehouse, ERP and physical counts and give every difference a reason | transformation | supported |
| `ops-otif` | Measure on-time-in-full delivery by customer, carrier and plant | transformation | supported |
| `ops-procurement-spend` | Build the procurement spend cube and flag invoice lines on or off contract | transformation | supported |
| `people-attrition-tenure` | Measure attrition, tenure and hire-cohort retention from the headcount outputs | transformation | supported |
| `people-headcount-rollforward` | Build period-end headcount and FTE by org and a roll-forward that ties every period | transformation | supported |
| `people-pay-band-gaps` | Check pay against salary bands and report pay gaps at an aggregate grain | governance-cost | supported |
| `people-payroll-gl-tieout` | Tie payroll to the general ledger at every cut-off and classify every break | transformation | supported |
| `pii-classification-and-masking` | Tag personal-data columns, mask them by kind for a lower-privilege audience and prove the masked outputs | governance-cost | supported |
| `prove-dbt-change-safe` | Assess an existing dbt change for safe merge without modifying it | data-quality | supported |
| `readiness-gated-orchestration` | Gate a consumer pipeline on upstream data readiness instead of a clock | orchestration | supported |
| `revops-bookings-billings-cash` | Tie bookings to billings to cash and classify every break | transformation | supported |
| `revops-pipeline-snapshots` | Build a periodic opportunity pipeline snapshot with stage conversion and slippage | transformation | supported |
| `revops-quota-commission` | Build commission-eligible bookings and quota attainment from explicit plan rules | transformation | supported |
| `scalar-sql-function-to-dbt-macro` | Convert a scalar SQL function into a dbt macro and prove equivalence | transformation | supported |
| `service-ticket-sla` | Track ticket SLA attainment and backlog aging outside the vendor dashboard | transformation | supported |
| `shift-unit-economics` | Build shift revenue, cost and margin with reconciled rollups | transformation | supported |
| `source-freshness-sla` | Declare source freshness SLAs and make stale data fail before downstream work | data-quality | supported |
| `spark-ingestion-notebook-to-dlt` | Convert a Spark ingestion notebook into a dlt pipeline and reconcile what it lands | ingestion | supported |
| `stored-procedure-to-dbt` | Convert a stored procedure into a dbt model and prove parity | transformation | supported |

----

Generated by `scripts/build_catalog.py`. Do not edit by hand.
