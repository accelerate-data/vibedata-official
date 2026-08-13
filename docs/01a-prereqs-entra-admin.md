---
applies-to: vibedata v0.1.33
verified-against: studio@a121fc466
verified-on: 2026-08-13
sources:
  - docs/functional/data-platform/fabric-backend.md
  - docs/functional/data-platform/README.md
  - docs/functional/gha-data-platform-oidc-flow/README.md
  - docs/functional/gha-data-platform-oidc-flow/oidc-mechanics.md
  - docs/functional/sso-oauth-flows/README.md
  - docs/design/identity-management/sso-oauth-flows/README.md
  - src/server/lib/auth/better-auth-config.ts
  - src/server/modules/auth/sso-providers/sso-providers.schemas.ts
  - src/server/modules/auth/sso-providers/sso-providers.service.ts
  - src/server/modules/user-data-platform-links/oauth-flow.ts
  - src/server/modules/user-data-platform-links/fabric-u2m-scopes.ts
  - src/server/modules/data-platforms/helpers/fabric-candidate-validator.ts
  - src/server/modules/secret-stores/helpers/secret-store-link-oauth-flow.ts
  - src/server/modules/secret-stores/helpers/azure-key-vault-candidate-validator.ts
  - src/server/lib/graph/federated-credential-client.ts
  - src/server/modules/data-platforms/providers/fabric.provider.ts
  - src/server/modules/data-platforms/data-platforms.schemas.ts
  - src/features/data-platforms/components/data-platform-editors/fabric-editors.tsx
  - src/features/data-platforms/components/data-platform-editors/payload-builders.ts
---

# Request for your Microsoft Entra administrator: Fabric app registrations and Studio SSO

Forward this page to whoever holds **Application Administrator** or **Cloud Application
Administrator** rights in your Microsoft Entra tenant. Nothing here requires access to
Studio or to any Accelerate Data system — only to your organisation's Entra tenant.

## Two independent requests on this page

This page carries two unrelated requests. Whether each one applies depends on a different
choice you made when picking your combination.

- The **Microsoft Fabric app registrations** section applies if your data platform is
  Microsoft Fabric. Skip that section if your data platform is DuckDB or MotherDuck.
- The **Studio SSO app registration** section applies if your deployment style is
  Kubernetes on Azure. Skip that section if your deployment style is Local Docker.

You may need one section, the other, both, or neither. If you chose **Local Docker together
with DuckDB or MotherDuck**, neither section applies — skip this entire page and do not
forward it.

If Microsoft Fabric applies to you, also read the **recurring task** section below. It
repeats every time your team creates a new domain, not just at initial setup.

## Microsoft Fabric — Entra app registrations

> **Applies to: Microsoft Fabric.** Skip if you chose DuckDB or MotherDuck.

Skipping this section does not mean skipping the rest of this page — the Studio SSO section
below is a separate request tied to your deployment style, not your data platform.

**One value you may need before you start — on Kubernetes on Azure only.** If your deployment
style is Kubernetes on Azure, this section needs `STUDIO_DOMAIN`, the DNS name Studio is served
on, to build a redirect URI on the app registration Studio signs people in through. It comes from your Azure
infrastructure owner — see [01d-prereqs-azure-infra](01d-prereqs-azure-infra.md), which
produces it only on that deployment style. The Studio SSO section below uses the same value for
a different redirect URI.

**Under Local Docker you need nothing before you start.** No interactive sign-in runs against
the M2M app there, so no redirect URI is registered and `STUDIO_DOMAIN` is not used on this
page at all.

### Why two app registrations

Studio's Fabric integration separates two identities:

- **U2M (user-to-machine)** — the app your team members sign into when they connect their
  own Fabric access inside Studio. This is the identity for interactive work.
- **M2M (machine-to-machine)** — a service principal with its own client secret, used for
  background work Studio does without a person driving: scheduled jobs and the GitHub
  Actions CI/CD workflow.

Studio never creates either identity. Create the M2M service principal directly in Entra
and hand back its credentials — the U2M app registration is needed only in one specific
case, covered next.

**Create the U2M app registration only if your deployment style is Kubernetes on Azure and
your operator deliberately chooses to keep the U2M and M2M identities separate.** Under
Local Docker, Studio has no signed-in user to delegate through, so the U2M app registration
is never required, regardless of data platform. Under Kubernetes on Azure, Studio's own
Fabric connection form defaults to reusing the M2M app's credentials for U2M too — a "Use
the same app for service (m2m) and user (u2m) access" checkbox, **checked by default**.
Leave that default in place and no separate U2M app registration is needed at all; a
separate one is required only if your operator unchecks that box to keep the two identities
apart. Whether the M2M service principal is required depends on your deployment style. On
**Kubernetes on Azure** it is required — Studio's background work runs as it. On **Local
Docker** Studio's own form marks the M2M fields optional, because background work there runs
as the operator's ambient `az` session instead. It is still needed on Local Docker if that
team will use the GitHub Actions CI/CD path, which has no ambient session to fall back on.

### Create the app registrations

1. **Check your deployment style first.** If it is Local Docker, skip straight to step 2 —
   do not create a U2M app registration; it is never used there. If it is Kubernetes on
   Azure, ask your operator whether they plan to keep U2M and M2M separate in Studio's
   Fabric connection form. If not — the default — skip to step 2; Studio reuses the M2M
   app registration for U2M automatically. Only if they confirm they will keep the
   identities separate, create a second Entra app registration for **U2M** use. Studio
   needs its tenant ID, client ID, and a client secret.
2. Create an Entra app registration (or a service principal) for **M2M** use, with its own
   client secret. On Kubernetes on Azure this is required. On Local Docker Studio's own form
   marks the M2M fields optional — the label reads "(optional; required for GHA)" — so a
   Fabric connection can be registered without them there. Create the service principal anyway
   if that team will ever use the GitHub Actions CI/CD path, which cannot run without it.
3. The Fabric tenant setting "service principals can use Fabric APIs" is the Fabric
   administrator's task, not yours — it is covered in
   [01b-prereqs-fabric-admin](01b-prereqs-fabric-admin.md), together with the egress hosts
   this connection needs.

Granting the M2M service principal a role on a specific Fabric workspace — so it can read or
write that workspace — is a separate request from your organisation's Fabric admin, not part
of this page. See [01b-prereqs-fabric-admin](01b-prereqs-fabric-admin.md).

### Which app carries the interactive sign-in

The next two sections — the redirect URI and the delegated permissions — belong to **whichever
app registration Studio signs people in through**, not to the M2M app by name:

| Your operator's choice | The interactive app | Where the redirect URI and delegated permissions go |
| --- | --- | --- |
| Leaves "use the same app for m2m and u2m" checked — **the default** | The M2M app | On the **M2M** app registration |
| Unchecks it, keeping the identities separate | The U2M app | On the **U2M** app registration. The M2M app then needs neither |

Read the next two sections with that substitution in mind. Configuring them on the M2M app when
your operator keeps the identities separate leaves the U2M app with no reply address and no
permissions — and the first person who connects Fabric gets `AADSTS500113`, the exact failure
those sections exist to prevent.

### The interactive app also needs redirect URIs

> **Applies to: Microsoft Fabric on Kubernetes on Azure.** Skip if your deployment style is
> Local Docker — Studio shows no U2M section there at all, so no interactive sign-in runs
> against this app and no reply address is needed.

Two different flows sign into this app. Your team members sign in when they connect their own
Fabric access inside Studio, and Studio signs in again when an operator saves the Fabric data
platform in Org Settings. An interactive sign-in needs a reply address, and an app registered
for service credentials alone has none — which is why a pure M2M app fails here when it is
also carrying the interactive flow.

Register both of these as **Web** redirect URIs on the interactive app — **the M2M app by
default, the U2M app if your operator keeps the identities separate**:

| Redirect URI | Which flow uses it | Fails with |
| --- | --- | --- |
| `https://<STUDIO_DOMAIN>/api/auth/fabric/callback` | A person connecting their own Fabric access inside Studio | `AADSTS500113: No reply address is registered for the application` |
| `https://<STUDIO_DOMAIN>/api/v1/data-platforms/validation/callback` | An operator saving the Fabric data platform in Org Settings | `AADSTS50011: The redirect URI … does not match the redirect URIs configured for the application` |

**Register both.** They are two separate flows on two different paths, and Studio builds each
one itself — neither falls back to the other. An app carrying only the first signs your team
in correctly and then rejects the operator's save, which reads as a Studio problem rather than
an app registration problem.

The second URI is new. Studio began sending it at release **v0.1.32**; releases up to and
including v0.1.31 used only the first. If your app registration was built for an earlier
release and has been carrying one URI since, it stopped being complete at that upgrade. Nothing
announces this: sign-in keeps working, and the gap appears the next time somebody saves a data
platform, which may be weeks later.

Neither URI can be pointed somewhere else. Studio builds the second from its own base URL in
code, with no setting an operator can change, so it must be registered exactly as shown.

**If you add these with the Azure CLI, pass the complete set.** `az ad app update
--web-redirect-uris` replaces the whole list rather than adding to it, so passing only the new
URI silently removes the one already there and breaks Fabric sign-in:

```
az ad app update --id <app-id> \
  --web-redirect-uris \
    "https://<STUDIO_DOMAIN>/api/auth/fabric/callback" \
    "https://<STUDIO_DOMAIN>/api/v1/data-platforms/validation/callback"
```

These are separate from the Studio SSO redirect URI further down this page, which sits on a
different app registration. Register both sets if both sections apply to you.

### Delegated API permissions on the interactive app

> **Applies to: Microsoft Fabric on Kubernetes on Azure.** Skip if your deployment style is
> Local Docker, for the same reason as the section above.

**These go on the same app as the redirect URI above** — the M2M app by default, the U2M app if
your operator keeps the identities separate.
Because that app carries the interactive sign-in, it needs delegated permissions for every
resource Studio reaches on the signed-in person's behalf. Add these, then grant admin consent for
the tenant.

| Resource | Application ID | Delegated permissions |
| --- | --- | --- |
| Power BI Service — the first-party resource that Fabric API scopes route through | `00000009-0000-0000-c000-000000000000` | `Item.ReadWrite.All`, `Item.Execute.All`, `Workspace.ReadWrite.All`, `Workspace.GitUpdate.All`, `Connection.Read.All`, `Lakehouse.ReadWrite.All`, `OneLake.ReadWrite.All`, `Capacity.Read.All` |
| Microsoft Graph | `00000003-0000-0000-c000-000000000000` | `openid`, `offline_access` |
| Azure Storage | `e406a681-f3d4-42a8-90b6-c2b029497af1` | `user_impersonation` |
| Azure SQL Database | `022907d3-0f1b-48f7-badc-1ba6abab6d66` | `user_impersonation` |
| Azure Service Management | listed in the portal under this name | `user_impersonation` |
| Azure Key Vault — **only if** any domain will use Azure Key Vault as its secret store | listed in the portal under this name | `user_impersonation` |

Look these up by application ID, not by name. Fabric's delegated scopes are published by the
Power BI Service resource, so searching the portal for "Fabric" does not find them.

**Add one more:** Microsoft Graph **`Application.ReadWrite.All`**, delegated, admin-consented.
The recurring federated-credential task further down this page needs it. Put it on the app
registration Studio signs people in through — **the M2M app when the identities are shared,
which is the default; the U2M app when your operator keeps them separate.** Studio makes that
call under whichever app issued the person's token, so the grant is inert on the other one. It
is repeated in that section; add it here so the whole permission set is done in one sitting.

The Azure Key Vault row is conditional. Studio asks for it only when a domain's secret store is
Azure Key Vault; if every domain keeps its secrets in a local file instead, the check is skipped
and the scope is never needed. Grant it if you do not yet know which store your domains will use
— an unused delegated scope costs nothing, and a missing one blocks the domain.

**An Azure Key Vault secret store needs its own two redirect URIs.** Studio asks for a tenant ID
and client credentials on each Azure Key Vault secret store, so the app registration behind a
secret store is whichever one your operator enters there. It is a separate registration from the
Fabric one unless your operator deliberately reuses the same app. Whichever app it is needs both
of these as **Web** redirect URIs:

| Redirect URI | Which flow uses it | Since |
| --- | --- | --- |
| `https://<STUDIO_DOMAIN>/api/auth/secret-store-links/callback` | A person linking their own Key Vault access inside Studio | Every release this documentation has covered |
| `https://<STUDIO_DOMAIN>/api/v1/secret-stores/validation/callback` | An operator saving the secret store | **v0.1.32** |

This pair follows the same rule as the Fabric pair above: two flows, two paths, both built by
Studio, neither able to stand in for the other. If your operator reuses one app registration for
both the Fabric data platform and the Key Vault secret store, that single app needs all four
URIs — and the `az ad app update` warning above applies with all four in the command.

Each missing scope fails at a different moment, and the error names the scope. Without the Azure
SQL Database scope, activating an intent fails with `AADSTS65001 consent_required` for
`https://database.windows.net/user_impersonation`. Without the Power BI Service scopes, the same
error names the Fabric API scopes instead.

### Warning: adding a permission can remove the ones already there

**Before you change permissions on an app that is already in use, snapshot its current grants:**

```
az ad app permission list-grants --id <app id>
```

**Check the same command immediately afterwards.** Adding one permission through the CLI, when the
follow-up consent call hits a `Directory_ConcurrencyViolation`, has been observed to clear the
app's other existing consent grants instead of adding to them — taking a working deployment down
while fixing something unrelated to it.

If grants have disappeared, re-add and re-grant each removed resource **one at a time**, with a
short pause between them, so the concurrency conflict does not repeat. Adding everything in the
table above in a single sitting, before anyone is using the app, avoids the situation entirely.

### Values to send back

| Value | What it is |
| --- | --- |
| `TENANT_ID` | Your Entra tenant ID. |
| `U2M_CLIENT_ID`, `U2M_CLIENT_SECRET` | The U2M app registration's client ID and client secret. Only if your deployment style is Kubernetes on Azure and your operator is keeping U2M separate from M2M — Studio's default reuses the M2M credentials and needs neither value. |
| `M2M_CLIENT_ID`, `M2M_CLIENT_SECRET` | The M2M service principal's client ID and client secret. Always needed on Kubernetes on Azure. On Local Docker, Studio's form marks them optional — send them only if that team will use the GitHub Actions CI/CD path. |
| `M2M_SP_OBJECT_ID` | The M2M service principal's **object ID** — a different GUID, on the enterprise application rather than the app registration. Your Microsoft Fabric administrator needs it to make the service principal a capacity administrator; the client ID is rejected there. Read it with `az ad sp show --id <M2M_CLIENT_ID> --query id -o tsv`. |

## Studio SSO app registration

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

This section is independent of the Fabric section above. Check your deployment style
separately — skipping or completing the Fabric section does not decide whether this section
applies.

### Why

Kubernetes on Azure supports multiple people signing in to Studio. Studio uses Microsoft
Entra as the sign-in provider through a dedicated app registration, separate from any Fabric
app registration above.

### Create the app registration

Create a single-tenant Entra app registration and configure it with these exact values.

- **Redirect URI to register:** append `/api/auth/oauth2/callback/sso-azure` to your Studio
  domain, in full. If your Studio domain is `studio.example.com`, the redirect URI is
  `https://studio.example.com/api/auth/oauth2/callback/sso-azure`. Register the complete
  URL, not the path alone. `STUDIO_DOMAIN` — the DNS name for this URL — comes from your
  Azure infrastructure owner; see
  [01d-prereqs-azure-infra](01d-prereqs-azure-infra.md).
- **Scopes:** `openid profile email offline_access`. Studio requests exactly these four and
  no others.
- **PKCE:** always on for this connection, and nothing for you to configure in Entra. It is
  fixed behaviour for the Entra provider, not a setting anyone can turn off.
- **Credential type: client secret only.** Studio does not support a certificate credential
  or a managed identity for this connection — issue a client secret.
- **Account type: single-tenant.** Studio's v1 SSO connection supports one Entra tenant per
  deployment.
- **Admin consent:** generally not required. Studio requests only user-consentable scopes —
  no directory permissions and no API permissions. Your tenant may still require admin
  consent if it has been configured to disable user consent for all apps; that policy, if
  present, is yours to apply as usual.
  **This applies to the SSO app registration only.** The Fabric interactive app above — whichever
  one the routing table sends you to — does need API permissions and does need admin consent. The
  two app registrations have opposite requirements, so do not carry this "no permissions" posture
  across to the Fabric one.
- **App roles and group claims: none needed.** Do not configure app roles or group claims on
  this app registration — Studio does not read them. Entra authenticates the sign-in only;
  it does not decide what a signed-in person can do inside Studio. See
  [05-configure-org](05-configure-org.md) for where Studio access is actually assigned.

### Values to send back

| Value | What it is |
| --- | --- |
| `TENANT_ID` | Your Entra tenant ID (the same value as the Fabric section, if you completed it). |
| `ENTRA_SSO_CLIENT_ID`, `ENTRA_SSO_CLIENT_SECRET` | The SSO app registration's client ID and client secret. |

## Recurring task: the per-repo federated credential

This applies under the same condition as the Fabric section above — skip it if your data
platform is DuckDB or MotherDuck.

**This is not a one-time setup step.** Every time your team creates a new Studio domain, the
M2M app registration needs one more federated credential — one per domain repository. Plan
for this as an ongoing task for whoever holds Entra rights on that app, not something to
finish once during initial setup.

**Wait until the domain exists in Studio before you start.** The credential's name contains the
domain's slug, and Studio assigns that slug when the domain is created. You cannot create this
credential in advance.

Create a federated credential on the M2M app registration with exactly these parameters:

| Parameter | Value |
| --- | --- |
| Name | `vibedata-{domain-slug}-{repo}`, with `{domain-slug}` replaced by the domain's slug in Studio and `{repo}` by the GitHub repository name. Shorten `{repo}` from the end if the whole name would exceed 120 characters. |
| Issuer | `https://token.actions.githubusercontent.com` |
| Audience | `api://AzureADTokenExchange` |
| Subject | `repo:{org}/{repo}:ref:refs/heads/{default-branch}`, with `{org}/{repo}` replaced by the domain's actual GitHub repository and `{default-branch}` by that repository's default branch |

**The name is not a label — Studio finds the credential by it.** Studio asks Microsoft Graph for
this exact name. If the name differs, Graph returns nothing and Studio reports the credential as
**missing**, even when the issuer, audience, and subject are all correct. Ask your operator for
the domain's slug; it is shown with the domain in Studio.

Keep the full repository name in the **Subject** even when you shortened it in the **Name**. Token
matching uses the subject, so it must stay exact.

**Use the repository's real default branch in the subject.** Studio builds the subject it
verifies against from the default branch it recorded for that repository, so `master`, `develop`
or any other name belongs in the subject exactly as GitHub reports it. Studio falls back to
`main` only when it holds no recorded default branch for the repository.

> **Applies to: releases before v0.1.33.** On v0.1.32 and every earlier release the opposite was
> true — Studio's check accepted only `refs/heads/main` regardless of the repository's actual
> default branch, so a credential created against `master` was created correctly and then failed
> verification, with no way to clear the warning. If you are following this page against an
> older release, use the literal `main`. On v0.1.33 and later, use the real branch.

The credential is only half the trust: GitHub Actions must present a token whose subject matches
it. Both sides follow the repository's default branch, so a repository that renames its default
branch after the credential is created needs the credential replaced.

**Replacing means deleting first.** Studio reports a credential whose subject no longer matches
as **invalid**, not missing, and the credential name is built from the domain slug and the
repository — not from the branch. Creating a corrected credential without deleting the old one
therefore fails on a duplicate name. Delete the named credential, then create its replacement.

**Permissions this needs — on Kubernetes on Azure.** Add Microsoft Graph
**`Application.ReadWrite.All`** as a **delegated** permission on the app registration Studio
signs people in through — the M2M app when the identities are shared (the default), the U2M app
when they are kept separate — and grant admin consent for the tenant.

> **Applies to: Local Docker.** Under Local Docker this grant is not what matters. Studio has no
> signed-in user to delegate through, so it reaches Graph with a token from the operator's own
> `az` session inside the `api` container. The check therefore runs as **that person's** Entra
> identity, and the permission on the M2M app is irrelevant to it. What the operator's account
> needs is the ability to write federated credentials on the app registration — being an
> **Owner** of it is the usual way. The two bullets below are about the delegated flow, so they
> apply on Kubernetes on Azure.

Two common substitutes do not work here:

- `Application.ReadWrite.OwnedBy` exists only as an *application* permission. Microsoft does not
  publish a delegated version of it, and Studio uses the delegated flow.
- Being listed as an **Owner** of the app registration is a directory relationship, not a Graph
  permission. It lets a person manage the app in the portal or through `az`. It grants Studio's
  own calls nothing.

Without the permission the calling account needs, Studio's check on this credential fails as a
**soft** warning — "Fabric federated credential could not be verified — the calling account may
lack permission to read it, or the external system may be unreachable" — no matter how
correctly the credential itself is configured. The domain still reaches `Active`, so nothing
stops until the first CI run.

**Studio only verifies this credential. It never creates or edits it.** After a domain is
created, Studio checks that a matching federated credential already exists on the M2M app
registration. If it is missing, Studio's own check fails with a remediation message — but
creating the credential is always your team's action, not Studio's.

## Secret lifetime and rotation

Every client secret on this page expires. Entra caps a client secret at **24 months**, and
Microsoft recommends less than 12. Whatever you choose, the deployment stops working on that date
unless somebody replaces the secret first.

- **Record the expiry date of each secret and hand it back with the secret.** The operator has no
  other way to learn it, and Studio does not warn anyone in advance.
- **Do not give every secret the same expiry date.** If you issue all of them in one sitting with
  the same lifetime, sign-in, Fabric access, and every domain's deploy all break on the same day.
- **Know what expiry breaks.** An expired M2M secret stops Fabric connections and fails every
  domain's GitHub Actions deploy with an authentication error. An expired SSO secret stops
  everyone signing in.
- **Rotation is your team's job, not Studio's.** Studio never rotates a secret and never renews
  one. When you issue a replacement, the operator re-enters it during organisation setup — see
  [05-configure-org](05-configure-org.md).

## Sending secrets back

This page asks for up to three client secrets. Send them through a secret manager, password
vault, or another channel your organisation already trusts for credential handoff — not by
email or chat.

## Values this page needs before you start

| Token | Comes from | Needed when |
| --- | --- | --- |
| `STUDIO_DOMAIN` | Your Azure infrastructure owner — [01d-prereqs-azure-infra](01d-prereqs-azure-infra.md) | **Kubernetes on Azure only** — for the SSO app's redirect URI, and on Microsoft Fabric also for the interactive app's (the M2M app by default, the U2M app if the identities are kept separate). Local Docker needs it for neither, and `01d` does not produce it on that deployment style |
| The domain's slug | Your Studio operator, after the domain is created | Every time the recurring federated-credential task runs |

## All values this page collects

| Token | Comes from | Needed when |
| --- | --- | --- |
| `TENANT_ID` | Your Entra tenant ID | Either section applies |
| `U2M_CLIENT_ID` | The Fabric U2M app registration | Microsoft Fabric **and** Kubernetes on Azure, only if the operator keeps U2M separate from M2M (Studio's default reuses M2M) |
| `U2M_CLIENT_SECRET` | The Fabric U2M app registration | Microsoft Fabric **and** Kubernetes on Azure, only if the operator keeps U2M separate from M2M (Studio's default reuses M2M) |
| `M2M_CLIENT_ID` | The Fabric M2M service principal | Microsoft Fabric — always on Kubernetes on Azure; on Local Docker only if that team will use the GitHub Actions CI/CD path |
| `M2M_SP_OBJECT_ID` | The same service principal's object ID, for the Fabric capacity admin list | Microsoft Fabric — always on Kubernetes on Azure; on Local Docker only if that team will use the GitHub Actions CI/CD path |
| `M2M_CLIENT_SECRET` | The Fabric M2M service principal | Microsoft Fabric — always on Kubernetes on Azure; on Local Docker only if that team will use the GitHub Actions CI/CD path |
| `ENTRA_SSO_CLIENT_ID` | The Studio SSO app registration | Kubernetes on Azure |
| `ENTRA_SSO_CLIENT_SECRET` | The Studio SSO app registration | Kubernetes on Azure |

## Where this goes

The operator enters all of these values during organisation setup — see
[05-configure-org](05-configure-org.md). `TENANT_ID`, `M2M_CLIENT_ID`, and
`M2M_CLIENT_SECRET` are also used again later, in
[06-first-domain](06-first-domain.md), when each new domain is created and the recurring
federated-credential task above comes up again.
