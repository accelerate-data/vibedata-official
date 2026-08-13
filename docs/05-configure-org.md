---
applies-to: vibedata v0.1.33
verified-against: studio@a121fc466
verified-on: 2026-08-13
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
| Profile name | 1–64 characters. Must start with a letter or number, and may then contain only letters, numbers, periods, underscores or hyphens — no spaces. It must not end in `.json`. The name must be unique across your organisation. Studio rejects anything else with a message naming the whole rule. On `v0.1.26` this field was called **Display name**, allowed up to 80 characters and accepted any of them, so a name chosen then may not be re-enterable now. |
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

**Everything else on this form is optional, and "empty" is a real setting.** `v0.1.33` added a
large set of execution controls — sampling, prompt caching, reasoning effort and budget, native
tool calling, per-token cost — plus tracked model-capability signals and metadata an agent uses
to pick between profiles. Leave them all empty. An empty field means **use default**: Studio
omits the setting entirely so the model's own default applies, which is what you want until you
have a reason to change it. Filling one in to "be explicit" replaces a sensible provider default
with your guess.

**Two of the new fields are Azure-only, and one of them you may need.** **API version** and
**API mode** are accepted for Azure Foundry and rejected for every other provider. Both can stay
empty — see the API version note at the end of this section.

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
3. **An API key is required.** This form accepts no other credential type, for any provider
   it offers — there is no managed-identity option anywhere on it. If you don't have a key
   yet, get one from whoever provisioned your Azure AI Foundry resource before starting this
   step.

If saving this profile fails, or a later request to it returns `404`, see
[90-troubleshooting](90-troubleshooting.md) before re-checking every field by hand.

**The API version is now yours to set, and the default moved.** Studio's default is
`2024-10-21`, and leaving the **API version** field empty uses it. On `v0.1.26` the version was
fixed at `2024-08-01-preview` with no field at all.

Setting it explicitly is worth doing only if your Azure AI Foundry resource requires a specific
version. The reason to leave it empty is that the same value now flows everywhere — the save-time
check, every probe, and the running agent session all target one version. On `v0.1.26` they did
not: the form validated against its fixed version while agent chat supplied its own, so a profile
that saved successfully was no proof that chat would work. That gap is closed, but
[07](07-verify.md) is still where you confirm chat end to end.

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

**If you leave the checkbox checked, the M2M application must carry a redirect URI.** Keeping
one application for both roles means Studio runs an interactive, browser-based sign-in against
your **M2M** app — and an application registered for service credentials alone has no reply
address. Registration succeeds without one, so nothing fails here. It fails when the first
person tries to connect their own Fabric access, with:

```
AADSTS500113: No reply address is registered for the application
```

Confirm with your Entra administrator that the app registration you are about to enter carries
**both** of these as **Web** redirect URIs before you save this connection:

```
https://<STUDIO_DOMAIN>/api/auth/fabric/callback
https://<STUDIO_DOMAIN>/api/v1/data-platforms/validation/callback
```

That ask is on [01a-prereqs-entra-admin](01a-prereqs-entra-admin.md), along with the delegated
permissions the same application needs. A real deployment hit both, one after the other, at
this exact point.

**The two fail at different moments, which is why one is easy to miss.** Saving this connection
runs a validation sign-in against the **second** URI. So a registration carrying only the first
lets your team sign in perfectly well and then rejects your save with:

```
AADSTS50011: The redirect URI 'https://<STUDIO_DOMAIN>/api/v1/data-platforms/validation/callback'
specified in the request does not match the redirect URIs configured for the application
```

That error names the Azure portal, not Studio, so it reads as an infrastructure problem rather
than a missing prerequisite on this page.

**If you are upgrading rather than installing fresh, re-check this.** Studio began sending the
validation URI at `v0.1.32`. A registration built for an earlier release was complete when it
was made and stopped being complete at that upgrade, with nothing to announce it — the gap
appears the first time somebody saves a data platform, which may be weeks later.

**Whoever adds it must pass both URIs at once.** `az ad app update --web-redirect-uris` replaces
the list rather than adding to it, so passing only the new URI removes the existing one and
breaks Fabric sign-in.

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

Open **Org Settings → GitHub** — the panel that configures the GitHub Commit Provider. The
panel has six inputs. Four of them take the values your GitHub organisation owner sent back
after [01c-prereqs-github-org-owner](01c-prereqs-github-org-owner.md):

| Field | Value |
| --- | --- |
| Client ID | `GITHUB_APP_CLIENT_ID` |
| Client secret | `GITHUB_APP_CLIENT_SECRET` |
| App ID | `GITHUB_APP_ID` |
| Private key | `GITHUB_APP_PRIVATE_KEY` |
| Default installation ID | Optional. Leave it empty unless your GitHub organisation owner also returned `GITHUB_APP_INSTALLATION_ID`. If they did, enter the bare number and nothing else — Studio rejects any value that is not a positive integer, in the browser, before it sends anything. |
| Status | Leave it at **Active**. **Archived** retires a connection you already configured; it has no role in first-time setup. |

**There are three values to enter and no Test button.** Enter the Client ID, client secret and
private key from
[01c-prereqs-github-org-owner](01c-prereqs-github-org-owner.md), then **Save**. There is no App
ID field: Studio authenticates as the App with the Client ID and private key, asks GitHub who
that App is, and stores the App's numeric ID and slug from the answer.

**Save is the check.** It calls GitHub before it stores anything, so a wrong Client ID or a
malformed private key fails the save with a message naming which: *"Could not authenticate as
the GitHub App with the provided Client ID and private key."* No browser window opens, and there
is nothing to run afterwards to confirm it worked. A save that succeeds has already proved the
App credentials.

> **Applies to: releases before v0.1.33.** Earlier releases had a separate **Test** button that
> opened GitHub in a popup, and a **GitHub App ID** field alongside the Client ID. Save stored
> values without contacting GitHub, so Test was the only proof the credentials worked, and it
> had to be run after every Save. Both are gone: there is no `/test` endpoint and no App ID
> field on `v0.1.33`.

The panel shows **one** callback URL, `/api/v1/connect/github-commits/callback`. Register
exactly that one URL on the GitHub App — step 4 of
[01c-prereqs-github-org-owner](01c-prereqs-github-org-owner.md) covers it.

**Saving does not check the callback URL, and cannot.** Only one flow uses it: a person linking
their own GitHub account. So an unregistered or mistyped callback URL passes this step silently
and fails later, for somebody else, with `redirect_uri_mismatch`. Confirm it is registered from
the GitHub side rather than expecting Studio to tell you.

**A successful save does not prove your team can use this connection either.** It proves the App
credentials are valid, nothing about who may authorize the App. That is decided by the App's
visibility, a setting on GitHub that this panel neither shows nor controls: a private App can be
authorized only by members of the organisation that owns it, and a private App owned by a
personal account only by that one person. If some of your users are outside that organisation —
or the App was registered under a personal account — the App must be set to **Any account**.
Step 7 of [01c-prereqs-github-org-owner](01c-prereqs-github-org-owner.md) covers it, and the
symptom is in [90-troubleshooting](90-troubleshooting.md).

## Step 4: Users

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

If you chose Local Docker, skip this step entirely. Signing in with your own `gh` session
already made you `vibedata_owner`, the one operator this deployment has, as described in
[03-deploy-docker](03-deploy-docker.md) — there is nothing further to configure. Studio hides
the **Add user** button on this deployment style and says why: without delegated authentication
there is no second identity that could sign in against a new record. Existing users and their
access stay manageable. On `v0.1.26` and `v0.1.27` the button was shown and the record could be
created — it simply bought nobody anything; the gating arrived at `v0.1.28`. There is no Entra SSO provider to register here either —
the rest of this step applies only to Kubernetes on Azure.

### Register the Entra SSO provider

Open **Org Settings → SSO Providers** and register Microsoft Entra as a sign-in provider with
the values your Entra administrator sent back in
[01a-prereqs-entra-admin](01a-prereqs-entra-admin.md):

| Field | Value |
| --- | --- |
| Display name | Required. Any name you choose — it labels this connection on Studio's sign-in page. Nothing in `01a` supplies it. |
| Tenant ID | `TENANT_ID` |
| Client ID | `ENTRA_SSO_CLIENT_ID` |
| OAuth client credential | `ENTRA_SSO_CLIENT_SECRET` |

The fields appear in that order on the form. Two of these names are easy to get wrong:
**Display name** is required, so leaving it empty stops you saving; and the secret field is
labelled **OAuth client credential**, not "Client secret" — Entra calls the same value a
client secret, and the GitHub panel in Step 3 labels its own secret that way, but this form
does not.

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
