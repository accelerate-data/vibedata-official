---
applies-to: vibedata v0.1.26
verified-against: studio@653beeced
verified-on: 2026-08-05
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
  connection in [05-configure-org](05-configure-org.md), and Azure AI Foundry is the LLM
  provider Studio implements.

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

**The one hard dependency below:** create the AKS cluster (step 1) before granting its
identity access to the Key Vault (part of step 3) — that grant needs the cluster's own
identity to already exist. Otherwise, do these four in whatever order is convenient; none of
the others depends on one that comes before it.

### 1. Create the AKS cluster

Create an AKS cluster sized to run Studio and its agent workloads — node count and size are
your call. Studio ships a default-deny network policy that isolates each agent pod from the
others and from the database; enforcing it needs a CNI that actually implements Kubernetes
NetworkPolicy. On AKS, choose **Azure CNI powered by Cilium** — the plain Azure Network
Policy Manager has known gaps in a rule construct this policy depends on, so the isolation
would silently fail to take effect on it.

Two more settings on this same cluster, both silent failures if you get them wrong — no
later page in this doc set can fix a cluster's network configuration after the fact, so this
is the point to get them right:

- **Do not enable NodeLocal DNSCache.** Agents resolve through a link-local host resolver
  that this network policy's DNS rule cannot select — they lose DNS entirely, not just the
  policy's enforcement.
- **Do not enable dual-stack (IPv6) networking.** The policy has no IPv6 allow rule, so IPv6
  egress from agent pods is fail-closed.

Return access to the cluster as a kubeconfig: `AKS_KUBECONFIG`.

### 2. Create two Azure Files shares

Create a **premium** Azure Files storage account with an **NFS v4.1** share for Studio's
shared data directory, and a second NFS share in the same storage account for backups. NFS,
not the default SMB — Studio's agent pods run `git` on this share, and SMB's file locking
does not support what git needs.

Return the data share's URL as `AZURE_FILES_SHARE_URL`, in the exact form
`https://<storage-account>.file.core.windows.net/<share-name>` — the installer parses that
specific shape. If the storage account sits in a different resource group than the AKS
cluster's own node resource group, also tell your operator that resource group's name; the
installer takes it as a separate input.

The backup share does not go through this page's values table. Your operator points to it
directly, later, whenever a backup is run — it is never given to the installer.

### 3. Create a Key Vault and load the fixed-name secrets

Create an Azure Key Vault, or nominate an existing one. Studio's installer reads these exact
secret names from it — spelled exactly as shown, nothing substitutable:

| Secret name | What it holds |
| --- | --- |
| `pg-password` | Password for the in-cluster Postgres |
| `auth-secret` | Studio's session-signing secret |
| `data-encryption-key` | The active data-encryption key |
| `data-encryption-key-id` | ID of the active data-encryption key |
| `data-encryption-retired-keys` | Retired data-encryption keys, kept so old data can still be decrypted |
| `obot-client-secret` | OAuth client secret for Studio's bundled agent runtime (obot) |
| `obot-db-password` | Password for obot's own database |
| `obot-tunnel-peer-token` | Shared token obot's replicas use to authenticate to each other |
| `bootstrap-key` | One-time key used to create the first Studio admin |

Whoever picks the values for `pg-password` and `obot-db-password`: both get pasted directly
into a Postgres connection string with no escaping, so avoid the characters `@ : / # ? &` in
either one — a plain hex string is a safe choice.

**No share-key secret is needed.** The NFS v4.1 share from step 2 mounts key-free, over the
network — Studio never reads a storage key from this vault on Azure.

**If your operator turns on optional monitoring**, the vault needs additional secrets, on
top of the nine above:

- `--with-observability` adds: `grafana-client-secret` · `grafana-admin-password`
- `--full-observability` (the same monitoring stack, plus Langfuse) adds those two, plus:
  `langfuse-salt` · `langfuse-nextauth-secret` · `langfuse-encryption-key` ·
  `langfuse-client-secret` · `langfuse-clickhouse-password` · `langfuse-redis-password` ·
  `langfuse-minio-password` · `langfuse-init-project-public-key` ·
  `langfuse-init-project-secret-key`

Confirm this list before creating it: ask your operator to run
`vibedata install kubernetes --list-secrets` — a read-only command that touches nothing in
the cluster or the vault — for the exact set their chosen profile needs.

Grant the AKS cluster's own managed identity **read (`get`)** access to the vault's secrets —
that is how the cluster reads them. One exception: your operator needs the value of the
`bootstrap-key` secret specifically, to enter it into Studio's sign-in page the first time
your organisation is bootstrapped — see
[05-configure-org](05-configure-org.md#where-to-start-if-you-chose-kubernetes-on-azure).
Either grant your operator `get` access to that one secret so they can retrieve it
themselves, or read it out and hand it to them through your organisation's secret-handoff
channel. No other secret in this vault needs a person's own access.

Return the vault's URL as `KEY_VAULT_URL`.

### 4. Put a managed HTTPS front door and DNS in front of the cluster

Create an Azure Front Door instance with a managed TLS certificate for the domain your team
will use for Studio (for example `studio.acme.com`), and point that domain's DNS at Front
Door.

Wiring Front Door's origin to the cluster happens later, after your operator runs the
install and gets back a private address to point it at — that is not part of this request.
Your job here is to have Front Door, the certificate, and DNS ready, with the domain name
agreed with your Studio operator — the same domain name is also needed by your Entra
administrator, to build the SSO redirect URI in
[01a-prereqs-entra-admin](01a-prereqs-entra-admin.md), so it must not be picked in
isolation.

Return the domain as `STUDIO_DOMAIN`.

### Values to send back

| Token | Comes from |
| --- | --- |
| `AKS_KUBECONFIG` | Step 1, the AKS cluster |
| `AZURE_FILES_SHARE_URL` | Step 2, the data share |
| `KEY_VAULT_URL` | Step 3, the Key Vault |
| `STUDIO_DOMAIN` | Step 4, the domain pointed at Front Door |

## Azure AI Foundry resource (needed on every combination)

Unlike the four requests above, this one applies no matter which deployment style or data
platform your team chose. Create an Azure AI Foundry resource, or nominate an existing one,
deploy a model to it, and hand back three values. Three details matter here — each one is a
real way this fails if it is missed:

1. **The endpoint must be host-only, with nothing after the domain.** Hand back exactly
   `https://<resource-name>.openai.azure.com` — no trailing path. Studio strips one trailing
   slash from whatever you give it and then appends its own request path; if the value
   already carries a path segment (for example, ending in `/openai`), Studio's appended path
   lands after that segment instead of at the root, and the request fails. Do not hand back
   a `*.services.ai.azure.com` endpoint either — that is a different Foundry API surface with
   a different request shape than the one Studio calls.

   Find this value in the Azure portal, on the resource's **Keys and Endpoint** page, or in
   the Azure AI Foundry portal's **Deployments** view — both show the same endpoint.

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
| `AKS_KUBECONFIG` | Step 1, the AKS cluster | Kubernetes on Azure |
| `AZURE_FILES_SHARE_URL` | Step 2, the data share | Kubernetes on Azure |
| `KEY_VAULT_URL` | Step 3, the Key Vault | Kubernetes on Azure |
| `bootstrap-key` | Step 3, the Key Vault secret of that name — retrieved by the operator directly, not sent back by you | Kubernetes on Azure |
| `STUDIO_DOMAIN` | Step 4, the domain pointed at Front Door | Kubernetes on Azure |
| `FOUNDRY_BASE_URL` | The Azure AI Foundry resource's endpoint | Every combination |
| `FOUNDRY_API_KEY` | An API key for that resource | Every combination |
| `FOUNDRY_DEPLOYMENT_NAME` | The deployed model's deployment name | Every combination |

## Where this goes

`AKS_KUBECONFIG`, `AZURE_FILES_SHARE_URL`, and `KEY_VAULT_URL` are entered by the operator
when they run the Kubernetes install — see
[04-deploy-kubernetes-azure](04-deploy-kubernetes-azure.md). The operator retrieves
`bootstrap-key` directly from the Key Vault and uses it to sign in and create the first
`vibedata_owner` — see [05-configure-org](05-configure-org.md). `STUDIO_DOMAIN` is used there
too, and also by your organisation's Entra administrator, to build the full Studio SSO
redirect URI — see [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md). `FOUNDRY_BASE_URL`,
`FOUNDRY_API_KEY`, and `FOUNDRY_DEPLOYMENT_NAME` are entered by the operator during
organisation setup, on every combination — see [05-configure-org](05-configure-org.md).
