# Create your first Domain

A Domain binds a GitHub repository to a data platform and persistent resource. It also defines user authentication, service authentication, and a secret store for work in that Domain.

## Before you start

Complete [[Configure the Studio Instance]]. Confirm that you can access the repository, that your downstream user connection is healthy, and that the intended persistent data resources exist. Studio can create supported schemas and managed DuckDB files from the form.

## Open Create domain

1. Open **Domains** from the application rail.
2. Select **Add domain**.

The **Create domain** page has **Basics**, **Data platform**, and **Secret store** steps. Switching steps preserves the draft. Leaving with changes requires confirmation to discard them.

## Complete Basics

1. Enter **Name**.
2. Review the derived **Slug**, which cannot change after creation.
3. Choose an **Icon** if required.
4. Add an optional **Description**.
5. Select **Account / organization**.
6. Select **Repository**.
7. Select **Continue to data platform** while the draft is incomplete.

Repositories come from the GitHub App installations and your authorised GitHub view. The creating identity must have the required access, including write permission where Studio must seed or update repository content.

The repository binding and recorded default branch become read-only after creation. Domain instructions are edited later under **General**; keep credentials out of them.

## Configure Data platform

1. Select **Data platform type**.
2. Complete the displayed user-authentication fields.
3. Complete **Service authentication** where required.
4. Continue to the resource configuration with **Continue to workspace**.
5. Select the persistent resources for the chosen platform.
6. Select **Continue to secret store** while the draft is incomplete.

The fields depend on the selected platform. There is no instance-level data-platform registration step. Search resource lists using part of the visible name. Where a selector supports an exact identifier, select its explicit option to commit it; typing alone does not select a resource.

### Microsoft Fabric

Select the connected Entra **Identity provider** for user access. If no eligible connection is available, complete **User Settings → Connections**, or ask an owner to repair the provider when the message requires one. Return to Domain creation after the connection is healthy.

For **Service authentication**, select **Reuse user identity provider** when eligible, or **Dedicated identity**. Dedicated identity requires a separate client ID and client secret in the selected provider's tenant. Reuse follows the provider's active credentials and their rotation; it does not copy a secret into an independent Domain credential.

Select the persistent workspace, Lakehouse, and schema, and the capacity for ephemeral workspaces. The persistent workspace and Lakehouse must already exist. Studio can create a schema; that external schema remains if you later cancel Domain creation.

### MotherDuck

Use your own connected PAT for interactive work and configure the Domain service PAT for unattended work. Select the database and schema. Studio can discover accessible resources and create a schema.

The acting identity must own the bound database to activate an Intent. Access through a shared database does not satisfy that requirement. See [[Prerequisites MotherDuck Administrator]].

### DuckDB

Select an existing Studio-managed database file or create one through the form, then select or create the schema. You cannot supply an arbitrary host filesystem path. No external user or service identity is required.

## Configure Secret store

1. Open **Secret store**.
2. Select **Secret store type** from the available options.
3. Complete the selected store's displayed authentication and resource fields.

The registered types include **Internal**, **Local File**, **Azure Key Vault**, and **GCP Secret Manager**. Use only the types available in your deployment.

| Store | Setup and later secret entry |
| --- | --- |
| Internal | No external connection or resource fields. After saving, open the Domain's **Secrets** tab to add secrets. |
| Local File | No connection fields in the form. The operator supplies the Domain's secrets file outside Studio and outside Git. Selecting this store does not make every other store file-based. |
| Azure Key Vault | Configure its connection and vault. Use **Reuse data platform connection** where eligible, or **Separate connection**; configure service authentication as shown. Add values through the vault's secret-management surface. |
| GCP Secret Manager | Complete the displayed connection and resource fields if the type is available. Add values through the external store's secret-management surface. |

The source-connection agent later supplies the exact secret names for a store supported by the deployed source workflow. Store availability in Domain creation alone does not prove connector delivery. Never put values in agent chat, Domain instructions, or Git. Changing stores does not copy secret values between them.

## Create and check the result

1. Review the Domain summary and all three steps.
2. Select **Create** when the complete draft enables it.
3. Open the saved Domain's **Resources** tab.
4. Read the checks for repository, data platform, and secret store.
5. Repair any missing access or configuration reported by those checks.
6. Select **Reconcile** to run the applicable readiness checks again.

**Create** can appear on an earlier step when the whole draft is complete. Step completion checks required form values; it does not prove that external credentials and resources work. Saving starts the applicable readiness checks. A saved Domain can still need repair before an Intent can activate.

Treat the repository, data-platform type, and bound database/workspace/Lakehouse/schema identity as fixed after creation. Supported credential rotation, ephemeral capacity, and secret-store changes use their own update controls.

GitHub Actions setup is separate from basic Domain readiness. Continue to [[Verify the First Domain]] for an Intent run, LLM turn, and any CI checks you need.

---

_Release scope and source-review limits: [Home](README.md#release-and-verification-scope)._
