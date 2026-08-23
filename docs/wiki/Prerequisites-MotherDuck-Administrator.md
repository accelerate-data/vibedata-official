# Request for your MotherDuck administrator

> **Applies to: MotherDuck.** Skip for DuckDB and Microsoft Fabric.

Current Studio configures MotherDuck directly on each Domain. There is no instance-level MotherDuck registration step.

## Identity model

MotherDuck uses PAT authentication in current Studio.

### Local Docker

Local Docker uses ambient authentication. One shared Domain PAT serves the operating identity. The Domain cannot defer that service credential in ambient mode.

### Kubernetes on Azure

Delegated deployments use two credential lanes:

- each contributor connects their own MotherDuck PAT for interactive work;
- the Domain stores a service PAT for unattended work.

The Domain can initially defer its service identity, but Intents cannot activate while a required service credential remains unconfigured.

## 1. Provide a Domain service PAT

Create or select a MotherDuck identity for unattended Domain work and issue a PAT with the access Studio needs to validate the bound database and perform the Domain's runtime operations.

Return the PAT through a secure credential channel.

Do not provide a read-only token when the Domain's intended work requires writes. Studio uses one PAT credential type for this service lane and does not automatically upgrade a read-only token.

## 2. Prepare the database

Create or nominate the database the Domain will bind to.

The database is part of the Domain's immutable resource identity. Choose it before Domain creation. Current Studio can discover databases visible to the connected user and can select the database in the Domain form.

Return the database name.

## 3. Prepare the primary schema

The Domain also binds to one schema. Current Studio can list existing schemas and create a schema from the Domain form.

Return the intended schema name, or let the operator create it while creating the Domain.

The database and schema form the persistent Domain resource and should be treated as immutable after creation.

## 4. Decide whether the Domain needs a Share

Current Studio's MotherDuck backend supports an optional `shareName` on the Domain.

A Share is how an identity that does not own the bound database can gain read access to it. Studio does not create the Share or issue the MotherDuck grant; the customer establishes it out of band.

Important current behavior:

- without a Share, only an identity that can directly resolve the database can activate against it;
- with a configured Share, a non-owner can use the granted Share as the source for its isolated Intent database;
- the database identity stays fixed, but the Share association is not part of database uniqueness and current backend behavior supports changing or clearing it later.

If several people will contribute to one MotherDuck Domain, plan the MotherDuck sharing model before onboarding them. Do not use the old assumption that every MotherDuck Domain is permanently single-contributor.

## 5. User PATs on delegated deployments

> **Applies to: Kubernetes on Azure.**

Each human who will drive MotherDuck work needs a compatible MotherDuck user credential in Studio. They connect it from **User Settings → Connections** when the Domain requires it.

Studio does not fall back to another person's PAT. User credentials are isolated per Studio user.

The customer's MotherDuck organisation and commercial plan must allow the intended users and service identities. Do not rely on the seat counts or plan prices from an older copy of this onboarding guide; those are vendor terms and can change without a Studio release.

## 6. Intent isolation and plan-dependent behavior

Studio creates an isolated MotherDuck database for an Intent by cloning from the Domain's source database or an accessible Share.

MotherDuck snapshot-retention entitlements can affect whether that clone succeeds. If a database carries retention settings outside the acting identity's current plan limits, activation can fail even though the PAT itself is valid.

If this happens, verify the source database's retention and the acting MotherDuck account's current entitlement with MotherDuck. Do not treat it as a Studio authentication failure first.

## Network access

Allow Studio and its agent runtime to reach MotherDuck over HTTPS. The runtime may also need to load the MotherDuck DuckDB extension when it is not already available locally.

In restricted egress environments, validate this path before the first Domain is created. Do not rely on a static wildcard hostname list as a permanent vendor contract.

## Values to return

Give the Studio operator:

| Value | Used for |
| --- | --- |
| Domain service PAT | Domain service authentication |
| Database name | Domain resource binding |
| Schema name | Domain resource binding |
| Share name, when used | Cross-identity database access |

Each delegated contributor supplies their own user PAT directly through Studio rather than sending it to the Domain operator.

---

_Applies to: studio/main (unreleased snapshot). Verified against `studio@5c9d2bbf339a` on 2026-08-22._
