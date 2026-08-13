---
applies-to: vibedata v0.1.33
verified-against: studio@a121fc466
verified-on: 2026-08-13
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
  - src/server/config/auth-enabled.ts
  - src/server/modules/data-platforms/providers/fabric/helpers/fabric-api-config.ts
---

# Request for your Microsoft Fabric administrators: capacity, workspace, and service principal access

This page asks for three kinds of rights in your organisation's Microsoft Fabric tenant — tenant administration, capacity administration, and workspace administration — plus one outbound network change. Each of these may be the same person or different people; every ask below carries a **Who:** tag naming which right it needs, so forward each ask to whoever holds the tag it names. Nothing here requires access to Studio or to any Accelerate Data system, only to your organisation's Microsoft Fabric tenant.

This whole page applies only if your data platform is **Microsoft Fabric**. Skip it entirely if you chose **DuckDB** or **MotherDuck**. Everything on this page applies whether your deployment style is **Local Docker** or **Kubernetes on Azure** — none of it is specific to one deployment style, except where a section says otherwise.

## What this page consumes

This page needs two values for the same M2M service principal, both from your organisation's Entra administrator — see [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md):

| Value | Used for |
| --- | --- |
| `M2M_CLIENT_ID` — the application (client) ID | Adding the service principal to a security group (step 1) and to workspace roles (steps 4 and 5) |
| The **service principal object ID** — a different GUID, on the enterprise application | Adding the service principal as a capacity administrator (step 2). The client ID is rejected there. |

That service principal must already exist in Entra before steps 1, 2, 4 and 5 can proceed: you cannot add a service principal to a security group, or grant it a workspace role, before it has been created. Step 3 depends on step 2, not on the service principal. **Step 6 needs nothing from `01a`** — it is a firewall change, and whoever controls outbound network policy can make it on day one, before the service principal exists.

## The six things this page asks for

Two hard dependencies, both of which the real builds hit:

- **Step 1 must happen before steps 4 and 5.** A role cannot usefully be granted to a service principal your tenant does not yet permit to call Fabric APIs.
- **The M2M service principal must be a capacity administrator (step 2) before the workspace in step 3 can be created under that capacity.** In many tenants the service principal has to create the workspace itself — see step 2.

Otherwise, do these roughly in the order below because later steps need the workspace from step 3 to exist — not because every step strictly requires the one before it.

### 1. Enable service principals to call Fabric APIs

**Who:** Fabric tenant administrator.

A Fabric service principal cannot call any Fabric API until your tenant allows it. The setting is called **"Service principals can call Fabric public APIs"** in your Fabric tenant's admin settings.

**Check its current state before you change anything.**

- **If it is already enabled for your whole organisation, you are done. Do not narrow it.** Restricting an existing tenant-wide setting to one security group affects every other team's service principals, not only this deployment. That is not a change to make for one install.
- **If it is disabled, enable it and scope it to a security group that contains the M2M service principal (`M2M_CLIENT_ID`).** Scoping to a group is the narrower option and is preferred when you are turning the setting on for the first time.

Enabling this tenant setting requires the **Fabric Administrator** role, or **Global Administrator**. Fabric Administrator is a different right from the **Application Administrator** or **Cloud Application Administrator** role used in [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md) to create the service principal itself — holding one does not imply holding the other. If the person who created the M2M service principal does not also hold one of these roles, route this step to whoever does.

Studio never sets this tenant setting. It is entirely your organisation's action, done once per tenant.

### 2. Provision Fabric capacity

**Who:** Fabric capacity administrator (often the same person as the tenant administrator).

Provision a Fabric capacity for this domain, or nominate an existing one. Return its **Fabric-side capacity GUID** — see "Which capacity ID to return" below, because it is not the identifier the Azure portal shows you.

**Size: F2 is enough.** F2 is the smallest F SKU. A full Studio stack — the domain workspace, a schema-enabled Lakehouse, and Studio's own short-lived per-intent workspaces — runs on one. Start there and scale up against your own workload. F64, the size most Fabric guidance centres on, is 32 times the capacity units and 32 times the cost, with no benefit at this stage.

**Per-user licences: Free is enough, and Power BI Pro is not required.** Everything Studio creates in Fabric — Lakehouses, schemas, workspaces — is a non-Power BI Fabric item, and Microsoft's licensing rules let a user with a **Microsoft Fabric (Free)** licence create and share those in any workspace backed by an F SKU. There is no per-seat purchase to make for Studio itself, at F2 or at any other size.

Two things follow from that, and both bite in practice:

- **A Free licence is granted automatically the first time a person signs in to the Fabric portal**, and only if Fabric is enabled in your tenant. Somebody who has never opened Fabric has no licence yet. Studio reports this as: *"Fabric rejected the call because the account has no Fabric licence assigned. Ask a Microsoft 365 administrator to assign one, then retry."*
- **Below F64, viewing Power BI content still needs Pro or PPU.** This does not affect Studio, which creates no Power BI items. It affects your team if they also expect to open Power BI reports from the same workspace. If that matters to you, it is a reason to consider F64 — the only one at this stage.

**Name: lowercase letters and digits only.** The capacity name must match `^[a-z][a-z0-9]*$` — it must start with a letter, and **hyphens are not allowed**. `axeval-fabric` is rejected; `axevalfabric` is accepted.

#### Who can be a capacity administrator

**Creating a capacity requires at least one administrator member, and that member must be an in-tenant user or service principal.** This is a required input, not an option.

**Guest and external (B2B) identities are rejected.** This is routine in organisations managed by a partner or spanning several tenants, and it fails in a way that does not name the cause. If your own account is a guest in this tenant, you will see one of:

- `BadRequest: All provided principals must be existing, user or service principals`
- `BadRequest: Invalid principal name`
- `Unauthorized: Unable to authorize with Azure Active Directory`

The fix is to name an administrator who is a native member of the Fabric tenant, not a guest.

#### Add the M2M service principal as a capacity administrator

**Add the M2M service principal as a capacity administrator too, using its service principal object ID.** Two different values look like the right one and only one works:

- The **application (client) ID** — `M2M_CLIENT_ID` — is **rejected** here.
- The **service principal object ID** — the enterprise application's object ID in Entra, a different GUID — is accepted.

Ask your Entra administrator for the service principal object ID if you do not have it.

This is needed for two reasons. First, when the human administrator is a guest identity, the service principal is the only identity that can create the workspace in step 3 — it authenticates directly with its client credentials and creates the workspace itself. Second, Studio's own runtime creates and deletes short-lived workspaces on this capacity for per-intent work, so the service principal needs capacity-level rights regardless of who creates the domain workspace.

#### Which capacity ID to return

**Fabric needs its own capacity GUID, not the Azure resource ID.** These are two different values for the same capacity:

| Value | Looks like | Correct? |
| --- | --- | --- |
| Azure resource ID | `/subscriptions/…/resourceGroups/…/providers/Microsoft.Fabric/capacities/<name>` | **No** |
| Fabric-side capacity GUID | a plain GUID, such as `00000000-1111-2222-3333-444444444444` | **Yes** |

The Azure portal and the `az` command line show only the resource ID. The GUID is not exposed there at all.

To find the GUID, call the Power BI Admin API: `GET https://api.powerbi.com/v1.0/myorg/admin/capacities`. It lists capacities provisioned through Azure. The Fabric endpoint `GET /v1/capacities` may not return a newly created F-SKU capacity at all, so do not treat an empty result there as a problem with the capacity.

**Allow for a delay.** A capacity created through Azure does not appear on the Fabric side straight away, and it can still be missing after several checks. A capacity you cannot see yet is not a broken capacity — wait and check again.

If the wrong value reaches Studio, nothing fails at registration. Lakehouse creation fails later, during domain creation, with an unclear Fabric error — which is the exact failure this step exists to prevent.

#### Set the capacity ID at registration

**Set the capacity ID now — do not leave it for later.** When your operator registers this Fabric connection in Studio, the capacity ID field is optional and free-text. Studio accepts an empty value with no warning at that point. But when your operator later creates a domain and binds a workspace that has no capacity of its own — most commonly because it was created fresh rather than picked from an existing one — Studio falls back to this connection's capacity ID. If neither is set, creating that domain's Lakehouse fails immediately, as part of domain creation itself — not at registration, and not as some separate, later step. Provide the capacity ID at registration to avoid hitting this failure.

Unlike the workspace, Lakehouse, and schema in step 3, the capacity ID is not permanent: if you provide the wrong one, your operator can correct it later, in the domain's own settings. That correction path exists for fixing a mistake — it is not a reason to leave the value empty now, which is the failure this step exists to prevent.

### 3. Create or nominate the domain's workspace, lakehouse, and schema

**Who:** Fabric workspace administrator (Admin or Member on the workspace).

Create a new Fabric workspace for this domain, or nominate an existing one. Inside it, create or nominate a Lakehouse. Return four values: the workspace ID, the Lakehouse **name**, the Lakehouse **ID**, and the schema name. Your operator enters these when the domain is created in Studio and cannot change them afterward — the binding is permanent for that domain.

**Who creates the workspace.** If your own account is a guest in this tenant, you may not be able to create the workspace at all. Have the M2M service principal create it, using the capacity administrator rights granted in step 2. A workspace created by the service principal makes that service principal the workspace Admin automatically, which satisfies steps 4 and 5 below without a separate grant.

**The Lakehouse must be schema-enabled, and this cannot be changed later.**

- In the Fabric portal, the **Lakehouse schemas** checkbox is selected by default. Leave it selected.
- Through the REST API, schemas are **off** by default. You must send `"creationPayload": {"enableSchemas": true}` when you create the Lakehouse.
- There is no way to add schema support to an existing Lakehouse. Microsoft does not offer a migration path.

A Lakehouse without schema support has no schema to return, so this step cannot be completed with one. Because the binding is permanent, the only recovery is to create a new Lakehouse and recreate the domain against it.

**The schema is `dbo`. There is nothing to create.** Every schema-enabled Lakehouse gets a `dbo` schema automatically, and it cannot be renamed or removed. Return `dbo` unless you deliberately created an additional schema and want the domain bound to that one instead.

**Read access for people who need to browse the workspace.** Studio does not check any human identity's access to this workspace, so no grant here is required for a domain to activate. If the people driving the domain want to open the workspace in Fabric's own UI, grant them **Viewer**. That is a convenience, not a prerequisite.

### 4. Grant the service principal a deploy-capable workspace role

**Who:** Fabric workspace administrator (Admin or Member on the workspace).

On the workspace from step 3, grant the M2M service principal (`M2M_CLIENT_ID`) a role that can deploy: **Contributor** or **Member**. In the Fabric workspace, use **Manage access** to add the service principal by its app name and assign the role.

This role is needed regardless of deployment style: it is what lets the service principal push changes to the workspace when your team's domain repository deploys through its GitHub Actions workflow.

**Studio never grants a deploy-capable role, and never checks whether one is present.** Studio's own check on this workspace looks only for read access (step 5), and read access cannot deploy. A missing or insufficient deploy role does not show up as a Studio error at any point — not at registration, not at domain activation. It only surfaces the first time a deploy runs, as a failure from Fabric itself.

### 5. Confirm the service principal's read access to the domain workspace

**Who:** Fabric workspace administrator (Admin or Member on the workspace).

On the same workspace, make sure the M2M service principal holds at least **Viewer** access — Viewer, Contributor, Member, or Admin all satisfy this. If you already completed step 4, this is already satisfied, since Contributor and Member both include read access.

**This is a hard prerequisite, and Studio will not fix it for you.** When a domain using this
workspace activates under Kubernetes on Azure, Studio checks that the M2M service principal can
already read the workspace. If it cannot, activation fails. Studio grants nothing, so nothing
here resolves on its own — the grant has to exist before activation.

**Studio proves the access as the service principal, not as you.** The check is a plain workspace
read issued with the registered M2M credential, which is the identity that actually has to work
later. When a person triggers activation, Studio still runs the check under that same M2M
credential rather than the person's own Fabric access, so the operator's workspace role has no
bearing on whether this step passes. The failure names both halves of the problem:

```
Service Principal <M2M_CLIENT_ID> does not have at least Viewer access to
Fabric workspace <workspace-id>.
```

**Only a genuine denial fails the step.** Studio treats a 403, and a workspace that is invisible
to the identity, as proof the access is missing. A network error, a 5xx, or a 401 propagates
untouched instead of being reported as missing access — an important distinction, because those
send you to Fabric's **Manage access** panel for a problem that panel cannot fix.

**Studio does not read role assignments to decide this.** Listing a workspace's role assignments
itself requires Member or Admin, which a Viewer-baseline service principal does not hold. Studio
therefore proves the access by using it rather than by enumerating it.

> **Applies to: releases before v0.1.32.** Earlier releases behaved almost oppositely, and if you
> are following this page against one of them, the old rules apply. On `v0.1.26` through
> `v0.1.31`, Studio *assigned* Viewer to the service principal when it was missing — making this
> step a convenience rather than a prerequisite — but it made that call under the **operator's
> own** Fabric credential. An operator holding less than Member on the workspace left the domain
> `PENDING`, retryable by a colleague with more access. From `v0.1.32` the grant is gone: the
> step verifies and never writes, so step 4's grant became mandatory and the operator's own
> workspace role stopped mattering.

Under **Local Docker**, Studio records **this step** as succeeded without reading the workspace at all — no service-principal grant is verified or made. That is specific to this step. A different check, binding validation, still reads the workspace on both deployment styles, under the operator's own Azure identity — see [02-prereqs-operator](02-prereqs-operator.md). The service principal still needs real access, because the GitHub Actions deploy in step 4 cannot run without it. Studio will not tell you when *that* grant is missing; you find out at the first deploy.

**Steps 4 and 5 are not the same grant, and Studio treats them very differently.** Studio checks step 5's read baseline (on Kubernetes on Azure) but never verifies step 4's deploy role, on either deployment style. Viewer access satisfies Studio's own check and still leaves the deploy workflow unable to push changes. Granting Contributor or Member in step 4 satisfies both at once, which is the simplest way to be done with this: do that and step 5 needs nothing further.

**Studio still grants roles in one place, and it is nothing for you to configure.** On the workspace you nominate in step 3, Studio assigns no role at all. On the short-lived per-intent workspaces it creates and deletes itself on the capacity from step 2, it grants the M2M service principal Admin and grants individual collaborators Contributor when they are added to an intent. Those are not the workspace you nominate, and you act on nothing to make them happen.

### 6. Allow outbound network access

**Who:** whoever controls outbound network policy where Studio and its deploy workflows run.

Allow outbound access (443/tcp) to all seven hosts below. Allowing only the first three is a common mistake: the deployment authenticates and reads workspaces successfully, then fails later with connection timeouts on the data paths.

| Host | Purpose |
| --- | --- |
| `login.microsoftonline.com` | The Entra token endpoint. Studio's service principal exchanges its client ID and secret here for an access token, using the OAuth client-credentials flow. |
| `api.fabric.microsoft.com` | The Fabric REST API. Studio calls this to read and write workspaces, Lakehouses, and schemas under the service principal's token. |
| `graph.microsoft.com` | Microsoft Graph. Studio calls this to check whether the per-repository federated credential already exists on the service principal's app registration — see the recurring task in [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md). |
| `api.powerbi.com` | The Power BI service, which publishes Fabric's delegated permission scopes and the admin API that returns the Fabric-side capacity GUID from step 2. |
| `*.datawarehouse.fabric.microsoft.com` | The Fabric SQL analytics endpoint. Studio queries Lakehouse data through it. This is on the normal data path, not an optional feature. |
| `onelake.dfs.fabric.microsoft.com` | OneLake storage. Studio reads and writes Lakehouse files here. |
| `onelake.table.fabric.microsoft.com` | The OneLake table API. Studio lists a Lakehouse's schemas through it when it checks what a domain's Lakehouse contains. A separate host from the `dfs` one above, and allowing only `dfs` leaves schema reads timing out. |

`login.microsoftonline.com` is shared with the Entra-side requests in [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md); the other six are specific to Fabric.

Two hosts you may see named in Microsoft's own Fabric guidance are **not** needed here.
`app.fabric.microsoft.com` is the Fabric web UI — Studio builds links to it for people to click, but never calls it. `analysis.windows.net` appears inside the Power BI permission scopes, as part of the scope's name rather than as an address anything connects to.

## Values to send back

| Token | Comes from |
| --- | --- |
| `FABRIC_CAPACITY_ID` | The **Fabric-side capacity GUID** from step 2 — not the Azure resource ID. |
| `FABRIC_WORKSPACE_ID` | The workspace ID from step 3. |
| `FABRIC_LAKEHOUSE_NAME` | The Lakehouse name from step 3. |
| `FABRIC_LAKEHOUSE_ID` | The Lakehouse ID from step 3. Studio needs both the name and the ID — they are used by different calls, so returning only one leaves a gap that surfaces later. |
| `FABRIC_SCHEMA` | The schema name from step 3 — `dbo`, unless you deliberately created another. |

## Where this goes

`FABRIC_CAPACITY_ID` is entered by the operator during organisation setup — see [05-configure-org](05-configure-org.md) — and used again in [06-first-domain](06-first-domain.md). `FABRIC_WORKSPACE_ID`, `FABRIC_LAKEHOUSE_NAME`, `FABRIC_LAKEHOUSE_ID`, and `FABRIC_SCHEMA` are entered only in [06-first-domain](06-first-domain.md), when the domain is created and bound to this workspace.
