# Request for your Microsoft Fabric administrators

This page covers the Fabric-side prerequisites for a Domain. It does not create Entra applications; see [[Prerequisites Entra Administrator]] for those.

## What Studio needs

A Fabric Domain binds to:

- one Fabric workspace;
- one Lakehouse in that workspace;
- one schema in that Lakehouse;
- optionally, a capacity ID used for later ephemeral workspaces.

For delegated deployments, it also needs:

- a user who can discover and validate those resources through the selected Entra Identity Provider;
- a Domain service principal for unattended work.

For Local Docker, user operations use the Azure CLI identity inside Studio's API container. A separate Domain service principal is still required for unattended features when the Domain configuration selects one.

## 1. Enable service-principal Fabric API access

**Who:** Fabric tenant administrator.

If your tenant restricts service principals from using Fabric APIs, enable the relevant Fabric tenant setting and scope it according to your organization's policy. The Domain service principal must be permitted to call the Fabric APIs Studio uses.

Do not narrow an existing tenant-wide setting solely for this deployment without considering other service principals already using it.

## 2. Provide Fabric capacity

**Who:** Fabric capacity administrator.

Studio creates short-lived Fabric workspaces for Intents. The Domain form lets the operator choose an **Ephemeral Workspace Capacity**. Current Studio can discover available capacities and stores the selected capacity ID on the Domain.

Provide a Fabric capacity with enough available capacity to create those temporary workspaces. Capacity exhaustion is a hard Intent-activation failure; Studio does not queue indefinitely waiting for Fabric capacity.

Return the **Fabric capacity ID** used by the Fabric API, not an Azure Resource Manager resource path.

Do not treat a specific SKU such as F2 or F64 as a Studio requirement. Capacity sizing is workload- and tenant-dependent and can change independently of Studio.

## 3. Create or nominate the persistent Domain resources

**Who:** Fabric workspace administrator.

Provide or create:

1. a Fabric workspace;
2. a schema-enabled Lakehouse;
3. the schema Studio should use as the Domain's primary schema.

Return:

- workspace ID;
- workspace name;
- Lakehouse ID;
- Lakehouse name;
- schema name;
- capacity ID when applicable.

Current Studio can discover existing workspaces and Lakehouses. It does **not** create the persistent Domain workspace or Lakehouse from the Domain form. It can create a schema from the form.

The Domain resource identity is immutable after creation. Confirm the workspace, Lakehouse, and schema before the operator saves the Domain.

## 4. Give the Domain service principal persistent workspace access

**Who:** Fabric workspace administrator.

Grant the Domain service principal enough access to read and operate against the persistent Domain workspace. Studio verifies access; it does not silently repair a missing persistent-workspace grant.

At minimum, the service lane must be able to read the workspace for readiness verification. CI/CD and other unattended operations may require a broader deploy-capable role. Grant only the role required by your workflow.

A successful Studio readiness check does not prove every future CI operation is authorized. Fabric can accept the identity and still reject a later deployment operation that needs a stronger workspace role.

## 5. Ephemeral workspace behavior

Current Studio creates an ephemeral Fabric workspace and Lakehouse for an Intent. It then:

- creates the Domain's primary schema in the ephemeral Lakehouse;
- grants the Domain service principal **Admin** on that ephemeral workspace when the service-principal object ID is available;
- tears the ephemeral workspace down when the Intent lifecycle requires it.

This means the service identity needs authority that lets Studio create and delete workspaces on the selected capacity and manage the required ephemeral workspace role.

The persistent Domain workspace and the ephemeral Intent workspace are different resources. Do not grant persistent production access merely because the ephemeral workspace needs Admin.

## 6. GitHub Actions federated credential

**Who:** Entra application owner / administrator for the Domain service principal.

Fabric GitHub Actions uses an Entra federated identity credential on the Domain service principal's application registration.

The expected subject is based on the Domain repository's **recorded default branch**:

```text
repo:<org>/<repo>:ref:refs/heads/<default-branch>
```

Do not hard-code `main` unless `main` is the repository's actual recorded default branch.

Studio's GitHub Actions setup verifies this credential and reports a safe remediation when it is missing or invalid. The administrator creates or repairs the federated credential out of band.

## 7. Network access

Where Studio runs, allow outbound HTTPS access to the Microsoft identity and Fabric endpoints required for:

- Entra token acquisition;
- Fabric REST APIs;
- Fabric SQL endpoint access;
- Microsoft Graph when Studio verifies the federated credential;
- Azure resource audiences used by the current credential broker.

Use your organization's current Microsoft endpoint policy rather than a copied static hostname list. Microsoft endpoint inventories change independently of Studio.

## Values to return

Give the Studio operator:

| Value | Used for |
| --- | --- |
| Workspace ID and name | Domain resource binding |
| Lakehouse ID and name | Domain resource binding |
| Schema name | Domain primary schema |
| Fabric capacity ID | Ephemeral workspace placement |
| Domain service-principal object ID | Ephemeral workspace role grant |
| Confirmation of persistent workspace access | Service-lane readiness and unattended operations |
| Confirmation that Fabric APIs allow the service principal | Fabric API calls |

The Entra tenant/client/secret values are returned through [[Prerequisites Entra Administrator]].

---

_Applies to: studio/main (unreleased snapshot). Verified against `studio@5c9d2bbf339a` on 2026-08-22._
