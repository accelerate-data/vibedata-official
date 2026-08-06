---
applies-to: vibedata v0.1.26
verified-against: studio@653beeced
verified-on: 2026-08-05
sources:
  - docs/functional/data-platform/fabric-backend.md
  - docs/functional/data-platform/README.md
  - docs/functional/gha-data-platform-oidc-flow/README.md
  - docs/functional/gha-data-platform-oidc-flow/oidc-mechanics.md
  - docs/functional/sso-oauth-flows/README.md
  - docs/design/identity-management/sso-oauth-flows/README.md
  - src/server/lib/auth/better-auth-config.ts
  - src/server/modules/auth/sso-providers/sso-providers.schemas.ts
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
apart. The M2M service principal is required for Microsoft Fabric on both deployment
styles, since Studio's background and CI/CD work needs it either way.

### Create the app registrations

1. **Check your deployment style first.** If it is Local Docker, skip straight to step 2 —
   do not create a U2M app registration; it is never used there. If it is Kubernetes on
   Azure, ask your operator whether they plan to keep U2M and M2M separate in Studio's
   Fabric connection form. If not — the default — skip to step 2; Studio reuses the M2M
   app registration for U2M automatically. Only if they confirm they will keep the
   identities separate, create a second Entra app registration for **U2M** use. Studio
   needs its tenant ID, client ID, and a client secret.
2. Create an Entra app registration (or a service principal) for **M2M** use, with its own
   client secret. This one is required for Microsoft Fabric regardless of deployment style.
3. The Fabric tenant setting "service principals can use Fabric APIs" is the Fabric
   administrator's task, not yours — it is covered in
   [01b-prereqs-fabric-admin](01b-prereqs-fabric-admin.md), together with the egress hosts
   this connection needs.

Granting the M2M service principal a role on a specific Fabric workspace — so it can read or
write that workspace — is a separate request from your organisation's Fabric admin, not part
of this page. See [01b-prereqs-fabric-admin](01b-prereqs-fabric-admin.md).

### Values to send back

| Value | What it is |
| --- | --- |
| `TENANT_ID` | Your Entra tenant ID. |
| `U2M_CLIENT_ID`, `U2M_CLIENT_SECRET` | The U2M app registration's client ID and client secret. Only if your deployment style is Kubernetes on Azure and your operator is keeping U2M separate from M2M — Studio's default reuses the M2M credentials and needs neither value. |
| `M2M_CLIENT_ID`, `M2M_CLIENT_SECRET` | The M2M service principal's client ID and client secret. |

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
- **PKCE:** always on for this connection. No configuration needed on your side.
- **Credential type: client secret only.** Studio does not support a certificate credential
  or a managed identity for this connection — issue a client secret.
- **Account type: single-tenant.** Studio's v1 SSO connection supports one Entra tenant per
  deployment.
- **Admin consent:** generally not required. Studio requests only user-consentable scopes —
  no directory permissions and no API permissions. Your tenant may still require admin
  consent if it has been configured to disable user consent for all apps; that policy, if
  present, is yours to apply as usual.
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

Create a federated credential on the M2M app registration with exactly these parameters:

| Parameter | Value |
| --- | --- |
| Issuer | `https://token.actions.githubusercontent.com` |
| Audience | `api://AzureADTokenExchange` |
| Subject | `repo:{org}/{repo}:ref:refs/heads/main`, with `{org}/{repo}` replaced by the domain's actual GitHub repository |

**Use the literal `main` in the subject, even when the domain repository's default branch is
not `main`.** Studio's own check for this credential accepts only `refs/heads/main` — it
does not read the repository's configured default branch. Creating the credential against
any other branch name will fail Studio's verification.

Creating this requires the `Application.ReadWrite.OwnedBy` right on the M2M app registration
— in practice, being listed as an **Owner** of that App Registration in Entra.

**Studio only verifies this credential. It never creates or edits it.** After a domain is
created, Studio checks that a matching federated credential already exists on the M2M app
registration. If it is missing, Studio's own check fails with a remediation message — but
creating the credential is always your team's action, not Studio's.

## Sending secrets back

This page asks for up to three client secrets. Send them through a secret manager, password
vault, or another channel your organisation already trusts for credential handoff — not by
email or chat.

## All values this page collects

| Token | Comes from | Needed when |
| --- | --- | --- |
| `TENANT_ID` | Your Entra tenant ID | Either section applies |
| `U2M_CLIENT_ID` | The Fabric U2M app registration | Microsoft Fabric **and** Kubernetes on Azure, only if the operator keeps U2M separate from M2M (Studio's default reuses M2M) |
| `U2M_CLIENT_SECRET` | The Fabric U2M app registration | Microsoft Fabric **and** Kubernetes on Azure, only if the operator keeps U2M separate from M2M (Studio's default reuses M2M) |
| `M2M_CLIENT_ID` | The Fabric M2M service principal | Microsoft Fabric |
| `M2M_CLIENT_SECRET` | The Fabric M2M service principal | Microsoft Fabric |
| `ENTRA_SSO_CLIENT_ID` | The Studio SSO app registration | Kubernetes on Azure |
| `ENTRA_SSO_CLIENT_SECRET` | The Studio SSO app registration | Kubernetes on Azure |

## Where this goes

The operator enters all of these values during organisation setup — see
[05-configure-org](05-configure-org.md). `TENANT_ID`, `M2M_CLIENT_ID`, and
`M2M_CLIENT_SECRET` are also used again later, in
[06-first-domain](06-first-domain.md), when each new domain is created and the recurring
federated-credential task above comes up again.
