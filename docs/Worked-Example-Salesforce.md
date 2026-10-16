# Worked example: add Salesforce as a source

Use a Salesforce environment you are authorised to read. This example adds and verifies a connection; a later ingestion or transformation request is a separate data task.

## Prepare the Domain

Confirm that the Domain has a declared data platform, a working Intent runtime, Git access, and a saved secret store supported by the source workflow. Complete [[Verify the First Domain]] first.

Open an Intent with `build` selected.

## Ask for the source

For example:

> Add a Salesforce source called `sf_prod`.

The agent discovers and introspects the connector available in your deployment. It uses the bounded source-connection flow described in [[Getting Started as a Contributor]].

## Select an authentication method

Choose from the methods the connector reports. The connector version and your Salesforce configuration determine the usable fields. Use the current introspection result instead of a fixed credential list from a static example.

Answer only questions about non-secret configuration. If the method needs a token, password, client secret, or other credential value, the agent must name the secret for you to enter outside chat.

## Enter secrets in the saved Domain store

1. Read the exact names returned by the agent for `sf_prod`.
2. Open the saved Domain's **Resources** tab to confirm its secret-store type.
3. Add the values through that store's entry method.
4. Tell the agent to continue.

| Saved store | Where to enter the values |
| --- | --- |
| Internal | The Domain's **Secrets** tab |
| Azure Key Vault | The bound vault's secret-management surface |
| Local File | The Domain's secrets file, updated by an operator outside Studio and Git |

Secret names depend on the store. A dotted key path for Local File is not the vault secret name. Use the names returned for the current Domain rather than converting or guessing them yourself.

The agent never needs to see a credential value. Do not put it in the Intent, Domain instructions, or Git.

## Verify the connection

The agent verifies through the runtime path used by the eventual pipeline. If verification reports missing secrets, enter the missing values in the bound store and ask it to retry.

The flow records the connection configuration only after verification succeeds. If you abandon a failing attempt, it must not remain recorded as a working connection.

## Ask for the data outcome

After the connection verifies, ask the agent to discover the source schema against your actual Salesforce connection. Available objects depend on the org, permissions, and connector version.

Then request the outcome, such as ingesting selected objects, transforming landed data, or adding a schedule. A product change starts at **capturing-requirements**, followed by design, plan, execute, verify, and approved shipping.

## Check the result

The example is complete when the connection verifies, its non-secret configuration is recorded on the Intent branch, and the agent can discover or read the objects needed for the next task. No secret value may be present in Git or chat.

This guide supplies no Salesforce credentials, test endpoint, or expected row count. Use evidence from your authorised environment.

---

_Release scope and source-review limits: [Home](README.md#release-and-verification-scope)._
