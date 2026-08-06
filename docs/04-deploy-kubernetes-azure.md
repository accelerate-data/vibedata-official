---
applies-to: vibedata v0.1.26
verified-against: studio@653beeced
verified-on: 2026-08-05
sources:
  - docs/design/kubernetes-deployment/cloud.md
  - docs/design/kubernetes-deployment/README.md
  - docs/design/kubernetes-deployment/concepts.md
  - cli/vibedata/src/vibedata/main.py
  - cli/vibedata/src/vibedata/commands/install.py
  - cli/vibedata/src/vibedata/commands/install_kubernetes.py
  - cli/vibedata/src/vibedata/k8s/cluster.py
  - cli/vibedata/src/vibedata/k8s/providers.py
  - cli/vibedata/src/vibedata/k8s/render.py
---

# Deploy Studio: Kubernetes on Azure

This whole page is about `Kubernetes on Azure`. It applies the same way for all three data
platforms — `DuckDB`, `MotherDuck`, and `Microsoft Fabric` — so nothing here is scoped by
data platform. If you chose `Local Docker`, skip this page and use
[03-deploy-docker](03-deploy-docker.md) instead.

This continues from [02-prereqs-operator](02-prereqs-operator.md): you already have a
working `vibedata` binary, `kubectl`, and `helm` on this machine.

## Before you start: confirm the cluster infrastructure exists

`vibedata install kubernetes` creates no cloud resources of its own — it only talks to the
Kubernetes API of a cluster you already have, and to the Key Vault and Azure Files share
that cluster can already reach. Everything below needs to exist first. Full detail on each
item, including how to create it, is in
[01d-prereqs-azure-infra](01d-prereqs-azure-infra.md) — this is a checklist to confirm you
have it, not a repeat of that page.

- [ ] An AKS cluster, with Azure CNI powered by Cilium, NodeLocal DNSCache off, and
      dual-stack (IPv6) off. Access as a kubeconfig — `AKS_KUBECONFIG`.
- [ ] A premium Azure Files NFS v4.1 share for Studio's data, plus a second NFS share for
      backups. The data share's URL — `AZURE_FILES_SHARE_URL`.
- [ ] A Key Vault holding the fixed-name secrets `01d` lists, with the cluster's managed
      identity granted `get` access. The vault's URL — `KEY_VAULT_URL`.
- [ ] An Azure Front Door instance with a managed TLS certificate for your domain, and DNS
      pointed at Front Door. The domain — `STUDIO_DOMAIN`.

You can check the exact secret set your observability profile needs, without touching the
cluster or the vault, by running the same profile flag you plan to install with:

```bash
vibedata install kubernetes --list-secrets
vibedata install kubernetes --list-secrets --with-observability
vibedata install kubernetes --list-secrets --full-observability
```

The bare form reports the core set only. Add the profile flag matching your planned install
to see what that profile adds on top.

## Bring Studio up

Run:

```bash
vibedata install kubernetes
```

Azure is the only cloud this command supports today.

Run at a terminal with no flags, this prompts for whichever values you didn't pass: which
cluster to install into (see below), then Studio's domain, the storage share URL, and the
vault URL from `01d`. Answer those last three with `STUDIO_DOMAIN`, `AZURE_FILES_SHARE_URL`,
and `KEY_VAULT_URL`.

Running it non-interactively — no terminal attached, or scripted — skips every prompt, and
each value is required as a flag instead:

- `--domain` — `STUDIO_DOMAIN`
- `--storage-url` — `AZURE_FILES_SHARE_URL`
- `--vault-url` — `KEY_VAULT_URL`
- `--storage-resource-group` — only if your Azure infrastructure owner told you the storage
  account sits in a different resource group than the AKS cluster's own node resource group
  (see [01d-prereqs-azure-infra](01d-prereqs-azure-infra.md)). Leave it unset otherwise; this
  one is not part of the interactive prompt sequence above, so pass it as a flag if you need
  it.

**Which cluster it installs into** works differently depending on what you pass and whether
you're at a terminal:

- **`--kubeconfig <file>`** — that file is used.
- **`--kube-context <name>`** — that context is named explicitly; kubectl resolves which
  file holds it.
- **Neither, at a terminal** — the CLI prompts for the kubeconfig file (default
  `~/.kube/config`), then, only if that file holds more than one context, prompts again for
  which context to use, defaulting to the file's current context (or its first context, if
  none is current). You're asked, not guessed for.
- **Neither, non-interactive** — no prompt is possible. kubectl resolves **which file** to
  use, from `$KUBECONFIG`/its default path, but the CLI itself picks the **context**: the
  file's only context if it has one, otherwise its current context. If neither can be
  determined, the CLI passes nothing and kubectl fails loudly rather than choosing silently.
  This is the case to be careful about in CI or any scripted run — what you get depends on
  the contents of whichever kubeconfig the environment happens to supply, so name
  `--kubeconfig` or `--kube-context` explicitly instead.

This installs into your cluster:

- **External Secrets Operator**, pointed at your Key Vault, to sync the secrets above into
  the cluster as Kubernetes Secrets.
- **ingress-nginx**, exposed through a **private** (internal) load balancer — not reachable
  from the open internet.
- **Argo CD**.

It then registers Studio as an Argo CD application and waits for Argo to report it healthy.

## The chart

Argo pulls Studio from the public OCI registry:

```
oci://ghcr.io/accelerate-data/studio-charts/studio
```

version `0.1.26` — observed at digest
`sha256:4a050dc31a1f2bc8cb27a274425e763980a30a920a400c3288d7cd1c507b650d` as of this page's
stamp date. A republish of the same version can move the digest, so treat the version
number as the durable identity and the digest as a point-in-time observation, not a pin.
The pull is anonymous — no registry credentials needed.

**Watch the tag prefix.** The chart is tagged `0.1.26`, with no `v`. Studio's images and the
`vibedata` CLI itself are tagged `v0.1.26`, with the `v`. The chart's own `Chart.yaml`
carries both forms side by side — `version: 0.1.26` and `appVersion: v0.1.26` — which is a
clean illustration of the difference. Copy the `v` prefix into a chart pull and it fails.

**Chart defaults are not what you get, for scheme and host.** The chart's own default values
target a local install (`scheme: http`, `host: studio.localhost`), and the CLI overrides
both for this deployment style, setting the scheme to `https` and the host to your
`STUDIO_DOMAIN` (`cli/vibedata/src/vibedata/k8s/render.py:528,531`). Authentication is
different: the published chart already defaults `auth.enabled` to `true`, and the CLI pins
the same value again explicitly on top of that default
(`cli/vibedata/src/vibedata/k8s/render.py:532`). Two independent things would have to
change for a `Kubernetes on Azure` install to run unauthenticated, and neither does — every
install here runs with delegated authentication on. The cluster boots in bootstrap mode;
the first admin is created using the `bootstrap-key` secret from your Key Vault (see `01d`'s
secret table). Setting up sign-in for the rest of your organisation is covered in
[05-configure-org](05-configure-org.md).

Studio's durable data lives on the in-cluster `/data` path, mounted from the Azure Files
share `01d` created (`AZURE_FILES_SHARE_URL`) — the pulled chart mounts it into the backend
and every agent pod. This is a different thing from the `DATA_DIR` directory
[02-prereqs-operator](02-prereqs-operator.md) describes on your own machine: on this
deployment style, that directory holds only your local CLI credential, never Studio's data.

## Go live: Front Door, origin, DNS

`01d` already created your Front Door instance with its managed certificate, and pointed
DNS at Front Door. Once the install finishes, confirm both are in place and do the one
piece of wiring that is new here, in order:

1. Confirm your domain and its managed certificate are set on Front Door — from `01d`.
2. **Point Front Door's origin at the private ingress address the install just created.**
   This is the step this page adds.
3. Confirm DNS is pointed at Front Door — also from `01d`.

The certificate itself never enters the cluster — Front Door terminates TLS and forwards
plain traffic to the private ingress inside.

## Keep the health probe on `/healthz`

Keep the in-cluster ingress private — only Front Door should reach it. Point the load
balancer's health probe at `/healthz`, not whatever path the cloud defaults to.

The default probe path is `/`, and ingress-nginx answers that with a 404. A load balancer
that reads this as unhealthy marks every node down and silently stops sending traffic
through it — nothing crashes, requests just stop arriving. `/healthz` is ingress-nginx's own
health endpoint, and it's the one that actually reports controller health.

**You cannot verify this from inside the cluster.** A pod-local `curl` to the load
balancer's address is short-circuited straight to a backend pod by `kube-proxy` and returns
200 regardless of which path the probe is actually configured to use. Check the load
balancer's own backend-health metric, or test from a genuinely external client. If traffic
still doesn't reach the cluster after this, see
[90-troubleshooting](90-troubleshooting.md).

## Optional: verify image signatures with Kyverno

Studio's images are signed keyless at release time — there is no public key to distribute;
the policy instead checks the signing certificate's identity and the OIDC issuer that issued
it. Applying this policy is optional:

> Enforcement is opt-in: skip it and Studio still runs — it just isn't actively blocking
> fakes. Signing and pinning are always on regardless.

If you want it, install Kyverno — **version 1.13 or later**, because the policy uses a
per-rule `failureAction` that older Kyverno does not support — then apply the bundled
policy:

```bash
kubectl apply -f https://raw.githubusercontent.com/accelerate-data/vibedata-official/main/docs/security/kyverno-verify-studio-images.yaml
```

Your cluster's nodes need to reach the public sigstore services — Fulcio, Rekor, and the
TUF root — to verify keyless signatures. An air-gapped cluster needs a mirrored sigstore
trust root instead.

**This policy does not cover everything in the namespace.** Third-party images — Obot,
PostgreSQL — don't match the policy's image references, so it lets them through unverified,
by design.

## What's next

Multi-user sign-in — Entra SSO, and the rest of your organisation's users and roles — is
configured after Studio is running, in [05-configure-org](05-configure-org.md).
