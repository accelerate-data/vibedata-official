# Request for your MotherDuck administrator

> **Applies to: MotherDuck.** Skip for DuckDB and Microsoft Fabric.

Configure MotherDuck on each Domain. Prepare a user PAT for each contributor's interactive work and a Domain service PAT for unattended work. These are separate credential lanes; Studio does not fall back to another person's PAT.

## Prepare the database and schema

1. Select the persistent database the Domain will bind to.
2. Confirm that the intended acting identity owns that database.
3. Select the primary schema, or let the operator create it from the Domain form.

The database and schema form the Domain's immutable resource identity. Studio can discover visible databases and schemas, but visibility alone does not prove that an Intent can activate.

Intent activation requires ownership of the bound database by the acting MotherDuck identity. A MotherDuck Share does not provide a fallback for a non-owner. New Domains have no Share field; legacy Share state does not make non-owner activation valid.

Check this ownership restriction before onboarding contributors to a shared Domain. Do not promise multi-user activation based only on a sharing grant.

## Provide the service PAT

Issue a PAT for the identity that will perform unattended Domain work. It must have the access required for validation and runtime operations; a read-only token is insufficient for work that writes.

Return the service PAT to the operator through an approved secret-management channel. Configure it on the Domain before expecting unattended work to succeed.

## Connect each user's PAT

Each contributor supplies their own PAT directly through **User Settings → Connections**. They do not send it to the Domain operator or the agent.

Confirm that the customer's MotherDuck organisation and plan permit the intended identities and operations. Seat counts, prices, and entitlements are vendor terms and can change independently of Studio.

## Verify Intent isolation

Studio uses an isolated clone of the Domain's source database for an Intent. The ownership requirement applies before clone activation.

Snapshot-retention entitlements can also affect cloning. If activation fails after an account or plan change, check the source database's retention settings against the acting identity's current entitlement.

Allow Studio and its agent runtime to reach MotherDuck over HTTPS and load the MotherDuck extension when required. Use the customer's current egress policy rather than a fixed hostname list copied from an old guide.

## Handoff

| Value | Used for |
| --- | --- |
| Domain service PAT | Unattended Domain operations |
| Database name and ownership confirmation | Persistent binding and Intent activation |
| Schema name | Persistent Domain schema |

Each contributor must still connect and verify their own user credential. Continue to [[Create Your First Domain]].

---

_Release scope and source-review limits: [Home](README.md#release-and-verification-scope)._
