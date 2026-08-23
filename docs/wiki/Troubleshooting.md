# Troubleshooting

Use the symptom that matches what you see. Current Studio persists diagnostics for Domain provisioning; read those before rebuilding resources.

## Local Docker

### `vibedata install compose` cannot find GitHub authentication

Run on the host:

```bash
gh auth login --scopes repo,read:org,workflow
```

Then rerun:

```bash
vibedata install compose
```

The installer imports the host session into the API container. Environment PAT variables are not the supported ambient replacement.

### Port 5173 is already in use

Do not stop an unrelated service just because an old guide said 5173 was fixed.

Use another port:

```bash
vibedata install compose --frontend-port 5174
```

### Studio opens locally but companion login fails from another machine

Install or rerender with the URL people actually use:

```bash
vibedata install compose --studio-url http://<host>:<port>
```

The companion OAuth callback is tied to this origin.

### Fabric works in my host shell but Studio cannot authenticate

The host's Azure CLI session is not Studio's ambient Fabric credential.

Sign in inside the API container:

```bash
docker compose -f ~/.vibedata/studio/docker-compose.yml exec -it api az login --use-device-code
```

Then confirm with `az account show` inside the same container.

## Kubernetes installation

### Installer says `kubectl` or `helm` is missing

Install the missing executable and make sure it is on `PATH` in the same shell that runs `vibedata`.

### Installer cannot reach the cluster

Check the exact context first:

```bash
kubectl --kubeconfig <path> --context <context> get nodes
```

Do not troubleshoot Argo or Studio until this succeeds.

### Installer reports missing/unreadable vault secrets

Ask the CLI for the exact list for your selected profile:

```bash
vibedata install kubernetes --cloud azure --list-secrets
```

Add `--with-observability` or `--full-observability` when applicable.

Create or repair every value the installer reports. Also confirm the cluster identity can read the vault.

### Installer reaches readiness but blocks

Inspect:

```bash
kubectl -n argocd get applications
kubectl -n studio get pods
```

Current readiness includes enabled companion applications. `studio-obot` must be healthy; with observability enabled, the selected LGTM/Langfuse applications also matter.

Read the failing pod or Argo application before rerunning the install.

### `studio-obot` is Degraded

Treat this as a current fault, not an expected successful-install state.

Check:

- Obot pod status and logs;
- ExternalSecret synchronization;
- `obot-client-secret`, `obot-db-password`, and `obot-tunnel-peer-token` availability;
- cluster capacity.

After fixing the prerequisite, rerun the same installer command.

## First sign-in and instance setup

### SSO callback is rejected

Use the callback URL shown by **Org Settings → SSO Providers** for the exact SSO Provider. Do not copy a Fabric Identity Provider callback.

Confirm the public Studio origin used by the browser matches the origin registered in the identity provider.

### Fabric user OAuth callback is rejected

Current downstream Fabric OAuth uses **Org Settings → Identity Providers** and a provider-specific callback of the form:

```text
/api/auth/oauth2/callback/<identity-provider-id>
```

Do not use the retired fixed Fabric callback paths from the earlier data-platform registry flow.

### GitHub provider Save fails on permissions

Check the GitHub App has:

- Administration read;
- Contents write;
- Metadata read;
- Pull requests write;
- Workflows write;
- Variables write;
- Secrets write.

Then check the **installation** has approved any recently added permissions. Updating the App definition alone may leave an existing installation on the old grant set.

## Domain creation and provisioning

### I cannot find Org Settings → Data Platforms

That surface is intentionally absent from current `main`.

Create the Data Platform candidate inside **Add Data Domain**. The Domain owns its Data Platform Type, authentication, and exact resource coordinates.

### I cannot find a Secret Store picker when creating a Domain

Current Domain create does not expose one. Studio automatically initializes the Domain's local secrets file.

Do not block Domain creation waiting for a legacy Secret Store registration step.

### Domain was created with `Defer service identity`, but Intents cannot activate

This is expected. The service lane is required by providers such as Fabric and delegated MotherDuck for unattended/ephemeral work.

Open Domain Settings and configure the required service credential, then retry provisioning/verification.

### Opening Domain Settings does not re-check readiness

Use **Verify** on an Active Domain or **Retry provisioning** after a failed provisioning state. Current behavior does not use page-open as an implicit verification trigger.

## Microsoft Fabric

### User cannot discover or validate Fabric resources

On Kubernetes:

- confirm the Domain selected the correct Entra Identity Provider;
- confirm the user connected that downstream provider;
- confirm the user can reach the Fabric workspace/Lakehouse/schema.

On Local Docker:

- confirm the API container's `az` session;
- confirm that Azure identity can reach the resources.

### Service lane cannot verify the persistent workspace

Grant the Domain service principal the required persistent workspace access. Current Studio verifies this baseline; it does not automatically grant the missing persistent-workspace role.

### Intent activation fails creating an ephemeral Fabric workspace

Check:

- selected ephemeral capacity ID;
- Fabric capacity availability;
- service identity authorization;
- Lakehouse SQL endpoint creation;
- schema name validity.

Capacity exhaustion is a hard activation failure rather than a hidden wait queue.

### GitHub Actions OIDC reports a federated-credential mismatch

The expected subject uses the Domain repository's **recorded default branch**:

```text
repo:<org>/<repo>:ref:refs/heads/<default-branch>
```

Do not rewrite it to `main` unless `main` is actually the Domain's recorded default branch.

### OIDC exchange succeeds but deployment still fails

Federation proves identity, not Fabric permissions. Check the Domain service principal's deploy-capable workspace role and relevant Fabric tenant/API permissions.

## MotherDuck

### User PAT authenticates but Intent activation cannot resolve the database

Check whether that user:

- owns/can directly resolve the bound database, or
- has the Domain's configured MotherDuck Share granted and visible.

Studio does not create the Share or grant it for you.

### Service PAT cannot provision unattended work

Check the Domain service PAT separately from the user's PAT. On delegated deployments they are different credential lanes.

### Clone fails after a MotherDuck plan change

Check the source database's snapshot-retention setting against the acting account's current plan entitlement. A valid PAT does not guarantee that a plan-gated clone is permitted.

## DuckDB

### DuckDB reports a lock/busy error

DuckDB is a file-backed database. Concurrent writers can contend on the same file.

Stop the conflicting writer, let the active request complete, and retry. Do not duplicate or manually replace the Studio-managed Domain database file as a first response.

## Source connections

### Agent says a secret key is missing

This is often the expected first verification attempt.

Add the exact key to the Domain's local `secrets.toml` outside the agent, then tell the agent to retry. Do not paste the value into chat.

### Static onboarding field names differ from the connector

Trust the connector introspection from the current run. Connector authentication fields come from the upstream connector and can change without a Studio release.

## LLM Profiles

### LLM Profile will not save

Connection-field changes run a real provider test. Check:

- API base;
- API key;
- model identifier or Azure deployment name;
- provider-specific endpoint requirements.

The previous persisted profile is preserved when a connection edit fails validation.

### Profile saves but an Intent turn fails

A successful connection test does not prove every runtime capability. The selected model may not support a requested tool or reasoning feature.

Check the Intent's bound profile, the model capability advisory fields, and the provider error from the actual turn.

## Last resort

Before deleting a Domain or reinstalling Studio, record:

- current Domain provisioning outcome;
- failed step and safe diagnostic;
- relevant Argo/pod state for Kubernetes;
- the exact CLI command used;
- the Studio/CLI version or `studio/main` SHA.

Recreation removes evidence and can make a deterministic external-configuration failure harder to diagnose.

---

_Applies to: studio/main (unreleased snapshot). Verified against `studio@5c9d2bbf339a` on 2026-08-22._
