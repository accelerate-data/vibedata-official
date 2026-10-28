# Recipes

Third-party content is collated from upstream sources, provided as is, and used at your own risk. vibedata does not review each upstream change.

| Recipe | Title | Area | Readiness |
| --- | --- | --- | --- |
| `adf-mapping-data-flow-to-dlt-dbt` | Convert an ADF mapping data flow into dlt and dbt and prove parity | transformation | supported |
| `api-to-bronze-incremental-contract` | Land a SaaS or REST API into bronze with an incremental cursor and a schema contract | ingestion | supported |
| `assess-synapse-ssis-for-fabric` | Assess a Synapse dedicated pool or SSIS estate for a Fabric rebuild and recommend whether to go | re-engineering | supported |
| `banking-aml-features` | Build AML monitoring features at account-day grain | transformation | supported |
| `banking-delinquency-vintages` | Build loan delinquency roll rates and vintage curves from loan, schedule, payment and event records | transformation | supported |
| `batch-cdc-current-state` | Build current-state tables from exported database change events | ingestion | supported |
| `bitemporal-business-history` | Preserve business-effective history and what was known at each reporting cutoff | transformation | supported |
| `bounded-partition-backfill` | Backfill a bounded date range after a logic change without a full refresh | transformation | supported |
| `business-event-fact` | Build a business-event fact with auditable duplicate handling | transformation | supported |
| `cost-attribution-by-model-job` | Attribute warehouse spend to the models and job runs behind it, keeping idle and untied cost visible | governance-cost | supported |
| `cpg-promotion-lift` | Measure trade-promotion lift and the post-promotion dip against an explicit baseline | transformation | supported |
| `cross-platform-dbt-macro` | Port a dbt macro to each approved warehouse without changing its callers | transformation | supported |
| `cross-platform-live-reconciliation` | Reconcile equivalent data across two live systems before cutover | data-quality | supported |
| `cross-platform-scheduled-job` | Convert a scheduled data job to another platform without changing its required behavior | orchestration | supported |
| `customer-consent-preferences` | Unify consent and communication preferences with auditable latest-wins logic | governance-cost | supported |
| `customer-historical-ltv` | Compute historical customer lifetime value with margin | transformation | supported |
| `customer-retention-churn-features` | Build retention cohorts and a churn feature table | transformation | supported |
| `customer-rfm-segmentation` | Score customers with RFM, maintain segments incrementally and explain every move | transformation | supported |
| `database-tables-to-bronze` | Load a database table set into bronze with a bounded incremental strategy and landed-data proof | ingestion | supported |
| `dbt-full-refresh-to-incremental` | Convert a full-refresh dbt model to incremental and show the runtime delta | transformation | supported |
| `dbt-refactor-output-identical` | Refactor dbt models without changing consumer output | transformation | supported |
| `dbt-snapshot-history` | Add dimension history with verified historical fact classification | transformation | supported |
| `effective-dated-bom-requirements` | Explode an effective-dated bill of materials into component requirements | transformation | supported |
| `effective-dated-business-rules` | Build historical event amounts from effective-dated business rules | transformation | supported |
| `event-resource-attribution` | Build auditable event-to-resource attribution | transformation | supported |
| `fabric-data-pipeline-as-code` | Author a Fabric Data Pipeline that sequences ingestion, dbt, and downstream refresh as committed code | orchestration | supported |
| `fabric-direct-lake-semantic-model` | Author a Direct Lake semantic model as code over governed gold tables | semantic-layer | supported |
| `file-drop-to-bronze` | Load a recurring file drop into bronze with file-completeness and schema controls | ingestion | supported |
| `finance-ap-aging` | Age payables from open items as of any chosen date and reconcile the total | transformation | supported |
| `finance-ar-aging-dso` | Age receivables and compute DSO from open invoices as of any chosen date | transformation | supported |
| `finance-budget-forecast-actual` | Compare budget and forecast to actuals at cost-center grain | transformation | supported |
| `finance-duplicate-invoice-detection` | Detect duplicate invoice candidates from explicit matching rules before payment | data-quality | supported |
| `finance-fixed-asset-rollforward` | Build a fixed-asset register and reconcile its net-book-value roll-forward | transformation | supported |
| `finance-gl-subledger-tieout` | Tie the general ledger to its subledgers and classify every break | transformation | supported |
| `finance-gross-margin-variance-bridge` | Explain gross-margin change with a reconciled price, volume, mix, and cost bridge | transformation | supported |
| `finance-revenue-recognition` | Generate the revenue-recognition schedule and deferred-revenue roll-forward from contracts | transformation | supported |
| `finance-thirteen-week-cash-plan` | Build a thirteen-week cash plan with traceable scenario assumptions | transformation | supported |
| `finance-trial-balance-close` | Produce the trial balance and close pack as code | transformation | supported |
| `finops-cloud-allocation` | Allocate cloud and platform spend to teams and flag untagged cost and daily spikes | governance-cost | supported |
| `finops-saas-license-utilization` | Measure SaaS licence utilisation and shelfware against contracts and invoices | governance-cost | supported |
| `governed-spreadsheet-table` | Promote a spreadsheet or CSV to a governed, tested table | ingestion | supported |
| `healthcare-claims-remittance` | Reconcile billed claims to payer remittances, denials and batch payments by payer | transformation | supported |
| `healthcare-readmission-cohort` | Build a thirty-day readmission cohort with explicit exclusions | transformation | supported |
| `hospitality-occupancy-adr-revpar` | Build nightly occupancy, ADR and RevPAR by property with closed-night restatements | transformation | supported |
| `identity-golden-record-crosswalk` | Deduplicate customers into a golden record with a source crosswalk | transformation | supported |
| `identity-standardize-names-addresses` | Standardize names and addresses and mint deterministic match keys | transformation | supported |
| `incremental-dbt-model-with-contract` | Author an incremental dbt model with its contract and prove idempotency | transformation | supported |
| `insurance-loss-triangles` | Build paid and incurred claims loss triangles by accident and development period | transformation | supported |
| `inventory-lot-traceability` | Trace a recalled input lot to affected shipments and flag unreconciled runs and lineage that cannot be traced | transformation | supported |
| `inventory-valuation-cogs` | Value inventory movements, closing stock and cost of goods sold under an approved costing policy | transformation | supported |
| `legacy-sql-to-dbt` | Convert a legacy SQL script or view into a dbt model and prove parity | transformation | supported |
| `life-sciences-enrollment` | Build clinical-trial enrollment and site-performance models with every screened subject accounted for | transformation | supported |
| `logistics-fleet-utilization` | Build fleet utilisation against explicit asset availability | transformation | supported |
| `logistics-lane-on-time-performance` | Build lane-day on-time transport performance with open trips and exceptions shown as approved | transformation | supported |
| `managed-connector-to-dlt` | Replace a Fivetran or Airbyte connector with a dlt pipeline and reconcile the result | ingestion | supported |
| `manufacturing-oee-downtime` | Build overall equipment effectiveness and a downtime Pareto | transformation | supported |
| `marketing-acquisition-cost-payback` | Build fully loaded acquisition cost and contribution payback by customer cohort | transformation | supported |
| `marketing-attribution-models` | Attribute conversions to touchpoints under several models side by side | transformation | supported |
| `marketing-campaign-budget-pacing` | Build a campaign-day budget pacing ledger against versioned flight plans | transformation | supported |
| `marketing-contact-pressure-eligibility` | Build cross-channel contact-pressure and send-eligibility decisions for planned contacts | transformation | supported |
| `master-b2b-account-hierarchy` | Resolve B2B account hierarchies and roll measures to the ultimate parent | transformation | supported |
| `master-product-sku-hierarchy` | Conform product and SKU hierarchies across systems | transformation | supported |
| `materialized-view-to-dbt` | Convert a materialized view into a dbt model and preserve its required refresh semantics | transformation | supported |
| `metric-population-and-rollups` | Build a metric with explicit eligibility and reconcilable rollups | transformation | supported |
| `metricflow-semantic-model` | Define governed metrics as a MetricFlow semantic model over a gold mart | semantic-layer | supported |
| `motherduck-flight-scheduling` | Schedule a dlt load and a dbt build on MotherDuck as a committed MotherDuck Flight | orchestration | supported |
| `move-dbt-project-destination` | Move a dbt project to a new destination and check parity before cutover | transformation | planned |
| `notebook-transformation-to-dbt` | Convert a notebook transformation into a dbt model and prove parity | transformation | supported |
| `operational-state-duration` | Build state durations by entity, location and reporting period | transformation | supported |
| `ops-inventory-reconciliation` | Reconcile inventory positions across warehouse, ERP and physical counts and give every difference a reason | transformation | supported |
| `ops-otif` | Measure on-time-in-full delivery by customer, carrier and plant | transformation | supported |
| `ops-procurement-spend` | Build the procurement spend cube and flag invoice lines on or off contract | transformation | supported |
| `order-return-contribution-margin` | Build order-line contribution margin with order and period rollups after refunds and returns | transformation | supported |
| `people-attrition-tenure` | Measure attrition, tenure and hire-cohort retention from the headcount outputs | transformation | supported |
| `people-headcount-rollforward` | Build period-end headcount and FTE by org and a roll-forward that ties every period | transformation | supported |
| `people-pay-band-gaps` | Check pay against salary bands and report pay gaps at an aggregate grain | governance-cost | supported |
| `people-payroll-gl-tieout` | Tie payroll to the general ledger at every cut-off and classify every break | transformation | supported |
| `pii-classification-and-masking` | Tag personal-data columns, mask them by kind for a lower-privilege audience and prove the masked outputs | governance-cost | supported |
| `point-in-time-training-dataset` | Build a training dataset that uses only information available at prediction time | transformation | supported |
| `procurement-open-commitment-rollforward` | Build the open purchase commitment balance and a roll-forward that explains every cutoff | transformation | supported |
| `procurement-savings-realization` | Reconcile negotiated procurement savings to realized invoice prices in a traceable savings ledger | transformation | supported |
| `procurement-supplier-rebate-accrual` | Accrue supplier rebates from purchasing contracts and reconcile settlements | transformation | supported |
| `procurement-three-way-match` | Match purchase orders, receipts and invoices line by line with an exception ledger | transformation | supported |
| `product-sessionization-funnels` | Sessionize event streams and build reproducible funnels from batch exports | transformation | supported |
| `prove-dbt-change-safe` | Assess an existing dbt change for safe merge without modifying it | data-quality | supported |
| `public-sector-grant-funds` | Track grant funds per award from authorization to drawdown and flag exceptions | transformation | supported |
| `readiness-gated-orchestration` | Gate a consumer pipeline on upstream data readiness instead of a clock | orchestration | supported |
| `retail-reservation-availability-ledger` | Reconstruct available-to-promise stock by SKU, location and cutoff from reservation and fulfilment events | transformation | supported |
| `retail-sell-through-stockout` | Build sell-through and stockout risk by store, SKU, and day | transformation | supported |
| `revops-bookings-billings-cash` | Tie bookings to billings to cash and classify every break | transformation | supported |
| `revops-pipeline-snapshots` | Build a periodic opportunity pipeline snapshot with stage conversion and slippage | transformation | supported |
| `revops-quota-commission` | Build commission-eligible bookings and quota attainment from explicit plan rules | transformation | supported |
| `saas-mrr-waterfall-nrr` | Build the MRR waterfall with net and gross revenue retention | transformation | supported |
| `sales-commission-payout-ledger` | Build a sales commission payout ledger with accelerator tiers, caps and clawbacks | transformation | supported |
| `sales-forecast-backtesting` | Score submitted sales forecasts against realized bookings by forecast horizon | transformation | supported |
| `sales-lead-opportunity-lifecycle` | Build an auditable lead-to-account-to-opportunity lifecycle that counts deals and new customers once | transformation | supported |
| `sales-quote-order-price-reconciliation` | Reconcile accepted quote versions to orders and invoices with a price-exception ledger | transformation | supported |
| `scalar-sql-function-to-dbt-macro` | Convert a scalar SQL function into a dbt macro and prove equivalence | transformation | supported |
| `scd-procedure-to-dbt-snapshot` | Convert a hand-written history routine into a dbt snapshot and prove history parity | transformation | supported |
| `service-ticket-sla` | Track ticket SLA attainment and backlog aging outside the vendor dashboard | transformation | supported |
| `shared-calendar-fiscal-periods` | Build one shared calendar and fiscal-period date table | transformation | supported |
| `shared-fx-conversion` | Normalize multi-currency amounts to a reporting currency with as-of rates | transformation | supported |
| `shift-unit-economics` | Build shift revenue, cost and margin with reconciled rollups | transformation | supported |
| `source-freshness-sla` | Declare source freshness SLAs and make stale data fail before downstream work | data-quality | supported |
| `spark-ingestion-notebook-to-dlt` | Convert a Spark ingestion notebook into a dlt pipeline and reconcile what it lands | ingestion | supported |
| `stored-procedure-to-dbt` | Convert a stored procedure into a dbt model and prove parity | transformation | supported |
| `telecom-cdr-usage` | Land call-detail batches and aggregate them into subscriber-day usage with manifest completeness | ingestion | supported |
| `usage-metering-rated-charges` | Calculate rated usage charges with allowances, tiers, credits and restated corrections | transformation | supported |
| `utilities-meter-to-bill` | Reconcile meter reads to bills and quantify unbilled energy | transformation | supported |
| `versioned-data-contract-cutover` | Add a breaking data contract change as a new version beside the old one and revise its named consumers | transformation | supported |

----

Generated by `scripts/build_catalog.py`. Do not edit by hand.
