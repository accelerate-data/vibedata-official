# Create your first Domain

A Domain connects a GitHub repository to one Data Platform Type and one exact persistent resource. It also defines the authentication policy inherited by Intents.

## Before you start

Confirm:

- Studio is running;
- GitHub access works;
- at least one LLM Profile exists;
- delegated users are signed in through SSO;
- Fabric has an active downstream Identity Provider on delegated deployments;
- the intended persistent data-platform resources already exist, except schemas or local DuckDB files that Studio can create from the form.

## 1. Open the Domain form

Open **Settings → Domains → Add Data Domain**.

Fill in:

- **Name**;
- **Icon**;
- optional **Description**;
- optional **Domain Instructions**.

Domain Instructions are injected into the agent context for Intents in this Domain. Put stable business and engineering guidance there, not credentials.

## 2. Select the Git repository

Choose:

- **Organization**;
- **Repository**.

On Kubernetes, organisations come from GitHub App installations and the user's authorized GitHub view. On Local Docker, Studio uses the imported `gh` session.

The repository binding and recorded default branch become read-only after Domain creation. To move a Domain to another repository, create a new Domain.

Make sure the creating identity can access the repository and, where Studio must seed or update repository content, has the required write authority.

## 3. Choose the Data Platform Type

Choose one:

- Microsoft Fabric;
- MotherDuck;
- DuckDB-local.

There is no instance-level Data Platform entry to select. The form builds a typed Domain candidate directly.

## 4. Choose user authentication

The available options come from the selected Data Platform descriptor.

### Microsoft Fabric

> **Applies to: Microsoft Fabric.**

- On Kubernetes, select OAuth/OIDC and the Entra **Identity Provider** registered in Org Settings.
- On Local Docker, Studio uses the ambient Azure CLI identity in the API container.

If the delegated Identity Provider is not connected for your user, use the connection action and complete the OAuth flow before relying on automatic resource discovery.

### MotherDuck

> **Applies to: MotherDuck.**

- On Kubernetes, each user connects their own PAT.
- On Local Docker, the shared Domain PAT is the ambient operating credential.

### DuckDB-local

> **Applies to: DuckDB.**

No external user credential is required.

## 5. Configure service authentication

Current Domain auth UI supports a separate service lane.

Where the provider allows it, **Defer service identity** is the default. That lets the Domain record be created, but Studio warns that Intents cannot activate until the required service identity is configured.

For a first usable Domain, configure the service identity now when possible.

### Fabric service identity

Enter the Domain service-principal credential supplied by the Entra administrator. This is independent of the user's OAuth Identity Provider unless the current UI explicitly offers an eligible application-reuse option.

### MotherDuck service identity

On a delegated deployment, enter the Domain service PAT for unattended work. On Local Docker, the ambient/shared PAT is required rather than deferred.

### DuckDB

No service identity is required.

The form can offer **Test service authentication**. This is diagnostic. Current create semantics validate the complete candidate at the persistence boundary, but the UI does not require every optional test action to have been run manually before Create.

## 6. Select the persistent data resources

Where a platform supports both, **Auto** discovery is the default and **Manual** is available as a fallback.

### Microsoft Fabric

Select or enter:

- Workspace;
- Lakehouse;
- Schema;
- optional Ephemeral Workspace Capacity.

Auto mode discovers workspaces and Lakehouses visible to your user. Studio resolves the SQL endpoint. The persistent Workspace and Lakehouse must already exist; Studio does not create them from this form.

Studio can create a schema from the form. A schema created before the Domain is finally saved remains on Fabric even if you cancel the Domain.

### MotherDuck

Select or enter:

- Database;
- Schema;
- optional Share where the current editor exposes it.

Studio can discover databases and schemas visible to the acting PAT and can create a schema.

The backend supports an optional MotherDuck Share for cross-identity access. The database is the binding identity; a Share is access configuration, not a replacement database.

### DuckDB-local

Pick an existing Studio-managed `.duckdb` file or create a new database through the form, then select or create the schema.

You do not enter an arbitrary host filesystem path. Studio owns the DuckDB directory under its data area.

## 7. Secret Store behavior

There is **no Domain Secret Store picker** in the current create UI.

When the Domain is persisted, Studio initializes a local secrets file for it under the Studio data directory. This file is outside the Git repository.

Source connection setup later tells you the exact keys to place there. Never put those values into Domain Instructions or Git.

## 8. Create the Domain

Select **Create Domain**.

Studio persists the Domain and starts provisioning/reconciliation. Service-lane readiness depends on the authentication you selected:

- a complete service credential can reconcile immediately;
- a deferred required service credential remains not configured and prevents Intent activation until repaired;
- external permission or resource failures move the relevant readiness lane into failure and surface a safe diagnostic.

## 9. What is immutable

Treat these as fixed after creation:

- Git repository binding;
- Data Platform Type;
- persistent Fabric workspace/Lakehouse/schema;
- MotherDuck database/schema;
- DuckDB database/schema resource identity.

Operational settings such as a Fabric ephemeral capacity and replaceable service credentials have separate update paths. MotherDuck Share configuration is not the database identity and can be changed by the supported Domain update path.

## 10. GitHub Actions setup

GitHub Actions setup is separate from basic Domain persistence/readiness. Fabric and MotherDuck CI/CD may require repository variables/secrets and, for Fabric, a correctly configured federated credential.

Do not infer that an `Active` badge proves every CI/CD prerequisite. [[Verify the First Domain]] covers the post-create checks.

Continue to [[Verify the First Domain]].

---

_Applies to: studio/main (unreleased snapshot). Verified against `studio@5c9d2bbf339a` on 2026-08-22._
