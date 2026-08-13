---
applies-to: vibedata v0.1.33
verified-against: studio@a121fc466
verified-on: 2026-08-13
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

- [ ] A virtual network your Azure owner created, with a **node subnet** carrying a
      `Microsoft.Storage` service endpoint and a separate **private-link subnet** with both
      private-endpoint and private-link-service network policies disabled. The names —
      `VNET_NAME` and `PRIVATE_LINK_SUBNET`.
- [ ] An AKS cluster on the node subnet, with Azure CNI powered by Cilium, NodeLocal DNSCache
      off, and dual-stack (IPv6) off. Access as a kubeconfig — `AKS_KUBECONFIG`.
- [ ] Enough cluster capacity for the profile you plan to install. 8 vCPU is **not** enough
      for `--full-observability`; plan for at least 10. Check that the subscription's regional
      vCPU quota leaves room for one more node — if it does not, you cannot add capacity
      yourself and must go back to your Azure owner.
- [ ] The client ID of the cluster's **kubelet** identity — `AKS_KUBELET_CLIENT_ID`. You pass
      this to the installer. Without it the install cannot read the vault.
- [ ] A premium Azure Files NFS v4.1 share for Studio's data, plus a second NFS share for
      backups, with encryption in transit **off** and the account locked to the node subnet.
      The data share's URL — `AZURE_FILES_SHARE_URL` — and its resource group,
      `STORAGE_RESOURCE_GROUP`.
- [ ] A Key Vault holding the fixed-name secrets `01d` lists, with the cluster's **kubelet**
      identity granted `Key Vault Secrets User`. The vault's URL — `KEY_VAULT_URL`.
- [ ] An Azure Front Door profile on the **Premium** tier. Standard cannot reach a private
      cluster — Private Link origins are Premium-only. Check the tier before you start; if it
      is Standard, your Azure owner can upgrade it in place. The profile name, its resource
      group, and the endpoint name — `FRONT_DOOR_PROFILE`. The domain — `STUDIO_DOMAIN`,
      either a custom domain with a managed certificate and DNS, or Front Door's own
      generated `*.azurefd.net` hostname.

**Count the secrets in the vault before you start.** The set depends on the monitoring profile
you install with:

| Profile | Secrets, on `v0.1.33` |
| --- | --- |
| Core (no flag, or `--no-observability`) | 9 |
| `--with-observability` | 11 |
| `--full-observability` | 21 |

`01d` lists every name and its required value format. Check the formats, not just the names —
`data-encryption-key` must be base64-encoded 32 random bytes, and a hex value is the most
common cause of a failed install on this page.

**Ask the CLI rather than trusting the table.** From `v0.1.32` the installer prints the exact
set and exits without touching anything:

```bash
vibedata install kubernetes --list-secrets --full-observability
```

The list is derived from the manifests the install actually renders, so it cannot drift. The
counts above came from running it against the released `v0.1.33` binary. On `v0.1.26` the flag
does not exist and answers `No such option: --list-secrets`; use `01d`'s tables there.

## Bring Studio up

This is the full command. Every flag in it is needed; the sections below explain each one.

```bash
vibedata install kubernetes \
  --cloud azure \
  --kube-context <your-context> \
  --domain "$STUDIO_DOMAIN" \
  --storage-url "$AZURE_FILES_SHARE_URL" \
  --vault-url "$KEY_VAULT_URL" \
  --vault-identity-client-id "$AKS_KUBELET_CLIENT_ID" \
  --version 0.1.33
```

Azure is the only cloud this command supports today.

**This runs unattended on `v0.1.33`.** With `--kube-context` given, the command asks nothing —
it was checked with stdin closed and went straight to the cluster check. So it is safe in a
script, a pipeline, or CI.

> **Applies to: releases before v0.1.32.** Earlier releases opened a
> `Cluster (kubeconfig) [~/.kube/config]:` prompt even when `--kube-context` was passed, and
> with stdin closed the prompt read end-of-file and **aborted** the command. The workaround was
> to pipe a newline — `yes '' | vibedata install kubernetes …` — which answered the prompt with
> its own default. Harmless to keep, and unnecessary from `v0.1.32`.

**`--vault-identity-client-id` is not optional.** It carries `AKS_KUBELET_CLIENT_ID` from
`01d`. This flag chooses how Studio authenticates to the Key Vault. Pass it and Studio uses
the cluster's managed identity, which is what `01d` set up. Leave it out and Studio silently
switches to workload identity, which needs an OIDC issuer, a federated credential and an
annotated service account that nobody created — the install then fails at the vault step, with
an error pointing at the vault rather than at the missing flag.

**`--version` pins the chart.** Without it, Argo tracks an open-ended version range and will
upgrade your cluster to any newer chart Accelerate Data publishes, including a new major
version, with no action from you. See [The chart](#the-chart) below.

The remaining values:

| Flag | Value from `01d` |
| --- | --- |
| `--domain` | `STUDIO_DOMAIN` |
| `--storage-url` | `AZURE_FILES_SHARE_URL` |
| `--vault-url` | `KEY_VAULT_URL` |
| `--storage-resource-group` | `STORAGE_RESOURCE_GROUP`, if the installer asks for it. It has no prompt, so pass it as a flag |

### Choose the monitoring profile at install time

The profile is set by a flag on **this** command, not later:

- no flag, or `--no-observability` — core Studio only.
- `--with-observability` — adds Grafana and the metrics collector.
- `--full-observability` — adds those plus Langfuse.

The profile must match the secrets in your vault. Changing it afterwards means re-running the
install with a different flag.

### Which cluster it installs into

- **`--kube-context <name>`** — the context is named explicitly and kubectl resolves which
  file holds it. From `v0.1.32` nothing else is asked; on earlier releases you were prompted
  for the kubeconfig file first, which is why older copies of this page piped a newline in.
- **`--kubeconfig <file>`** — that file is used.
- **Neither, at a terminal** — the CLI prompts for the kubeconfig file (default
  `~/.kube/config`), then, only if that file holds more than one context, prompts again for
  which context to use, defaulting to the file's current context (or its first context, if
  none is current).
- **Neither, in a script** — you cannot rely on this. Name `--kube-context` or `--kubeconfig`
  explicitly. Without one, what you install into depends on whichever kubeconfig the
  environment happens to supply.

### If the install stops with `READINESS_FAILED`

The installer waits for Argo CD to report Studio healthy, and gives up after **600 seconds**
by default. `--timeout <seconds>` changes that.

Hitting the timeout is not a broken cluster. It usually means one component is still starting,
or one vault secret has a bad value. **Re-running the whole command is the intended recovery.**
Every step is idempotent: it skips what is already in place and continues from where it
stopped. A real install hit this timeout once, was fixed by correcting one secret, and
completed on a plain re-run of the same command.

If the same timeout repeats, check in this order:

1. `kubectl -n studio get pods` — anything in `CrashLoopBackOff` names the failing component.
2. The backend pod's log. A `ZodError` there names a vault secret whose **value format** is
   wrong. `data-encryption-key` in hex instead of base64 is the usual one.
3. `kubectl -n studio get events` for `Insufficient cpu`. That is a capacity problem, not a
   configuration problem — see the capacity item in the checklist above.

Then see [90-troubleshooting](90-troubleshooting.md).

### What the install puts in your cluster

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

version `0.1.33` — observed at digest
`sha256:87e502699651d0102537cf1647a66f12dc78149569dc3ad19481b952972bccc4` as of this page's
stamp date. A republish of the same version can move the digest, so treat the version
number as the durable identity and the digest as a point-in-time observation, not a pin.
The pull is anonymous — no registry credentials needed.

**Without `--version`, Argo does not stay on the version you installed.** The installer hands
Argo an open-ended range — "0.1.33 or newer" — rather than a fixed version. Argo then upgrades
the cluster to any newer chart Accelerate Data publishes, on its own schedule, with no
operator action and across major versions. Passing `--version 0.1.33` collapses that range to
a single pinned version, which is why the install command above includes it. To move to a new
version afterwards, re-run the install with the new `--version`.

**Watch the tag prefix.** The chart is tagged `0.1.33`, with no `v`. Studio's images and the
`vibedata` CLI itself are tagged `v0.1.33`, with the `v`. The chart's own `Chart.yaml`
carries both forms side by side — `version: 0.1.33` and `appVersion: v0.1.33` — which is a
clean illustration of the difference. Copy the `v` prefix into a chart pull and it fails.

**Not every release publishes a chart.** The registry holds `0.1.25`, `0.1.26`, `0.1.32` and
`0.1.33` — there is no chart for `0.1.27` through `0.1.31`. So a `--version` taken from a CLI
release number will not always resolve. Check the tag list before pinning a version this page
does not name.

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
share `01d` created (`AZURE_FILES_SHARE_URL`). The backend mounts it, and the agent pods
Studio creates at run time share the same volume. This is a different thing from the
`DATA_DIR` directory [02-prereqs-operator](02-prereqs-operator.md) describes on your own
machine: on this deployment style, that directory holds only your local CLI credential, never
Studio's data.

## What a finished install looks like

The command ends by printing a block like this:

```
Studio is installed. Finish going live:
  Studio URL      https://<STUDIO_DOMAIN>   (after the steps below)
  Private ingress <private-ingress-address>   ← point your HTTPS edge origin here
  Bootstrap key   in your vault: 'bootstrap-key' (use once at /login)
  Grafana         https://<STUDIO_DOMAIN>/grafana/   (sign in with Studio)
  Alloy UI        https://<STUDIO_DOMAIN>/alloy/     (collector debug)
  Langfuse        https://<STUDIO_DOMAIN>/langfuse   (sign in with Studio)
```

The Grafana, Alloy and Langfuse lines appear only for the monitoring profile you installed.
They are subpaths of the same domain, so none of them work until the go-live wiring below is
finished.

**Write down the private ingress address.** It is the one value the whole next section needs,
and the installer prints it only once.

**One Argo CD application reports `Degraded` on a correct install.** Check the applications:

```bash
kubectl -n argocd get applications
```

On `v0.1.33`, `studio-app` and the monitoring applications report `Healthy`, and
**`studio-obot` should reach `Healthy` on `v0.1.33`.** Earlier releases could not: they never
rendered the object obot's tunnel configuration reads, so obot logged
`invalid tunnel peer configuration: ... missing ID, Token` and sat `Degraded`. That was fixed at
`v0.1.31`, and the vault secret it needs is now part of the core set rather than an extra.

If `studio-obot` is `Degraded`, check the object exists and that its secret synced:

```
kubectl -n studio get externalsecret obot-tunnel-peer
kubectl -n studio get secret obot-tunnel-peer
```

On `v0.1.33` the ExternalSecret is always rendered, so `NotFound` here means something went
wrong with the install rather than a missing feature. A `SecretSyncedError` instead points at
the vault: confirm `obot-tunnel-peer-token` exists there — it is one of the nine core secrets in
[01d](01d-prereqs-azure-infra.md), and a vault built against an older copy of that page will not
have it.

**Do not treat a Degraded `studio-obot` as cosmetic.** The installer's health gate waits only on
`studio-app`, so the install reports success either way, and **starting a conversation on an
activated intent will fail** later, at the last step of this guide.

> **Applies to: releases before v0.1.31.** On `v0.1.26` through `v0.1.30`, `kubectl -n studio get
> externalsecret obot-tunnel-peer` is **always** `NotFound` and nothing fixes it from the outside:
> the vault secret has no consumer, and re-running the install or rebuilding the cluster does not
> create the object. Upgrading is the fix. See
> [90-troubleshooting](90-troubleshooting.md) for the manual workaround and its cost.

## Go live: wire Front Door to the private ingress

Studio's ingress is a **private** load balancer with no public address. Front Door reaches it
over Azure Private Link. That is a sequence of six steps, in this order. Skipping or reordering
them produces a site that returns nothing, with no error anywhere.

You need these values from `01d`: `FRONT_DOOR_PROFILE` (profile name, resource group, endpoint
name), `VNET_NAME`, `PRIVATE_LINK_SUBNET`, and `STUDIO_DOMAIN`. Plus the private ingress
address the install just printed.

### Step 1 — Point the load balancer health probe at `/healthz`

Do this **first**, before creating anything in Front Door.

```bash
kubectl -n ingress-nginx annotate svc ingress-nginx-controller \
  service.beta.kubernetes.io/azure-load-balancer-health-probe-request-path=/healthz
```

The Azure load balancer defaults its probe path to `/`, and ingress-nginx answers `/` with a
404. Every node then reads as unhealthy and the load balancer **silently drops all inbound
traffic**. Nothing crashes; requests just never arrive.

**From `v0.1.32` the installer sets this for you.** `k8s/providers.py:110` applies
`service.beta.kubernetes.io/azure-load-balancer-health-probe-request-path: /healthz` to the
ingress service, so a fresh `v0.1.33` install arrives with it already correct.

Confirm it rather than assuming, because it is cheap and the failure is silent — and because an
**upgraded** cluster is not covered by that: releases `v0.1.26` through `v0.1.31` set no
annotation, so a cluster first installed on one of them keeps whatever it has until something
reapplies the service:

```bash
kubectl -n ingress-nginx get svc ingress-nginx-controller \
  -o jsonpath='{.metadata.annotations}'
```

Editing the probe in the Azure portal does not work — the cloud provider rebuilds the load
balancer from the Kubernetes Service and reverts it. The annotation is the only durable way.

**Day-2 warning.** This annotation lives on the live Service object, not in ingress-nginx's
Helm values. If ingress-nginx is ever upgraded or redeployed with Helm, the annotation is lost
and the whole deployment goes silently offline again. Re-apply it after any such upgrade, or
pin it into `controller.service.annotations`.

**You cannot verify the probe from inside the cluster.** A pod-local `curl` to the load
balancer's address is short-circuited straight to a backend pod by `kube-proxy` and returns
200 regardless of the probe path. Check the load balancer's own backend-health metric, or test
from a genuinely external client.

### Step 2 — Create a Private Link Service against the internal load balancer

```bash
az network private-link-service create \
  --resource-group <rg> --name <pls-name> \
  --vnet-name "$VNET_NAME" --subnet "$PRIVATE_LINK_SUBNET" \
  --lb-frontend-ip-configs <frontend-ip-config-id-of-kubernetes-internal-lb> \
  --location <region>
```

The frontend IP configuration belongs to the `kubernetes-internal` load balancer, which AKS
created in the cluster's own generated node resource group — not the resource group you
created the cluster in.

**Do not use the `azure-pls-create` Kubernetes annotation instead.** It is the obvious
Kubernetes-native path and it does not work: a real attempt failed with `AuthorizationFailed`
for more than 40 minutes with correct permissions confirmed at the exact subnet scope, and
never succeeded. Creating the service directly with `az`, as above, works on the first try.

### Step 3 — Create the origin group with a `/healthz` probe

```bash
az afd origin-group create \
  --resource-group <rg> --profile-name <fd-profile> --origin-group-name studio-og \
  --probe-request-type GET --probe-protocol Http --probe-path /healthz \
  --probe-interval-in-seconds 100 --sample-size 4 --successful-samples-required 3 \
  --additional-latency-in-milliseconds 50
```

Front Door's own default probe path is also `/`, which is also a 404. Without `--probe-path
/healthz` the origin sits at 0% health and never serves traffic.

### Step 4 — Create the origin

```bash
az afd origin create \
  --resource-group <rg> --profile-name <fd-profile> --origin-group-name studio-og \
  --origin-name studio-ingress \
  --host-name <private-ingress-address> \
  --origin-host-header "$STUDIO_DOMAIN" \
  --http-port 80 --https-port 443 --priority 1 --weight 1000 --enabled-state Enabled \
  --enforce-certificate-name-check true \
  --shared-private-link-resource '{"private-link":{"id":"<private-link-service-resource-id>"},"private-link-location":"<region>","request-message":"studio ingress"}'
```

Two flags here are traps:

- **`--host-name` and `--origin-host-header` must be different.** `--host-name` is the private
  IP address Front Door connects to. `--origin-host-header` is the HTTP `Host` header it
  sends, and Studio's ingress rule matches on the domain. Setting both to the IP address
  produces a bare nginx 404 on every request — while Front Door's origin health and the load
  balancer's backend health both read 100%, because `/healthz` is not host-matched. This
  exact mistake cost a real deployment ten minutes of debugging against green metrics.
- **`--enforce-certificate-name-check true` is required**, even though the route below
  forwards plain HTTP. Azure rejects `false` outright with
  `EnforceCertificateNameCheck must be enabled for Private Link`.

### Step 5 — Create the route

```bash
az afd route create \
  --resource-group <rg> --profile-name <fd-profile> --endpoint-name <fd-endpoint> \
  --route-name studio-route --origin-group studio-og \
  --supported-protocols Http Https --forwarding-protocol HttpOnly \
  --https-redirect Enabled --link-to-default-domain Enabled
```

Use `--link-to-default-domain Enabled` if `STUDIO_DOMAIN` is Front Door's own generated
hostname. If you have a custom domain, link the route to that custom domain instead.

The TLS certificate never enters the cluster. Front Door terminates TLS and forwards plain
HTTP to the private ingress, which is why `--forwarding-protocol HttpOnly` is correct here.

### Step 6 — Approve the private endpoint connection

```bash
az network private-endpoint-connection approve \
  --id <private-link-service>/privateEndpointConnections/<connection-id> \
  --description "Approved for Front Door origin"
```

**This is not automatic, even when you own both ends.** The connection request comes from
Microsoft's own Front Door subscription, so owning the subscription on your side does not
approve it. Without this step the origin stays permanently dead and nothing anywhere reports
an error.

### Then wait — the numbers are larger than Azure's documentation suggests

Two propagation delays, both measured on a setup that was entirely correct:

| After you | Expect up to |
| --- | --- |
| Approve the private endpoint connection | **~30 minutes** before origin health first turns green. It sits flat at 0% until then |
| Change any origin setting afterwards | **~15 minutes** before the edge actually serves the change |

`az afd origin show` reflects a change **instantly** while the edge still serves the old
behaviour. A control-plane read is not evidence the change is live.

**Green health metrics do not mean requests work.** Origin health and load-balancer backend
health confirm only the probe path, which is not host-matched. If the site returns 404 while
both read 100%, test from inside the cluster before touching Front Door:

```bash
kubectl -n studio run curl --rm -it --image=curlimages/curl --restart=Never -- \
  curl -sS -o /dev/null -w '%{http_code}\n' \
  -H "Host: $STUDIO_DOMAIN" http://<private-ingress-address>/
```

A 200 here means the cluster is serving correctly and the problem is at the edge — most likely
the origin host header from step 4. A 404 here means the problem is inside the cluster. This
check has no propagation delay in it, which is what makes it useful.

If traffic still doesn't reach the cluster after all of this, see
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
