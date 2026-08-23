# Verify the first Domain

Do not treat Domain creation as the final check. Verify both Domain readiness and the separate CI/CD prerequisites you intend to use.

## 1. Check the Domain state

Open **Settings → Domains → <your Domain>**.

For a fully usable Domain, the required human and service lanes must be ready for the operations you intend to run.

A required service identity left as **deferred** is not a harmless cosmetic warning. Current Domain-create UI states that Intents cannot activate until the service identity is configured.

## 2. Use Verify deliberately

Current Studio does not re-run full Domain verification simply because you reopened Settings.

For an Active Domain, use the supported **Verify** action to check current external readiness.

For a Domain that failed provisioning, use **Retry provisioning** after fixing the underlying cause.

Do not repeatedly recreate the Domain as a first troubleshooting step. The persisted diagnostics are intended to tell you which external prerequisite is wrong.

## 3. Verify GitHub repository access

Confirm the bound repository is the one you selected and still exists.

On Kubernetes, repository access is bounded by:

- the selected GitHub App installation;
- the App's repository selection;
- the App's approved permission map;
- the acting user's GitHub authorization where the operation is user-driven.

On Local Docker, it is bounded by the imported `gh` CLI credential and that GitHub account's repository permissions.

## 4. Verify the data-platform resource

### DuckDB

> **Applies to: DuckDB.**

Confirm the Studio-managed database file exists under Studio's data directory and the selected schema can be opened.

No external data-platform credential is required.

### MotherDuck

> **Applies to: MotherDuck.**

Verify that:

- the acting user PAT can reach the bound database or configured Share;
- the Domain service PAT can perform the unattended operations expected of it;
- the selected schema exists;
- MotherDuck plan/retention constraints do not prevent the per-Intent clone.

A PAT that authenticates successfully but cannot see the bound database is not enough.

### Microsoft Fabric

> **Applies to: Microsoft Fabric.**

Verify that:

- the acting user can reach the persistent workspace, Lakehouse, SQL endpoint, and schema;
- the Domain service principal can reach the persistent workspace;
- the selected ephemeral capacity exists and has capacity for temporary workspace creation;
- the service principal has the rights needed for its unattended operations.

Current Studio's persistent-workspace access step is verify-only. It does not silently grant a missing persistent workspace role.

## 5. Verify GitHub Actions setup separately

For MotherDuck and Fabric Domains that use CI/CD, run or review the Domain's GitHub Actions setup flow.

Repository profile materialization and platform-specific CI checks are separate from the basic Domain resource binding. A Domain can have valid core provisioning while GitHub Actions setup is incomplete.

### Fabric federated credential

> **Applies to: Microsoft Fabric.**

The expected Entra federated credential is pinned to the Domain repository and the Domain's **recorded default branch**:

```text
repo:<org>/<repo>:ref:refs/heads/<default-branch>
```

The old rule that this must always end in `refs/heads/main` is obsolete.

Studio verifies the credential. If it is missing or invalid, use the remediation Studio reports to create or replace it on the Domain service principal's Entra application.

### Fabric deployment role

Successful OIDC federation proves identity, not authorization. The CI service identity must still have enough Fabric workspace access for the deployment operation.

A workflow can therefore pass token exchange and fail on its first Fabric operation. Fix the Fabric role rather than changing the federated credential when that is the failure.

## 6. Verify an LLM turn

Open an Intent and run a simple question or bounded task using the intended LLM Profile.

An LLM Profile save includes a connection test, but an actual Intent turn is the end-to-end proof that:

- the profile is selectable;
- the runtime can reach the provider;
- the configured model supports the requested runtime behavior.

## 7. Verify an Intent can activate

Create an Intent in the Domain and ensure its runtime can become usable.

This is the first real proof of the Domain's ephemeral-resource path:

- Fabric creates an ephemeral workspace/Lakehouse/schema and applies the required service-principal grant;
- MotherDuck creates or resolves the isolated clone path;
- DuckDB creates the isolated local runtime resource.

If activation fails, use the exact data-platform diagnostic before looking at the chat layer.

## 8. Kubernetes deployment health

> **Applies to: Kubernetes on Azure.**

The installer already requires enabled companion applications to become healthy, but verify the cluster after setup:

```bash
kubectl -n argocd get applications
kubectl -n studio get pods
```

`studio-obot` being degraded is a real condition to investigate on current `main`, not an expected successful-install state.

## Done criteria

For the first usable Domain, confirm:

- Studio deployment is healthy;
- a real user can sign in where delegated auth applies;
- GitHub repository access works;
- the Domain's required human/service lanes are ready;
- the persistent data resource is reachable;
- an Intent can activate;
- an LLM turn succeeds;
- CI/CD-specific checks are green if you intend to use CI/CD.

Then continue to [[Getting Started as a Contributor]].

---

_Applies to: studio/main (unreleased snapshot). Verified against `studio@5c9d2bbf339a` on 2026-08-22._
