---
applies-to: vibedata v0.1.26
verified-against: studio@653beeced
verified-on: 2026-08-05
sources:
  - docs/functional/data-platform/fabric-backend.md
  - docs/functional/data-platform/README.md
  - docs/functional/gha-data-platform-oidc-flow/README.md
  - src/server/modules/data-platforms/providers/fabric.provider.ts
  - src/server/modules/data-platforms/data-platforms.schemas.ts
  - src/server/modules/data-platforms/providers/fabric.descriptor.ts
  - src/server/modules/data-platforms/providers/fabric/helpers/fabric-catalog-client.ts
  - src/server/modules/data-platforms/providers/fabric/helpers/fabric-route-access.ts
  - src/server/modules/domains/services/domain-provisioning-diagnostic.ts
  - src/server/modules/intents/services/ephemeral-access-grant.service.ts
  - src/server/lib/graph/federated-credential-client.ts
  - src/server/modules/domains/services/domain-verification-plan.ts
  - src/server/modules/domains/services/domain-verification.service.ts
  - src/server/modules/data-platforms/providers/fabric-ephemeral-client.ts
  - src/server/modules/domains/routers/domains-crud.router.ts
---

# Request for your Microsoft Fabric administrators: capacity, workspace, and service principal access

This page asks for three kinds of rights in your organisation's Microsoft Fabric tenant: tenant administration, capacity administration, and workspace administration. Each of these may be the same person or different people — every ask below carries a **Who:** tag naming which right it needs, so forward each ask to whoever holds the tag it names. Nothing here requires access to Studio or to any Accelerate Data system, only to your organisation's Microsoft Fabric tenant.

This whole page applies only if your data platform is **Microsoft Fabric**. Skip it entirely if you chose **DuckDB** or **MotherDuck**. Everything on this page applies whether your deployment style is **Local Docker** or **Kubernetes on Azure** — none of it is specific to one deployment style, except where a section says otherwise.

## What this page consumes

This page needs the M2M service principal's client ID, `M2M_CLIENT_ID`, which is created by your organisation's Entra administrator — see [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md). That service principal must already exist in Entra before any task below can proceed: you cannot add a service principal to a security group, or grant it a workspace role, before it has been created.

## The six things this page asks for

The one hard dependency: step 1 must happen before steps 5 and 6, since a role cannot usefully be granted to a service principal your tenant does not yet permit to call Fabric APIs. Otherwise, do these roughly in the order below because later steps need the workspace from step 3 to exist — not because every step strictly requires the one before it.

### 1. Enable service principals to call Fabric APIs

**Who:** Fabric tenant administrator.

A Fabric service principal cannot call any Fabric API until your tenant allows it. In your Fabric tenant's admin settings, enable the setting that allows service principals to use Fabric APIs, and scope it to a security group that contains the M2M service principal (`M2M_CLIENT_ID`) — not your entire organisation, unless your organisation already scopes this setting that broadly for other reasons.

Enabling this tenant setting requires the **Fabric Administrator** role. This is a different right from the **Application Administrator** or **Cloud Application Administrator** role used in [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md) to create the service principal itself — holding one does not imply holding the other. If the person who created the M2M service principal does not also hold Fabric Administrator, route this step to whoever does.

Studio never sets this tenant setting. It is entirely your organisation's action, done once per tenant.

### 2. Provision Fabric capacity

**Who:** Fabric capacity administrator (often the same person as the tenant administrator).

Provision a Fabric capacity for this domain, or nominate an existing one. Return its capacity ID.

**Set the capacity ID now — do not leave it for later.** When your operator registers this Fabric connection in Studio, the capacity ID field is optional and free-text. Studio accepts an empty value with no warning at that point. But when your operator later creates a domain and binds a workspace that has no capacity of its own — most commonly because it was created fresh rather than picked from an existing one — Studio falls back to this connection's capacity ID. If neither is set, creating that domain's Lakehouse fails immediately, as part of domain creation itself — not at registration, and not as some separate, later step. Provide the capacity ID at registration to avoid hitting this failure.

Unlike the workspace, Lakehouse, and schema in step 3, the capacity ID is not permanent: if you provide the wrong one, your operator can correct it later, in the domain's own settings. That correction path exists for fixing a mistake — it is not a reason to leave the value empty now, which is the failure this step exists to prevent.

### 3. Create or nominate the domain's workspace, lakehouse, and schema

**Who:** Fabric workspace administrator (Admin or Member on the workspace).

Create a new Fabric workspace for this domain, or nominate an existing one. Inside it, create or nominate a Lakehouse, and inside the Lakehouse, create or nominate a schema. Return all three identifiers: the workspace ID, the Lakehouse, and the schema. Your operator enters these when the domain is created in Studio and cannot change them afterward — the binding is permanent for that domain.

### 4. Confirm the operating identity's own read access to the workspace

**Who:** Fabric workspace administrator (Admin or Member on the workspace).

Before Studio ever checks the M2M service principal (steps 5 and 6 below), it checks a different identity first: the one actually operating the domain, not the service principal. Grant that identity at least **Viewer** access to the workspace from step 3.

- Under **Kubernetes on Azure**, this is the account of whoever is signed in to Studio and driving work in this domain — their own account, not the service principal.
- Under **Local Docker**, this is the host Azure identity Studio itself runs as. You cannot look this identity up yourself — ask your Studio operator which Azure identity that is (it comes from an `az login` session on the machine running Studio), then grant that identity Viewer access.

These are two distinct identities, not the same requirement worded twice for two deployment styles: grant read access to whichever one applies to your deployment style.

This check runs first, before either service-principal check below, on **both** deployment styles. An admin who completes steps 1, 2, 3, 5, and 6 perfectly can still watch domain activation fail here, on an identity this page would otherwise never have named.

### 5. Grant the service principal a deploy-capable workspace role

**Who:** Fabric workspace administrator (Admin or Member on the workspace).

On the workspace from step 3, grant the M2M service principal (`M2M_CLIENT_ID`) a role that can deploy: **Contributor** or **Member**. In the Fabric workspace, use **Manage access** to add the service principal by its app name and assign the role.

This role is needed regardless of deployment style: it is what lets the service principal push changes to the workspace when your team's domain repository deploys through its GitHub Actions workflow.

**Studio never grants this role, and never checks whether it is present.** A missing or insufficient deploy role does not show up as a Studio error at any point — not at registration, not at domain activation. It only surfaces the first time a deploy runs, as a failure from Fabric itself.

### 6. Confirm the service principal's read access to the domain workspace

**Who:** Fabric workspace administrator (Admin or Member on the workspace).

On the same workspace, make sure the M2M service principal holds at least **Viewer** access — Viewer, Contributor, Member, or Admin all satisfy this. If you already completed step 5, this is already satisfied, since Contributor and Member both include read access.

**Studio does check this one — but only if your deployment style is Kubernetes on Azure.** When a domain using this workspace activates under Kubernetes on Azure, Studio reads the workspace under the service principal's own credentials to confirm it can see it. If that read fails, the domain is left in a `PENDING` state — retryable once you grant the access, not a hard failure. Studio never grants this access itself; it only checks for it and reports which service principal and workspace are missing it.

Under **Local Docker**, Studio skips this specific check: it records this step as succeeded without reading the workspace under the service principal, regardless of whether the service principal has any access at all. **This does not mean no workspace read is checked under Local Docker** — step 4 above (the operating identity's own read access, checked against the host Azure identity) still runs unconditionally on this deployment style. Only the service-principal-specific check in this step is skipped. This does not remove the need for the service principal's own access either — the GitHub Actions deploy in step 5 still needs at least the same read access to run — it only means Studio itself will not catch a missing grant for you on this deployment style.

**Steps 5 and 6 are not the same grant, and Studio treats them very differently.** Studio verifies step 6's read baseline (on Kubernetes on Azure) but never verifies step 5's deploy role, on either deployment style. Granting only Viewer access satisfies Studio's own check and still leaves the deploy workflow unable to push changes — grant both roles, not just one.

**"Studio never grants a role" above means on this workspace specifically — the one you nominate in step 3, the domain's permanent workspace.** Studio does grant roles elsewhere in Fabric, on workspaces it creates and deletes itself for its own short-lived, per-intent work, on the capacity from step 2: it grants the M2M service principal Admin on those workspaces, and it grants individual collaborators Contributor there when they are added to an intent. Those are not the workspace you nominate, and nothing the admin does on this page changes because of them — you configure and act on nothing to make them happen.

## Network access

Allow outbound access (443/tcp) from wherever Studio and its deploy workflows run to:

| Host | Purpose |
| --- | --- |
| `login.microsoftonline.com` | The Entra token endpoint. Studio's service principal exchanges its client ID and secret here for an access token, using the OAuth client-credentials flow. |
| `api.fabric.microsoft.com` | The Fabric REST API. Studio calls this to read and write workspaces, Lakehouses, and schemas under the service principal's token. |
| `graph.microsoft.com` | Microsoft Graph. Studio calls this to check whether the per-repository federated credential already exists on the service principal's app registration — see the recurring task in [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md). |

`login.microsoftonline.com` is shared with the Entra-side requests in [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md); the other two are specific to Fabric.

## Values to send back

| Token | Comes from |
| --- | --- |
| `FABRIC_CAPACITY_ID` | The capacity ID from step 2. |
| `FABRIC_WORKSPACE_ID` | The workspace ID from step 3. |
| `FABRIC_LAKEHOUSE` | The Lakehouse name or ID from step 3. |
| `FABRIC_SCHEMA` | The schema name from step 3. |

## Where this goes

`FABRIC_CAPACITY_ID` is entered by the operator during organisation setup — see [05-configure-org](05-configure-org.md) — and used again in [06-first-domain](06-first-domain.md). `FABRIC_WORKSPACE_ID`, `FABRIC_LAKEHOUSE`, and `FABRIC_SCHEMA` are entered only in [06-first-domain](06-first-domain.md), when the domain is created and bound to this workspace.
