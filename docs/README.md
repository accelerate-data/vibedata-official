---
applies-to: vibedata v0.1.26
verified-against: studio@653beeced
verified-on: 2026-08-05
sources:
  - docs/functional/container-deployment/README.md
  - docs/design/kubernetes-deployment/cloud.md
  - README.md
  - cli/vibedata/src/vibedata/main.py
  - cli/vibedata/src/vibedata/commands/install.py
  - src/server/modules/data-platforms/providers/descriptor-catalog.ts
  - src/server/modules/data-platforms/providers/registry.ts
  - cli/vibedata/src/vibedata/templates/env.j2
---

# VibeData Studio: Deployment and Onboarding

VibeData Studio is a workspace where an AI agent helps a data team build, test, and run
data pipelines against a connected data platform, with changes tracked through a connected
GitHub repository. This guide takes a reader with no access to any private Accelerate Data
repository from an empty machine to a first domain: created, connected to a data platform,
wired to GitHub, and validated.

## Pick your combination

Two choices shape everything that follows. Pick one deployment style and one data platform.

| Axis | Choices |
| --- | --- |
| Deployment style | Local Docker · Kubernetes on Azure |
| Data platform | DuckDB · MotherDuck · Microsoft Fabric |

Studio implements both deployment styles and registers all three data platforms as backends.
All six combinations below are documented to equal depth. None is recommended over another.

| Deployment style | Data platform |
| --- | --- |
| Local Docker | DuckDB |
| Local Docker | MotherDuck |
| Local Docker | Microsoft Fabric |
| Kubernetes on Azure | DuckDB |
| Kubernetes on Azure | MotherDuck |
| Kubernetes on Azure | Microsoft Fabric |

**Local Docker** runs Studio as containers on one machine, using the `vibedata` CLI's
`install compose` command. It has no SSO — the single operator signs in as the host's own
GitHub identity.

**Kubernetes on Azure** runs Studio on an existing AKS cluster, using the `vibedata` CLI's
`install kubernetes` command. It supports multiple users signing in through Microsoft Entra
SSO.

## Which admin pages your combination needs

Studio has one operator and up to five administrators, each holding rights that usually sit
in a different team: Entra, Fabric, GitHub, Azure infrastructure, and MotherDuck. Each admin
page is a self-contained request the operator forwards to the person who holds that role. No
combination needs all five.

| Combination | Admin pages |
| --- | --- |
| Local Docker + DuckDB | `01d-prereqs-azure-infra` (Foundry only) |
| Local Docker + MotherDuck | `01d-prereqs-azure-infra` (Foundry only) · `01e-prereqs-motherduck-admin` |
| Local Docker + Microsoft Fabric | `01a-prereqs-entra-admin` · `01b-prereqs-fabric-admin` · `01d-prereqs-azure-infra` (Foundry only) |
| Kubernetes on Azure + DuckDB | `01a-prereqs-entra-admin` (SSO only) · `01c-prereqs-github-org-owner` · `01d-prereqs-azure-infra` |
| Kubernetes on Azure + MotherDuck | `01a-prereqs-entra-admin` (SSO only) · `01c-prereqs-github-org-owner` · `01d-prereqs-azure-infra` · `01e-prereqs-motherduck-admin` |
| Kubernetes on Azure + Microsoft Fabric | `01a-prereqs-entra-admin` · `01b-prereqs-fabric-admin` · `01c-prereqs-github-org-owner` · `01d-prereqs-azure-infra` |

What each admin page is for:

- [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md) — Entra admin. The page has a Fabric
  section (applies when your data platform is Microsoft Fabric) and a Studio-SSO section
  (applies when your deployment style is Kubernetes on Azure). The `(SSO only)` marker in
  the table above means only the SSO section applies to that row — it does not mean skip the
  page. If your data platform is Microsoft Fabric, read the Fabric section regardless of
  deployment style.
- [01b-prereqs-fabric-admin](01b-prereqs-fabric-admin.md) — Fabric admin. Applies only when
  your data platform is Microsoft Fabric.
- [01c-prereqs-github-org-owner](01c-prereqs-github-org-owner.md) — GitHub org owner. Applies
  only when your deployment style is Kubernetes on Azure. Under Local Docker, Studio uses the
  operator's own GitHub sign-in instead, and no organisation owner action is needed.
- [01d-prereqs-azure-infra](01d-prereqs-azure-infra.md) — Azure infrastructure owner. This
  page has two independent parts. Its infrastructure requests (AKS, storage, Key Vault,
  front door, DNS) apply only to Kubernetes on Azure. Its Azure AI Foundry request — the LLM
  provider every combination configures — applies to all six combinations; that is what the
  `(Foundry only)` marker means on the three Local Docker rows above.
- [01e-prereqs-motherduck-admin](01e-prereqs-motherduck-admin.md) — MotherDuck org admin.
  Applies only when your data platform is MotherDuck.

## Reading path

Follow this order. Skip the admin pages your combination does not need, and skip whichever
of `03-deploy-docker`/`04-deploy-kubernetes-azure` does not match your deployment style.

1. The admin pages listed above for your combination — forward each one to the person who
   holds that role.
2. [02-prereqs-operator](02-prereqs-operator.md) — what the operator installs and signs into
   before deploying.
3. [03-deploy-docker](03-deploy-docker.md) for Local Docker, or
   [04-deploy-kubernetes-azure](04-deploy-kubernetes-azure.md) for Kubernetes on Azure.
4. [05-configure-org](05-configure-org.md) — organisation-level setup: LLM profile, data
   platform, GitHub App, users.
5. [06-first-domain](06-first-domain.md) — create and bind the first domain.
6. [07-verify](07-verify.md) — confirm the domain is done.

If something goes wrong along the way, check
[90-troubleshooting](90-troubleshooting.md).

## What this does not cover

This guide stops once the first domain is created, bound to a data platform, wired to
GitHub, and validated. It does not cover building pipelines, authoring intents, or ingesting
data into that domain — for those, continue with the Studio user guide:
<https://accelerate-data.github.io/studio/>.

Upgrade, backup, and restore are not covered in this pass. They are planned for this same
doc set later.
