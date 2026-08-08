---
applies-to: vibedata v0.1.26
verified-against: studio@653beeced
verified-on: 2026-08-08
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

> **Applies to: MotherDuck and Microsoft Fabric on Kubernetes on Azure.** Skip if you chose
> DuckDB, or if you chose Local Docker.
>
> **Connect your own data platform account first, under User Settings → Data Platforms.**
> This is a different object from the connection you registered in `05`. The connection in
> `05` belongs to the organisation and holds the service credential. This one belongs to you
> personally and holds your own credential. Registering the first does not create the second.
>
> Do this before you open the create form. Without it, the Data Destination fields stay
> disabled and **Create Domain** refuses to submit, with the message *"Connect to the selected
> MotherDuck data platform in User Settings first"* — or the same message naming Fabric.
> Every person who will create a domain does this once, for themselves.

### GitHub access the repository needs

This applies to **all six combinations**, DuckDB included. Studio uses GitHub during
provisioning for every platform, not only for the platforms that later get CI variables.

Confirm before you start:

- **The identity creating the domain can write to the repository you will bind.** If that
  repository is empty, Studio creates the first commit in it — a single `README.md` on the
  repository's default branch, with the message `chore: initialize repo via Vibe Data
  Studio`. Without write access this is a hard failure and the domain lands `Failed`. If the
  repository already has at least one commit, Studio writes nothing and this does not apply.
- **The GitHub App has the permissions the flow uses.** Studio publishes no permission list,
  so check the installation against this table before you create the first domain.

| Permission | Level | Used for | When |
| --- | --- | --- | --- |
| Metadata | read | Reading the repository and its default branch | Every domain, every platform |
| Contents | write | Creating the first commit in an empty repository | Every platform, only when the bound repository is empty |
| Variables | read and write | Writing CI variables | MotherDuck and Microsoft Fabric, at GitHub Actions setup |
| Secrets | read and write | Writing CI secrets | MotherDuck and Microsoft Fabric, at GitHub Actions setup |
| Administration | read | Reading branch protection for the hygiene warning | MotherDuck and Microsoft Fabric, at GitHub Actions setup |

`Administration: read` is the one you can safely leave out. Without it, GitHub Actions setup
still completes; it just reports a warning that it cannot verify branch protection. Without
any of the other four, the matching step fails.

> **Applies to: Local Docker.** Skip if you chose Kubernetes on Azure. The table above
> describes a GitHub App, and you have none. Studio uses your own signed-in `gh` session
> instead, so what matters is the scopes on that session and your own write access to the
> repository you bind. The steps that need each level of access are the same.

## Open the domain creation form

As a `vibedata_owner`, open **Settings → Domains** and select **Add Data Domain**. Your first
domain must be created by a `vibedata_owner` specifically: a `domain_owner` can create further
domains too, but only because they already hold membership on an existing one — an ability
this first domain cannot grant in advance.

Fill in:

| Field | Notes |
| --- | --- |
| Name | Required. Studio derives a URL- and path-safe slug from it; the slug is permanent. |
| Icon | Pre-selected. Pick one of Studio's built-in icons — see the note below this table. |
| Description | Optional. |

The Icon field is not blank by default. Studio pre-selects the first icon in its list and
always submits one, so leaving the field alone gives you that icon rather than no icon.

Two fields Studio's create form does not expose at all — **colour** and **maximum concurrent
ephemeral workspaces** — take Studio's own defaults: colour `#6366f1`, and up to 5 concurrent
ephemeral workspaces. They differ in what you can do about that afterwards:

- **Maximum concurrent ephemeral workspaces** is editable from the domain's own settings once
  the domain exists.
- **Colour** is not. Studio has no colour editor on any screen. The value stays `#6366f1`
  unless someone changes it through a direct API call. Do not plan on setting it later.

Custom instructions are a third case: the create form has no field for them, and the domain's
settings does have one — add them there after creation.

## Git repository

Every combination binds a Git repository at create time. Open **GitHub Repository
Configuration** and pick an **Organization**, then a **Repository**,
from the dropdowns. Studio fills in the underlying fields from your selection — installation,
organisation name, repository ID, repository name, repository full name, and the default
branch — so you never type them directly.

**There is no Default branch field to fill in.** Studio takes the repository's real default
branch from your selection, and during provisioning it replaces that value with whatever
GitHub reports for the repository at that moment. You cannot set this to `main` by leaving
something blank, and you cannot set it at all. This matters later: Microsoft Fabric's
federated credential must name the literal `main` regardless of your repository's real default
branch — see the federated credential section below.

A repository can be bound to only one unarchived domain at a time. More precisely, the
uniqueness is on the pairing of installation and repository, so the same repository reached
through a different GitHub App installation counts as a separate binding.

**Studio may commit to the repository you bind.** If the repository is empty, provisioning
creates the first commit in it — see "GitHub access the repository needs" above.

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
database, the schema, the workspace, the lakehouse, the file name — is rejected
with the message *"Domain Workspace/resource binding is immutable after create"*. The only
remedy for a wrong value anywhere in this binding is creating a new domain.

Two things behave differently from that rule, in opposite directions:

- **Microsoft Fabric's optional capacity ID** is genuinely editable later. See that section
  below.
- **A DuckDB domain's Schema Name looks editable and is not.** The domain's settings panel
  renders it as an editable field. Saving a new value reports success and changes nothing —
  the domain keeps the schema it was created with. Treat the DuckDB schema as frozen at
  create, the same as every other binding field, and ignore the fact that the field accepts
  typing.

### DuckDB

> **Applies to: DuckDB.** Skip if you chose MotherDuck or Microsoft Fabric.

**The Database field is a picker over files that already exist, not a name you type.** On a
new deployment no DuckDB files exist yet, so the list is empty, the field cannot be typed
into, and **Create Domain** stays disabled with nothing on screen explaining why. This is the
step most likely to stop you.

Create the file first:

1. Select **New** beside the Database field.
2. The name is already filled in for you: `<your-domain-slug>.duckdb`, derived from the domain
   name you entered. Keep it or change it.
3. Submit the inline form. Studio creates the file and selects it in the picker.

Only then does **Create Domain** become available.

**Schema** defaults to `main` and is correct as it stands for DuckDB. Leave it unless you have
a reason to change it — and change it now if so, because it cannot be changed afterwards (see
the note above).

A name you create must be a bare filename — no slashes, no `..` — matching
`^[a-zA-Z0-9_-]+\.duckdb$` for the database, and `^[a-zA-Z0-9_]+$` for the schema.

The path is entirely server-managed: Studio resolves your filename under its own data
directory itself. You never enter a filesystem path, and you cannot point a domain at an
arbitrary location on the host. Studio shows you where the file will land, as
`DATA_DIR/duckdb/<your-file-name>`.

### MotherDuck

> **Applies to: MotherDuck.** Skip if you chose DuckDB or Microsoft Fabric.

Select the registered MotherDuck data platform from `05`, then pick or create a **Database**
and a **Schema**. Both are required. That is the whole binding — **there is no Share field on
this form.** Builds after `v0.1.26` add an optional Share picker here; on `v0.1.26` a domain
reaches its database by name alone, and nothing on this screen lets you name a Share.

**That does not mean Shares are irrelevant — it means you cannot choose one here.** Under
Kubernetes on Azure, Studio still runs a check asking whether the registered Service PAT can
reach the bound database, and a Share is one of the two ways to satisfy it. Because you cannot
pick the Share, it has to be arranged before you get here: either the Service PAT's own
identity owns the database, or a Share **named exactly like the database** has been granted to
it. Read the Pending check under "Create the domain" below before you create the domain, and
see
[01e-prereqs-motherduck-admin](01e-prereqs-motherduck-admin.md#4-create-a-share-and-grant-read).

### Microsoft Fabric

> **Applies to: Microsoft Fabric.** Skip if you chose DuckDB or MotherDuck.

Select the registered Fabric data platform from `05`, then pick or create a **Fabric
Workspace** and a **Lakehouse Name**, then a **Schema Name**. All three are required.

**Change the pre-filled Schema Name. It is wrong for Fabric.** Studio fills this field with
`main`, which is a DuckDB default applied to a Fabric form. A schema-enabled Fabric lakehouse
gets `dbo` by default. Studio accepts any non-empty value here, so **Create Domain** stays
available with the wrong value in the box, and the failure only appears afterwards: the
binding check fails and the domain lands `Failed`.

Use the `FABRIC_SCHEMA` value your Fabric administrator returned in
[01b-prereqs-fabric-admin](01b-prereqs-fabric-admin.md). If you do not have it, `dbo` is the
default for a lakehouse created the way that page instructs. Confirm it against the
lakehouse's own `defaultSchema` property rather than assuming.

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

**Two of the checks are the same for every platform, and both reach GitHub.** They run around
the platform-specific check, in this order:

1. `github_repository_exists` — Studio reads the bound repository. This runs **before** the
   platform check. A GitHub error here — the token cannot see the repository, the
   installation was removed, the repository was renamed — is a hard failure: **Failed**.
2. The platform-specific binding check, described per platform below.
3. `default_branch_materialization` — Studio records the repository's authoritative default
   branch and, if the repository is empty, creates the first commit in it. No write access
   means a hard failure: **Failed**.

This applies to DuckDB exactly as it does to MotherDuck and Microsoft Fabric.

What can fail, per platform:

- **DuckDB.** Studio checks that your filename resolves to a path it manages and that the
  schema is usable in that file. That check reaches no external system. The two GitHub steps
  above still run, so a DuckDB domain can land `Failed` on a GitHub error even though nothing
  about your data platform is wrong. If a DuckDB domain fails, read the diagnostic before
  assuming the problem is the file — it names the step that failed.
- **MotherDuck.** Picking your Database or Schema in the creation form each open a
  real MotherDuck connection immediately, to fetch the MotherDuck extension over
  `extensions.duckdb.org` — before you ever select **Create Domain**. If that host is
  unreachable — an egress-restricted or air-gapped network — you may see the picker itself
  fail while you're still filling in the form. If none of those connections ran, the same
  connection happens again during domain creation itself, and failing there fails domain
  creation outright: **Failed**, not Pending, and not a later surprise when someone first
  queries the domain.
  > **Applies to: MotherDuck on Kubernetes on Azure.** Skip if you chose Local Docker. A
  > separate, retryable check runs under the registered Service PAT's own identity. A failure
  > here leaves the domain **Pending**, not Failed. Under `Local Docker` this check is a no-op
  > that always records success, so it cannot produce a `Pending` MotherDuck domain.
  >
  > **The check is always resolved against the bound database's name**, because on `v0.1.26`
  > that is the only name the binding carries. The Service PAT must either **own** the bound
  > database, or hold a Share **of the same name**. Nothing you do on the create form changes
  > what this check asks.
  >
  > This is the case that catches people out: if you created the database under your own
  > personal MotherDuck identity and the Service PAT belongs to a service account, the Service
  > PAT owns nothing and sees nothing, and the domain lands `Pending`. The diagnostic reads
  > *"MotherDuck service read validation failed. Confirm the service PAT can access the bound
  > share, then retry."* — even though you were never offered a Share to bind. Read "the bound
  > share" as "the bound database". Fix it by creating a
  > Share named after the database and granting the Service PAT READ, or by making the Service
  > PAT's identity the database owner. See
  > [01e-prereqs-motherduck-admin](01e-prereqs-motherduck-admin.md#4-create-a-share-and-grant-read).
- **Microsoft Fabric.** Studio checks that the workspace and lakehouse you picked are still
  accessible and that the schema exists — under your own operating identity. A failure here
  (workspace or lakehouse deleted or inaccessible, schema missing) is **Failed**.
  > **Applies to: Microsoft Fabric on Kubernetes on Azure.** Skip if you chose Local Docker.
  > A second, separate step runs after the first, `fabric_workspace_grant`: Studio checks
  > whether the domain's M2M service principal already holds at least Viewer on the bound
  > workspace and, on `v0.1.26`, **assigns Viewer itself if it does not**. It makes that call
  > under **your own** Fabric credential, not the service principal's, so what fails here is
  > your own permission to assign a role — you need Member or Admin on that workspace. The
  > diagnostic says so: *"the calling account lacks permission. This check runs under your
  > credentials; a Domain Owner or Vibedata Owner can retry using their own access."* A failure
  > leaves the domain **Pending**, not Failed. Under `Local Docker` this step is a no-op that
  > always records success. Unreleased development builds change this step so it no longer
  > assigns anything and only verifies the service principal's read baseline, which would make a
  > Viewer grant a hard prerequisite. **No published release does that yet** — `v0.1.26` through
  > `v0.1.29` all still assign the role here.

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

**This action also checks the repository's branch rules, and can warn.** Before writing
anything, Studio reads the bound repository and its default-branch protection, then raises a
warning — not a failure — if any of these hold:

- The default branch is not protected.
- Delete-branch-on-merge is turned off.
- Studio cannot read the branch protection at all, because the identity lacks
  `Administration: read`.

The third is the one to expect, because that permission is easy to leave out. The warning
reads *"cannot verify default-branch protection (insufficient permission)"*. In every case the
variables and secrets are still written and the domain stays `Active`. Treat this as advice
about your repository settings, not as a sign that setup failed.

### The Fabric federated credential — required every time, and it never blocks

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
If you act on the overall result alone, nothing stops you — and the failure appears later, as
an OIDC token-exchange error the first time that repository's workflow actually runs.

**Studio does tell you, on the domain's own screen. Look for it.** After running the setup,
check two places in the domain's provisioning panel:

- The **provisioning steps checklist**, where `fabric_federated_credential` shows as `Failed`.
- The amber **provisioning warnings** box, which carries Studio's own remediation text —
  including a ready-to-run `az ad app federated-credential create` command with your
  application ID, credential name, and repository already filled in.

Use that command rather than composing the request by hand — but check the subject first.
Studio builds it from your repository's real default branch, so on a repository that does not
default to `main` the printed command names the wrong branch and will not satisfy the check.
Replace that part of the subject with `refs/heads/main` before sending it.

Then continue to [07-verify](07-verify.md) to confirm this worked, rather than trusting
`Active` alone.

## What's next

Continue to [07-verify](07-verify.md) to confirm the domain is genuinely ready — not just
`Active` — before you start working in it.
