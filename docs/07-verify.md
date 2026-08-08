---
applies-to: vibedata v0.1.26
verified-against: studio@653beeced
verified-on: 2026-08-08
sources:
  - src/shared/schemas.ts
  - src/server/modules/domains/services/domain-provisioning-step.ts
  - src/server/modules/domains/services/domain-provisioning.service.ts
  - src/server/modules/domains/services/domain-provisioning-runner.service.ts
  - src/server/modules/domains/services/domain-gha-setup.service.ts
  - src/server/modules/domains/services/domain-verification.service.ts
  - src/server/modules/domains/services/domain-verification-plan.ts
  - src/server/modules/domains/services/domain-repository-profile.service.ts
  - src/server/modules/domains/routers/domain-provisioning.router.ts
  - src/server/modules/domains/helpers/domain-response-relations.ts
  - src/server/modules/domains/helpers/domain-response.ts
  - src/server/modules/domains/helpers/domain-repository-values.ts
  - src/server/modules/data-platforms/providers/fabric.provider.ts
  - src/server/lib/graph/federated-credential-client.ts
  - src/features/settings/components/Settings/panels/domain-settings/DomainProvisioningSection.tsx
  - src/features/settings/components/Settings/panels/domain-settings/DomainVerificationFailures.tsx
  - src/features/settings/components/Settings/panels/domain-settings/DomainSettingsPanel.tsx
  - src/features/domain/hooks/use-domains.ts
  - src/features/domain/api.ts
  - cli/vibedata/src/vibedata/core/data_dir.py
  - cli/vibedata/src/vibedata/templates/docker-compose.yml.j2
  - ext/domain-cicd/domain-ci-duckdb-bundle/.github/workflows/ci.yml
  - ext/domain-cicd/domain-ci-duckdb-bundle/.github/profiles/profiles.yml
  - src/server/modules/data-platforms/providers/duckdb-local-sql.ts
  - deploy/docker/docker-compose.yml
  - deploy/k8s/kind-cluster.yaml
  - docs/design/kubernetes-deployment/README.md
---

# Confirm you're done

This page continues from [06-first-domain](06-first-domain.md). It applies to **all six
combinations**. It closes the deployment and setup sequence. Two pages follow it and cover
how work happens inside a finished domain.

## Why `Active` is not the finish line

It is reasonable to see your domain's Provisioning status turn **Active** and assume you are
finished. Don't. `Active` reports one thing: your data platform binding is valid and the
domain's core setup succeeded. It does not cover credential and network dependencies that
Studio only exercises later — the first time your domain repository's GitHub Actions
workflow actually runs.

**Done means two things together: the domain reports `Active`, and every GitHub Actions
setup step reports success.** Neither alone is proof. A domain can be `Active` while one of
its setup steps quietly failed.

### Two ways this happens silently

**1. A missing Fabric federated credential — the central example.**

> **Applies to: Microsoft Fabric.** Skip if you chose DuckDB or MotherDuck.

Studio treats the federated-credential check as a **soft** check. When it fails, Studio does
not stop and does not fail the domain: the failure is recorded against that one step, a
warning is logged, and setup continues. The result: GitHub Actions setup still returns
**HTTP 200**, the domain still shows `Active`, and the CI variables and secrets are still
written into your repository. Nothing in that response's headline tells you the credential is
missing.

The failure surfaces later — the first time your domain repository's workflow actually runs,
as an OIDC token-exchange error.

The good news: the failed step **does** show up if you look at the right place, described
below.

**2. An absent instance LLM profile at setup time.**

If no instance LLM profile exists yet when you run GitHub Actions setup, the `LLM_API_URL`,
`LLM_MODEL`, and `LLM_API_KEY` entries are **omitted** from what gets seeded — not written as
blank values, and nothing reports an error at the time. The failure surfaces later, the first
time your domain's CI tries to call the LLM. Configuring the instance LLM profile before
running GitHub Actions setup avoids this.

If you set it up afterward, **re-run Set up GitHub Actions** on the domain. Exactly two controls
on the domain's settings panel write repository values: **Set up GitHub Actions**, and **Sync
GitHub Actions profile**, which overwrites the Studio-managed variables and secrets from the
domain's current configuration. Either one seeds the missing `LLM_*` entries; **Set up GitHub
Actions** is the one to use, because it also re-runs the setup steps.

Nothing else writes them. Re-opening the settings panel re-runs the readiness check, and **Retry
provisioning** re-runs provisioning, but neither touches repository values — readiness
deliberately does not look at GitHub Actions configuration at all. So a domain can pass every
readiness check, show no warning, and still have no `LLM_*` values in its repository.

*A related but different case, already covered on [06](06-first-domain.md): if the
MotherDuck extension host is unreachable, you'll see it loudly — either the Database/Schema
picker failing while you're still filling in the creation form, or, if none of those
connections ran, domain creation itself failing outright with `Failed`. Either way it's
immediate, not a later surprise. That is a loud failure, the opposite of the two silent
cases above, so it isn't one of them.*

## The status set

Provisioning status is one of seven values: `PENDING`, `ACTIVE`, `FAILED`, `STALE`, `LOCKED`,
`ARCHIVING`, `ARCHIVED`. The domain settings panel title-cases whatever value is present, so
it can also show `Stale`, `Locked`, `Archiving`, or `Archived`. This page and [06](06-first-domain.md) only ever produce `Active`, `Pending`, or
`Failed` — the other four values belong to a domain's later life (archiving, locking during
an export/import run, and so on), not to first-time setup. Seeing one of them here doesn't
mean something on this page is wrong.

As established on [06](06-first-domain.md): a domain can land in `Pending` two ways. Only
two specific checks can leave it there, both scoped to `Kubernetes on Azure` and requiring
delegated authentication. Separately, under **either** deployment style, a provisioning run
that was interrupted or never finished also leaves a domain `Pending` — this second cause is
not auth-gated and is not one of those two checks. **Retry provisioning** is the fix either
way.

## Where to look: the domain's Provisioning status

Open the domain's settings (the same "Provisioning status" panel from
[06](06-first-domain.md)). It shows more than the lifecycle label:

- **Provisioning steps** — every step Studio has run for this domain, each listed by its
  internal key with a status of **Passed**, **Pending**, or **Failed**.
- **Provisioning warnings** — any step currently showing a failure, grouped as blockers or
  warnings, each with a human-readable message. For a soft-check failure like the Fabric
  federated credential, this message includes the exact remediation to run — for example the
  `az ad app federated-credential create` command your Entra administrator needs.
- **Domain verification failures** — results from the most recent readiness check (see
  below), grouped by your connections and the domain's own automation.

A domain that shows `Active` at the top can still show a step **Failed** further down this
same panel — that combination is the whole point of this page. A step that is `hard` severity
failing would have kept the domain out of `Active` in the first place, so any `Failed` step
you see on an `Active` domain is a soft one. There are two soft steps, not one:

- `fabric_federated_credential` — the federated-credential case described above. Microsoft
  Fabric only.
- `github_branch_protection` — runs for **both** MotherDuck and Microsoft Fabric domains,
  every time GitHub Actions setup runs. It fails when the domain repository's default branch
  is unprotected, when `delete-branch-on-merge` is switched off, or when Studio cannot read
  the branch protection settings with the credentials it has. The warning message names which
  of those applies.

The second one surprises people. A MotherDuck operator, who skips every Fabric block on this
page, can still land on an `Active` domain with a `Failed` step and a warning about branch
rules. That is this check, and it does not mean your domain is broken — see
[90-troubleshooting](90-troubleshooting.md) for what to change.

If you have permission to update the domain — true for the `vibedata_owner` or
`domain_owner` following this guide — re-opening this panel also re-runs the readiness check
automatically for a domain that is `Active` or previously `Failed`. See "Re-run readiness"
below.

## The checks, in order

1. **Domain status is `Active`.**
2. **Every GitHub Actions setup step reports success** — read the Provisioning steps list
   and the Provisioning warnings box described above. Don't stop at the domain badge.
   > **Applies to: MotherDuck and Microsoft Fabric.** Skip if you chose DuckDB — Studio has
   > no GitHub Actions setup for DuckDB domains, so there is nothing to check here.
3. **The bound repository is the one you selected.** Open it on GitHub and confirm it's the
   repository you picked on [06](06-first-domain.md). Don't expect to find `.github/workflows/`
   files yet: Studio seeds the CI workflow bundle into this repository when you clone your
   **first intent workspace**, not at domain creation or during GitHub Actions setup — that
   step is still ahead of you. See
   [08-getting-started-contributor](08-getting-started-contributor.md) for what an intent is.
   > **Applies to: DuckDB.** A DuckDB domain never receives a CI workflow bundle, at any
   > point — only the domain-owned skeleton files. An empty `.github/workflows/` here isn't
   > something to fix; it's expected for DuckDB, before and after your first intent.
4. **Re-run readiness if anything is unclear.**
   - If the domain is `Active` and a step in the Provisioning steps list shows `Failed`
     (either soft step described above), re-running **Set up GitHub Actions** is the
     idempotent retry — it re-checks that step without disturbing the ones that already
     succeeded.
   - If the domain is `Pending` or `Failed`, select **Retry provisioning** instead — the same
     idempotent retry from [06](06-first-domain.md).

   One difference from domain creation is worth knowing: when your domain was created,
   Studio ran its binding check first and waited for it before starting the rest.
   Re-verification does not work that way — its checks run concurrently, and a check that
   fails does not stop the others. So a re-run can surface several failures at once rather
   than one at a time. Read the whole Domain verification failures list, not just the first
   entry.

## Per-platform confirmation

> **Applies to: Microsoft Fabric.** Skip if you chose DuckDB or MotherDuck.

Confirm the federated credential exists for **this repository**. It is scoped per repository,
so a credential created for a different domain does not count. The subject your Entra
administrator registers must be the literal string
`repo:<org>/<repo>:ref:refs/heads/main` — always `main`, regardless of what branch this
repository actually defaults to. Studio's check only matches that exact subject. If the
Provisioning warnings box reports this step as failed, that means the credential is missing
or was registered with the wrong subject.

**If your repository's default branch is not `main`, edit the command before you run it.**
The remediation command in the warning message builds its subject from your repository's
actual default branch, not from the literal `main` the check above requires. The two agree
only when your default branch happens to be `main`. Before running the command, check the
`subject` field it contains — if it ends in anything other than `ref:refs/heads/main`,
replace that branch name with the literal `main` first. Running the command unedited on a
non-`main` repository creates a credential the check will keep rejecting, and you'll see the
same warning again.

> **Applies to: MotherDuck.** Skip if you chose DuckDB or Microsoft Fabric.

There is no check available at this point in the journey that proves a query runs. That
proof needs your domain repository's CI workflow, and — like the workflows check in step 3
above — that workflow isn't seeded into your repository until you clone your **first intent
workspace**. Confirming the MotherDuck extension actually loaded and the seeded
`MOTHERDUCK_TOKEN` actually works is real, and it matters, but it happens on that first
intent run, not as part of this page's `Active`-and-steps-succeeded checklist. Don't treat
its absence here as something unresolved on this page.

> **Applies to: DuckDB.** Skip if you chose MotherDuck or Microsoft Fabric.

Confirm the database file was created. Studio manages the path for you, under
`DATA_DIR/duckdb/` — not the root of the data directory — and where that data directory
lives depends on your deployment style:

- **Local Docker** — under the operator machine's data directory, `~/.vibedata/studio` by
  default (or wherever `DATA_DIR` was set when Studio was installed). The file is at
  `~/.vibedata/studio/duckdb/` under that default.
- **Kubernetes on Azure** — under the in-cluster `/data` volume, backed by the Azure Files
  share from [01d-prereqs-azure-infra](01d-prereqs-azure-infra.md). The file is at
  `/data/duckdb/` inside that share.

> A domain reporting `Active` here does not rule out one more thing: Studio opens each
> DuckDB connection directly against the file, with no locking or single-writer
> coordination layered on top beyond `READ_ONLY` reads. Two writers reaching the same file
> at the same time contend on the file itself — a real runtime failure mode that only shows
> up once concurrent writers actually collide, not at binding time and not at verify time.
> This is a property of how a DuckDB file is shared, not a defect in your setup, and the
> underlying mechanism is identical on both deployment styles. The practical exposure
> differs: under **Kubernetes on Azure**, Studio's backend runs as multiple replicas across
> nodes, all mounted to the same shared `/data` volume, so colliding writers can come from
> different pods; under **Local Docker**, Studio runs as a single backend process, so the
> same collision can only come from two concurrent requests within that one process —
> narrower, but not impossible. See [90-troubleshooting](90-troubleshooting.md) for what
> this looks like and how to recover.

## One thing that looks broken and is not

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker — there is no Argo CD
> and no `studio-obot` application there.

If you look at the cluster's Argo CD applications — and you may well have, because the
installer's own guidance points you at `kubectl -n argocd get applications` whenever an
install is blocked — you will probably see this:

```
studio-obot   ...   Degraded
```

**This is not something you caused, but it is not finished either.** The `obot` component
reports `Degraded` because of a defect in `v0.1.26`: the installer never creates the
`obot-tunnel-peer` object that `obot` cannot boot without, even though the vault secret behind it
is present and correct.

The checks on this page still pass — none of them depend on `obot`, and the installer waits on
`studio-app` only, which is why your install reported success. **But your team cannot start a
conversation on an activated intent until this is fixed**, and that is what the domain you just
validated exists to do.

Confirm which case you are in:

```
kubectl -n studio get externalsecret obot-tunnel-peer
```

`NotFound` confirms the defect.

**Upgrading will not fix this yet.** No released CLI creates the `obot-tunnel-peer` object —
not `v0.1.26`, and not `v0.1.27`, `v0.1.28` or `v0.1.29`. The installer that renders it exists
only in unreleased development builds, so re-running the install from any published version
changes nothing here. Check what is currently published before you plan an upgrade around this.

**Do not roll back, re-run the install from `v0.1.26`, or change vault secrets** — none of those
creates the missing object either. Use the manual workaround: see
[90-troubleshooting](90-troubleshooting.md) for the full entry and the manual workaround. Its cost
is narrower than it may sound: the missing secret object survives Argo CD sync on its own, and
only the accompanying Deployment patch requires turning off automated sync for that one
application until you upgrade.

## What's next

Your domain is ready. Continue to
[08-getting-started-contributor](08-getting-started-contributor.md) to learn how work happens
inside a domain, then [09-worked-example-salesforce](09-worked-example-salesforce.md) to walk
one example end to end.
