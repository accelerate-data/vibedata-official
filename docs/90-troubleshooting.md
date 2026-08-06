---
applies-to: vibedata v0.1.26
verified-against: studio@653beeced
verified-on: 2026-08-05
sources:
  - cli/vibedata/src/vibedata/auth/github_container_auth.py
  - cli/vibedata/src/vibedata/commands/install.py
  - cli/vibedata/src/vibedata/commands/install_kubernetes.py
  - cli/vibedata/src/vibedata/commands/login.py
  - cli/vibedata/src/vibedata/core/blocked.py
  - cli/vibedata/src/vibedata/core/exit_codes.py
  - cli/vibedata/src/vibedata/templates/docker-compose.yml.j2
  - scripts/generate-install-script.sh
  - .github/workflows/release.yml
  - src/server/lib/graph/federated-credential-client.ts
  - src/server/modules/data-platforms/providers/fabric.provider.ts
  - src/server/modules/data-platforms/providers/motherduck.provider.ts
  - src/server/modules/data-platforms/providers/motherduck-sql.ts
  - src/server/modules/data-platforms/providers/duckdb-local-sql.ts
  - src/server/modules/domains/services/domain-provisioning.service.ts
  - src/server/modules/domains/services/domain-provisioning-step.ts
  - src/server/modules/domains/services/domain-gha-setup.service.ts
  - src/server/modules/chat/openhands/side-channel-completion.ts
  - docs/design/kubernetes-deployment/cloud.md
  - docs/design/kubernetes-deployment/concepts.md
  - deploy/docker/docker-compose.yml
  - deploy/k8s/kind-cluster.yaml
  - docs/design/kubernetes-deployment/README.md
---

# Troubleshooting

This is a reference, not a walkthrough. Find the symptom you are seeing and read that entry
on its own — it states its own scope, so you do not need anything from earlier in this page
or from the rest of this doc set to use it.

Symptoms covered on this page:

- [Install reports missing CLI authentication](#install-reports-missing-cli-authentication)
- [Domain stays Pending — Microsoft Fabric workspace access](#domain-stays-pending--microsoft-fabric-workspace-access)
- [Domain Failed — Microsoft Fabric host identity lacks workspace access (Local Docker)](#domain-failed--microsoft-fabric-host-identity-lacks-workspace-access-local-docker)
- [Domain stays Pending — provisioning run interrupted](#domain-stays-pending--provisioning-run-interrupted)
- [CI fails with an OIDC token-exchange error (Microsoft Fabric)](#ci-fails-with-an-oidc-token-exchange-error-microsoft-fabric)
- [CI runs but cannot reach a model](#ci-runs-but-cannot-reach-a-model)
- [Foundry requests return 404](#foundry-requests-return-404)
- [MotherDuck picker or domain creation fails in an egress-restricted network](#motherduck-picker-or-domain-creation-fails-in-an-egress-restricted-network)
- [MotherDuck domain stays Pending — service PAT read check](#motherduck-domain-stays-pending--service-pat-read-check)
- [MotherDuck rejects a user with a connect-required error](#motherduck-rejects-a-user-with-a-connect-required-error)
- [DuckDB reports a lock error](#duckdb-reports-a-lock-error)
- [Kubernetes on Azure: traffic drops although pods are healthy](#kubernetes-on-azure-traffic-drops-although-pods-are-healthy)
- [Helm chart pull fails](#helm-chart-pull-fails)
- [Windows: the `vibedata` command is not found](#windows-the-vibedata-command-is-not-found)

## Install reports missing CLI authentication

> **Applies to: Local Docker.** Skip if you chose Kubernetes on Azure — that installer
> never touches GitHub authentication at all.

**Symptom:** `vibedata install compose` stops with a blocked result whose reason is
`MISSING_CLI_AUTH`, and the process exits with code `3`. This gate fires *after* the
containers are already up — a blocked install still leaves Studio's containers running, and
because the check happens before the step that prints service URLs, you don't get a URL
back either.

**Cause:** the CLI could not find a working `gh` CLI session, on the container or the host.

**Fix:** run `gh auth login --scopes repo,read:org,workflow`, then re-run `vibedata install
compose`. You don't need to stop or remove the containers already running — the command is
safe to re-run against them and picks up from where it left off once auth succeeds. The
installer only checks that a session exists, not which scopes it carries — but grant all
three: Studio's GitHub features use them.

## Domain stays Pending — Microsoft Fabric workspace access

> **Applies to: Microsoft Fabric on Kubernetes on Azure.** Skip if you chose Local Docker —
> this check is auth-gated and never runs there, so it never produces a `Pending` Fabric
> domain under Local Docker. (A Local Docker domain can still show `Pending`, but from a
> provisioning run that was interrupted or never finished, not this check — select **Retry
> provisioning** either way.) Skip also if you chose DuckDB or MotherDuck.

**Symptom:** a newly created domain's Provisioning status is `Pending`.

**Step key:** `fabric_workspace_grant`, shown in the Provisioning steps list on the
domain's settings panel.

**Cause:** the domain's M2M service principal lacks Viewer-or-higher read access on the
bound Fabric workspace. Studio checks for this access; it never grants it.

**Fix:** ask a Fabric workspace admin to grant the M2M service principal at least Viewer
access on the workspace, then select **Retry provisioning**.

## Domain Failed — Microsoft Fabric host identity lacks workspace access (Local Docker)

> **Applies to: Microsoft Fabric on Local Docker.** Skip if you chose Kubernetes on Azure,
> or your data platform is DuckDB or MotherDuck.

**Symptom:** your first domain's Provisioning status is `Failed` immediately after
creation.

**Step key:** `provider_binding_validation`, shown in the Provisioning steps list on the
domain's settings panel. This is the step that validates the binding during domain
creation; it is a hard step, so failing it stops the domain reaching `Active`.

**Cause:** under Local Docker, Studio checks Fabric workspace access using the host
machine's own Azure identity — the one behind its `az login` session, not a signed-in
Studio user. If that identity lacks at least Viewer access to the bound workspace, this
check fails and the domain is `Failed`. See
[02-prereqs-operator](02-prereqs-operator.md) for the `az login` step, and
[01b-prereqs-fabric-admin](01b-prereqs-fabric-admin.md) for what this check does.

**Fix:** ask a Fabric workspace admin to grant that `az login` identity at least Viewer
access to the workspace, then select **Retry provisioning**.

## Domain stays Pending — provisioning run interrupted

**Symptom:** a newly created domain's Provisioning status is `Pending`, but none of the
per-platform checks elsewhere on this page name it — no `fabric_workspace_grant` or
`motherduck_service_rw_probe` step shows in the Provisioning steps list.

**Cause:** the provisioning run itself was interrupted or never finished. This cause is not
gated by delegated authentication and can happen under either deployment style, `Local
Docker` or `Kubernetes on Azure`, with any data platform — unlike the auth-gated checks
above, which only ever run on `Kubernetes on Azure`.

**Fix:** select **Retry provisioning** on the domain's settings panel.

## CI fails with an OIDC token-exchange error (Microsoft Fabric)

> **Applies to: Microsoft Fabric.** Skip if you chose DuckDB or MotherDuck.

**Symptom:** the domain shows `Active`, GitHub Actions setup reported success, but the
domain repository's first workflow run fails with an OIDC token-exchange error.

**Cause:** the per-repository federated credential is missing, or was created with the
wrong subject, on the Fabric M2M application in Entra. Studio's GitHub Actions setup
treats this check as non-blocking: the domain still reports `Active`, the setup call
still returns success, and the CI variables and secrets still get written — nothing in
that response tells you the credential is missing or wrong.

**Fix:** ask your Entra administrator to create (or correct) the federated credential
with:

- Issuer: `https://token.actions.githubusercontent.com`
- Audience: `api://AzureADTokenExchange`
- Subject: `repo:<org>/<repo>:ref:refs/heads/main`

As a single command:

```
az ad app federated-credential create --id <m2m-app-client-id> --parameters '{"name":"<credential-name>","issuer":"https://token.actions.githubusercontent.com","subject":"repo:<org>/<repo>:ref:refs/heads/main","audiences":["api://AzureADTokenExchange"]}'
```

The subject is always the literal `main` — never this repository's actual default branch.
Studio's check accepts only an exact match against `refs/heads/main`.

**The trap:** if this check is failing, Studio's own Provisioning warnings panel prints a
command shaped like the one above — but built from *this repository's actual default
branch* instead of the literal `main` the check requires. If your repository's default
branch is not `main`, edit the subject in that printed command before running it: replace
the branch name with the literal `main`, matching the command shown above. Running the
printed command unedited on a non-`main` repository creates a credential the check will
keep rejecting, and you will see the identical warning again.

## CI runs but cannot reach a model

> **Applies to: MotherDuck and Microsoft Fabric.** Skip if you chose DuckDB — a DuckDB
> domain has no GitHub Actions setup step at all, so it never seeds an LLM credential and
> this failure mode does not apply.

**Symptom:** the domain repository's CI runs, but a step calling the LLM fails, or behaves
as if no credential were configured.

**Cause:** no instance LLM profile existed yet when **Set up GitHub Actions** last ran for
this domain. When that's true, Studio omits `LLM_API_URL`, `LLM_MODEL`, and `LLM_API_KEY`
from what it seeds into the repository — it does not write them blank, and nothing reports
an error at the time.

**Fix:** configure the instance LLM profile in Org Settings, then re-run **Set up GitHub
Actions** for this domain. It is idempotent — re-running it seeds the LLM variables and
secret without disturbing anything that already succeeded.

## Foundry requests return 404

**Symptom:** requests to your Azure AI Foundry LLM profile fail with `404`.

**Cause:** one of two configuration mistakes in the Azure AI Foundry LLM profile:

- The **Model** field holds a model family name (for example `gpt-4o`) instead of the
  actual Azure deployment name. Studio builds the request URL from this field directly, so
  it must be the deployment name.
- The **Base URL** contains a path. Studio appends its own path onto whatever you enter,
  so a URL that already includes a path produces a doubled, invalid path.

**Fix:** set **Model** to the deployment name shown in the Azure AI Foundry portal's
**Deployments** view — not the Keys and Endpoint page, which shows the endpoint but not
deployment names. Set **Base URL** to the host only, `https://<resource-name>.openai.azure.com`
with no trailing path, using the endpoint shown on either the Azure portal's Keys and
Endpoint page or the Foundry portal's Deployments view — both show the same endpoint.

## MotherDuck picker or domain creation fails in an egress-restricted network

> **Applies to: MotherDuck.** Skip if you chose DuckDB or Microsoft Fabric.

**Symptom:** one of two things, depending on how far you got. Most commonly, the Database,
Schema, or Share picker fails while you're still filling in the domain creation form — no
domain exists yet at that point. Less commonly, the domain does get created and its
Provisioning status goes to `Failed`, not `Pending`. Either way it happens immediately —
never as a later surprise on a first query against the domain.

**Step key:** if you reach the `Failed` domain state, the failing step shows as
`provider_binding_validation` in the Provisioning steps list. The picker failure happens
before a domain object exists, so it has no step key of its own.

**Cause:** the DuckDB MotherDuck extension is not bundled into Studio's image — it loads at
runtime, the first time Studio opens a connection to MotherDuck. That first connection can
happen earlier than you'd expect: picking a Database, Schema, or Share in the domain
creation form each open a MotherDuck connection immediately, as does registering a personal
PAT — before you ever select **Create Domain**. If none of those ran, the same connection
happens again inside domain creation's binding validation, which is a hard check: if it
fails there, domain creation fails outright and the domain never reaches `Active`. Either
way, if the network can't reach `extensions.duckdb.org`, the extension can't load — most
often you'll see it as the Database/Schema/Share picker failing while you're still filling
in the form; less often, as the domain reaching `Failed`.

**Fix:** allow egress to `extensions.duckdb.org` before you start creating the domain —
including before opening the Database, Schema, or Share pickers — then create it (or retry,
if the domain object already exists in `Failed`).

## MotherDuck domain stays Pending — service PAT read check

> **Applies to: MotherDuck on Kubernetes on Azure.** Skip if you chose Local Docker — this
> check runs only when delegated authentication is enabled, so it never produces a
> `Pending` MotherDuck domain under Local Docker. Skip also if you chose DuckDB or
> Microsoft Fabric.

**Symptom:** a newly created domain's Provisioning status is `Pending`. This is a
different symptom from a MotherDuck extension-host connectivity failure (picker error, or
domain `Failed`): binding validation itself passed here, so this isn't that hard `Failed`
case — this domain got further before stalling.

**Step key:** `motherduck_service_rw_probe`, shown in the Provisioning steps list on the
domain's settings panel.

**Cause:** a separate, retryable check — whether the registered service PAT can read the
bound Share — failed.

**Fix:** confirm the service PAT still has read access to the bound Share (or grant it),
then select **Retry provisioning**.

## MotherDuck rejects a user with a connect-required error

> **Applies to: MotherDuck on Kubernetes on Azure.** Skip if you chose Local Docker — under
> Local Docker, one registry service PAT serves every user, so this error cannot occur.
> Skip also if you chose DuckDB or Microsoft Fabric.

**Symptom:** a user working in a MotherDuck-backed domain gets rejected with:

```
AppError('Connect to <platform> before using this Domain', 401, 'platform_connect_required')
```

**Cause:** under delegated authentication, each contributor authenticates to MotherDuck
with their own personal PAT, not the registry's service PAT. This user has not connected
one yet. There is no fallback to the service PAT for a user in this state.

**Fix:** have that user connect their own MotherDuck account and issue a personal PAT. Each
contributor needs their own MotherDuck seat under this deployment style.

## DuckDB reports a lock error

> **Applies to: DuckDB.** Skip if you chose MotherDuck or Microsoft Fabric.

**Symptom:** a write against a DuckDB domain fails with a file-lock or IO error.

**Cause:** DuckDB opens the domain's database file directly. There is no locking or
single-writer coordination layered on top of it in Studio beyond opening read-only
connections in read-only mode — two writers reaching the same file at the same time
contend on the file itself. This is a property of how a single DuckDB file is shared, not
a defect in your setup, and the underlying mechanism is the same on both deployment styles.
Under `Kubernetes on Azure`, Studio's backend runs multiple replicas across nodes against
the same shared volume, so the colliding writers can be different pods; under `Local
Docker`, Studio runs as a single backend process, so the same collision can only come from
two concurrent requests within that process.

**Fix:** retry the write. As an operational practice, avoid running concurrent write
workloads against a single DuckDB domain.

## Kubernetes on Azure: traffic drops although pods are healthy

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

**Symptom:** the load balancer in front of the cluster reports every backend node as
unhealthy and stops sending traffic, even though the pods themselves are healthy.

**Cause:** the load balancer's health probe is on the cloud default path, and ingress-nginx
answers that default path with `404` — which the load balancer reads as unhealthy.

**Fix:** point the load balancer's health probe at `/healthz` instead of the default path.
Verify the fix from **outside** the cluster — a `curl` run from inside a pod returns `200`
on the default path regardless, because kube-proxy short-circuits it; only a check that
actually goes through the external load balancer proves the probe is fixed.

## Helm chart pull fails

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker — Local Docker never
> pulls the Helm chart.

**Symptom:** `helm pull` (or an install driven from it) fails to find the chart at the tag
you gave it.

**Cause:** the tag form differs between artefact types. Helm charts are tagged `0.1.26` —
no `v` prefix. Container images and CLI releases are tagged `v0.1.26` — with the prefix. A
`v` copied over from an image or CLI tag breaks the chart pull.

**Fix:** check the tag you passed to `helm pull`. Drop any leading `v` for a chart tag.

## Windows: the `vibedata` command is not found

**Symptom:** after downloading the CLI release asset from GitHub on a Windows machine,
running `vibedata` does nothing — the shell reports no such command.

**Cause:** the Windows release asset is published as `vibedata-windows-x86_64.exe`, not
`vibedata.exe`. On Linux and macOS, the one-line install script downloads this same kind of
platform-qualified asset and saves it locally under the plain name `vibedata` for you —
but that install script only runs on Linux and macOS; it exits immediately with an error on
any other operating system. There is no equivalent installer for Windows, so a manual
download keeps its platform-qualified filename.

**Fix:** after downloading, rename the file to `vibedata.exe` (or place it on `PATH` under
that name) before running it.
