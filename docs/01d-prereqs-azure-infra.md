---
applies-to: vibedata v0.1.33
verified-against: studio@a121fc466
verified-on: 2026-08-13
sources:
  - docs/design/kubernetes-deployment/cloud.md
  - docs/design/kubernetes-deployment/README.md
  - cli/vibedata/src/vibedata/k8s/providers.py
  - cli/vibedata/src/vibedata/k8s/render.py
  - cli/vibedata/src/vibedata/commands/install_kubernetes.py
  - cli/vibedata/src/vibedata/backup/kubernetes.py
  - src/server/modules/model-catalog/profile.schemas.ts
  - src/server/modules/model-catalog/connection-test.ts
  - src/server/modules/chat/openhands/side-channel-completion.ts
  - src/server/modules/model-catalog/risk-annotation-probe.ts
  - src/server/modules/model-catalog/profile.service.ts
---

# Request for your Azure subscription owner or contributor: infrastructure and the Azure AI Foundry resource

Forward this page to whoever holds **Owner** or **Contributor** rights on the Azure
subscription that will host Studio. Nothing here requires access to Studio or to any
Accelerate Data system — only to your organisation's Azure subscription.

## This page has two independent parts

- The **infrastructure requests** below — the AKS cluster, storage, Key Vault, and the
  HTTPS front door — apply only if your deployment style is **Kubernetes on Azure**. Skip
  them entirely if you chose **Local Docker**.
- The **Azure AI Foundry resource** request applies to **all six combinations**, including
  all three **Local Docker** combinations. Every combination configures a large-language-model
  connection in [05-configure-org](05-configure-org.md), and Azure AI Foundry is the provider
  this doc set uses for it. Studio itself supports several providers; this guide documents the
  Foundry path only, so that is what your operator will be asked for.

If you chose **Local Docker**, skip straight to [Azure AI Foundry
resource](#azure-ai-foundry-resource-needed-on-every-combination) below — the infrastructure
section does not apply to you. If you chose **Kubernetes on Azure**, you need both parts of
this page.

## Kubernetes infrastructure

> **Applies to: Kubernetes on Azure.** Skip to "Azure AI Foundry resource" below if you
> chose Local Docker.

**The Studio CLI creates no cloud resources of its own.** `vibedata install kubernetes` only
talks to the Kubernetes API of a cluster you already created — it never calls Azure on your
behalf. Everything in this section must exist before your operator runs that command.

**Two things people often add out of habit that Studio does not need:**

- **No Azure Container Registry.** Studio's images and Helm charts come from Accelerate
  Data's own registry, not from anything in your subscription.
- **No Azure Database for PostgreSQL.** Studio runs Postgres as a container inside the
  cluster itself; there is no managed database to provision.

**Do these four steps in order.** Each one depends on the one before it:

1. **Network and cluster** — the virtual network and its two subnets, then the AKS cluster
   attached to one of them.
2. **Storage** — the storage account is locked to the subnet the cluster's nodes actually run
   in, so the cluster must exist first.
3. **Key Vault** — the role assignment needs the cluster's kubelet identity, which only exists
   after the cluster is created.
4. **Front door** — the private link into the cluster is wired later, by your operator.

There is one exception to the order, and it depends on a choice in step 4. If you do **not**
use a custom domain, Front Door has to be created first, because Studio's domain is then Front
Door's own generated hostname and other administrators need that name before they can start.
Read step 4 before you begin.

### 1. Create the network and the AKS cluster

**Create your own virtual network first.** Do not let AKS create one for you. The network AKS
generates by default cannot carry the storage service endpoint that step 2 needs, and leaves
nowhere to put the private link that step 4 needs. No later page in this doc set can fix a
cluster's network configuration after the fact, so this is the point to get it right.

The virtual network needs **two** subnets:

| Subnet | What it holds | The setting that matters |
| --- | --- | --- |
| Node subnet | The AKS nodes | A `Microsoft.Storage` **service endpoint**. Step 2 allow-lists this exact subnet on the storage account, and an NFS share can only be reached through a service endpoint |
| Private-link subnet | The private link your operator creates in front of the cluster | `privateLinkServiceNetworkPolicies` set to `Disabled`. The portal does this for you when you create a Private Link service there; every other route — CLI, PowerShell, ARM template — needs it set explicitly, and private link creation fails without it. Leave `privateEndpointNetworkPolicies` alone: it is a separate setting, it governs network security groups and route tables rather than the Private Link service, and disabling it is not required here |

Create the AKS cluster attached to the **node** subnet, with a standard load balancer.

**Size the cluster against a floor, not a guess.** Studio's own workloads, plus a two-replica
backend, plus the optional monitoring stack, do not fit on a small cluster:

- **Core profile** (no monitoring): 8 vCPU across at least 2 nodes.
- **Full monitoring** (`--full-observability`, which your operator may choose): 8 vCPU is
  **not** enough. A real install with 2 × 4-vCPU nodes could not schedule one of Studio's own
  components — both nodes sat at 88–95% CPU allocation. Plan for at least 10 vCPU.

**Check your subscription's regional vCPU quota before you create the cluster.** The default
quota in a new region is small — often 10 vCPU. Size the cluster so at least one more node
still fits inside the quota. In the same real install, the quota left no room for a third node
of the original size, and the operator could not add capacity without coming back to you. Only
you can see or raise this quota, and a quota increase is not granted the same day.

Studio ships a default-deny network policy that isolates each agent pod from the others and
from the database; enforcing it needs a CNI that actually implements Kubernetes NetworkPolicy.
On AKS, choose **Azure CNI powered by Cilium** — the plain Azure Network Policy Manager has
known gaps in a rule construct this policy depends on, so the isolation would silently fail to
take effect on it.

Two more settings on this same cluster, both silent failures if you get them wrong:

- **Do not enable NodeLocal DNSCache.** Agents resolve through a link-local host resolver
  that this network policy's DNS rule cannot select — they lose DNS entirely, not just the
  policy's enforcement.
- **Do not enable dual-stack (IPv6) networking.** The policy has no IPv6 allow rule, so IPv6
  egress from agent pods is fail-closed.

You do **not** need to enable the OIDC issuer or the workload-identity add-on. Studio reads
the Key Vault using the cluster's kubelet identity instead — see step 3.

Return four things from this step:

| Token | What it is |
| --- | --- |
| `AKS_KUBECONFIG` | Access to the cluster as a kubeconfig. Tell your operator the **context name** as well — that is what they reference at install time |
| `AKS_KUBELET_CLIENT_ID` | The **client ID** of the cluster's kubelet identity. Not the cluster (control-plane) identity — these are two different identities. Read it from the cluster's `identityProfile.kubeletidentity.clientId` |
| `VNET_NAME` | The virtual network's name and resource group |
| `PRIVATE_LINK_SUBNET` | The name of the private-link subnet. Your operator needs it in step 4's wiring |

### 2. Create two Azure Files shares

Create a **premium** Azure Files storage account with an **NFS v4.1** share for Studio's
shared data directory, and a second NFS share in the same storage account for backups. NFS,
not the default SMB — Studio's agent pods run `git` on this share, and SMB's file locking
does not support what git needs.

**Turn off encryption in transit on this storage account.** Both **Secure transfer required**
and **Require encryption in transit for NFS** must be off. Both are **on by default** on a
storage account created in the Azure portal, and Studio's cluster mounts the NFS share
directly, with no mount helper. Leave either one on and the mount fails.

This is less alarming than it looks. An NFS v4.1 Azure Files share has no user-level
authentication at all — access is controlled entirely at the network layer, which is what the
next paragraph sets up.

**Lock the account to the cluster's node subnet.** Add a network rule allowing the **node**
subnet you created in step 1 — the subnet the AKS nodes actually run in — then set the
account's default network action to Deny. Do not create a separate subnet for storage. The
nodes' traffic never leaves the node subnet, so allow-listing any other subnet locks the
cluster out of its own share. The failure looks like a pod stuck mounting a volume, not like a
permission error.

Return the data share's URL as `AZURE_FILES_SHARE_URL`, in the exact form
`https://<storage-account>.file.core.windows.net/<share-name>` — the installer parses that
specific shape. Also return the storage account's own resource group as
`STORAGE_RESOURCE_GROUP`. Always send it, even if it looks unnecessary: the operator passes it
only when the installer needs it, and it costs you nothing to supply.

The backup share does not go through this page's values table. Your operator points to it
directly, later, whenever a backup is run — it is never given to the installer.

### 3. Create a Key Vault and load the fixed-name secrets

Create an Azure Key Vault, or nominate an existing one. Use **Azure role-based access
control** for its permission model, not the older access-policy model.

**Grant yourself `Key Vault Secrets Officer` on the vault before you do anything else.** On an
RBAC vault, creating the vault does not give you permission to write secrets into it. Without
this role you cannot create a single one of the secrets below.

Studio's installer reads these exact secret names — spelled exactly as shown, nothing
substitutable. The value formats are not suggestions: Studio's backend validates each one at
startup, and a wrongly formatted value stops the whole install.

| Secret name | What it holds | Required value format |
| --- | --- | --- |
| `pg-password` | Password for the in-cluster Postgres | Any password. See the character warning below |
| `auth-secret` | Studio's session-signing secret | At least 32 characters. A shorter value is rejected |
| `data-encryption-key` | The active data-encryption key | 32 random bytes, **base64**-encoded. Generate with `openssl rand -base64 32` |
| `obot-client-secret` | OAuth client secret for Studio's bundled agent runtime (obot) | Any random string |
| `obot-db-password` | Password for obot's own database | Any password. See the character warning below |
| `bootstrap-key` | One-time key used to create the first Studio admin | Any random string |
| `data-encryption-key-id` | The label Studio stamps on data it encrypts | 1–64 characters from `A-Z a-z 0-9 . _ -`. Choose once and never change it — see the warning below |
| `data-encryption-retired-keys` | Retired key labels and the key material each was used with | A JSON object. `{}` is correct for a deployment that has never rotated |
| `obot-tunnel-peer-token` | Shared token for obot's tunnel peer | Any random string |

That is the complete core set for `v0.1.33` — **nine secrets**, read from the released binary's
own `--list-secrets` output rather than from source.

**Three names that were optional on older releases are now required.**
`data-encryption-key-id`, `data-encryption-retired-keys` and `obot-tunnel-peer-token` are part of
the core set from `v0.1.33`. On `v0.1.26` the installer never read them, and this page previously
said they could be skipped. If you built a vault against that advice, add all three before an
upgrade.

`data-encryption-retired-keys` is the one to think about rather than generate. It is a JSON
object mapping a retired key label to the base64 key that label was used with, and `{}` is a
valid, correct value for a vault that has never rotated its encryption key. What it must not be
is `{}` on a deployment whose key label *has* changed — see the warning under
`data-encryption-key-id` below.

**`data-encryption-key-id` deserves a deliberate choice, not a default.** It is a label on the
encryption key, not a key. When it is unset, Studio labels everything it encrypts `k1`. Setting
it to any other value on a deployment that has already encrypted data under `k1` makes that data
unreadable, and Studio reports it as `UnknownKidError: Unknown kid in ciphertext envelope: k1`.
The recovery is to add the old label to `data-encryption-retired-keys` pointing at the **same**
key material — the label changed, the key did not:

```
data-encryption-retired-keys:  {"k1": "<the same value as data-encryption-key>"}
```

Pick the label once, before the first install, and do not change it afterwards. A deployment
built on an older release that had no `data-encryption-key-id` secret has been labelling under
`k1` all along, so supplying a different value at upgrade time is exactly the failure above.

**Do not use hex for `data-encryption-key`.** This is the single most common way this install
fails. `openssl rand -hex 32` produces a value that looks correct, passes every check a person
would make by eye, and then decodes to the wrong length — the backend refuses to start. The
failure surfaces about ten minutes later as a readiness timeout on the install, and the real
error is only in a pod log. Use `openssl rand -base64 32`.

**Character warning, for `pg-password` and `obot-db-password` only.** Both get pasted directly
into a Postgres connection string with no escaping, so avoid the characters `@ : / # ? &` in
either one — a plain hex string is a safe choice for these two. Do not carry that advice
across to the encryption keys above; they have their own formats.

**No share-key secret is needed.** The NFS v4.1 share from step 2 mounts key-free, over the
network — Studio never reads a storage key from this vault on Azure.

**If your operator turns on optional monitoring**, the vault needs additional secrets, on
top of the six above:

- `--with-observability` adds: `grafana-client-secret` · `grafana-admin-password`
- `--full-observability` (the same monitoring stack, plus Langfuse) adds those two, plus:
  `langfuse-salt` · `langfuse-nextauth-secret` · `langfuse-encryption-key` ·
  `langfuse-client-secret` · `langfuse-clickhouse-password` · `langfuse-db-password` ·
  `langfuse-redis-password` · `langfuse-minio-password` ·
  `langfuse-init-project-public-key` · `langfuse-init-project-secret-key`

`langfuse-db-password` is new in `v0.1.33`. Langfuse now connects to Postgres under its own
role rather than sharing Studio's, so a vault built for an earlier release is one secret short.

**Ask the CLI rather than counting by hand.** From `v0.1.32` the installer prints the exact set
for a profile and exits without touching anything — no cluster, no vault, no share needed:

```
vibedata install kubernetes --list-secrets
vibedata install kubernetes --list-secrets --with-observability
vibedata install kubernetes --list-secrets --full-observability
```

The list is derived from what the install actually renders, so it cannot drift from what the
install demands. Prefer it over the lists above, which are a convenience for people who do not
have the CLI to hand yet.

| Profile | Secrets in the vault, on `v0.1.33` |
| --- | --- |
| Core (no monitoring) | 9 |
| `--with-observability` | 11 |
| `--full-observability` | 21 |

These counts were read from the released `v0.1.33` binary, not from source. The set grew twice:
`v0.1.26` needed 6, 8 and 17; `v0.1.32` moved the core set to 9, 11 and 20; `v0.1.33` added
`langfuse-db-password` to the full profile only. A vault built against an older copy of this page
is short regardless of which profile it used.

**The flag does not exist before `v0.1.32`.** On `v0.1.26` it answers `No such option:
--list-secrets`. If you get that error, you are running an older CLI than this page describes;
use the lists above.

#### Grant access: two different identities

The mistake to avoid is treating this as one grant. Two distinct principals need two distinct
roles — one of them is you:

| Who | Role | Scope | Why |
| --- | --- | --- | --- |
| **You**, the person creating the secrets | `Key Vault Secrets Officer` | The vault | On an RBAC vault, you cannot write the secrets above without it |
| The cluster's **kubelet** identity | `Key Vault Secrets User` | The vault | This is how Studio reads the secrets at run time. It is **not** the cluster's control-plane identity — those are two different identities, and granting the wrong one leaves the install unable to read the vault |

On an RBAC vault there is no `get` access policy to grant. If you are looking for an
access-policy tab, the vault is in the wrong permission model.

**Do not grant the cluster's control-plane identity `Network Contributor` on the network.**
You may find that advice elsewhere, for letting the cluster create the private link itself.
Do not follow it here. One deployment tried that path: the grant was confirmed applied at the
exact subnet scope, and the cluster-driven path still failed for more than forty minutes. A
later deployment succeeded end to end **without making this grant at all**, because your
operator creates the private link directly, with their own credentials — a path that needs no
cluster permission on the network.

Granting it would leave a standing subscription-level privilege that nothing uses.

One exception for a person, not a machine: your operator needs the value of the
`bootstrap-key` secret specifically, to enter it into Studio's sign-in page the first time
your organisation is bootstrapped — see
[05-configure-org](05-configure-org.md#where-to-start-if-you-chose-kubernetes-on-azure).
Either grant your operator `Key Vault Secrets User` on that one secret so they can retrieve it
themselves, or read it out and hand it to them through your organisation's secret-handoff
channel. No other secret in this vault needs a person's own access.

Return the vault's URL as `KEY_VAULT_URL`.

### 4. Create the Front Door profile and settle the domain

Create an Azure Front Door profile on the **Premium** tier.

**Premium is mandatory, not a preference.** Studio's ingress inside the cluster is a private
load balancer with no public address. The only way Front Door can reach it is Azure Private
Link, and Private Link origins are not supported on the Standard tier. Standard is the
cheaper, more common default, and a Standard profile cannot serve Studio at all. Your operator
would discover this only at the last wiring step, after the cluster is built and billing.

If you have already created a Standard profile, you can upgrade it to Premium in place, with
no downtime. Note that the upgrade is one-way — Azure does not support downgrading Premium
back to Standard — and Premium bills at a higher base rate.

**Set the origin response timeout to 180 seconds when you create the profile.** The default is
30 seconds, and 30 is too short. The first time someone starts a conversation in Studio, the
platform cold-starts a container for them: clone, install, start, become ready, write
credentials. A real deployment measured that sequence at about **36 seconds** — so Front Door
cut the connection before it finished.

```
--origin-response-timeout-seconds 180
```

Set it at creation time. It can be changed later on an existing profile with
`az afd profile update`, but there is no reason to wait: the failure it causes appears at the
very last step of this whole guide, days after you finish, to a different person. The error
they see says a fetch failed and the caller disconnected — nothing that points back to Front
Door or to a timeout.

If you do end up deleting and recreating a profile, be aware that Front Door profile names
carry a subscription-wide cooldown after deletion, so the name you agreed with your team may
not be immediately reusable.

Create the profile and one endpoint on it. Wiring the origin to the cluster happens later,
after your operator runs the install and gets back a private address to point it at — that is
not part of this request. Your operator will need the private-link subnet from step 1 for it.

#### Choose the domain: two paths

| Path | What you do now | Cost |
| --- | --- | --- |
| **Front Door's own hostname** | Nothing extra. The endpoint you create gets a generated `*.azurefd.net` hostname. No certificate, no DNS record | The hostname is not pretty, and it does not exist until you create the endpoint |
| **A custom domain** | Add the domain to Front Door, issue a managed TLS certificate for it, and point that domain's DNS at Front Door | More work, and it must be agreed with your team before anyone starts |

Both paths are fully supported. Studio does not care which you use.

**If you choose Front Door's own hostname, create Front Door first — before steps 1 to 3.**
The hostname does not exist until the endpoint exists, and the administrators below cannot
start their work without it. This reverses the step order given at the top of this page, and
it is the only reason that order has an exception.

**Settle this domain name first, whichever path you chose.** Other administrators build URLs
from it and cannot finish their own request until they have it. Every one of these is a URL
the administrator must register on their side, and each rejects a request that arrives at an
unregistered address:

| Who | What they build from it | When it applies |
| --- | --- | --- |
| Entra administrator — [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md) | The SSO redirect URI | Always, on this deployment style |
| Entra administrator — [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md) | **Two** further redirect URIs — `/api/auth/fabric/callback` and `/api/v1/data-platforms/validation/callback` — on the app registration entered for the Fabric data platform | Only when your data platform is Microsoft Fabric |
| Entra administrator — [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md) | Two more — `/api/auth/secret-store-links/callback` and `/api/v1/secret-stores/validation/callback` — on the app registration entered for the secret store | Only when a domain will use Azure Key Vault as its secret store |
| GitHub organisation owner — [01c-prereqs-github-org-owner](01c-prereqs-github-org-owner.md) | The GitHub App's callback URL | Always, on this deployment style |

So the name must not be picked in isolation, and it must not change afterwards. Changing it
later means editing the registrations in every page above, and on the custom-domain path it
also means reissuing the certificate.

#### Before you tear any of this down

Note this now, because you are the only person who can do it and this is the only page
addressed to you. Once Studio is wired up, these resources must be deleted **in this order**:

1. The Front Door profile. On a Premium profile with a live private-link origin this takes
   15 to 20 minutes, and the delete command does not accept a confirmation flag — expect to
   poll for it.
2. The private-endpoint connection.
3. The private link service.
4. Only then the AKS cluster.

Deleting the cluster while the private link service still exists fails with
`CannotDeleteLoadBalancerWithPrivateLinkService`, because the cluster's internal load balancer
is still referenced. Also: a Front Door create that reports a conflict can still have created
a billing resource, so check for orphans before you retry.

### Values to send back

| Token | Comes from |
| --- | --- |
| `AKS_KUBECONFIG` | Step 1, the AKS cluster, plus the context name |
| `AKS_KUBELET_CLIENT_ID` | Step 1, the cluster's kubelet identity |
| `VNET_NAME` | Step 1, the virtual network and its resource group |
| `PRIVATE_LINK_SUBNET` | Step 1, the private-link subnet |
| `AZURE_FILES_SHARE_URL` | Step 2, the data share |
| `STORAGE_RESOURCE_GROUP` | Step 2, the storage account's resource group |
| `KEY_VAULT_URL` | Step 3, the Key Vault |
| `STUDIO_DOMAIN` | Step 4, the domain — either your custom domain or Front Door's own hostname |
| `FRONT_DOOR_PROFILE` | Step 4, the Front Door profile name, its resource group, and the endpoint name |

## Azure AI Foundry resource (needed on every combination)

Unlike the four requests above, this one applies no matter which deployment style or data
platform your team chose. Create an Azure AI Foundry resource, or nominate an existing one,
deploy a model to it, and hand back three values. Three details matter here — each one is a
real way this fails if it is missed:

1. **The endpoint must be host-only, with nothing after the domain.** Hand back exactly
   `https://<resource-name>.openai.azure.com` — no trailing path. Studio strips one trailing
   slash from whatever you give it and then appends its own request path; if the value
   already carries a path segment (for example, ending in `/openai`), Studio's appended path
   lands after that segment instead of at the root, and the request fails. Hand back the
   `openai.azure.com` host, not a `*.services.ai.azure.com` one. Microsoft documents
   `services.ai.azure.com` for the newer `/openai/v1/` route, which passes the deployment name
   in the request body and carries no `api-version`. Studio calls the older per-deployment
   route, `/openai/deployments/<name>/chat/completions?api-version=…`, and Microsoft documents
   that one against the `openai.azure.com` host.

   Find this value in the Azure portal, on the resource's **Keys and Endpoint** page, or in
   the Azure AI Foundry portal's **Deployments** view — both show the same endpoint.

   From `v0.1.33` this matters more than it did, because Studio can now call **two** different
   Azure paths off the endpoint you hand back — `/openai/deployments/<name>/chat/completions`
   or `/openai/responses`, both with an `api-version`. Your operator chooses between them with
   a new **API mode** setting. Both are appended to the bare host, so one host-only endpoint
   serves either choice, and a value carrying a path breaks both.

2. **Hand back the deployment name, not the model's family name.** Studio has one field for
   this ("Model"), and it expects the name you gave the deployment when you created it in
   Foundry — not the underlying model name. If you deployed `gpt-4o` under the deployment
   name `docs-gpt4o`, hand back `docs-gpt4o`. There is no separate deployment-name field.

3. **An API key is required.** Generate one for the resource and hand it back. Studio's
   Azure AI Foundry connection has no managed-identity or certificate option — an API key is
   the only credential it accepts.

### Values to send back

| Token | Comes from |
| --- | --- |
| `FOUNDRY_BASE_URL` | The Foundry resource's endpoint, host-only |
| `FOUNDRY_API_KEY` | An API key for the resource |
| `FOUNDRY_DEPLOYMENT_NAME` | The name of the deployment you created for the model |

## All values this page collects

| Token | Comes from | Needed when |
| --- | --- | --- |
| `AKS_KUBECONFIG` | Step 1, the AKS cluster, plus the context name | Kubernetes on Azure |
| `AKS_KUBELET_CLIENT_ID` | Step 1, the cluster's kubelet identity client ID | Kubernetes on Azure |
| `VNET_NAME` | Step 1, the virtual network and its resource group | Kubernetes on Azure |
| `PRIVATE_LINK_SUBNET` | Step 1, the private-link subnet | Kubernetes on Azure |
| `AZURE_FILES_SHARE_URL` | Step 2, the data share | Kubernetes on Azure |
| `STORAGE_RESOURCE_GROUP` | Step 2, the storage account's resource group | Kubernetes on Azure |
| `KEY_VAULT_URL` | Step 3, the Key Vault | Kubernetes on Azure |
| `bootstrap-key` | Step 3, the Key Vault secret of that name — retrieved by the operator directly, not sent back by you | Kubernetes on Azure |
| `STUDIO_DOMAIN` | Step 4, the domain — custom, or Front Door's own hostname | Kubernetes on Azure |
| `FRONT_DOOR_PROFILE` | Step 4, the profile name, its resource group, and the endpoint name | Kubernetes on Azure |
| `FOUNDRY_BASE_URL` | The Azure AI Foundry resource's endpoint | Every combination |
| `FOUNDRY_API_KEY` | An API key for that resource | Every combination |
| `FOUNDRY_DEPLOYMENT_NAME` | The deployed model's deployment name | Every combination |

## Where this goes

`AKS_KUBECONFIG`, `AZURE_FILES_SHARE_URL`, `STORAGE_RESOURCE_GROUP`, `KEY_VAULT_URL`, and
`AKS_KUBELET_CLIENT_ID` are entered by the operator when they run the Kubernetes install.
`VNET_NAME`, `PRIVATE_LINK_SUBNET`, and `FRONT_DOOR_PROFILE` are used by the operator in the
go-live wiring after the install — see
[04-deploy-kubernetes-azure](04-deploy-kubernetes-azure.md). The operator retrieves
`bootstrap-key` directly from the Key Vault and uses it to sign in and create the first
`vibedata_owner` — see [05-configure-org](05-configure-org.md). `STUDIO_DOMAIN` is used there
too, and also by your organisation's Entra administrator, to build the full Studio SSO
redirect URI — see [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md). `FOUNDRY_BASE_URL`,
`FOUNDRY_API_KEY`, and `FOUNDRY_DEPLOYMENT_NAME` are entered by the operator during
organisation setup, on every combination — see [05-configure-org](05-configure-org.md).
