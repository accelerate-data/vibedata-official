---
applies-to: vibedata v0.1.33
verified-against: studio@a121fc466
verified-on: 2026-08-13
sources:
  - docs/functional/container-deployment/README.md
  - docs/design/kubernetes-deployment/cloud.md
  - README.md
  - cli/vibedata/src/vibedata/main.py
  - cli/vibedata/src/vibedata/commands/install.py
  - src/server/modules/data-platforms/providers/descriptor-catalog.ts
  - src/server/modules/data-platforms/providers/registry.ts
  - cli/vibedata/src/vibedata/templates/env.j2
---

# VibeData Studio: Deployment and Onboarding

VibeData Studio is a workspace where an AI agent helps a data team build, test, and run
data pipelines against a connected data platform, with changes tracked through a connected
GitHub repository. This guide takes a reader with no access to any private Accelerate Data
repository from an empty machine to a first domain: created, connected to a data platform,
wired to GitHub, and validated.

## Pick your combination

Two choices shape everything that follows. Pick one deployment style and one data platform.

| Axis | Choices |
| --- | --- |
| Deployment style | Local Docker · Kubernetes on Azure |
| Data platform | DuckDB · MotherDuck · Microsoft Fabric |

Studio implements both deployment styles and registers all three data platforms as backends.
All six combinations below are documented to equal depth. None is recommended over another.

| Deployment style | Data platform |
| --- | --- |
| Local Docker | DuckDB |
| Local Docker | MotherDuck |
| Local Docker | Microsoft Fabric |
| Kubernetes on Azure | DuckDB |
| Kubernetes on Azure | MotherDuck |
| Kubernetes on Azure | Microsoft Fabric |

**Local Docker** runs Studio as containers on one machine, using the `vibedata` CLI's
`install compose` command. It has no SSO — the single operator signs in as the host's own
GitHub identity.

**Kubernetes on Azure** runs Studio on an existing AKS cluster, using the `vibedata` CLI's
`install kubernetes` command. It supports multiple users signing in through Microsoft Entra
SSO.

## Which admin pages your combination needs

Studio has one operator and five admin pages: Entra, Fabric, GitHub, Azure infrastructure, and
MotherDuck. Each page is addressed to one role and is written to be forwarded as a single
request.

**One page does not mean one person.** `01b-prereqs-fabric-admin` alone asks for three separate
Fabric rights — tenant, capacity, and workspace administration — and tags every ask with the
right it needs so each can be routed separately. The recurring task in `01a-prereqs-entra-admin`
needs a right the rest of that page does not. Kubernetes on Azure with Microsoft Fabric can need
up to eight distinct right-holders across four pages. Plan the handoff from the roles the pages
name, not from the number of pages.

**Forwarding a page does not always unblock it.** Four of the five pages need a value from
somewhere else before their reader can start, and two asks reopen after the install. The wave
table in the reading path below says which asks can go out immediately, and each page entry
below lists what it consumes and what it produces.

No combination needs all five pages.

| Combination | Admin pages |
| --- | --- |
| Local Docker + DuckDB | `01d-prereqs-azure-infra` (Foundry only) |
| Local Docker + MotherDuck | `01d-prereqs-azure-infra` (Foundry only) · `01e-prereqs-motherduck-admin` |
| Local Docker + Microsoft Fabric | `01a-prereqs-entra-admin` (Fabric only) · `01b-prereqs-fabric-admin` · `01d-prereqs-azure-infra` (Foundry only) |
| Kubernetes on Azure + DuckDB | `01a-prereqs-entra-admin` (SSO only) · `01c-prereqs-github-org-owner` · `01d-prereqs-azure-infra` |
| Kubernetes on Azure + MotherDuck | `01a-prereqs-entra-admin` (SSO only) · `01c-prereqs-github-org-owner` · `01d-prereqs-azure-infra` · `01e-prereqs-motherduck-admin` |
| Kubernetes on Azure + Microsoft Fabric | `01a-prereqs-entra-admin` · `01b-prereqs-fabric-admin` · `01c-prereqs-github-org-owner` · `01d-prereqs-azure-infra` |

What each admin page is for. **Consumes** is what the page needs before its reader can start;
**produces** is what comes back. Each page states the same thing in full; this list is here so
you can plan the handoff without reading all five.

- [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md) — Entra admin. The page has a Fabric
  section (applies when your data platform is Microsoft Fabric) and a Studio-SSO section
  (applies when your deployment style is Kubernetes on Azure). The `(SSO only)` marker in
  the table above means only the SSO section applies to that row, and `(Fabric only)` means only
  the Fabric section applies — neither marker means skip the page. If your data platform is
  Microsoft Fabric, read the Fabric section regardless of deployment style.
  - **Consumes:** `STUDIO_DOMAIN` from `01d` step 4, for the SSO redirect URI (Kubernetes on
    Azure) and, on Microsoft Fabric, for the M2M app's redirect URI as well · your decision on whether to keep the U2M and M2M identities separate, which the
    Entra admin is told to ask you for (Microsoft Fabric on Kubernetes on Azure) · each new
    domain's GitHub repository, `{org}/{repo}`, from step 5 of the reading path, for the
    recurring federated credential (Microsoft Fabric).
  - **Produces:** `TENANT_ID` · `M2M_CLIENT_ID` and `M2M_CLIENT_SECRET` (Microsoft Fabric) ·
    `U2M_CLIENT_ID` and `U2M_CLIENT_SECRET` (only if you keep U2M separate from M2M) ·
    `ENTRA_SSO_CLIENT_ID` and `ENTRA_SSO_CLIENT_SECRET` (Kubernetes on Azure) · one federated
    credential per domain repository, created again for every new domain.
- [01b-prereqs-fabric-admin](01b-prereqs-fabric-admin.md) — Fabric admin. Applies only when
  your data platform is Microsoft Fabric. Its six asks route to three different rights: tenant,
  capacity, and workspace administration.
  - **Consumes:** the service principal from `01a`, which must exist before steps 1, 2, 4 and 5
    can be done at all. Two different values: `M2M_CLIENT_ID` (the application ID) for steps 1,
    4 and 5, and the service principal's **object ID** for step 2 — the client ID is rejected
    there. Step 3 follows step 2 unless you nominate an existing workspace. Step 6 needs
    nothing from `01a`.
  - **Produces:** `FABRIC_CAPACITY_ID` · `FABRIC_WORKSPACE_ID` · `FABRIC_LAKEHOUSE_NAME` **and**
    `FABRIC_LAKEHOUSE_ID` — both are needed · `FABRIC_SCHEMA` · the tenant setting and the
    workspace role grants, which are actions rather than values.
- [01c-prereqs-github-org-owner](01c-prereqs-github-org-owner.md) — GitHub org owner. Applies
  only when your deployment style is Kubernetes on Azure. Under Local Docker, Studio uses the
  operator's own GitHub sign-in instead, and no organisation owner action is needed.
  - **Consumes:** `STUDIO_DOMAIN` from `01d` step 4 — the callback URL is built from it, and
    GitHub rejects any sign-in that arrives at an unregistered URL.
  - **Produces:** the GitHub App's App ID, client ID, client secret, and private key · the App
    installed on the account that owns your domain repositories, and the list of repositories it
    can reach · a visibility setting that lets every Studio user authorize the App. An App
    registered under a personal account, or an organisation App with users outside that
    organisation, must be set to **Any account** or those users cannot connect GitHub at all.
- [01d-prereqs-azure-infra](01d-prereqs-azure-infra.md) — Azure infrastructure owner. This
  page has two independent parts. Its infrastructure requests (AKS, storage, Key Vault,
  front door, DNS) apply only to Kubernetes on Azure. Its Azure AI Foundry request — the LLM
  provider this doc set configures for every combination — applies to all six combinations; that
  is what the `(Foundry only)` marker means on the three Local Docker rows above.
  - **Consumes:** nothing, to start. Its step 4 finishes later: wiring Front Door's origin needs
    the private ingress address the install returns — see step 7 of the reading path.
  - **Produces:** `STUDIO_DOMAIN` · `AKS_KUBECONFIG` · `AZURE_FILES_SHARE_URL` ·
    `KEY_VAULT_URL` · the `bootstrap-key` vault secret (all Kubernetes on Azure) ·
    `FOUNDRY_BASE_URL`, `FOUNDRY_API_KEY`, and `FOUNDRY_DEPLOYMENT_NAME` (all six combinations).
- [01e-prereqs-motherduck-admin](01e-prereqs-motherduck-admin.md) — MotherDuck org admin.
  Applies only when your data platform is MotherDuck.
  - **Consumes:** the MotherDuck identities of your operator and of everyone who will work in
    the domain — the page needs them to grant Share READ and to size seats. Send them with the
    request; the MotherDuck admin cannot look them up.
  - **Produces:** the MotherDuck organisation account, a read-write Service PAT, and the
    database name. These are entered into Studio's own form rather than set as environment
    variables, so `01e` names no fixed token for them. A Share, if one is created, is **not**
    sent back — it is found by the bound database's own name.

## Reading path

Follow this order. Skip the admin pages your combination does not need, and skip whichever
of `03-deploy-docker`/`04-deploy-kubernetes-azure` does not match your deployment style.

Two parts of this order are not sequential, and both are called out where they arise: one ask in
step 1 waits on a later step, and step 7 is work that goes back to your administrators after the
install rather than work that follows step 6.

1. The admin pages listed above for your combination — forward each one to the person who
   holds that role. Forward each page whole; that is how they are written. **The waves below tell
   you when each ask inside a page becomes actionable**, so you can say so in the covering note
   instead of leaving the administrator to find out. Skip any wave whose pages your combination
   does not need.

   | Wave | Ask can be actioned | Blocked until |
   | --- | --- | --- |
   | 1 | `01d` (both parts) · `01e` · `01a` Fabric section (except the M2M redirect URI) · `01b` step 6 | Nothing. Send these on day one. On Kubernetes on Azure the M2M redirect URI waits for `STUDIO_DOMAIN` — see wave 2. |
   | 2 | `01a` Studio SSO section · `01c` | `STUDIO_DOMAIN` comes back from `01d` step 4. |
   | 3 | `01b` steps 1, 2, 3, 4, and 5 | The service principal must exist in Entra first — it cannot be put in a security group, made a capacity administrator, or given a workspace role before it is created. Steps 1, 4 and 5 need `M2M_CLIENT_ID` from `01a`. **Step 2 needs a different value**: the service principal's **object ID**, which `01a` also returns. The client ID is rejected there. Step 3 runs after step 2 — in many tenants the service principal has to create the workspace itself, using the capacity-admin rights step 2 grants. Only the "nominate an existing workspace" branch of step 3 is free of that. |
   | 4 | `01d` step 4 origin wiring · `01a` recurring federated credential | The install has run. This is step 7 below, not a prerequisite. |

   **Ask `01d` for step 4 first.** It settles `STUDIO_DOMAIN`, and wave 2 cannot start without
   it. On Microsoft Fabric, `01d` step 4 also lists a further redirect URI built from the same
   name. The name must not change afterwards.

   **Include your own answers when you forward wave 1.** The Entra admin is told to ask you
   whether you will keep the U2M and M2M identities separate in Studio's Fabric connection form
   (the default reuses M2M, and then no U2M app registration is needed). The MotherDuck admin
   needs the MotherDuck identities of everyone who will work in the domain. Neither person can
   find these out without you.

   **Wave 4 is not a prerequisite at all.** Both of its asks reopen after the install: `01d`'s
   Front Door origin needs the private address the install returns, and `01a`'s federated
   credential is created again for every new domain repository. Tell both administrators when
   you first forward their page that you will come back to them, so the request is not closed
   out as finished.
2. [02-prereqs-operator](02-prereqs-operator.md) — what the operator installs and signs into
   before deploying.
3. [03-deploy-docker](03-deploy-docker.md) for Local Docker, or
   [04-deploy-kubernetes-azure](04-deploy-kubernetes-azure.md) for Kubernetes on Azure.
4. [05-configure-org](05-configure-org.md) — organisation-level setup: LLM profile, data
   platform, GitHub App, users.
5. [06-first-domain](06-first-domain.md) — create and bind the first domain.
6. [07-verify](07-verify.md) — confirm the domain is done.
7. **Work that goes back to your administrators after the install.** Two asks live on the
   prerequisite pages but are not prerequisites. Do not close either request when the install
   finishes.

   | Ask | Goes back to | Applies to | When |
   | --- | --- | --- | --- |
   | Point Front Door's origin at the private ingress address the install returns | Azure infrastructure owner — [01d-prereqs-azure-infra](01d-prereqs-azure-infra.md) step 4 | Kubernetes on Azure | Right after step 3. The steps are in [04-deploy-kubernetes-azure](04-deploy-kubernetes-azure.md) under "Go live". |
   | Add one federated credential to the M2M app registration, for the new domain's repository | Whoever owns that app registration — [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md), "Recurring task" | Microsoft Fabric | Every time a domain is created, starting with step 5. Not once. |

   The first one blocks go-live: Front Door has no origin until the install has produced the
   private ingress address, so your domain does not reach Studio until this is wired. The second
   one recurs for the life of the deployment — tell the Entra rights-holder to expect it before
   they close their request, not after the first domain fails its check.
8. [08-getting-started-contributor](08-getting-started-contributor.md) — what a domain
   contributor needs to know before doing data work in a domain.
9. [09-worked-example-salesforce](09-worked-example-salesforce.md) — one worked example:
   a Salesforce source to Bronze, then a mart that answers one question.

If something goes wrong along the way, check
[90-troubleshooting](90-troubleshooting.md).

## What this does not cover

This guide stops once a contributor has landed data into a domain and built a mart from it,
as shown in [08-getting-started-contributor](08-getting-started-contributor.md) and
[09-worked-example-salesforce](09-worked-example-salesforce.md). Scheduling, automation
jobs, semantic models, and deploying a merged pipeline are out of scope. For those, continue
with the Studio user guide:
<https://accelerate-data.github.io/studio/>.

Upgrade, backup, and restore are not covered in this pass. They are planned for this same
doc set later.
