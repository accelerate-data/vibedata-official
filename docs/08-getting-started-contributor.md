---
applies-to: vibedata v0.1.33
verified-against: studio@a121fc466
verified-on: 2026-08-13
submodules:
  ext/vd-data-engineering: 7e0163a92
  ext/domain-cicd: 70baf2c45
plugin-version: vibedata-data-engineering 0.39.1
sources:
  - ext/vd-data-engineering/agents/build.md
  - ext/vd-data-engineering/agents/detect.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/add-or-update-source/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/registering-dbt-sources/SKILL.md
  - docs/functional/intent-add-source/README.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/using-data-engineering/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/framing-intent/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/designing-data-product/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/building-data-product/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/verifying-data-product/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/publishing-data-product/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/skills/classifying-data-intents/SKILL.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/agents/design-reviewer.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/agents/code-reviewer.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/_shared/templates/design-template.md
  - ext/vd-data-engineering/plugins/vibedata-data-engineering/_shared/references/playbooks/ingestion-artifact-paths.md
  - deploy/docker/Dockerfile.backend
  - docs/functional/intent/README.md
  - docs/functional/domain/README.md
  - docs/functional/release-management/README.md
  - docs/design/source-connection-setup/agentic-source-connections.md
  - src/server/modules/source-connections/source-connections.service.ts
  - docs/functional/custom-plugin-management/README.md
---

# Getting started as a domain contributor

This page continues from [07-verify](07-verify.md), for a different reader: someone who opens
a domain that is already `Active` and has data work to do inside it. It teaches the concepts
you need first. [09-worked-example-salesforce](09-worked-example-salesforce.md) walks through
all of them once, start to finish.

## Who this is for

You have access to Studio and to one domain that already reports `Active`. Someone else —
an operator, with help from administrators — did the work in pages `01` through `07`:
deploying Studio, configuring the organisation, creating the domain, and binding it to a
data platform and a GitHub repository. None of that is your job, and you do not need to
understand how it was done. You just need a domain to work in, and you have one.

## What your domain already gives you

By the time a domain reaches `Active`, four things are already in place:

- A **Git repository**, holding every artifact your work produces.
- A **bound data platform** — DuckDB, MotherDuck, or Microsoft Fabric — where your pipelines
  land data. It was chosen and fixed when the domain was created.
- A **bound secret store**, where credentials live. You never see a secret value; you see
  only where one should go.
- A **place to register source connections**. You add one by asking the intent's agent, in
  chat — there is no form and no picker. The catalogue already lists official, verified
  sources; you do not populate it yourself.

There is nothing here for you to install, enable, or wait for a grant on. It exists the
moment the domain is `Active`. The agents that do the work — `build`, `fix`, `detect`, and
the two reviewers — come with Studio itself. Nobody assigns them to your domain, and you do
not enable them.

## Intent — the unit of work

An **intent** is a durable, resumable engagement between you and an agent, aimed at one
specific outcome inside one specific domain. It survives you closing your laptop, the agent
process restarting, and days passing between turns.

An intent is not a chat thread — a thread ends when you close the tab; an intent does not.
It is not a support ticket, filed and forgotten. It is not a live, running process. It is a
handle on a piece of work that lives in your repository and outlives every conversation you
have about it.

## Agent identity

Before an intent does anything, it fixes an **agent identity**: `build`, `fix`, or `detect`.
`build` creates and changes data products. `fix` answers questions about a data product that
already ships, and repairs it. `detect` investigates and reports findings; it changes no data
and no pipeline, it records what it read and what it found, and it raises GitHub issues as its
report. As a contributor, you almost always start with `build`.

You choose the identity in your first turn, and it is fixed for the intent's entire life —
even across a Studio upgrade. Pick `build` for the wrong reason and you cannot switch this
intent to `fix` later; you open a new intent instead. The **LLM profile** behind the agent is
different: you can change which model answers your intent at any time, on any identity.

## Three things you can do inside an intent

These are the parts of the interface most worth knowing early. All three are per-intent and
leave your repository untouched unless the agent commits something.

**Fork, when you want to try a second approach.** A fork creates a parallel, independent intent
from an existing conversation, without interrupting the work already in it. Use it when you want
to explore an alternative without losing the thread you have — the source intent keeps running
as it was. A fork is a new intent, so it fixes its own agent identity and repeats resource
selection; it does not inherit a decision you are trying to change.

**Attach a file to a message.** You can supply a text, Markdown, JSON, JSONL, NDJSON, CSV, image
or Excel file with a message. It is staged privately to that intent, mounted into the agent's
session, and referenced from the message you send it with. Treat an attachment as input to a
conversation, not as stored data: the bytes stay with the conversation, but there is no record
for the file of its own, no recovery workflow, and no guaranteed way to download it later. If it
matters beyond the conversation, it belongs in the repository.

**Ask for a profile or a chart of a file you are working with.** The agent can produce a data
profile of one session-local tabular file, and can render read-only charts and tables inline in
the conversation. Two limits are worth knowing. They describe **only the file supplied** — a
profile is not a statement about the completeness of an upstream query or the platform behind
it. And a chart is a snapshot, not a live view: it is retained and replayed exactly as it was,
including when you reopen the intent later or switch between light and dark, and it is never
recalculated from the source.

## The loop

Not every request runs a loop. A `build` intent first sizes the work.

- A **small change** to a data product that already exists — add, update, or remove a source
  connection, test a connection, adjust one model — runs directly. The agent does that one
  job and stops. There are no stages and no approval points. The proof is the check the job
  itself runs, such as a green connection test.
- A **product build** — build a pipeline on a source, add a new model, change a published
  contract, or extend the set of tables a pipeline lands — runs the full loop.

A product build moves through five stages: **Frame**, **Design**, **Build**, **Verify**, and
**Publish**. This guide uses those names to talk about the flow. They are not labels you pick
from a menu; the agent moves between them, and Studio shows its live checklist while it
works. Each stage finishes before the next begins.

Three points in a product build ask for your approval. Each one is a hard stop: the agent
does not continue until you answer.

- **Intent approval**, at the end of Frame. You approve what the work is meant to achieve.
- **Design approval**, at the end of Design. You approve the architecture and the plan for
  building it. This point opens only after the `design-reviewer` returns an approving
  verdict.
- **Ship approval**, at the end of Publish. You approve the finished branch. That approval is
  where the agent's work stops.

Build and Verify ask you for nothing. Their gates are automated: the pipeline or model runs,
the tests pass, the reviewers report. The agent moves on only when those come back green.

One more question can appear, inside Publish. If a contract change removes a column or
changes a column's type, the agent stops and asks you to confirm it. When the change would
break something that depends on that data, the option to abort is offered first.

Approval is explicit only. Typing "approved", "go ahead", "proceed", "yes", or "lgtm"
counts. Silence, a question back, or anything ambiguous does not — the agent never reads
your pause as a yes. Every approval is recorded with the time you gave it.

Two reviewers check the work before it reaches you, and you will see both by name in the
chat. `design-reviewer` reads the design, during Design, before the design approval.
`code-reviewer` reads the built work, during Verify.

## What you decide, what the agent does

You own three things: the intent's scope, resolving any ambiguity the agent surfaces, and
every approval point above. The agent owns producing the artifacts — drafting the intent,
proposing the design, writing the build plan, working through it, and verifying the result.
The decision you approved and the work that followed are recorded in the same place, so they
stay together.

## The artifacts are files in your repo

A product build keeps two durable records. Both live under `intent/<slug>/` in your domain's
repository, where `<slug>` is the intent's own identifier:

- `intent.md` — what you asked for and the scope you approved.
- `design.md` — everything after that. It holds the architecture, an inventory of what will
  be built, the build plan the agent works through step by step, a ledger of every check that
  ran and what it returned, and your approvals with their timestamps.

`design.md` is the plan and the evidence in one file. There is no separate plan file and no
separate verification file. When the agent asks for an approval, it links the file, so you
can read it before you answer.

Alongside them, the work itself:

- `ingestion/` — the dlt pipeline that lands your source data, and the connection settings it
  reads.
- `transformation/models/` — the dbt models built on top of it.

The agent also keeps a live checklist while it works. That list is not a file; it lasts for
the session only. If the session restarts, the agent rebuilds it by reading `design.md` and
the repository, and continues from the first stage whose result is not yet recorded.

Nothing here is a database row you cannot see. It is all plain files, on a branch, in your
repository.

## Where credentials live

A source connection needs a credential — a session token, a key, a password. That value
never goes into your repository and never goes into Studio's database.

The agent reads the exact secret name out of the connector itself, by introspecting it. It
does not invent the name and does not build it from your connection name. It tells you the
name and asks you to create that secret in your domain's bound secret store, outside of
Studio. Then it verifies the connection by running the connector. The first attempt usually
fails, because the secret is not there yet — that is the expected path, not an error. You
create the secret, the agent runs again, and a green result confirms the value is in place.
The connection is recorded in your repository only after that green result. Studio itself
never writes a secret value.

## Where dlt and dbt fit

Ingestion and modelling both run through intents, using two open-source command-line tools:
**dlt** lands your source data into Bronze — the first, rawest layer in your data platform —
and **dbt** builds models on top of it. Both are pre-installed where the agent runs; you
never install either one. You do not choose between them either. The kind of work you ask
for selects the tool: an `ingestion` intent uses dlt, a `transformation` intent uses dbt.
A product build runs the same five stages in both cases.

## What "done" means

A product build is done when its branch is committed and pushed, and `design.md` records every
check as passed and carries your ship approval. The result is a branch ready for review.

**The agent does not open the pull request.** That is the one step it stops short of, on
purpose. Raising the pull request, reviewing it, and merging it are yours — or your team's
automation's. Until someone opens it, the intent sits and waits.

Someone reading `intent.md` and `design.md` six months from now can still tell what was
asked for, what was built, what was checked, and who approved it.

[09-worked-example-salesforce](09-worked-example-salesforce.md) walks one intent through
every stage in this page, against a real, running source, so you can see the loop.
