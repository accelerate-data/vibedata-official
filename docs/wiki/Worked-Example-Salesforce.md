# Worked example: add Salesforce as a source

This example demonstrates the current **bounded source-connection operation**. It deliberately does not depend on the old public Salesforce twin used by earlier versions of this draft. That fixture is not referenced by current Studio or the pinned data-engineering plugin, so this refresh does not claim it is still available.

Use a Salesforce environment you are authorized to read.

## What this example proves

By the end, you will have:

- asked `build` to add a Salesforce source;
- selected an authentication method returned by the connector's current introspection;
- created the required secret values outside the agent;
- let the agent verify the connection;
- persisted only the non-secret connection configuration after the verification is green.

Adding the source itself is a bounded operation. It does not require the full intent/design/plan/verify/ship chain.

## 1. Start in an active Domain

The Domain must already be usable, with:

- a declared Data Platform Type;
- a working Intent runtime;
- the automatically initialized local Domain secrets file from current Domain creation;
- Git access for the working branch.

Open a `build` Intent.

## 2. Ask naturally

For example:

> Add a Salesforce source called `sf_prod`.

There is no `/add-source` command to memorize and no Add Source form in Settings.

The agent uses the source-connection skill because the request is a bounded source operation.

## 3. Let the connector define its authentication fields

The agent prepares and introspects the current Salesforce connector. Do not copy a fixed field list from this guide and force it onto the run.

The upstream `dlt-hub/verified-sources` Salesforce source currently documents several supported Simple Salesforce credential shapes, including:

- username/password/security token;
- username/password/organization ID;
- session ID plus instance or instance URL;
- JWT/connected-app credentials;
- client credentials.

The agent's introspection result is authoritative for the connector version it actually loaded.

## 4. Choose an authentication method

Pick the method that matches your Salesforce setup.

For example, if you already have a valid Salesforce session, choose the session-based method when the agent offers it. The current upstream connector documents this shape:

```toml
[sources.salesforce.credentials]
session_id = "..."
instance_url = "..."
```

Your connection is named `sf_prod`, so the exact path the plugin returns is connection-scoped rather than copied literally from the upstream example.

## 5. Do not give secret values to the agent

For each credential field, the agent returns the exact dlt-native TOML key path.

With the current Local TOML skill, a credential under a named connection is expressed in this form:

```toml
[sources.sf_prod.credentials]
<field> = "..."
```

The actual fields come from connector introspection. The skill must not invent them.

The Domain's secrets file lives outside the Git repository under Studio's data directory. On the current Domain-create path it is the local secrets file created for the Domain.

The operator, or another person with access to that file, enters the values. The agent only sees the key names.

## 6. Keep non-secret configuration separate

If the connector exposes non-secret configuration such as API version, domain, proxy, or another option, answer the agent's questions for those values.

Non-secret connection configuration can be written to the working branch. Credential values cannot.

## 7. Expect the first verify attempt to find missing secrets

The source flow verifies the connection through the runtime path that the eventual pipeline will use.

Because the agent cannot create the secret values itself, a normal sequence is:

1. agent tells you the required key names;
2. verification reports the keys are missing;
3. you add the values out of band;
4. you tell the agent to continue;
5. the agent verifies again.

This retry loop is intentional.

## 8. Persistence happens only after green verification

Current source-connection contract requires the agent to persist the connection only after verification succeeds.

If you abandon the attempt while verification is failing, the pending configuration change should not be left as a recorded working connection.

## 9. Ask for a real data task after the source is connected

Once Salesforce is verified, ask for the actual data outcome you need.

Examples:

- ingest a selected set of Salesforce objects;
- build a transformation on landed Salesforce data;
- add an orchestration schedule;
- add a semantic-model definition.

Those requests can become product changes. `build` then classifies their `kinds:` and enters the current capture → design → plan → execute → verify → ship chain described in [[Getting Started as a Contributor]].

## 10. Do not assume the source schema

The current verified Salesforce source documents standard resources such as Opportunity, OpportunityLineItem, Product2, Account, Contact, Lead, and others. Your Salesforce org, permissions, custom objects, and connector version can expose a different effective schema.

Use the agent's source-schema discovery against your actual connection before defining the final product contract.

## Success criteria

This example is complete when:

- the Salesforce connection verifies green;
- no secret value is present in Git or chat;
- the source connection is recorded on the Intent working branch;
- the agent can discover or read the Salesforce objects required by the next task.

Do not use the synthetic row counts, token, or endpoint from the August 13 version of this guide as validation data. They were fixture-specific and are not part of the current Studio contract.

---

_Applies to: studio/main (unreleased snapshot). Verified against `studio@5c9d2bbf339a` on 2026-08-22._
