# Request for your Azure infrastructure owner

> **Applies to: Kubernetes on Azure.** Skip for Local Docker.

The `vibedata` installer deploys Studio into an **existing** AKS environment. It does not provision the Azure estate for you.

## Azure resources to provide

Prepare:

- an AKS cluster;
- an Azure Files NFS share for Studio durable data;
- a separate backup share;
- an Azure Key Vault;
- an Azure identity that the cluster can use to read Key Vault secrets;
- DNS and HTTPS ingress in front of the cluster;
- enough node capacity for Studio and the selected observability profile.

The current installer supports `--cloud azure`. AWS and GCP providers are not implemented in the executable CLI at this SHA.

## AKS sizing

Current Studio documentation uses two `Standard_D2s_v3`-class nodes as a practical baseline for core Studio and the lighter observability profile. Full observability needs more headroom; plan for at least about 8 vCPU total, such as two `D4s_v3`-class nodes.

These are starting points, not hard product minimums. Activated Intents create additional runtime workload, so size for expected concurrency.

## Storage

Studio's shared data volume uses **Azure Files NFS v4.1**, not SMB, in the current Kubernetes design.

Provide:

1. the primary Studio file share;
2. a separate backup share.

Return the storage URL and, when the share is outside the AKS node resource group, its storage resource group. The installer converts this into the Azure Files CSI configuration.

Do not put the backup inside the same logical data path it protects.

## Key Vault

Create the vault before running the installer. The exact secret set depends on the observability profile.

Get the authoritative current list from the same `vibedata` binary you will install with:

```bash
vibedata install kubernetes --cloud azure --list-secrets
vibedata install kubernetes --cloud azure --list-secrets --with-observability
vibedata install kubernetes --cloud azure --list-secrets --full-observability
```

For the core profile at this SHA, the rendered install expects these names:

```text
pg-password
auth-secret
data-encryption-key
data-encryption-key-id
data-encryption-retired-keys
obot-client-secret
obot-db-password
obot-tunnel-peer-token
bootstrap-key
```

Use the formats required by the installer. In particular, the data-encryption key is key material, not an arbitrary password. Keep the key identifier and retired-key map as separate values because upgrades and restores depend on them.

`--list-secrets` is more authoritative than this page if the two ever differ.

## Cluster identity and Key Vault access

External Secrets Operator reads the vault. Give the cluster identity used by that path permission to read the required Key Vault secrets, normally through the **Key Vault Secrets User** role or your equivalent least-privilege policy.

If the cluster has more than one candidate identity, return the correct client ID so the installer can use:

```text
--vault-identity-client-id <client-id>
```

## Public ingress and Azure Front Door

Studio needs a stable HTTPS origin for delegated browser authentication and companion-app OAuth.

The current Azure deployment guidance supports two Front Door patterns:

- **Front Door Standard** with a public ingress address restricted so only Azure Front Door can reach it. This is the normal lower-cost path.
- **Front Door Premium + Private Link** when the origin must have no public reachability.

Do not assume Premium/Private Link is mandatory.

For Front Door, configure a long enough origin response timeout for Studio's long-lived requests; the current deployment guide uses **240 seconds**.

Return the final Studio DNS name, for example:

```text
studio.example.com
```

The operator passes this as `--domain` to the installer. SSO and downstream OAuth registrations should use the same public origin when Studio displays their callback URLs.

## Kubeconfig

Return either:

- a kubeconfig path and context, or
- a context already present in the operator's normal kubeconfig.

The installer checks both `kubectl` and `helm`, verifies cluster reachability, and uses the selected context for every action.

## What the installer creates in the cluster

Current `vibedata install kubernetes` installs and manages:

- the Studio namespace;
- External Secrets Operator integration;
- ingress-nginx;
- Argo CD;
- the Studio Argo application;
- `studio-obot`;
- optional LGTM and Langfuse applications based on the profile.

Install success requires the enabled companion applications to become healthy. A healthy `studio-app` alone is no longer sufficient.

## Values to send back

Give the operator:

| Value | Installer option |
| --- | --- |
| Kubeconfig path | `--kubeconfig` |
| Kube context | `--kube-context` |
| Public Studio domain | `--domain` |
| Azure Files share URL | `--storage-url` |
| Key Vault URL | `--vault-url` |
| Vault identity client ID, when needed | `--vault-identity-client-id` |
| Storage resource group, when needed | `--storage-resource-group` |

The normal install then looks like:

```bash
vibedata install kubernetes \
  --cloud azure \
  --kubeconfig <path> \
  --kube-context <context> \
  --domain studio.example.com \
  --storage-url <azure-files-url> \
  --vault-url https://<vault>.vault.azure.net \
  --vault-identity-client-id <client-id> \
  --storage-resource-group <resource-group>
```

Add exactly one observability choice when required: `--with-observability`, `--full-observability`, or `--no-observability` when explicitly removing it.

Design documents in `studio/main` also describe a future declarative installation configuration. That is not the current CLI contract. Use the flags above for this snapshot.

---

_Applies to: studio/main (unreleased snapshot). Verified against `studio@5c9d2bbf339a` on 2026-08-22._
