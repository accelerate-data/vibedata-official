---
applies-to: vibedata v0.1.26
verified-against: studio@653beeced
verified-on: 2026-08-05
sources:
  - src/shared/schemas.ts
  - src/server/modules/domains/services/create-domain.service.ts
  - src/server/modules/domains/helpers/domain-create-binding.ts
  - src/server/modules/domains/helpers/duckdb-path.ts
  - src/server/modules/data-platforms/providers/duckdb-local.schemas.ts
  - src/server/modules/data-platforms/providers/motherduck.provider.ts
  - src/server/modules/data-platforms/providers/motherduck-sql.ts
  - src/server/modules/data-platforms/providers/fabric.provider.ts
  - src/server/modules/domains/services/domain-provisioning.service.ts
  - src/server/modules/domains/services/domain-provisioning-runner.service.ts
  - src/server/modules/domains/services/domain-provisioning-step.ts
  - src/server/modules/domains/services/domain-gha-setup.service.ts
  - src/server/modules/domains/helpers/domain-repository-values.ts
  - src/server/modules/domains/helpers/domain-binding-key.ts
  - src/shared/data-platform-kinds.ts
  - src/server/lib/graph/federated-credential-client.ts
  - src/server/modules/domains/routers/domains-crud.router.ts
  - src/server/modules/domains/routers/domain-provisioning.router.ts
  - src/server/config/auth-enabled.ts
  - src/features/settings/components/Settings/panels/domain-settings/DomainsIndexSection.tsx
  - src/features/settings/components/Settings/modals/DomainModal.tsx
  - src/features/settings/components/Settings/modals/FabricConfigSection.tsx
  - src/features/settings/components/Settings/modals/MotherDuckConfigSection.tsx
  - src/features/settings/components/Settings/modals/MotherDuckShareField.tsx
  - src/features/settings/components/Settings/modals/DuckdbConfigSection.tsx
  - src/features/settings/components/Settings/modals/domain-destination/fabric.tsx
  - src/features/settings/components/Settings/modals/domain-destination/fabric-views.tsx
  - src/features/settings/components/Settings/modals/domain-destination/motherduck.tsx
  - src/features/settings/components/Settings/modals/domain-destination/duckdb.tsx
  - src/features/settings/components/Settings/modals/domain-destination/shared.tsx
  - src/features/settings/components/Settings/panels/CreateDomainGitConfigPanel.tsx
  - src/features/settings/components/Settings/panels/domain-settings/DomainProvisioningSection.tsx
  - docs/functional/domain/README.md
  - docs/design/domain/provisioning.md
---

# Create your first domain

This page continues from [05-configure-org](05-configure-org.md). Your organisation is
configured: the LLM profile exists, a data platform is registered, and — on `Kubernetes on
Azure` — the GitHub App and your first `vibedata_owner` are in place. This page creates your
first domain and connects it to a Git repository. It applies to **all six combinations**; the
data platform you chose determines which binding fields you fill in.

## Before you start

Confirm these are already true:

- GitHub App installed on the organisation, from [05-configure-org](05-configure-org.md)
  (`Kubernetes on Azure` only — under `Local Docker` there is no GitHub App, and your own
  signed-in `gh` session stands in instead).
- A secret store is registered. This needs no setup on your part — every deployment always
  has at least the built-in local store, automatically, so this is satisfied even if you
  never touched Org Settings for it.
- Your data platform is registered, from [05-configure-org](05-configure-org.md) —
  MotherDuck or Microsoft Fabric. If you chose DuckDB, this is already satisfied: it's
  pre-registered with nothing to configure.
- The instance LLM profile is set, from [05-configure-org](05-configure-org.md). A domain
  can still be created and reach `Active` without one, but skip ahead to the warning under
  GitHub Actions setup below before you rely on that.

## Open the domain creation form

As a `vibedata_owner`, open **Settings → Domains** and select **Add Data Domain**. Your first
domain must be created by a `vibedata_owner` specifically: a `domain_owner` can create further
domains too, but only because they already hold membership on an existing one — an ability
this first domain cannot grant in advance.

Fill in:

| Field | Notes |
| --- | --- |
| Name | Required. Studio derives a URL- and path-safe slug from it; the slug is permanent. |
| Icon | Optional. Pick one of Studio's built-in icons. |
| Description | Optional. |

Two fields Studio's create form does not expose at all — **colour** and **maximum concurrent
ephemeral workspaces** — take Studio's own defaults (colour `#6366f1`; up to 5 concurrent
ephemeral workspaces). Set them later from the domain's own settings once it exists. Custom
instructions work the same way: the create form has no field for them — add them from the
domain's settings after creation.

## Git repository

Every combination binds a Git repository at create time. Open **GitHub Repository
Configuration** and pick an **Organization**, then a **Repository**,
from the dropdowns. Studio fills in the underlying fields from your selection — installation,
organisation name, repository ID, repository name, and repository full name — so you never
type them directly. Default branch is optional; if you leave it blank, Studio records `main`.

A repository can be bound to only one unarchived domain at a time.

> **Applies to: Local Docker.** Skip if you chose Kubernetes on Azure. There is no GitHub App
> to pick an installation from. The dropdowns instead list the organisations and repositories
> your own signed-in `gh` session can see.

If Studio asks you to connect GitHub before it shows any organisations, do that first. This
needs nothing set up in advance — it's a one-time, per-operator, in-app step, separate from
the org-level GitHub App from `05`, and Studio walks you through it right when it asks.

## Secret store

Every combination binds a secret store at create time. Pick the registered secret store this
domain will use for its source-connection secrets. This
choice is independent of your data platform, and it is **write-once**: you cannot change it
after the domain is created.

## Data platform

Open **Data Destination** and pick exactly one platform. Only the section for the platform
you registered in `05` is usable here.

**The resource you bind here is fixed for the life of the domain.** Studio compares the entire
bound resource as one unit, not field by field, so changing any part of it later — the
database, the schema, the workspace, the lakehouse, the Share, the file name — is rejected the
same way. There is no edit path for any of it. The only remedy for a wrong value anywhere in
this binding is creating a new domain. (Microsoft Fabric's optional capacity ID is the one
exception — see that section below.)

### DuckDB

> **Applies to: DuckDB.** Skip if you chose MotherDuck or Microsoft Fabric.

Studio suggests a **Database** file name derived from your domain's name
(`<your-domain-slug>.duckdb`) and a **Schema** of `main`. Accept both, or override either. An
override you create must be a bare filename — no slashes, no `..` — matching
`^[a-zA-Z0-9_-]+\.duckdb$` for the database, and `^[a-zA-Z0-9_]+$` for the schema.

The path is entirely server-managed: Studio resolves your filename under its own data
directory (`DATA_DIR/duckdb/`) itself. You never enter or see a filesystem path, and you
cannot point a domain at an arbitrary location on the host.

### MotherDuck

> **Applies to: MotherDuck.** Skip if you chose DuckDB or Microsoft Fabric.

Select the registered MotherDuck data platform from `05`, then pick or create a **Database**
and a **Schema**. Both are required. Optionally pick a **Share** — Studio lists only the
Shares your MotherDuck identity already holds read access to; you cannot type one in.

**The Share is the field most likely to catch you out here, because it's the one optional
field in this binding.** It's easy to assume you can add it later since it isn't required now
— you cannot. It's frozen along with the database and schema the moment you create the
domain. Leave it blank if only the database's owner will work in this domain; pick a Share now
if collaborators need to reach it too.

> **Applies to: MotherDuck on Kubernetes on Azure.** Skip if you chose Local Docker. This
> picker lists Shares under **your own** connected MotherDuck identity — a different
> identity from the registered **Service PAT** that the Pending check below verifies
> separately. Picking a Share here does not prove the Service PAT can also read it — see
> [01e-prereqs-motherduck-admin](01e-prereqs-motherduck-admin.md#4-create-a-share-and-grant-read-if-your-team-plans-to-use-one)
> for why both identities need their own grant.

### Microsoft Fabric

> **Applies to: Microsoft Fabric.** Skip if you chose DuckDB or MotherDuck.

Select the registered Fabric data platform from `05`, then pick or create a **Fabric
Workspace** and a **Lakehouse Name**, then a **Schema Name**. All three are required.
Optionally set **Ephemeral Workspace Capacity** — the Fabric capacity used for the
per-intent ephemeral workspaces this domain creates later. Picking an existing
capacity-backed workspace pre-fills this field automatically from that workspace's own
assigned capacity. It stays blank when the workspace you bound has no capacity of its own —
most commonly because you created it here rather than picking an existing one — and Studio
then falls back to the default capacity ID on the Fabric connection you registered in `05`,
if that connection has one set. If this field is blank and the connection has no default
either, the very next step — creating the lakehouse in that workspace — fails immediately,
not later ephemeral workspace creation. Set a capacity here or on the connection first if you
know it.

Unlike the fields above, the capacity ID is **not** part of the frozen binding. You can set or
change it later from the domain's own settings; doing so re-checks the workspace grant and
re-seeds the `FABRIC_CAPACITY_ID` CI variable rather than requiring a new domain.

## Create the domain

Select **Create Domain**. Studio validates your binding immediately, as part of creating the
domain — this is not deferred to a later check. The domain's **Provisioning status** shows one
of:

- **Active** — the domain is ready. Continue to GitHub Actions setup below (unless you chose
  DuckDB — see the note there).
- **Pending** — either a retryable check failed, or the provisioning run itself was
  interrupted or never finished. The second cause is not auth-gated and can happen under
  either deployment style; the first is narrower — only two specific checks can produce it,
  both scoped to `Kubernetes on Azure` — see the per-platform breakdown below. Select
  **Retry provisioning** in either case, once you've fixed the underlying cause if there
  was one.
- **Failed** — a hard check failed. The diagnostic names which one.

If you land in `Pending` or `Failed` and want to confirm the exact cause and fix before
retrying, see [90-troubleshooting](90-troubleshooting.md).

What can fail, per platform:

- **DuckDB.** Studio checks that your filename resolves to a path it manages and that the
  schema is usable in that file. There is no external system to reach and no further
  provisioning step after this check, so a DuckDB domain that passes it reaches `Active`
  immediately.
- **MotherDuck.** Picking your Database, Schema, or Share in the creation form each open a
  real MotherDuck connection immediately, to fetch the MotherDuck extension over
  `extensions.duckdb.org` — before you ever select **Create Domain**. If that host is
  unreachable — an egress-restricted or air-gapped network — you may see the picker itself
  fail while you're still filling in the form. If none of those connections ran, the same
  connection happens again during domain creation itself, and failing there fails domain
  creation outright: **Failed**, not Pending, and not a later surprise when someone first
  queries the domain.
  > **Applies to: MotherDuck on Kubernetes on Azure.** Skip if you chose Local Docker. A
  > separate, retryable check — whether the registered service PAT can read the bound
  > Share — runs only when delegated authentication is enabled. A failure here leaves the
  > domain **Pending**, not Failed. Under `Local Docker` this check is a no-op that always
  > records success, so it cannot produce a `Pending` MotherDuck domain.
- **Microsoft Fabric.** Studio checks that the workspace and lakehouse you picked are still
  accessible and that the schema exists — under your own operating identity. A failure here
  (workspace or lakehouse deleted or inaccessible, schema missing) is **Failed**.
  > **Applies to: Microsoft Fabric on Kubernetes on Azure.** Skip if you chose Local Docker.
  > A second, separate check runs after the first: whether the domain's M2M service principal
  > has at least Viewer access to the bound workspace. This check only runs when delegated
  > authentication is enabled. A failure here leaves the domain **Pending** — retryable once a
  > workspace admin grants that access — rather than Failed. Under `Local Docker` this check
  > is a no-op that always records success.

## Set up GitHub Actions

> **Applies to: MotherDuck and Microsoft Fabric.** Skip this whole section if you chose
> DuckDB — Studio has no GitHub Actions setup for DuckDB domains; there is nothing to run.

Once the domain is **Active**, open its settings and select **Set up GitHub Actions**. This
writes CI variables and secrets into the domain's repository:

| Platform | Variables | Secrets |
| --- | --- | --- |
| Microsoft Fabric | `TENANT_ID`, `SPN_CLIENT_ID`, `FABRIC_CAPACITY_ID` (only if you set a capacity ID), plus `LLM_API_URL` and `LLM_MODEL` if an instance LLM profile exists | `LLM_API_KEY` if an instance LLM profile exists — otherwise none |
| MotherDuck | `LLM_API_URL` and `LLM_MODEL` if an instance LLM profile exists — otherwise none | `MOTHERDUCK_TOKEN`, plus `LLM_API_KEY` if an instance LLM profile exists |
| DuckDB | none — this whole action does not exist for DuckDB domains | none |

**If no LLM profile exists yet when you run this** (see "Before you start" above),
`LLM_API_URL`, `LLM_MODEL`, and `LLM_API_KEY` are simply left out of what gets seeded — Studio
does not write them blank, and nothing reports an error at the time. The failure only surfaces
later, silently, the first time that domain's CI tries to call the LLM. Configure the LLM
profile before running this step to avoid it entirely.

Fabric CI authenticates over OIDC and never receives a client secret in the repository.

### The Fabric federated credential — required every time, and its check can lie

> **Applies to: Microsoft Fabric.** Skip if you chose DuckDB or MotherDuck.

Before GitHub Actions setup will actually work for this domain, a **per-repository** federated
credential must exist on the Fabric M2M application in Entra. This is not a one-time setup
step from `01a` — a new one is required for **every new Fabric domain**, because it names that
domain's specific repository. Studio never creates this credential; it only checks for it.

Send this request to your Entra administrator, giving them the exact subject string:

- **Issuer:** `https://token.actions.githubusercontent.com`
- **Audience:** `api://AzureADTokenExchange`
- **Subject:** `repo:<org>/<repo>:ref:refs/heads/main`

**The subject is always the literal `main` — never your domain's actual default branch.**
Studio's check only accepts an exact match against `refs/heads/main`, regardless of what
branch your repository actually defaults to. If your repository's default branch is not
`main`, request the credential with the subject above anyway; do not substitute your real
branch name.

**GitHub Actions setup reports success even when this credential is missing or wrong.**
Studio treats this check as a non-blocking warning: the domain still shows **Active**, the
setup action still reports success, and the CI variables and secrets above are still seeded.
Nothing in this flow tells you the credential is missing. The failure appears later, as an
OIDC token-exchange error the first time that repository's workflow actually runs. See
[07-verify](07-verify.md) for how to confirm this actually worked, rather than trusting
`Active` alone.

## What's next

Continue to [07-verify](07-verify.md) to confirm the domain is genuinely ready — not just
`Active` — before you start working in it.
