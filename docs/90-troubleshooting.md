---
applies-to: vibedata v0.1.26
verified-against: studio@653beeced
verified-on: 2026-08-08
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
  - src/server/config/env.ts
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

Entries are keyed on the exact text you see. If you have an error message in front of you,
search this page for a distinctive part of it.

**Install and upgrade**

- [Install reports missing CLI authentication](#install-reports-missing-cli-authentication)
- [Install is blocked with MISSING_DEPENDENCY](#install-is-blocked-with-missing_dependency)
- [Install is blocked with READINESS_FAILED](#install-is-blocked-with-readiness_failed)
- [Install is blocked with VAULT_SECRET_UNREADABLE](#install-is-blocked-with-vault_secret_unreadable)
- [A scripted or unattended install hangs, or reports "Aborted"](#a-scripted-or-unattended-install-hangs-or-reports-aborted)
- [The CLI version you looked up does not exist](#the-cli-version-you-looked-up-does-not-exist)
- [Helm chart pull fails](#helm-chart-pull-fails)
- [Windows: the `vibedata` command is not found](#windows-the-vibedata-command-is-not-found)

**After install: cluster health that looks wrong**

- [`studio-obot` shows Degraded in Argo CD](#studio-obot-shows-degraded-in-argo-cd)
- [Starting a conversation fails with "fetch failed"](#starting-a-conversation-fails-with-fetch-failed)
- [`studio-obot` will not schedule — Insufficient cpu](#studio-obot-will-not-schedule--insufficient-cpu)

**Domains and data platforms**

- [Domain stays Pending — Microsoft Fabric workspace access](#domain-stays-pending--microsoft-fabric-workspace-access)
- [Domain Failed — Microsoft Fabric host identity lacks workspace access (Local Docker)](#domain-failed--microsoft-fabric-host-identity-lacks-workspace-access-local-docker)
- [Domain stays Pending — provisioning run interrupted](#domain-stays-pending--provisioning-run-interrupted)
- [Domain is Active but a step shows Failed — branch rules](#domain-is-active-but-a-step-shows-failed--branch-rules)
- [CI fails with an OIDC token-exchange error (Microsoft Fabric)](#ci-fails-with-an-oidc-token-exchange-error-microsoft-fabric)
- [CI runs but cannot reach a model](#ci-runs-but-cannot-reach-a-model)
- [Foundry requests return 404](#foundry-requests-return-404)
- [MotherDuck picker or domain creation fails in an egress-restricted network](#motherduck-picker-or-domain-creation-fails-in-an-egress-restricted-network)
- [MotherDuck domain stays Pending — service PAT read check](#motherduck-domain-stays-pending--service-pat-read-check)
- [A user is rejected with a connect-required error](#a-user-is-rejected-with-a-connect-required-error)
- [GitHub rejects the sign-in with `redirect_uri_mismatch`](#github-rejects-the-sign-in-with-redirect_uri_mismatch)
- [Connecting Fabric fails with `AADSTS500113`](#connecting-fabric-fails-with-aadsts500113)
- [Fabric work fails with `AADSTS65001` consent required](#fabric-work-fails-with-aadsts65001-consent-required)
- [DuckDB reports a lock error](#duckdb-reports-a-lock-error)

**Kubernetes on Azure: the network and storage path**

- [Traffic drops although pods are healthy](#traffic-drops-although-pods-are-healthy)
- [The cluster cannot reach its own file share](#the-cluster-cannot-reach-its-own-file-share)
- [Private Link Service creation fails with AuthorizationFailed](#private-link-service-creation-fails-with-authorizationfailed)
- [`az afd origin create` rejects the Private Link argument](#az-afd-origin-create-rejects-the-private-link-argument)
- [Front Door returns 404 although both health metrics read 100%](#front-door-returns-404-although-both-health-metrics-read-100)
- [Front Door origin health sits at 0% on a correct configuration](#front-door-origin-health-sits-at-0-on-a-correct-configuration)

**Teardown and rebuild**

- [`az aks delete` fails on the load balancer](#az-aks-delete-fails-on-the-load-balancer)
- [The Private Link Service will not delete](#the-private-link-service-will-not-delete)
- [A Front Door profile name is not available after you deleted it](#a-front-door-profile-name-is-not-available-after-you-deleted-it)
- [A failed `az afd profile create` left a billing profile behind](#a-failed-az-afd-profile-create-left-a-billing-profile-behind)

---

## Install and upgrade

### Install reports missing CLI authentication

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

### Install is blocked with MISSING_DEPENDENCY

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

**Symptom:** the install stops almost immediately with:

```
BLOCKED: MISSING_DEPENDENCY
required tool(s) not found on PATH: ...
```

and the suggested next action `install kubectl and helm, then rerun`. Exit code is `3`.

**Cause:** the installer runs a tool preflight before it touches your cluster. It needs both
`kubectl` and `helm` on `PATH`. `helm` is the one people miss — installing `kubectl` alone,
or having it supplied by a cloud shell, is common.

**Fix:** install the missing tool and re-run. On macOS, `brew install helm`. Confirm with
`helm version` and `kubectl version --client` in the same shell you will run the install
from. Nothing was changed in your cluster, so there is nothing to undo.

### Install is blocked with READINESS_FAILED

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

**Symptom:** the install runs for a long time — up to the full timeout, 600 seconds by
default — and then stops with:

```
BLOCKED: READINESS_FAILED
```

with the suggested next actions `inspect Argo: kubectl -n argocd get applications` and
`then rerun once resolved`. Running that command shows `studio-app` is not `Healthy`.

**Cause, most common by far:** the `data-encryption-key` vault secret is not base64. Studio's
backend validates it at start-up and refuses to boot if it is any other encoding. The backend
pod then crash-loops, `studio-app` never reaches `Healthy`, and the installer times out
waiting.

Confirm it by reading the log of the backend pod that is restarting. Find it, then read it:

```
kubectl -n studio get pods
kubectl -n studio logs <backend-pod-name> --tail=50
```

The message names the field exactly:

```
DATA_ENCRYPTION_KEY must be 32 random bytes, base64-encoded (`openssl rand -base64 32`)
```

Generating this value with `openssl rand -hex 32` is the usual mistake. Hex is the right
choice for `pg-password` and `obot-db-password`, which go into a connection string — it is
the wrong choice here, and [01d-prereqs-azure-infra](01d-prereqs-azure-infra.md) is where the
correct generation command for each secret is listed.

**Fix:**

1. Generate a correct value: `openssl rand -base64 32`.
2. Update the `data-encryption-key` secret in the Key Vault.
3. Force the cluster to read it now, instead of waiting for the next scheduled refresh — that
   interval is one hour by default. Find the object that syncs it and annotate it:

   ```
   kubectl -n studio get externalsecrets
   kubectl -n studio annotate externalsecret <name> force-sync=$(date +%s) --overwrite
   ```

4. Wait for the backend's normal restart backoff to pick up the corrected value. You do not
   need to delete the pod.
5. Re-run the install.

**If the encryption key is not the cause:** read the same pod log for a different start-up
error, and check `kubectl -n argocd get applications` for which application is unhealthy. If
the unhealthy one is `studio-obot` rather than `studio-app`, see
[`studio-obot` shows Degraded in Argo CD](#studio-obot-shows-degraded-in-argo-cd) — that one
does not block a successful install.

### Install is blocked with VAULT_SECRET_UNREADABLE

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

**Symptom:** the install stops with:

```
BLOCKED: VAULT_SECRET_UNREADABLE
```

and names one or more secrets it could not read. With `--full-observability`, the two most
often missing are:

```
langfuse-init-project-public-key
langfuse-init-project-secret-key
```

**Cause:** the secret does not exist in the Key Vault, or the install identity cannot read
it. For the two named above, the usual cause is that they were never created. The
observability profile needs more secrets than the core install does, and these two are the
ones most often left out. [01d-prereqs-azure-infra](01d-prereqs-azure-infra.md) lists the
secrets to create.

**Fix:** create every secret the installer names, then re-run. For the two Langfuse project
keys, no format is enforced by the installer; values matching Langfuse's own API key shape
work — a `pk-lf-` prefix followed by 16 hex characters for the public key, and an `sk-lf-`
prefix followed by 24 hex characters for the secret key.

**One re-run clears every missing secret, not one per attempt.** The installer collects all the
secrets it could not read and reports them together, and its second suggested next action prints
the complete set your profile requires. So create everything the message names, then re-run once.
You are not facing a sequence of 600-second attempts that each reveal one more name.

**`--list-secrets` does not exist in any released CLI.** `vibedata install kubernetes
--list-secrets` fails with `No such option: --list-secrets` on `v0.1.26`, and on every release
up to and including `v0.1.29`. The flag exists only in unreleased development builds, so
upgrading will not give it to you. Where the CLI's own suggested next actions recommend running
it, ignore that suggestion and use the secret list on this page instead:

```
vibedata install kubernetes --help
```

If `--list-secrets` appears in that help output, use it — with the same profile flag you install
with, so the list matches the profile:

```
vibedata install kubernetes --list-secrets --full-observability
```

If it does not appear, your build is `v0.1.26` or older. Use the blocked message as the list; it
names exactly what is missing.

### A scripted or unattended install hangs, or reports "Aborted"

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

**Read this only if your CLI is `v0.1.26`.** This is fixed in builds after `v0.1.26`, where the
installer skips the kubeconfig prompt when `--kube-context` is given, and skips it whenever no
human can answer — `--json`, or a piped, closed, or absent standard input. If you are on a newer
build, neither symptom below occurs, and upgrading the CLI is the fix. Check with
`vibedata version`.

**Symptom:** one of two things, depending on how the job supplies standard input. Run from a
terminal, the install stops at a prompt you did not expect:

```
Cluster (kubeconfig) [~/.kube/config]:
```

Run from CI, a cron job, or with standard input redirected from `/dev/null`, it exits with
`Aborted` and no other explanation. Both happen even when you passed `--kube-context`.

**Cause:** on `v0.1.26` the installer opens the kubeconfig confirmation prompt regardless of
whether `--kube-context` was supplied. It suppresses the prompt only for `--json`. When standard
input is at end-of-file, the prompt reads that as a cancellation rather than as acceptance of the
bracketed default.

**Fix, if you can upgrade:** move to a CLI newer than `v0.1.26` and pass `--kube-context` as you
already were. No workaround is then needed.

**Fix on `v0.1.26`:** feed the prompt a real newline instead of letting it hit end-of-file:

```
yes "" | vibedata install kubernetes --kube-context <context> ...
```

Piping `yes ""` supplies newlines, which the prompt accepts as "use the default". Redirecting
from `/dev/null` does not work — that is the case that produces `Aborted`.

### The CLI version you looked up does not exist

**Symptom:** the version number you found is rejected, or the images and charts at that tag
cannot be pulled. The version you were told to install is one ahead of what actually ships.

**Cause:** you read the release list of the wrong repository. The `vibedata` CLI and its
install script are released from `accelerate-data/vibedata-official`.
`accelerate-data/studio` is a different repository with its own, independent release cadence,
and it is often ahead — on one occasion `studio` showed `v0.1.27` on the same day the shipped
CLI was `v0.1.26`. The two are easy to confuse because both hold parts of Studio.

**Fix:** always read the version from `vibedata-official`:

```
gh release list --repo accelerate-data/vibedata-official --limit 1
```

Use that number for the CLI, the container images, and — after dropping the leading `v` — the
Helm chart. See [Helm chart pull fails](#helm-chart-pull-fails) for the tag-form difference.

### Helm chart pull fails

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker — Local Docker never
> pulls the Helm chart.

**Symptom:** `helm pull` (or an install driven from it) fails to find the chart at the tag
you gave it.

**Cause:** the tag form differs between artefact types. Helm charts are tagged `0.1.26` —
no `v` prefix. Container images and CLI releases are tagged `v0.1.26` — with the prefix. A
`v` copied over from an image or CLI tag breaks the chart pull.

**Fix:** check the tag you passed to `helm pull`. Drop any leading `v` for a chart tag. If
you are also unsure the version number itself is right, see
[The CLI version you looked up does not exist](#the-cli-version-you-looked-up-does-not-exist).

### Windows: the `vibedata` command is not found

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

---

## After install: cluster health that looks wrong

### `studio-obot` shows Degraded in Argo CD

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker — there is no Argo CD
> and no `studio-obot` application there.

**Symptom:** `kubectl -n argocd get applications` shows:

```
studio-obot   ...   Degraded
```

The pod's log contains:

```
invalid tunnel peer configuration: tunnel peer config is incomplete: missing ID, Token
```

Everything else is `Healthy` and the install reported success.

**This is not harmless, and the install is not finished.** Your team will be able to sign in,
configure the organisation and create a domain — but **starting a conversation on an activated
intent will fail** until this is fixed. That is the last step this doc set leads you to.

**Cause:** a defect in `v0.1.26`. `obot` needs a Kubernetes `ExternalSecret` named
`obot-tunnel-peer`, which exposes the vault secret `obot-tunnel-peer-token` to the pod as
`OBOT_SERVER_TUNNEL_PEER_TOKEN`. The `v0.1.26` installer does not create that object at all. The
vault secret is present and correct the whole time; only the Kubernetes object is missing.
Confirm with:

```
kubectl -n studio get externalsecret obot-tunnel-peer
```

`NotFound` confirms this cause. Reproduced identically on two independent fresh deployments, so
this is not specific to your cluster.

**Upgrading the CLI does not fix this yet.** `obot-tunnel-peer` appears in no released CLI —
not `v0.1.26`, and not `v0.1.27`, `v0.1.28` or `v0.1.29`. The installer that renders and applies
that `ExternalSecret` exists only in unreleased development builds, so re-running the install
from any published version creates nothing and leaves `studio-obot` Degraded. Use the manual
workaround below until a release carries the fix, and check what is currently published from
`vibedata-official` — see
[The CLI version you looked up does not exist](#the-cli-version-you-looked-up-does-not-exist).
This is the fix to reach for first.

**Do not roll back, and do not re-run the install from `v0.1.26`** — neither creates the missing
object. Only a newer CLI does.

**If you cannot upgrade yet**, a manual workaround has been confirmed to restore conversations.
Ask Accelerate Data for the current procedure rather than improvising one. Two things about its
cost are worth knowing before you decide, because they are narrower than they first look:

- The `ExternalSecret` itself is applied with plain `kubectl apply` and carries no Argo CD
  tracking label, so Argo does not consider it part of any application and does not prune it. It
  survives a sync.
- The **Deployment** patch is the part Argo owns. `studio-obot` runs with self-healing on, so
  that patch is reverted on the next sync unless you disable automated sync on that one
  application and leave it disabled. That is the real cost: one application that no longer
  self-heals, until you upgrade and remove the patch.

Upgrading removes both, so treat the workaround as a bridge, not a settlement.

If `studio-app` itself is not `Healthy`, that is a different problem — see
[Install is blocked with READINESS_FAILED](#install-is-blocked-with-readiness_failed).

### Starting a conversation fails with "fetch failed"

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker — there is no Front Door
> in front of Studio there.

**Symptom:** a user activates an intent, starts a conversation, and it fails. Studio reports:

```
OpenHands agent server credential file write failed: fetch failed
```

The backend log separately shows `Open caller disconnected` AbortErrors at the same moment.

**Cause:** Azure Front Door's origin response timeout defaults to **30 seconds**, and the first
conversation takes longer than that. Starting one cold-spawns an agent workspace container —
git clone, connector install, container startup, readiness check, credential write. A real
deployment measured that at about **36 seconds**.

Front Door aborts the connection to the origin at 30 seconds. The backend sees that as the
caller having gone away mid-request, which is why the error names a disconnect rather than a
timeout, and why nothing in it points at Front Door.

Because the margin is small, a fast environment may succeed and a slow one fail — so this can
look intermittent rather than consistently broken.

**Fix:** raise the timeout on the Front Door profile.

```
az afd profile update -g <resource-group> --profile-name <profile> \
  --origin-response-timeout-seconds 180
```

This is your Azure infrastructure owner's resource — see
[01d-prereqs-azure-infra](01d-prereqs-azure-infra.md), which now asks them to set it at
creation time. Deployments built before that instruction will have the 30-second default.

**If raising the timeout does not fix it**, check whether `studio-obot` is `Degraded` — that
component is also required for conversations, and fails in a different way. See the entry above.

### `studio-obot` will not schedule — Insufficient cpu

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

**Symptom:** the `studio-obot` pod stays `Pending`. `kubectl -n studio describe pod` on it
ends with a scheduling message containing:

```
Insufficient cpu
```

Kubernetes builds the rest of that line from your actual cluster, so the numbers you see are
your own node count: `0/2 nodes are available: 2 Insufficient cpu` on a two-node cluster,
`0/3 nodes are available: 3 Insufficient cpu` on a three-node one. Search for
`Insufficient cpu` — that fragment is the same on every cluster size.

This is a different symptom from the one above: there, the pod runs and reports itself
unhealthy; here, no pod is placed at all.

**Cause:** the cluster has no node with enough free CPU left. A two-node cluster running
Studio's backend replicas plus the observability components can sit at 88–95% CPU allocation,
which leaves no room for this pod. Adding a third node of the same size often fails too,
because the subscription's regional vCPU quota is already close to its limit.

**Fix:** add a second, smaller node pool rather than a third node of the same size. One
2-vCPU node is enough for this component and usually fits inside whatever quota remains:

```
az aks nodepool add --resource-group <rg> --cluster-name <cluster> \
  --name obotpool --node-count 1 --node-vm-size Standard_D2s_v3
```

Check your remaining quota first with
`az vm list-usage --location <region> --query "[?contains(name.value, 'cores')]"`. If there is
no headroom at all, request a quota increase — that is a support request with its own lead
time, so start it early.

---

## Domains and data platforms

### Domain stays Pending — Microsoft Fabric workspace access

> **Applies to: Microsoft Fabric on Kubernetes on Azure.** Skip if you chose Local Docker —
> this check is auth-gated and never runs there, so it never produces a `Pending` Fabric
> domain under Local Docker. (A Local Docker domain can still show `Pending`, but from a
> provisioning run that was interrupted or never finished, not this check — select **Retry
> provisioning** either way.) Skip also if you chose DuckDB or MotherDuck.

**Symptom:** a newly created domain's Provisioning status is `Pending`.

**Step key:** `fabric_workspace_grant`, shown in the Provisioning steps list on the
domain's settings panel.

**Cause:** the domain's M2M service principal lacks Viewer-or-higher access on the bound
Fabric workspace, **and Studio could not add it**. On `v0.1.26` this step does not just check —
it tries to assign Viewer to the service principal itself. It makes that assignment using **the
operator's own Fabric credential**, so it fails when the signed-in operator holds only Viewer,
or no role at all, on that workspace. Assigning a role requires Member or Admin.

So the step failing usually means the operator lacks the rights to grant, not that anyone
forgot to ask.

**Fix:** either have a Fabric workspace admin grant the M2M service principal Viewer or higher
directly, or give the operator Member or Admin on the workspace so Studio's own assignment can
succeed. Then select **Retry provisioning**.

### Domain Failed — Microsoft Fabric host identity lacks workspace access (Local Docker)

> **Applies to: Microsoft Fabric on Local Docker.** Skip if you chose Kubernetes on Azure,
> or your data platform is DuckDB or MotherDuck.

**Symptom:** your first domain's Provisioning status is `Failed` immediately after
creation.

**Step key:** `provider_binding_validation`, shown in the Provisioning steps list on the
domain's settings panel. This is the step that validates the binding during domain
creation; it is a hard step, so failing it stops the domain reaching `Active`.

**Cause:** under Local Docker, Studio checks Fabric workspace access using the Azure identity
of the `az login` session **inside Studio's `api` container** — not a signed-in Studio user,
and not your own shell's `az` session. Those are different sessions and nothing copies one into
the other. If that identity lacks at least Viewer access to the bound workspace, this check
fails and the domain is `Failed`. See
[02-prereqs-operator](02-prereqs-operator.md) for the `az login` step, and
[01b-prereqs-fabric-admin](01b-prereqs-fabric-admin.md) for what this check does.

**Fix:** ask a Fabric workspace admin to grant the identity signed in **inside the container**
at least Viewer
access to the workspace, then select **Retry provisioning**.

### Domain stays Pending — provisioning run interrupted

**Symptom:** a newly created domain's Provisioning status is `Pending`, but none of the
per-platform checks elsewhere on this page name it — no `fabric_workspace_grant` or
`motherduck_service_rw_probe` step shows in the Provisioning steps list.

**Cause:** the provisioning run itself was interrupted or never finished. This cause is not
gated by delegated authentication and can happen under either deployment style, `Local
Docker` or `Kubernetes on Azure`, with any data platform — unlike the auth-gated checks
above, which only ever run on `Kubernetes on Azure`.

**Fix:** select **Retry provisioning** on the domain's settings panel.

### Domain is Active but a step shows Failed — branch rules

> **Applies to: MotherDuck and Microsoft Fabric.** Skip if you chose DuckDB — a DuckDB
> domain has no GitHub Actions setup step at all, so this check never runs.

**Symptom:** the domain reports `Active`, but the Provisioning steps list shows a `Failed`
step and the Provisioning warnings box holds a message like:

```
GitHub repository <org>/<repo> is missing recommended branch rules: default branch not
protected; delete-branch-on-merge disabled.
```

**Step key:** `github_branch_protection`.

**Cause:** Studio checks the domain repository's branch hygiene during GitHub Actions setup.
It is a soft check, so it warns and lets the domain reach `Active`. It reports any of three
things: the default branch has no protection rule, `delete-branch-on-merge` is switched off,
or Studio could not read the protection settings with the credentials it has.

The third case is worth reading carefully. If the message says the protection could not be
verified because of insufficient permission, the check ran under **your** credentials — a
`domain_owner` or `vibedata_owner` with more access on that repository can re-run it and get
a real answer.

**Fix:** this warning does not block anything, and a domain in this state works. To clear it,
in the domain repository's GitHub settings: add a branch protection rule on the default
branch, and switch on "Automatically delete head branches". Then re-run **Set up GitHub
Actions** on the domain — it is idempotent and re-checks only what has not already succeeded.

This check runs for MotherDuck domains as well as Fabric ones. Seeing a `Failed` step on an
`Active` MotherDuck domain does not mean you missed a Fabric step.

### CI fails with an OIDC token-exchange error (Microsoft Fabric)

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

### CI runs but cannot reach a model

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

**Only two controls write repository values**, and **Set up GitHub Actions** is the one to use
here. The other is **Sync GitHub Actions profile**, on the same settings panel, which overwrites
the Studio-managed variables and secrets from the domain's current configuration — it also seeds
the missing `LLM_*` entries, but it does not re-run the setup steps.

Nothing else writes them. Re-opening the domain's settings panel re-runs the readiness check, and
**Retry provisioning** re-runs provisioning. Neither touches repository values. A domain can pass
every readiness check with no warning and still have no `LLM_*` values in its repository.

### Foundry requests return 404

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

### MotherDuck picker or domain creation fails in an egress-restricted network

> **Applies to: MotherDuck.** Skip if you chose DuckDB or Microsoft Fabric.

**Symptom:** one of two things, depending on how far you got. Most commonly, the Database or
Schema picker fails while you're still filling in the domain creation form — no
domain exists yet at that point. Less commonly, the domain does get created and its
Provisioning status goes to `Failed`, not `Pending`. Either way it happens immediately —
never as a later surprise on a first query against the domain.

**Step key:** if you reach the `Failed` domain state, the failing step shows as
`provider_binding_validation` in the Provisioning steps list. The picker failure happens
before a domain object exists, so it has no step key of its own.

**Cause:** the DuckDB MotherDuck extension is not bundled into Studio's image — it loads at
runtime, the first time Studio opens a connection to MotherDuck. That first connection can
happen earlier than you'd expect: picking a Database or Schema in the domain
creation form each open a MotherDuck connection immediately, as does registering a personal
PAT — before you ever select **Create Domain**. If none of those ran, the same connection
happens again inside domain creation's binding validation, which is a hard check: if it
fails there, domain creation fails outright and the domain never reaches `Active`. Either
way, if the network can't reach `extensions.duckdb.org`, the extension can't load — most
often you'll see it as the Database/Schema picker failing while you're still filling
in the form; less often, as the domain reaching `Failed`.

**Fix:** allow egress to `extensions.duckdb.org` before you start creating the domain —
including before opening the Database or Schema pickers — then create it (or retry,
if the domain object already exists in `Failed`).

**If egress is fine and the domain still lands `Failed`,** the other cause is access rather
than network: binding validation could not reach the bound database with the registered Service
PAT. That check runs on **both** deployment styles, so a Local Docker domain fails this way too
— it is only the separate `Pending` read probe below that is skipped without delegated
authentication. Confirm the credential Studio uses can see the bound database — the registered
Service PAT under Local Docker, or the creating user's own personal PAT under Kubernetes on
Azure — either through a Share that
carries it or by owning it, then retry. See
[01e-prereqs-motherduck-admin](01e-prereqs-motherduck-admin.md).

### MotherDuck domain stays Pending — service PAT read check

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
bound **database** — failed. On `v0.1.26` the domain form has no Share field, so the probe
targets the database name the domain is bound to. It passes if that database reaches the
identity either way: received through a Share, or owned by the identity itself.

**Fix:** confirm the service PAT can read the bound database — either grant it READ on a Share
carrying that database, or make it the database's owner — then select **Retry provisioning**.

### A user is rejected with a connect-required error

> **Applies to: MotherDuck and Microsoft Fabric, on Kubernetes on Azure.** Skip if you chose
> Local Docker — there, one registry-level credential serves every user, so this error cannot
> occur. Skip also if you chose DuckDB.

**Symptom:** a user working in a domain gets rejected with:

```
AppError('Connect to <platform> before using this Domain', 401, 'platform_connect_required')
```

The message and code are identical for MotherDuck and for Microsoft Fabric. The platform name
in the message is the name of your registered connection, so read that to know which one it
is talking about.

**Cause:** under delegated authentication, each person authenticates to the data platform
with their **own** credential, not the connection's registry-level one. This user has not
connected theirs yet, or the stored credential has been revoked or expired. There is no
fallback to the registry credential for a user in this state.

- **MotherDuck** — the user has no personal PAT registered.
- **Microsoft Fabric** — the user has no stored refresh token, so Studio cannot mint a token
  on their behalf.

**Fix:** have that user connect their own account for the platform the message names, from
within Studio. Once the connection succeeds, retry the action.

> **Applies to: MotherDuck.** Skip if you chose Microsoft Fabric.

Because every contributor connects with a personal PAT rather than the registered service
PAT, each of them needs an account on your MotherDuck organisation. Check with your
MotherDuck organisation administrator — see
[01e-prereqs-motherduck-admin](01e-prereqs-motherduck-admin.md) — what your plan requires
per person before you add contributors.

### GitHub rejects the sign-in with `redirect_uri_mismatch`

> **Applies to: Local Docker and Kubernetes on Azure.** Skip only if you have not registered a
> GitHub App and configured a GitHub connection in **Org Settings → GitHub**.

Most reports of this come from `Kubernetes on Azure`, where registering a GitHub App is part of
the documented setup. Do not read that as a gate. Studio mounts both GitHub callback routes
unconditionally, and nothing in its GitHub module branches on deployment style — so a
`Local Docker` operator who configures a GitHub provider can reach the same error, and this is
the only entry that explains it. The evidence here is that no deployment-style gate exists in the
code, not a reproduction under `Local Docker`.

**Symptom:** the browser lands on a GitHub error page instead of returning to Studio, either
when an operator saves or tests the GitHub connection in **Org Settings → GitHub**, or when a
person connects their own GitHub account. GitHub reports:

```
redirect_uri_mismatch
```

**Cause:** the callback URL Studio sent is not registered on your GitHub App.

On the `v0.1.26` release Studio uses **one** callback URL, and the same one for both the
operator's save-and-test in Org Settings and each person's own GitHub link:

```
https://<STUDIO_DOMAIN>/api/v1/connect/github-commits/callback
```

The Org Settings panel displays exactly this URL, so it is a reliable thing to copy.

**Fix:** ask your GitHub organisation owner to register that URL on the App. See step 4 of
[01c-prereqs-github-org-owner](01c-prereqs-github-org-owner.md). It can be added or corrected
at any time from the App's own settings page.

Check three things before you conclude the URL is missing:

- The registered value is the **complete** URL, not the path alone.
- The domain matches the one Studio is actually reached at. If your operator changed
  `STUDIO_DOMAIN` after the App was created, the registered URL is now stale.
- There is no trailing slash or extra query string. GitHub matches the registered value
  exactly.

> **Applies to: builds newer than `v0.1.26`.** Skip if you are on `v0.1.26`.
>
> Later builds move the operator's save-and-test onto a second path,
> `/api/v1/github-commit-provider/validation/callback`. If your operator hits this error while
> saving, but individual users can link their accounts, that second URL is the one missing.
> Registering both is safe on any build — an unused callback URL has no effect.

### Connecting Fabric fails with `AADSTS500113`

> **Applies to: Microsoft Fabric.** Skip if your data platform is DuckDB or MotherDuck.

**Symptom:** connecting Microsoft Fabric from Studio fails immediately with:

```
AADSTS500113: No reply address is registered for the application
```

**Cause:** Studio's data-platform connection leaves "use the same app for service (M2M) and
user (U2M) access" checked by default. That means Studio runs an interactive sign-in against
the **M2M** app registration — and an app created for client credentials alone has no reply
address. Registration succeeds without one, so nothing fails until the first person tries to
connect their own Fabric access.

**Fix:** ask your Entra administrator to add a **Web** redirect URI to the **M2M** app
registration:

```
https://<STUDIO_DOMAIN>/api/auth/fabric/callback
```

This is a different URI, on a different app, from the SSO redirect URI. See
[01a-prereqs-entra-admin](01a-prereqs-entra-admin.md).

### Fabric work fails with `AADSTS65001` consent required

> **Applies to: Microsoft Fabric.** Skip if your data platform is DuckDB or MotherDuck.

**Symptom:** connecting Fabric, or activating an intent, fails with `AADSTS65001` naming a
scope — for example:

```
AADSTS65001: ... consent_required ... https://database.windows.net/user_impersonation
```

**Cause:** the app registration does not carry that delegated permission, or nobody has
granted admin consent for it. Studio needs delegated permissions across five resources, not
just the Fabric API — the SQL Database scope above is the one needed to query the Fabric SQL
analytics endpoint on a signed-in person's behalf.

**Fix:** ask your Entra administrator to add and consent the full permission set on the M2M
app. The complete list is in [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md). Read the
scope named in the error to know which one is missing.

**Warning for whoever applies the fix.** Adding one permission through the Azure CLI can
silently remove the app's existing consent grants, breaking connections that were working
moments earlier. Record the current state first:

```
az ad app permission list-grants --id <app-id>
```

Run it again immediately after the change and compare the count. If grants disappeared,
re-add and re-grant each lost resource individually, leaving a short pause between grants.

### DuckDB reports a lock error

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

---

## Kubernetes on Azure: the network and storage path

### Traffic drops although pods are healthy

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

**Symptom:** the load balancer in front of the cluster reports every backend node as
unhealthy and stops sending traffic, even though the pods themselves are healthy.

**Cause:** the load balancer's health probe is on the cloud default path, and ingress-nginx
answers that default path with `404` — which the load balancer reads as unhealthy.

**Fix:** point the load balancer's health probe at `/healthz` instead of the default path, by
annotating the ingress Service:

```
kubectl -n ingress-nginx annotate service ingress-nginx-controller \
  service.beta.kubernetes.io/azure-load-balancer-health-probe-request-path=/healthz --overwrite
```

Do this **before** you wire up anything that depends on this load balancer being healthy — a
Private Link Service, Front Door, an Application Gateway. Finding it afterwards means
debugging a downstream component that is reporting the truth.

Verify the fix from **outside** the cluster. A `curl` run from inside a pod returns `200`
on the default path regardless, because kube-proxy short-circuits traffic to a Service or
load-balancer IP straight to a backend pod without ever traversing the Azure load balancer.
Only a check that actually goes through the external load balancer proves the probe is fixed.

**Standing risk, worth recording in your own runbook:** this annotation lives on the live
Service object, not in ingress-nginx's Helm values. Redeploying or upgrading ingress-nginx
with Helm, without pinning `controller.service.annotations` to include it, removes the
annotation and reintroduces a total outage. Pin it in your values file.

### The cluster cannot reach its own file share

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

**Symptom:** pods cannot mount or read the NFS share backing Studio's data directory, after
network rules were tightened on the storage account.

**Cause:** the storage account's network rules allow a subnet that the AKS nodes are not in.
Traffic from pods and nodes originates from whatever subnet those nodes are actually attached
to. A dedicated "storage subnet" holding only the storage account's service endpoint carries
no node traffic, so allow-listing it and setting `default-action Deny` locks the cluster out
of its own share.

**Fix:** enable the `Microsoft.Storage` service endpoint directly on the subnet the AKS nodes
live in, and allow-list **that** subnet:

```
az network vnet subnet update --resource-group <rg> --vnet-name <vnet> \
  --name <node-subnet> --service-endpoints Microsoft.Storage

az storage account network-rule add --resource-group <rg> --account-name <account> \
  --subnet <node-subnet-resource-id>
```

No separate storage-only subnet is needed. Confirm which subnet your nodes are in with
`az aks show --resource-group <rg> --name <cluster> --query "agentPoolProfiles[].vnetSubnetId"`.

### Private Link Service creation fails with AuthorizationFailed

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

**Symptom:** you patched the ingress Service with
`service.beta.kubernetes.io/azure-pls-create: "true"` to have AKS create the Private Link
Service, and it fails with `AuthorizationFailed` reading the target subnet. It keeps failing —
observed unresolved for over 40 minutes — even after you confirm the cluster identity holds
`Network Contributor` at the exact subnet scope, and even after forcing `az aks update` to
flush the control plane.

**Cause:** the RBAC is not the problem. This looks like a token-caching fault on the AKS side,
and waiting does not clear it. A separate, real prerequisite hides behind it: with a custom or
bring-your-own VNet, `az aks create --vnet-subnet-id` auto-grants the cluster identity rights
on **that** subnet only. Any other subnet — such as one set aside for Private Link — needs an
explicit grant.

**Fix:** stop using the annotation. The internal load balancer already exists once the ingress
Service is up, so create the Private Link Service directly against its frontend IP
configuration, using your own credentials:

```
NODE_RG=$(az aks show --resource-group <rg> --name <cluster> \
  --query nodeResourceGroup -o tsv)

FRONTEND_ID=$(az network lb frontend-ip list --resource-group "$NODE_RG" \
  --lb-name kubernetes-internal --query "[0].id" -o tsv)

az network private-link-service create --resource-group <rg> --name <pls-name> \
  --location <region> --vnet-name <vnet> --subnet <pls-subnet> \
  --lb-frontend-ip-configs "$FRONTEND_ID"
```

Pass the frontend IP configuration by **resource ID**, as above. The internal load balancer
AKS creates is named `kubernetes-internal` and lives in the cluster's *node* resource group,
not the resource group you deployed into — so passing its name alone resolves against the
wrong group.

This path has no dependency on the AKS cluster identity or its permissions at all.

Before it works, the target subnet needs **both** network policies disabled, not just one:

```
az network vnet subnet update --resource-group <rg> --vnet-name <vnet> --name <pls-subnet> \
  --private-link-service-network-policies Disabled \
  --private-endpoint-network-policies Disabled
```

### `az afd origin create` rejects the Private Link argument

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

**Symptom:** creating a Front Door Premium origin over Private Link fails on the
`--shared-private-link-resource` argument. Common errors: only part of the value is consumed,
the tokenizer chokes on the `/` characters in a resource ID, or you get:

```
dict type value expected
```

**Cause:** the argument is a **single JSON string**, not space-separated `key=value` words,
and `private-link` inside it is a **nested object**, not a flat resource-ID string. A flat
string is what produces `dict type value expected`.

**Fix:** pass it as one quoted JSON string:

```
az afd origin create ... \
  --shared-private-link-resource '{"private-link":{"id":"<PLS resource ID>"},"private-link-location":"<region>","request-message":"..."}' \
  --enforce-certificate-name-check true
```

Two more constraints on the same command:

- `--enforce-certificate-name-check` must be `true`. The API hard-rejects `false` for any
  Private Link origin — `EnforceCertificateNameCheck must be enabled for Private Link` — even
  when the route forwards over plain HTTP.
- The private endpoint connection still needs **explicit approval**, even when you own both
  the Private Link Service and the Front Door profile. The request originates from Microsoft's
  own Front-Door-managed subscription, so ownership does not auto-approve it:
  `az network private-endpoint-connection approve --id <connection-id>`. Skipping this leaves
  an origin that looks created and never carries traffic.

### Front Door returns 404 although both health metrics read 100%

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

**Symptom:** requests through Front Door return a bare nginx `404`, while Front Door's
`OriginHealthPercentage` and the internal load balancer's `DipAvailability` both read 100%.

**Cause:** `--host-name` and `--origin-host-header` are different fields and were set to the
same value. `--host-name` is the address Front Door connects to over the private link — the
private IP. `--origin-host-header` is the HTTP `Host` header it sends — which must be your
actual `STUDIO_DOMAIN`, because ingress-nginx matches on it. Copying the IP into both is an
easy mistake and produces a request ingress-nginx cannot route, so its default backend answers
`404`.

**The health metrics cannot catch this.** Both layers probe `/healthz`, which is not
host-gated, so both stay green while every real request fails. Green health on both layers
does not confirm end-to-end routing.

**Fix:**

```
az afd origin update --resource-group <rg> --profile-name <profile> \
  --origin-group-name <group> --origin-name <origin> \
  --origin-host-header <STUDIO_DOMAIN>
```

Confirm routing directly, rather than trusting the metrics, by reproducing the request from
inside the cluster with an explicit header:
`curl -H "Host: <STUDIO_DOMAIN>" http://<ingress-private-ip>/`.

After the fix, expect a delay. `az afd origin show` reflects the new value immediately, but
the edge took about 14 minutes to start serving the corrected behaviour. Do not change
anything else during that window.

### Front Door origin health sits at 0% on a correct configuration

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

**Symptom:** you approved the private endpoint connection and everything is configured
correctly, but `OriginHealthPercentage` sits at a flat 0% and requests fail.

**Cause:** propagation, not misconfiguration. On a verified-correct setup this was observed at
a flat 0% for about **26 minutes** before flipping to 100% on its own, with no change made.

The "a few minutes" figure you will find in Azure's Private Link documentation is easy to misread
as the whole wait. It covers one step only: the private endpoint connection finishing its
establishment after you approve it. Front Door **configuration propagation** is a separate and
slower step. Microsoft's Front Door FAQ puts a single create, update, or delete operation at
**up to 15 minutes**, and back-to-back changes at approximately **30 minutes** in total.
Standing up a Private Link origin is back-to-back by nature — create the origin, create the
route, approve the endpoint connection — so an observed 26 minutes is inside Microsoft's own
documented window, not outside it.

Treat **45 minutes** as the point at which to start worrying, not 30. Microsoft has at times
extended propagation to up to 45 minutes for all create, update, delete and purge operations —
that was the published guidance after a 2025 platform incident, and support answers still cite
it. The FAQ's 15-and-30-minute figures are the normal case, not a ceiling. An observed 26
minutes is comfortably inside either.

"A few minutes" will have you changing a correct configuration long before Azure has finished
applying it — which is how a correct setup gets broken while waiting for it to come up.

**Fix:** before changing anything, check the cheap, fast signals:

- the load balancer's `DipAvailability` metric — is the backend pool healthy?
- the Private Link Service connection status — is it `Approved`?
- `provisioningState` on the origin and the route — are both `Succeeded`?

If all three are correct, the remaining wait is Azure propagating, and the fix is bounded
polling, not more configuration. Start debugging only when one of those three is itself wrong.
Changing a correct configuration during this window is the actual risk here — it makes a
working setup broken and hides the original state.

---

## Teardown and rebuild

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

The dependency chain matters more than the individual commands. Tear down in this order:

1. Delete the Front Door profile (`--no-wait`, then poll).
2. Delete the Private Link Service's private endpoint connection.
3. Delete the Private Link Service itself.
4. **Only then** run `az aks delete`.

The resource-group delete can run in parallel with the AKS delete. Front Door and AKS cannot
be torn down in parallel — see the first entry below for why.

### `az aks delete` fails on the load balancer

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

**Symptom:**

```
CannotDeleteLoadBalancerWithPrivateLinkService
```

usually after starting the AKS delete in parallel with the Front Door teardown to save time.

**Cause:** deleting the AKS node resource group deletes the internal load balancer
(`kubernetes-internal`). The Private Link Service still references that load balancer's
frontend, so the delete is refused. It is the Private Link Service that blocks AKS, not Front
Door directly.

**Fix:** delete the Private Link Service first (see the next entry for what blocks *that*),
then simply re-run `az aks delete`. It succeeds immediately. There is nothing to wait for and
nothing further to investigate.

### The Private Link Service will not delete

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

**Symptom:**

```
PrivateLinkServiceWithPrivateEndpointConnectionsCannotBeDeleted
```

even after the Front Door profile is confirmed fully gone.

**Cause:** deleting the Front Door profile does not release its private endpoint connection on
the Private Link Service side in time for a follow-up delete. The connection has to go
explicitly.

**Fix:**

```
az network private-endpoint-connection delete --id <connection-id> --yes
az network private-link-service delete --resource-group <rg> --name <pls-name>
```

Two argument traps in this sequence:

- The connection delete **does** need `--yes`.
- `az afd profile delete` and `az network private-link-service delete` do **not** accept
  `--yes`. Neither prompts, so there is nothing to skip, and passing it is a CLI error:
  `unrecognized arguments`.

Also budget time for the Front Door profile delete. On a Premium profile with an active
Private Link origin it took 15–20 minutes and blocks past most CLI timeouts. Run it with
`--no-wait` and poll `az afd profile show` until it returns `ResourceNotFound`, rather than
waiting on the foreground call.

### A Front Door profile name is not available after you deleted it

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

**Symptom:** recreating a Front Door profile with the same name — even in a **different
resource group** in the same subscription — fails with:

```
(Conflict) That resource name isn't available
```

`az afd profile show` on the old profile already returns `ResourceNotFound`, so it really is
deleted.

**Cause:** `Microsoft.Cdn/profiles` names carry a post-delete reservation that is
subscription-wide, not scoped to the resource group, and it outlives the delete confirming as
complete. Creating a throwaway profile with a different name in the same resource group
succeeds seconds later, which confirms the name — not your permissions or the region — is what
is blocked.

**Fix:** pick a different name rather than waiting out an unknown cooldown. If you are
rebuilding after a teardown, plan for this: name the rebuild `<name>02` from the start.

### A failed `az afd profile create` left a billing profile behind

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

**Symptom:** an `az afd profile create` reported an error — typically the `(Conflict)` above —
so you moved on to a different name. Later, `az resource list` shows **two**
`Microsoft.Cdn/profiles` in the resource group.

**Cause:** the create reported a conflict and created the resource anyway. The orphan is fully
provisioned (`provisioningState: Succeeded`, `resourceState: Active`) with no endpoint, origin,
or route — and it bills.

**Fix:** after **any** `az afd profile create` that errors, check whether it was created
regardless, before retrying under a different name:

```
az afd profile show --resource-group <rg> --profile-name <name>
```

If it exists, delete it immediately rather than leaving it for the next teardown. Do not rely
on this resource type's own error reporting to tell you whether the resource exists.
