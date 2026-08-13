---
applies-to: vibedata v0.1.33
verified-against: studio@a121fc466
verified-on: 2026-08-13
submodules:
  ext/vd-data-engineering: 7e0163a92
  ext/domain-cicd: 70baf2c45
plugin-version: vibedata-data-engineering 0.39.1
sources:
  - github.com/dlt-hub/verified-sources@master — sources/salesforce/__init__.py
  - github.com/dlt-hub/verified-sources@master — sources/salesforce/helpers/client.py
  - docs/functional/intent-add-source/README.md
  - docs/design/source-connection-setup/agentic-source-connections.md
  - docs/functional/instance-settings/secret-stores.md
  - src/server/modules/source-connections/source-connections.service.ts
  - src/features/chat/lib/harness-commands.ts
  - src/server/lib/workspace/workspace-path.ts
  - src/features/settings/components/Settings/modals/MotherDuckConfigSection.tsx
  - src/features/settings/components/Settings/modals/domain-destination/motherduck.tsx
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/add-or-update-source/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/add-or-update-source-keyvault/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/add-or-update-source-local-toml/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/test-source-connection/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/add-or-update-source/scripts/introspect_connector.py
  - ext/vd-data-engineering/agents/build.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/framing-intent/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/designing-data-product/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/building-data-product/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/verifying-data-product/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/publishing-data-product/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/classifying-data-intents/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/registering-dbt-sources/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/_shared/templates/intent-template.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/_shared/templates/design-template.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/_shared/templates/pipeline-inventory-template.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/_shared/references/playbooks/bronze-preview.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/_shared/references/playbooks/probe-rule.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/_shared/references/playbooks/dlt-resource-conventions.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/_shared/references/playbooks/ingestion-artifact-paths.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/_shared/references/conventions/domain-context-and-adrs.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/_shared/references/conventions/runtime-discipline.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/lib/contracts/reviewer-verdict.schema.json
---

# A worked example: Salesforce to a revenue mart

This page takes one source you have never connected and turns it into one dbt mart that
answers one business question. It uses a live Salesforce fixture that anyone reading this
page can reach, so every command below is a command you can actually run.

[08-getting-started-contributor](08-getting-started-contributor.md) teaches the concepts —
intents, agent identities, the loop, its approvals, its artifacts. This page does not repeat
them. Where the walkthrough reaches a phase or an approval, it names it and points back to
that page's **"The loop"** section.

## What you will build

Two intents, in order:

1. An `ingestion` intent that lands three Salesforce objects into Bronze with dlt.
2. A `transformation` intent that builds a dbt mart answering: **monthly closed-won revenue
   by product family**.

The second intent is the reason this page exists. The question sounds precise and is not.
You have to decide what it means before anything is built, and the difference between the
two possible answers is 22% of the closed-won total. Step 6 shows the numbers.

## Step 1 — Before you start

Three things must be true.

**Your domain reports `Active`.** Open it in Studio and check the status. If it does not, the
work in `01` through `07` is not finished and nothing on this page will run. That work is not
yours; ask whoever set the domain up.

**You can sign in and open an intent in that domain.** Nothing else needs installing,
enabling, or granting. The agents and the connector catalogue are already there — see page
08, "What your domain already gives you".

**The connection's credential values are in your domain's bound secret store.** This is the
one genuine hand-off on this page, and it may not be yours to do.

Studio never writes a secret value. Not into your repository, not into its own database, not
into `config.toml`. The values are created outside Studio by whoever owns the store, and dlt
reads them at run time. Who that person is depends on the store kind your domain is bound to:

| Bound secret store | Who creates the secrets |
| --- | --- |
| Azure Key Vault | Whoever can write secrets to the domain's Key Vault — usually an Azure administrator, often not you |
| Local TOML file | The operator who runs Studio. The file lives under Studio's data directory, outside your domain repository, and Studio writes nothing to it |

For this connection there are **two** values, not one:

- the demo token `vibedata-sfdc-ingest-ro-token`
- the twin's base URL `https://sfdc-twin.ainativedata.engineer`

The base URL surprises people. It is not confidential and it is printed all over this page,
yet the connector treats it as a credential, so it goes to the secret store like any other
one. **What counts as a credential is decided by the connector, not by whether a value looks
secret.** Step 3 shows what that means in practice.

You do not need either **name** yet, and you must not guess them. The agent reads the exact
names out of the connector in step 3 and tells you. What you need now is the two values and a
way to reach the person who can store them.

The token is printed in public documentation on purpose. The fixture is published as a
read-only demonstration source holding no real data, so the token is not treated as
sensitive. Treat a real Salesforce session token very differently.

## Step 2 — Meet the source

The source is a Salesforce twin at `https://sfdc-twin.ainativedata.engineer`. It is a
read-only demonstration fixture that speaks the Salesforce REST API. Querying it is expected
and safe. It holds synthetic bicycle-industry sales data: 27,600 opportunities, 69,000
opportunity line items, and 920 products.

### Check that the fixture is up

Run this before anything else, and run it again any time a later step behaves oddly:

```bash
curl -s -w '\nHTTP %{http_code}\n' https://sfdc-twin.ainativedata.engineer/healthz
```

A healthy twin answers exactly this:

```
{"status":"ok"}
HTTP 200
```

If you get a connection error, a timeout, or a `5xx`, the twin is unavailable. Nothing in
your own setup is wrong yet, and nothing after this point will work until it answers. This
check is the reason the rest of the page is diagnosable: it separates "the fixture is down"
from "my configuration is wrong".

### Look at the data before you touch Studio

The REST API takes the token as a bearer header:

```bash
curl -s -H 'Authorization: Bearer vibedata-sfdc-ingest-ro-token' \
  'https://sfdc-twin.ainativedata.engineer/services/data/v67.0/query/?q=SELECT+Id,Name,StageName,Amount+FROM+Opportunity+LIMIT+2'
```

The trailing slash after `query` is required. Without it the twin answers `404` with
`{"errorCode":"NOT_FOUND"}`, which looks like a broken fixture and is not one.

The response, abbreviated:

```json
{"totalSize": 2, "done": true, "records": [
  {"attributes": {"type": "Opportunity"},
   "Id": "006000000000000000",
   "Name": "Portland Bike Co. - 2025 Components Model Year Stocking Order",
   "StageName": "Closed Lost", "Amount": 462856.78},
  {"attributes": {"type": "Opportunity"},
   "Id": "006000000000000001",
   "Name": "Ridgeline Sports - 2025 Accessories New Dealer Order",
   "StageName": "Negotiation/Review", "Amount": 132076.57}
]}
```

Three failure shapes are worth recognising now, because you will meet them later:

- No `Authorization` header returns `401`.
- A wrong token returns `401` with `{"errorCode":"INVALID_SESSION_ID"}`.
- The login endpoints return `404`. The twin implements the REST data API and nothing else.
  This does not block anything: the connection you set up in step 3 uses a session token you
  already have, so nothing ever tries to log in.

**Do not ask the twin to count anything.** `SELECT COUNT() FROM Opportunity` returns
`MALFORMED_QUERY` with the message `DLT Extraction SOQL Profile v1 does not support aggregate
functions`. The same applies to `SUM()` and `GROUP BY`. Every aggregate on this page is
computed after the data lands, in your own data platform, which is where you want it anyway.

## Step 3 — Add the source connection

**There is no Add Source form, picker, wizard, or settings screen.** You add a source by
talking to the intent's agent in chat, and the sources panel only shows what has already been
recorded. Adding a source also does not enter the loop described on page 08. It is one
exchange, start to finish — no framing interview, no design phase, no reviewer, no approval
gate — and it either completes or it does not. The connection test is the only gate.

Open a `build` intent in your domain and type a request. What follows is the whole exchange,
in order.

**1. You ask.** Type something like *"Add a Salesforce source."* Use your own words. Asking
to add, update, or configure a source connection is what starts it — there is no command to
type and no exact phrase to learn. The `/add-source` command that older material mentions
was retired; this is a conversation now.

**2. The agent checks two things about your domain first.** That a data platform is set, and
that a secret store is set and of a kind it can work with. If either is missing, your
domain's setup is incomplete: the agent stops and tells you so, before it selects a connector
or installs anything.

**3. The agent lists the connectors available to you.** Salesforce comes from the official
catalogue entry, which you will see named `dlt-verified`. If a connector name appears under
two catalogue entries, the agent asks you which one and records your answer.

**4. You agree the connection name.** Lowercase letters, digits and underscores, starting
with a letter. The agent proposes a normalised form and waits for you to confirm. This page
uses `sf_twin`.

That one name is then used in several places at once, so pick a form and keep it: `sf-twin`
in one place and `sf_twin` in another fails later, with an error about an invalid schema
name. One connection is one entry, so two Salesforce accounts are two connections —
`sf_prod` and `sf_sandbox`, not one connection with two credentials. If the name already
exists, this run becomes an update and the agent shows you the current values first.

**5. The agent installs whatever the connector needs.** You install nothing.

**6. The agent reads the connector.** It asks the connector itself which authentication
methods it supports and which fields each one needs. Nothing here is guessed, and nothing is
taken from this page.

The connector is not part of Studio. It is maintained separately and changes on its own
schedule, so the authentication methods, the field names, and the resource list in step 4 can
all change without a Studio release. **If your own run shows something different from this
page, trust your run.**

Salesforce offers six authentication methods, so the agent asks you to pick one. Choose the
one shown as **`instance`**, with the display name **Instance**. It accepts a session token
you already have instead of logging in — which is what makes the twin usable, because the
twin has no login endpoint.

**7. The agent tells you which values are credentials, and asks you for the rest.** For every
field it treats as a credential it gives you the exact name to create and never asks you for
the value. For every other field it asks you for the value.

The connector decides which is which — not the agent, not you, and not whether a value looks
like a secret.

For the `instance` method, all three fields are credentials: `instance`, `instance_url`, and
`session_id`. **None of them is a value you type into a file.**

That is the opposite of what most readers expect. The base URL is a credential even though it
is printed all over this page, and the session token is not flagged as sensitive anywhere,
yet both go to the secret store. Which is exactly why you read the answer off your own run
rather than working it out in advance.

You need `session_id`, plus whichever of `instance` and `instance_url` you are using. This
page uses `instance_url`.

**Do not compute the names.** The agent gives you each one, and what it gives you depends on
your bound secret store:

| Bound secret store | What the agent gives you |
| --- | --- |
| Azure Key Vault | One vault secret name per credential field. Before prescribing a new name the agent lists the secret **names** already in the vault — never their values. Where a secret for this connection already exists under a different name it reuses that one and records the mapping, and where more than one could match it asks you which |
| Local TOML file | The section `[sources.sf_twin.credentials]`, with a key per credential field — here `session_id` and `instance_url` |

A name is never invented. It is either the name the connection itself resolves to, or one
that already exists in your store. Follow the names your own run reports.

**8. You create the secrets outside Studio.** Send each name, with `session_id`'s value
`vibedata-sfdc-ingest-ro-token` and `instance_url`'s value
`https://sfdc-twin.ainativedata.engineer`, to whoever owns the store, from step 1. The agent
cannot do this and never sees the result.

**9. The agent stages `config.toml`** in the working tree only, one section, no secret name
and no secret value:

```toml
[sources.sf_twin]
connector = "salesforce"
connector_source = "dlt-verified"
entry_point = "salesforce_source"
```

These three keys record which connector this connection uses. For this connection there is
nothing else to write, because every field this method asks you for is a credential. A connector with plain configuration fields would carry them here as extra keys.

Note what the section does **not** set: a `schema` key. That matters in step 5.

**10. The agent verifies, and the first attempt usually fails.** It runs the connection
exactly the way a real pipeline run would. If your secrets are not in place yet, the run
reports the names it looked for and could not find, and the agent asks you to create them —
through a question that waits for your reply, not a remark in passing. Then it verifies
again.

Expect this. It is the normal path, not an error, because you create the secrets outside
Studio and the agent has no way to know when you are done. This failure is also the most
reliable source of the names: the run states exactly what it looked for. If three consecutive
attempts fail on the same name after it has asked you, the agent stops, shows you what failed
and the verification output, and hands control back. That pause is a sanctioned outcome; resuming
re-verifies.

**11. On green, the agent commits and pushes.** It writes `ingestion/.dlt/config.toml` to the
intent's working branch and pushes it. Its definition of done is all three of: the section
written, verification green, and the branch pushed. A local commit does not count. The
connection then appears in that intent's source list.

**12. If you give up before green, nothing is left behind.** The agent reverts its
`config.toml` edit. An unverified connection is never written to the intent's working branch.

## Step 4 — Intent 1: land Salesforce into Bronze

Now the loop. Open a `build` intent and ask for the ingestion:

> Land Salesforce opportunities, opportunity line items, and products into Bronze from the
> `sf_twin` connection.

Everything below follows page 08's **"The loop"**. The loop has five phases — **Frame**,
**Design**, **Build**, **Verify**, **Publish** — and three approvals that belong to you.
This section names each phase and shows what it produces for this specific job; page 08
explains what the phases and approvals are.

### Frame

The agent classifies the request as `ingestion` work and writes `intent/<slug>/intent.md`.
That file is the durable record of what you asked for.

**The agent does not interview you.** It captures what your request already states, and it
writes every point your request leaves open into the file as an open question instead of
asking about it. It is allowed exactly one question, and only when a high-stakes axis — the
grain, the source objects, or the destination — is unstated and would change what gets
built. Everything else waits for the intent approval.

For this intent:

| What `intent.md` records | Value here |
| --- | --- |
| Goal | Land Salesforce deal data in Bronze so revenue can be modelled on it |
| Source system | The `sf_twin` Salesforce connection |
| Target | Your domain's data platform, Bronze |
| Objects in scope | Three resources: `opportunity`, `opportunity_line_item`, `product_2` |
| Deliverables | One row: the ingestion pipeline |
| Success criteria | The three tables land and can be queried |
| Out of scope | The other 12 resources |
| Open questions | Load history and refresh cadence. Your request states neither, and neither changes what is built now |

The connector declares **15** resources:

`sf_user`, `user_role`, `opportunity`, `opportunity_line_item`,
`opportunity_contact_role`, `account`, `contact`, `lead`, `campaign`, `campaign_member`,
`product_2`, `pricebook_2`, `pricebook_entry`, `task`, `event`.

One thing about that list is worth knowing before you choose from it. The twin exposes **36**
Salesforce objects, and the connector reads 15 of them. Every object the 15 resources need is
present on the twin, but the twin having an object does not mean the connector can read it.
`ProductFamily`, for instance, is an object on the twin and has no connector resource; the
product family you need in step 6 comes from a field on `Product2`, not from that object.

Frame ends at the **intent approval** — the first of three human approvals. The agent puts
the question to you with two options: approve, or ask for corrections. Nothing advances
without an explicit approval. Silence is not approval, and a question back is not approval.
Where the question arrives as free text rather than options, the accepted answers are
`approved`, `go ahead`, `proceed`, `yes`, and `lgtm`.

Read `intent.md` before you answer. The open questions are the reason. If the load history
or the refresh cadence matters to you, this is where you say so.

### Design

The agent reads the approved `intent.md` and writes `intent/<slug>/design.md`. These two
files are the whole durable record of an intent. `design.md` carries the architecture, the
inventory, the discovery evidence, the ordered build plan, a gate ledger, and the approvals.
There is no separate plan file and no separate verification file.

Its first move is to confirm the source is configured — that `[sources.sf_twin]` exists in
`ingestion/.dlt/config.toml`. It reads that file and never reads a secret value. Because you
did step 3, the section is there and discovery can run. If you had skipped step 3, the agent
would not guess: it would record that the source is not configured and add a build-plan step
to configure it first, so the schema is pinned only after the connection exists.

#### Where the data lands

The Design phase takes your domain's data platform as given. You pick nothing here. The
platform itself, and the workspace or database your domain is bound to, were fixed when the
domain was created and cannot be changed afterwards. A few named settings do stay editable,
and they differ by platform. All this step does is name where your rows arrive.

> **Applies to: DuckDB.** Skip if you chose MotherDuck or Microsoft Fabric. Your rows land in
> the **Database Path** and **Schema Name** set at domain creation — by default
> `<your-domain-slug>.duckdb` and schema `main`. The file path is server-managed under
> Studio's own data directory; you never see or enter a filesystem path, and Database Path is
> read-only after create. Schema Name is the exception: it stays editable from the domain's
> own settings.

> **Applies to: MotherDuck.** Skip if you chose DuckDB or Microsoft Fabric. Your rows land in
> the **Database** and **Schema** set at domain creation, inside your MotherDuck account. The
> binding is those two fields and nothing else — there is no Share to pick, on this release or
> any earlier one this guide covers. Both fields are fixed once the domain exists: the domain's
> settings panel shows them read-only and offers no edit path for either. That decision is
> already made; do not reopen it here.
>
> One consequence is worth knowing before you start work rather than after: only the bound
> database's **owner** can drive a MotherDuck domain. If the database belongs to somebody else,
> you will not be able to run this example in it, and no grant fixes that — sharing an intent
> and reassigning it are not offered on a MotherDuck domain.

> **Applies to: Microsoft Fabric.** Skip if you chose DuckDB or MotherDuck. Your rows land in
> the **Fabric Workspace**, **Lakehouse Name**, and **Schema Name** set at domain creation.
> All three are fixed. The optional **Ephemeral Workspace Capacity** is the one field in that
> binding you can still change, from the domain's own settings.

Four things are identical across all six deployment and platform combinations: the connector,
its resources, the modelling question in step 6, and every approval in the loop. Two tables on
this page vary with something other than your data platform — step 1's "Who creates the
secrets" and step 3's secret names. Both follow your bound secret store.

#### `Pipeline Inventory`

The agent runs schema discovery against each object you chose and writes one row per resource
under a `Pipeline Inventory` heading:

| resource | entry_point | columns | tables | data_type | write_disposition | incremental_cursor | notes | status |
|---|---|---|---|---|---|---|---|---|
| opportunity | salesforce_source | freeze | evolve | freeze | merge | SystemModstamp | primary_key=Id | working |
| opportunity_line_item | salesforce_source | freeze | evolve | freeze | merge | SystemModstamp | primary_key=Id | working |
| product_2 | salesforce_source | freeze | evolve | freeze | replace | | small reference table | working |

Read the columns. `write_disposition` is not a preference — it comes from the connector.
`opportunity` and `opportunity_line_item` are declared `merge` with an incremental cursor on
`SystemModstamp`, so repeated runs update changed rows instead of duplicating them.
`product_2` is declared `replace`, so every run rewrites it whole. The three contract columns
start in different states: `columns` and `data_type` are frozen from the first run, while
`tables` starts at `evolve` and is tightened once every resource has loaded.

#### The build plan

`design.md` also carries the **Build Plan** — the ordered steps the rest of the run
executes. One step per inventory row, or a sensible grouping, each naming what it produces
and the check that proves it. For this intent each step generates its resource in the dlt
pipeline, runs it in a sandbox, renders a preview of the landed rows, and runs its tests.

Nothing in that plan is marked done without an evidence line beside it: the command that
ran, its exit code, and the artifact it produced. This is also how a run resumes after an
interruption — the plan on disk wins over anything the agent believes.

When the design is written, a design reviewer reads it. The reviewer only reads; it changes
nothing. Its verdict is posted in the chat in full and recorded in `design.md`'s **Gate
Ledger**, alongside every other gate result for this intent.

### The design approval

The second human approval. It always fires, and there is no way to skip it. Read
`design.md`, then approve it or send it back.

A reviewer verdict is not an approval. The reviewer clears the way to the gate; you are the
gate. Your answer is recorded in `design.md`'s `## Approvals` section with a UTC timestamp,
and the gate itself is marked in the Gate Ledger.

### Build

This phase runs the build plan. **It asks you for nothing.** Its own automated checks are
the only gate. Nothing is marked done because the agent thinks it looks right: a step closes
only when the artifact it names exists on disk and its check has exited zero, and the
evidence line quotes that command and that exit code.

If the same operation fails twice in the same way, the agent stops repeating it. Two
identical failures mean the next edit will not change the outcome, so it reports the exact
error and hands back instead.

You will see this phase run for a while without asking you anything. That is correct.

### Verify

This phase runs a fixed suite of checks and records each one — the command, its exit code,
and the outcome — in the Gate Ledger. For ingestion work:

- **Destination identity** — asserts the destination the pipeline actually resolved matches
  your domain's platform. This catches a MotherDuck target quietly falling back to a local
  DuckDB file. A mismatch halts.
- **Fixture replay** — compares the load against a stored baseline, row-aware. On a first run
  there is no baseline yet, and the gate records `skipped` rather than failing. A mismatch
  rate above 1% halts, and so does a pipeline that returns three different results from the
  same input.
- **Pipeline audit** — a critical finding halts.
- **Development-artifact scan** — no development shortcut survives into the shipped pipeline:
  no test mode left switched on, no row limit left in, no target pinned to one environment. A
  hit fails the gate and must be fixed, never removed quietly.
- **A completion backstop** — a last pass that checks every claim the run makes is backed by
  something on disk. It returns `Verified`, `Downgraded`, or `Blocked`. Only `Verified`
  passes.

None of these is a judgement call. Each is a command with an exit code, and no finding is
downgraded to make the suite green.

Once the suite is green a code reviewer reads the work. Its verdict is posted in full, as
written, before any summary of it, and it is one of five:

| Verdict | What happens |
| --- | --- |
| `APPROVE` | The gate advances. |
| `APPROVE_WITH_WARNINGS` | The warnings go back to be addressed and the reviewer runs again. A second time, the warnings are surfaced and the gate advances. |
| `BLOCK` | The findings go back to be fixed and the reviewer runs again. A second `BLOCK` halts the gate and surfaces it to you. |
| `NEEDS_CLARIFICATION` | Comes straight to you. |
| `ERROR` | The gate halts. No retry. |

Any one gate gets two reviewer rounds at most.

**One check this phase will not do for you, and neither should you.** Do not confirm the load
by comparing line-item totals against the opportunity header `Amount`, and do not use a join
row count as a correctness check. The fixture is generated data and does not reconcile with
itself: `Quantity × UnitPrice` does not equal `TotalPrice` on any of the 69,000 line items,
`Quantity` values are fractional, 5,412 line items carry an `OpportunityId` that matches no
opportunity, and 15,179 carry a `Product2Id` that matches no product. None of that is a
defect in your pipeline, and a reader who used those as correctness checks would conclude
their own work was broken. Step 6 shows what to do with the orphans instead.

### Publish

This phase makes the branch ready to merge. It refreshes the pipeline documentation and
registers the landed Bronze tables into `transformation/models/sources.yml`. That
registration is where an ingestion intent hands its tables to dbt, and it is what makes
step 6 possible. It runs before the branch is declared ready, never after.

One conditional question can interrupt this phase on intents that change a model contract:
if a change removes a column or changes a type, the agent stops and asks you, and where the
change is breaking the first option offered is to abort. This intent builds no models, so
you will not see it here.

Then the branch is committed and pushed, and the **ship approval** — the third and last
human approval — asks you to approve. On approval the branch becomes a pull request. The
agent never approves this itself.

## Step 5 — Read what you got

Your Bronze tables are now in your data platform, in a schema named **`src_sf_twin`**.

That name is worth a moment, because it is not the connector's name. The destination schema
is whatever the connection's `schema` key declares in `ingestion/.dlt/config.toml`, and where
that key is omitted it defaults to `src_<connection name>`. Step 3's section sets no `schema`
key and the connection is called `sf_twin`, so the schema is `src_sf_twin`. Name your
connection `salesforce` and you get `src_salesforce` instead. Read this value out of
`config.toml`; never assume a schema name.

The three tables:

| Table | Rows | Shape |
| --- | --- | --- |
| `opportunity` | 27,600 | One row per deal, with `StageName`, `IsWon`, `IsClosed`, `Amount`, `CloseDate` |
| `opportunity_line_item` | 69,000 | One row per product on a deal, with `Product2Id`, `Quantity`, `UnitPrice`, `TotalPrice`, `Discount`, `Subtotal` |
| `product_2` | 920 | One row per product, with `Family` |

Every table carries dlt's own control columns alongside the source fields. Two matter to you:

- `_dlt_id` — a unique row identifier dlt generates.
- `_dlt_load_id` — which load produced this row.

There is also a `_dlt_loads` table, one row per load, recording when each load ran and whether
it completed. Joining `_dlt_load_id` back to `_dlt_loads` is how you tell which load a given
row came from. Leave the control columns alone in your own models: they are dlt's bookkeeping,
not business data.

The pipeline also wrote `ingestion/last-run-preview.md` in your repository — a short markdown
table of the landed rows for each table, so you can look at the result without opening the
warehouse. It is a real artifact, not a chat message; the Verify phase reads it directly.

Query the tables yourself now. This is the first point where aggregation is possible at all —
the twin refuses aggregate queries, your data platform does not.

## Step 6 — Intent 2: monthly closed-won revenue by product family

Open a second `build` intent and ask the question:

> Build a mart giving monthly closed-won revenue by product family, from the Salesforce data
> in `src_sf_twin`.

That sentence sounds precise. It is ambiguous twice over, and the agent will not build
anything until you resolve it.

### Why this does not go straight to a model

The Frame phase neither interviews you nor decides for you. It records what your request
states and writes every unresolved point into `intent.md` as an open question. It asks a
single question, and only where the answer would change what gets built — the grain, the
source objects, or the destination.

The rest surfaces at the intent approval. You read `intent.md`, you see the open questions,
and you settle them there. No model is written against an unresolved reading, because no
artifact is written at all before you approve the intent.

"Closed-won revenue" is unresolved twice over. One of the two has a measurable answer. The
other has no answer in any file.

### Question 1: what "closed won" means — this one can be measured

The `opportunity` table has three columns that all claim to describe the same thing:
`StageName`, `IsWon`, and `IsClosed`. Measure them before you approve the intent. If you do
not, the Design phase profiles the source tables and puts the same numbers in front of you
there, one approval later.

Measured across all 27,600 opportunities on 2026-08-07:

| Reading | Opportunities | Sum of `Amount` |
| --- | --- | --- |
| `StageName = 'Closed Won'` | 3,794 | $1,418,099,415.39 |
| `IsWon = true` | 2,961 | $1,105,896,541.69 |

The two readings differ by **833 opportunities** and by **$312,202,873.70**. Measure that
gap against the larger of the two readings — the $1,418,099,415.39 that
`StageName = 'Closed Won'` returns — and it is **22.0%**. Pick the wrong reading and your
closed-won figure is wrong by a fifth. (Against every opportunity in the system, won or not,
the same gap is 3.0%. Always say which total you mean.)

The 833 are not scattered noise. Every one of them is also `IsClosed = false`:

```
{'StageName': 'Closed Won', 'IsWon': False, 'IsClosed': False, 'Amount': 199573.11}
{'StageName': 'Closed Won', 'IsWon': True,  'IsClosed': True,  'Amount': 18917.09}
```

And the arithmetic closes exactly: 3,794 − 833 = 2,961. There are zero opportunities with
`IsWon = true` and some other stage. `IsWon = true` is precisely the subset of
stage-labelled wins that are also closed.

**This is a modelling question, not dirty data.** Nothing here is corrupt, missing, or
malformed. The records are internally consistent; they simply record two different things. The
stage label is where a salesperson has put the deal in the process. `IsWon` is whether the deal
has actually closed as a win. Both are true statements about the same record. A cleaning pass
would not help, because there is nothing to clean — someone has to say which of the two the
business means by "closed won", and that someone is you.

`IsWon = true` is the defensible reading, because a deal that is not closed has not produced
revenue. But nobody outside your business can settle it. If you have a documented business
rule that says otherwise, that rule wins — write it into `intent.md`.

### Question 2: what "revenue" means — this one has no answer anywhere

`Opportunity.Amount` is a header total on the deal. `opportunity_line_item` carries
`TotalPrice`, `UnitPrice`, `Quantity`, `Subtotal`, and `Discount` per product. Both are called
revenue by somebody.

Nothing in the data settles this, and nothing can. The question "which number does this
business call revenue" has no ground truth in any file. It also decides the grain, and grain
is the one axis the Frame phase is allowed to ask about — so this is the question you will
actually be asked.

It has a consequence you cannot avoid: **product family only exists on the line item.** A
header `Amount` cannot be split by product family at all. If you want the breakdown you
asked for, the grain must be the line item.

Line-item revenue, at line-item grain, summing `TotalPrice`, is the answer that fits the
question you asked.

### Where your answer is written down

Both readings go into **`intent.md`**, and you confirm them at the **intent approval** —
before Design, Build, Verify, or Publish run. That is the whole point of putting an approval
first. The reading is recorded once, in a file in your repository, before any model is
written against it.

It can also outlive this intent. When a Design decision sets a precedent — and choosing one
of several plausible business dimensions to aggregate by is exactly that — the agent writes
an architecture decision record into `docs/adr/` in your domain repository and links it from
the design. The next intent reads it before it starts.

Six months from now, the answer to "why does this mart say $1.1bn and the Salesforce report
say $1.4bn" is a line in `intent.md` with your approval next to it.

### Design

Grain is never something a file states until someone chooses it. You have now chosen: one row
per line item.

The Design phase profiles the source tables, lays out the layers, and writes a `Model
Inventory` — one row per model, each mart carrying its one-sentence grain. It also writes a
`Change Impact` section. On a first build that section says explicitly that nothing
downstream is affected.

A reasonable inventory for this job:

| Model | Layer | Grain |
| --- | --- | --- |
| `stg_sf_twin__opportunity` | staging | One row per opportunity |
| `stg_sf_twin__opportunity_line_item` | staging | One row per line item |
| `stg_sf_twin__product` | staging | One row per product |
| `dim_product` | mart | One row per product, carrying `product_family` |
| `fct_revenue` | mart | One row per line item, with its opportunity's close month and won flag |

Staging models rename and type the raw columns and drop dlt's control columns. `dim_product`
carries `Family` — the twin's nine values are `Accessories`, `Apparel`, `Components`,
`Electric Bikes`, `Helmets & Safety`, `Hybrid Bikes`, `Mountain Bikes`, `Road Bikes`, and
`Touring Bikes`. `fct_revenue` joins line items to their opportunity and to the product,
carrying `close_month`, `is_won`, `product_id`, and `total_price`. Monthly revenue by family
is then a group-by over `fct_revenue` joined to `dim_product`.

A design reviewer reads the design, and then the **design approval** fires. Same gate as
intent 1.

### The orphan rows are a design decision too

`fct_revenue` joins line items in two directions, and the fixture has orphans on both sides:

| Join | Orphans, of 69,000 line items |
| --- | --- |
| Line item to `opportunity`, on `OpportunityId` | 5,412 reference an opportunity that does not exist |
| Line item to `product_2`, on `Product2Id` | 15,179 reference a product that does not exist |

Both are properties of the generated fixture, not defects in your load, and both joins have
to do something about them.

An inner join drops the orphans silently. A left join keeps them, with nulls on the missing
side. Neither is wrong; they answer different questions. Whichever you choose, record it in
the design and make it visible in the model — a left join with an explicit `is_orphan` flag
lets a reader see how much revenue is unattributed instead of wondering why two numbers
disagree.

**Do not turn a join into a correctness check.** "The row counts match, so the join is right"
is exactly the wrong conclusion to draw from this dataset.

### Build, Verify, Publish

The build plan in `design.md` carries one step per `Model Inventory` row, each generating
its model, running it in a sandbox, and running its tests. Build runs them with no human
gate, closing each step only on a green check with an evidence line beside it.

Your dbt tests belong to the models, and they should assert what you actually decided:

- `unique` and `not_null` on each model's key.
- `not_null` on `product_family` in `dim_product`.
- `accepted_values` on the won flag.

Two tests you would normally write will fail on this fixture, for reasons that have nothing
to do with your work. Know about both before you write them.

**Do not assert `quantity * unit_price = total_price`.** Not one of the 69,000 line items
satisfies it.

**Be careful with a `relationships` test from `fct_revenue` to `dim_product`.** On a real
mart this test is expected, and review will look for it on foreign-key columns — but here it
fails on the 15,179 line items whose `Product2Id` matches no product.
If you kept those rows with a left join, test the relationship on the subset that is not
orphaned, or record in the design why the test is scoped that way. Do not delete the test
quietly and do not "fix" the data to make it pass.

Verify runs the transformation gates — a replay against the stored baseline, a dbt project
audit where any error-severity finding halts, the same development-artifact scan, and the
completion backstop — then a code reviewer reads the work. Publish enforces the model
contracts, refreshes the docs, and, after the ship approval, produces the intent's pull
request.

## Step 7 — What you have now, and where to go next

In your domain's repository:

```
intent/<ingestion-slug>/intent.md   design.md
intent/<mart-slug>/intent.md        design.md
docs/adr/                           (when a design decision set a precedent)
ingestion/.dlt/config.toml
ingestion/last-run-preview.md
transformation/models/sources.yml
transformation/models/
```

Two files per intent, and no more. `intent.md` is what you asked for and approved.
`design.md` is the plan, the build steps, the evidence for each one, the gate results, and
your approvals with their timestamps.

In your data platform: three Bronze tables in `src_sf_twin`, and two marts built on them
that answer a question with a recorded, approved definition behind it.

The part worth keeping is not the mart. It is that the definition of "closed won" is written
in a file, with an approval line and a date, next to the design that used it and the gate
ledger that records how it was verified. The 22.0% difference did not become an argument six
months later, because it became a decision on day one.

What to do next:

- **Change the reading and watch the number move.** Open a new intent and ask for the same
  mart on `StageName = 'Closed Won'`. Compare. The gap is the 833 rows.
- **Add a resource.** `account` and `campaign` are two of the twelve you left out. Adding one
  is another `ingestion` intent, and the connection already exists, so step 3 does not repeat.
- **Connect a real source.** The flow in step 3 works the same way for most connectors in the
  catalogue: only the authentication method and the secret names change, and the agent reads
  both out of the connector for you. Nine connectors are known not to work with it —
  `filesystem`, `rest_api`, `sql_database`, `mux`, `pokemon`, `scraping`, `kafka`,
  `pg_replication`, and `unstructured_data`. On any of them the agent halts and says why
  rather than guessing.
- **Read the concepts again.** [08-getting-started-contributor](08-getting-started-contributor.md)
  will read differently now that you have watched the loop run twice.

If a step behaved unexpectedly, check [90-troubleshooting](90-troubleshooting.md) — and check
the fixture health command in step 2 first.
