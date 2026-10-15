# Getting started as a Domain contributor

This page describes the data-engineering behavior baked into the exact `vd-data-engineering` submodule pinned by this Studio SHA.

## The three main agents

Current plugin behavior has three sibling identities:

| Agent | Use it for |
| --- | --- |
| `build` | New or changed data products: ingestion, transformation, orchestration, semantic models |
| `fix` | A defect or question anchored on an already-shipped product |
| `detect` | Domain-wide runtime-health investigation and triaged findings |

They are siblings. `build` does not dispatch `fix` or `detect` as subagents when the request belongs to one of them; it tells you to switch to the right identity.

## The first decision is size

`build` classifies the request by the finished outcome.

### Question

If nothing changes, it answers the question using the relevant skill or tool. No product-change workflow is created just because the topic is technical.

### Bounded operation

If the request changes something inside an already-decided shape, the owning skill runs directly.

Examples:

- add or update a source connection;
- test a connection;
- make one bounded model/configuration change.

A bounded operation does not enter the full intent/design/plan loop.

### Product change

If the request changes what a data product commits to deliver, the staged workflow begins.

Current product kinds are:

- ingestion;
- transformation;
- orchestration;
- semantic-model.

A compound request can contain more than one kind in one Intent.

## Current product-change chain

The current plugin no longer uses the older simplified five-label description from this onboarding set. Its durable chain is built from explicit skills:

1. **capturing-intent** — records the Requirement in `intent.md` and resolves the ordered `kinds:` list;
2. **designing** — creates the design records for the approved requirement;
3. **planning** — creates `plan.md`;
4. **executing-the-plan** — carries out the approved plan;
5. **verifying** — records evidence and certification in `verify.md`;
6. **shipping** — enforces ship gates, makes the branch PR-ready, asks for the final ship approval, and produces the registered ship product.

The plugin uses proposal chaining between stages. A later stage does not silently begin merely because an earlier one finished.

## Durable artifacts

For product work, expect the working branch to contain durable records such as:

- `intent.md` — requirement, kinds, scope, success criteria, approvals;
- design records — architecture and product-specific decisions;
- `plan.md` — implementation plan;
- `verify.md` — verification evidence, gate results, certification, and ship approvals.

Transformation work can also create a data-slice artifact during intent capture.

The repository and these files are the durable record. The agent is expected to re-read disk when resuming rather than trusting conversational memory.

## Shipping now includes the pull request

For the four `build` product kinds, the current registry declares the ship product as **an intent PR**. For `fix`, it is an intent PR on a case branch. `detect` is read-only and ships raised triaged issues instead.

This reverses an old onboarding statement that the agent deliberately stopped before opening a pull request.

Shipping has hard gates:

- verification must be certified first;
- the branch must pass the clean-diff gate;
- generated/runtime artifacts and secrets must not enter the PR;
- breaking schema changes require explicit approval;
- the final ship action requires explicit user approval.

The clean-diff protection also runs outside the conversational workflow on `git push` and PR creation, so the agent cannot simply claim the branch is clean.

## Source connections are a bounded operation

Adding or updating a source does not require the whole product-change chain by itself.

You ask the agent in conversation. The source flow then:

1. checks the Domain platform and available connector catalogue;
2. selects and prepares the connector;
3. introspects the connector for supported authentication methods and required fields;
4. asks for non-secret configuration only;
5. tells you the exact secret key names to create out of band;
6. verifies the connection through the real runtime path;
7. persists the source configuration only after verification is green.

The agent never needs the secret value.

For the current Domain-create path in this onboarding snapshot, those secret values go in the Domain's local secrets file under Studio's data directory.

## Git and working branches

Work happens on an Intent branch. Shipping pushes the branch and, for `build`/`fix`, opens the registered Intent PR after the required stop is approved.

Do not manually commit runtime outputs such as dbt `target/`, package directories, logs, `.env`, or secret TOML files. The shipping clean-diff gate blocks these classes of files.

## Platform guardrails

The current `build` agent reads the Domain's declared platform before choosing platform-specific tools or dialects.

It must not:

- substitute one data platform for another;
- write to the persistent production Domain while doing development work;
- dump environment variables;
- read `.env` or credential files;
- create or repair its own virtual environment as a workaround.

Development writes go to the runtime-declared ephemeral destination.

## Domain knowledge

The current plugin reads `CONTEXT.md` and `docs/adr/` as durable Domain knowledge and expects lasting language or architectural decisions to be recorded there when relevant.

## Next step

[[Worked Example Salesforce]] applies this model to one source-connection example. Treat the connector's own introspection result as authoritative if it differs from a static example.

---

_Applies to: studio/main (unreleased snapshot). Verified against `studio@5c9d2bbf339a` on 2026-08-22._
