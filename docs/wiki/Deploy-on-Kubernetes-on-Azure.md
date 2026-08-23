# Deploy Studio on Kubernetes on Azure

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

This deployment is the multi-user delegated-auth topology. The Azure infrastructure must already exist; see [[Prerequisites Azure Infrastructure]].

## 1. Check the CLI and cluster

Confirm:

```bash
vibedata version
kubectl --context <context> get nodes
helm version
```

The current installer requires `kubectl` and `helm` and currently implements Azure as its Kubernetes cloud provider.

## 2. Confirm the vault secret list

Before changing the cluster:

```bash
vibedata install kubernetes --cloud azure --list-secrets
```

Use the same observability flag you plan to install. Fix every missing Key Vault value before the deployment.

## 3. Run the install

Use the values provided by the Azure infrastructure owner:

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

Options that are not needed in your Azure layout can be omitted. In an interactive terminal, the installer can prompt for missing required values. In automation, provide them explicitly.

Current executable `main` does **not** use the future declarative `--config` installer described in some design documents.

## 4. Choose observability

| Flag | Topology |
| --- | --- |
| none | Studio core + Obot |
| `--with-observability` | Adds LGTM/Grafana |
| `--full-observability` | Adds LGTM and Langfuse |
| `--no-observability` | Explicitly disables optional observability |

The installer persists profile state so later operations can keep the same topology.

## 5. What the installer does

Current installation flow:

1. verifies local dependencies;
2. verifies cluster connectivity;
3. resolves the version-matched release artifacts;
4. checks the required Key Vault secret set;
5. installs External Secrets Operator and ingress prerequisites;
6. installs Argo CD;
7. renders the Studio manifests and applications;
8. applies the root Studio application;
9. waits for required applications and workload readiness.

The enabled companion applications are part of readiness. `studio-obot` must be healthy. With observability enabled, the relevant LGTM/Langfuse applications must also become healthy.

An old onboarding rule that allowed the install to succeed with `studio-obot` degraded is no longer correct.

## 6. Public HTTPS origin

Open the public HTTPS URL supplied by your infrastructure owner, normally behind Azure Front Door.

Use the same public origin for:

- Studio SSO callback URLs;
- downstream Identity Provider callback URLs;
- GitHub user-authorization callback;
- bundled companion OAuth.

Do not register callbacks against an internal service address if users reach Studio through Front Door.

## 7. Bootstrap the first owner

The Key Vault contains a `bootstrap-key` for first-boot administration.

Use the bootstrap path shown by Studio to establish the initial real administrator. The required outcome is:

1. register an SSO Provider under **Org Settings → SSO Providers**;
2. grant the first real user the `vibedata_owner` role;
3. sign out of bootstrap access;
4. sign back in through the SSO Provider.

Do not keep using the bootstrap credential as an ordinary operator identity.

## 8. Configure GitHub after real sign-in

As the first real owner, configure **Org Settings → GitHub** using the GitHub App values from [[Prerequisites GitHub Organisation Owner]].

Provider Save validates the App identity and required repository permission baseline.

## 9. Troubleshoot installer readiness

Start with:

```bash
kubectl -n argocd get applications
kubectl -n studio get pods
```

A blocked readiness result should be diagnosed from the unhealthy Argo application and the affected pod logs. Do not delete the deployment and start over before identifying the failing prerequisite; most failures are deterministic configuration problems such as missing vault values, storage reachability, or insufficient cluster capacity.

## 10. Re-run safely after fixing a prerequisite

The installer is designed for reconciliation. After fixing the external prerequisite, rerun the same `vibedata install kubernetes ...` command.

Use `--apply-only` only when you deliberately need to reapply the already-rendered installation state and understand that mode's narrower scope.

## Next step

Continue to [[Configure the Studio Instance]].

---

_Applies to: studio/main (unreleased snapshot). Verified against `studio@5c9d2bbf339a` on 2026-08-22._
