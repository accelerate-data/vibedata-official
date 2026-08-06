---
applies-to: vibedata v0.1.26
verified-against: studio@653beeced
verified-on: 2026-08-05
sources:
  - docs/functional/configure-llm-profile/README.md
  - docs/functional/instance-settings/README.md
  - docs/functional/data-platform/README.md
  - docs/design/sso-oauth-flows/README.md
  - docs/functional/sso-oauth-flows/README.md
  - src/server/modules/model-catalog/profile.schemas.ts
  - src/features/model-catalog/components/profile-form.tsx
  - src/server/modules/chat/openhands/side-channel-completion.ts
  - src/server/modules/auth/ability.ts
  - src/server/lib/auth/better-auth-config.ts
  - src/server/modules/data-platforms/data-platforms.schemas.ts
  - src/features/data-platforms/components/data-platform-editors/motherduck-editors.tsx
  - src/features/data-platforms/components/data-platform-editors/fabric-editors.tsx
  - src/features/data-platforms/components/data-platform-editors/registry.ts
  - src/server/modules/external-services/external-services.schemas.ts
  - src/server/modules/external-services/github-commit-provider.service.ts
  - src/features/settings/components/Settings/OrgSettingsPanel.tsx
  - src/server/modules/auth/sso-providers/sso-providers.schemas.ts
  - src/server/modules/auth/bootstrap-principal.ts
  - src/server/modules/auth/bootstrap-auth.middleware.ts
  - src/server/modules/auth/setup/setup.router.ts
  - src/server/modules/users/users.router.ts
  - src/server/modules/auth/oauth-clients/oauth-clients.router.ts
  - src/server/modules/domains/routers/domain-members.router.ts
  - src/shared/data-platform-kinds.ts
  - src/server/modules/domains/helpers/domain-repository-values.ts
  - src/server/modules/model-catalog/profile.service.ts
  - src/features/data-platforms/components/data-platform-editors/payload-builders.ts
  - src/features/auth/components/LoginPage.tsx
  - src/lib/bootstrap-auth.ts
  - src/lib/api.ts
  - src/server/modules/domains/services/create-domain.service.ts
  - src/server/modules/users/users.schemas.ts
---

# Configure the organisation

This page applies to **all six combinations**. It continues from either
[03-deploy-docker](03-deploy-docker.md) or
[04-deploy-kubernetes-azure](04-deploy-kubernetes-azure.md): Studio is running. Under `Local
Docker`, signing in already made you `vibedata_owner`, the one operator this deployment has.
Under `Kubernetes on Azure`, nobody holds a Studio role yet — the cluster booted in bootstrap
mode, and establishing your first `vibedata_owner` is the first thing this page walks you
through; see "Where to start, if you chose Kubernetes on Azure" below before you do anything
else. This page configures the instance before your team creates its first domain, in
[06-first-domain](06-first-domain.md).

All settings on this page live in **Org Settings**, inside Studio's own UI.

## Do this before you connect a domain

Configure the LLM profile — Step 1 below — **before** you connect a domain. Wait to run the
GitHub Actions setup on a domain until the LLM profile exists.

Here is why the order matters, for a **MotherDuck** or **Microsoft Fabric** domain. When that
domain's GitHub Actions setup runs, it seeds `LLM_API_URL`, `LLM_MODEL`, and `LLM_API_KEY`
into the domain's own repository, copied from the **instance-level** LLM profile you
configure in Step 1. If no LLM profile exists yet when that setup runs, all three keys are
simply **left out of what gets seeded** — not written as blank values — and **nothing reports
an error at the time.** The failure only surfaces later, silently, the first time that
domain's CI tries to call the LLM and finds no credentials. Configuring the LLM profile first
avoids this entirely.

A **DuckDB** domain never reaches this failure: Studio seeds no repository values of any kind
for DuckDB domains, `LLM_*` included. Configure the LLM profile first regardless of your data
platform anyway — Studio still needs it for chat inside Studio itself, on every combination —
but a DuckDB reader is not the one who can hit this particular silent failure.

The four steps below go in order for the same reason the rule above exists: Step 1 (LLM
profile) has to exist before any domain is created, Step 2 (data platform) is needed before a
domain can bind to it, and — on `Kubernetes on Azure` — so is Step 3 (GitHub App). Step 4
(users), also `Kubernetes on Azure` only, is where everyone past the first operator gets
access to do any of this themselves.

## Where to start, if you chose Kubernetes on Azure

> **Applies to: Kubernetes on Azure.** Skip this section if you chose Local Docker — signing
> in already made you `vibedata_owner`, so you can just work through Steps 1–4 in order below.

Right now, nobody holds a Studio role: the cluster booted in bootstrap mode, and the only
credential you have is the bootstrap key from `01d`'s Key Vault. Step 1 requires a
`vibedata_owner`, which you are not yet — so do part of Step 4 first, in this order:

1. On Studio's sign-in page, choose **Continue with bootstrap key** and enter it. Studio
   takes you straight to **Org Settings → SSO Providers**.
2. Register the Entra SSO provider there — see "Register the Entra SSO provider" under Step
   4 below.
3. Still in that same browser session — the bootstrap key stays attached to your requests
   until you sign in for real — go to **Org Settings → Users** and add yourself, by the
   email address you'll sign in with through Entra, with the `vibedata_owner` role. You have
   no Studio user record yet, so this creates one rather than editing an existing account.
4. Sign out, then sign back in through the Entra SSO connection you just registered. You are
   now a real, signed-in `vibedata_owner`.

Only after that, come back and work through Steps 1 to 3 below in order. Step 4's remaining
material — the four-role model and the bootstrap key's own broader reach — is worth reading
once you get there, for context on what you just did.

## Step 1: LLM profile

Every combination configures exactly one LLM connection, for Azure AI Foundry — the only LLM
provider this page configures, and the one every combination uses.

Only a `vibedata_owner` may create or edit an LLM profile. No other Studio role can manage
it. A `domain_owner` or `domain_contributor` can read it, through their membership on a
domain; `user_access_administrator` has no access to it at all, on its own. This is
instance-level configuration: there is no per-domain override, so whatever you set here
applies to every domain your organisation creates.

Open **Org Settings → LLM Profiles** and create a profile with these fields:

| Field | What to enter |
| --- | --- |
| Profile name | Any name you choose, for your own reference. |
| Provider | Azure Foundry. |
| API key | Required. Paste the API key for your Azure AI Foundry resource. There is no managed-identity option — a key is the only credential this connection accepts. |
| Base URL | `https://<resource-name>.openai.azure.com` — see the trap below. |
| Model | The Azure **deployment name** — see the trap below. |

`FOUNDRY_BASE_URL`, `FOUNDRY_API_KEY`, and `FOUNDRY_DEPLOYMENT_NAME` are the three values your
Azure subscription owner or contributor sent back after
[01d-prereqs-azure-infra](01d-prereqs-azure-infra.md). Enter them as Base URL, API key, and
Model respectively.

The form also shows an optional context-window size, an optional compaction-threshold
percentage, and a "default" checkbox. You do not need to touch the default checkbox: Studio
automatically promotes the very first profile you create to the default, so it is ready to
use — and it is the default profile that a domain's GitHub Actions setup reads from — the
moment it exists.

### Three things that go wrong here

1. **Base URL must be host-only, with no path.** Studio strips exactly one trailing slash
   from whatever you enter, then appends its own request path unconditionally. A value that
   already contains a path segment — for example, one ending in `/openai` — produces a
   doubled path and the connection fails. Enter exactly
   `https://<resource-name>.openai.azure.com`, nothing after the hostname.
2. **The Model field holds the deployment name, not the model family name.** There is no
   separate deployment-name field. If you deployed the model `gpt-4o` under the deployment
   name `docs-gpt4o` in Azure AI Foundry, enter `docs-gpt4o` here — entering `gpt-4o` instead
   fails.
3. **An API key is required.** Azure AI Foundry is the one provider on this form with no
   managed-identity option. If you don't have a key yet, get one from whoever provisioned
   your Azure AI Foundry resource before starting this step.

If saving this profile fails, or a later request to it returns `404`, see
[90-troubleshooting](90-troubleshooting.md) before re-checking every field by hand.

The API version this form uses to create and validate a profile is fixed at
`2024-08-01-preview` and is not exposed as a field here — you cannot change it. It governs
the checks this page runs against your Azure AI Foundry endpoint. Agent chat reaches the
same endpoint by a different path that supplies its own API version, so a profile that
saves here is not by itself proof that chat will work — [07](07-verify.md) is where you
confirm that.

## Step 2: Data platform

### DuckDB

> **Applies to: DuckDB.** Skip if you chose MotherDuck or Microsoft Fabric.

There is nothing to configure. DuckDB is pre-registered as a read-only entry, and Studio
has no editor for it in Org Settings — there is no form to fill in. Move on to Step 3.

### MotherDuck

> **Applies to: MotherDuck.** Skip if you chose DuckDB or Microsoft Fabric.

Open **Org Settings → Data Platforms** and register a MotherDuck connection with these
fields:

| Field | Required | Notes |
| --- | --- | --- |
| Name | Yes | For your own reference. |
| MotherDuck account | Yes | **Write-once.** You cannot change it after saving; to point at a different account, register a new connection instead. |
| Service PAT | Yes | Must have read-write access. Rotatable later without re-entering the account. |

You can register one connection per MotherDuck account, but as many accounts as you need —
there is no single global slot. `MOTHERDUCK_ACCOUNT` and `MOTHERDUCK_SERVICE_PAT`, from your
MotherDuck organisation administrator in
[01e-prereqs-motherduck-admin](01e-prereqs-motherduck-admin.md), go into MotherDuck account
and Service PAT above.

### Microsoft Fabric

> **Applies to: Microsoft Fabric.** Skip if you chose DuckDB or MotherDuck.

Open **Org Settings → Data Platforms** and register a Microsoft Fabric connection with these
fields:

| Field | Required | Notes |
| --- | --- | --- |
| Name | Yes | For your own reference. |
| Fabric tenant ID | Yes | **Write-once.** You cannot change it after saving. |
| Fabric default capacity ID | No, but set it now | Registering without it succeeds with no warning. A domain created later without its own capacity ID falls back to this value — but if neither this nor the domain supplies one, creating that domain's Lakehouse fails immediately, as part of domain creation itself. Set it now to avoid that. |
| M2M client ID / secret | Studio's form requires it under Kubernetes on Azure; optional under Local Docker | Studio's own form marks this field "optional; required for GHA" under Local Docker — you can register without it, but you need it to use GitHub Actions CI/CD on this connection. |

> **Applies to: Microsoft Fabric on Kubernetes on Azure.** Skip the rest of this section if
> you chose Local Docker — Studio's form does not show a U2M section at all under Local
> Docker; there is nothing there to leave blank, because the fields do not exist.

Under Kubernetes on Azure, the form also shows a "Use the same app for service (m2m) and user
(u2m) access" checkbox, **checked by default**, plus U2M client ID and secret fields. Leave
the checkbox checked and Studio registers your M2M credentials as the U2M credentials too —
one Entra application covers both, and you do not need the separate U2M app registration
`01a` describes unless you specifically want the two identities kept apart. Untick it to
enter a distinct U2M client ID and secret instead; U2M client ID is write-once.

You can register one connection per Microsoft Fabric tenant. `TENANT_ID`, `U2M_CLIENT_ID` /
`U2M_CLIENT_SECRET`, and `M2M_CLIENT_ID` / `M2M_CLIENT_SECRET` come from your Entra
administrator in [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md);
`FABRIC_CAPACITY_ID` comes from your Microsoft Fabric administrator in
[01b-prereqs-fabric-admin](01b-prereqs-fabric-admin.md). If you're on Local Docker and skipping
M2M for now because you don't need CI/CD yet, you can still request it later — nothing about
registering without it is permanent.

## Step 3: GitHub App

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

If you chose Local Docker, there is nothing to do in this step — skip to Step 4. Studio uses
your own signed-in GitHub identity instead of a GitHub App on that deployment style.

Open **Org Settings → GitHub** — the panel that configures the GitHub Commit Provider — and
enter the four values your GitHub organisation owner sent back after
[01c-prereqs-github-org-owner](01c-prereqs-github-org-owner.md):

| Field | Value |
| --- | --- |
| App ID | `GITHUB_APP_ID` |
| Client ID | `GITHUB_APP_CLIENT_ID` |
| Client secret | `GITHUB_APP_CLIENT_SECRET` |
| Private key | `GITHUB_APP_PRIVATE_KEY` |

Enter all four. App ID and private key must arrive together — Studio rejects one without the
other — and a client secret is effectively required the first time you save this connection.

## Step 4: Users

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

If you chose Local Docker, skip this step entirely — user management is not merely
unnecessary there, it is unavailable. Studio requires delegated authentication to manage
users at all; Local Docker runs without it, so any attempt is refused outright. Signing in
with your own `gh` session already made you `vibedata_owner`, the one operator this
deployment has, as described in [03-deploy-docker](03-deploy-docker.md) — there is nothing
further to configure.

### Register the Entra SSO provider

Open **Org Settings → SSO Providers** and register Microsoft Entra as a sign-in provider with
the values your Entra administrator sent back in
[01a-prereqs-entra-admin](01a-prereqs-entra-admin.md):

| Field | Value |
| --- | --- |
| Tenant ID | `TENANT_ID` |
| Client ID | `ENTRA_SSO_CLIENT_ID` |
| Client secret | `ENTRA_SSO_CLIENT_SECRET` |

### Entra controls sign-in, not what a person can do inside Studio

Registering Entra SSO controls **who can sign in** to Studio. It decides nothing about what a
signed-in person can then do. Studio reads no Entra app role and no Entra group claim, at
sign-in or ever — adding a user to an Entra group, or assigning them an app role on the
Studio app registration, grants that person **nothing** inside Studio.

What a person can do is decided entirely by a Studio role, assigned **by hand, per user, in
Org Settings → Users** — a separate, later action from registering the SSO provider above.
Studio has four roles:

- `vibedata_owner`
- `domain_owner`
- `domain_contributor`
- `user_access_administrator`

Because Entra grants no role automatically, assigning roles to new users is an **ongoing**
task as your team grows, not a one-time step you finish during this setup.

### The first administrator

The bootstrap key — the value your operator retrieved directly from the Key Vault in
[01d-prereqs-azure-infra](01d-prereqs-azure-infra.md) — matters here, but its reach is not
limited to this step. Presenting it authenticates a temporary,
request-scoped identity — no session is created, nothing is written to the database — with
broad administrative authority: it can manage users, manage domain membership on **any**
domain, manage SSO providers, manage external services (including the GitHub App from Step
3), and manage secret stores. It never reaches everything a `vibedata_owner` can do, but it
reaches well beyond "assign one role."

Treat it as a privileged credential for initial setup, not a routine login. Use it once, to
add yourself (or whoever should hold it) with the `vibedata_owner` role in Org Settings →
Users, then stop using it — every day-to-day administrative action after that
should go through a real, signed-in `vibedata_owner` or `user_access_administrator` account
instead. The bootstrap key itself never becomes a Studio role and is never persisted as one;
it exists only to get your organisation to the point where a real person holds one.

Under Local Docker, the bootstrap key has no effect. With delegated authentication off,
Studio treats it as meaningless and falls back to your ambient `gh` sign-in instead — which
is also why Local Docker has no bootstrap key of its own to hand out. Every role assignment
after that first one happens by hand, in Org Settings → Users, the same way for every user
your organisation adds afterward.

## What's next

With the LLM profile, data platform, and (on Kubernetes on Azure) GitHub App and users in
place, your organisation is configured. Continue to
[06-first-domain](06-first-domain.md) to create and bind your first domain.
