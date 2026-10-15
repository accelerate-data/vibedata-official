# Request for your Microsoft Entra administrator

This page covers the Entra applications current Studio needs. There are three distinct roles. Do not treat them as one registration by default.

1. **Studio SSO application** — signs people into Studio on a delegated deployment.
2. **Fabric Identity Provider application** — lets an already-signed-in Studio user obtain delegated Fabric credentials.
3. **Fabric Domain service principal** — unattended service identity for one Fabric Domain.

A single Entra application can sometimes be reused for the Fabric user and service roles when Studio reports that reuse as eligible. That is optional. Studio explicitly models the Domain service credential separately from the downstream Identity Provider.

## A. Studio SSO application

**Applies to:** Kubernetes on Azure only. Skip for Local Docker.

Studio's browser sign-in uses an SSO Provider configured under **Org Settings → SSO Providers**. The operator registers the provider in Studio and Studio shows the callback URL to use.

Create a Microsoft Entra application registration for Studio sign-in and return:

- tenant ID;
- application/client ID;
- client secret.

Register the exact callback URL Studio displays for that SSO Provider. Do not guess or reuse the Fabric callback path. The SSO Provider surface owns its own callback.

The registration is for browser login to Studio only. It is not the Fabric user credential and not the Fabric service identity.

## B. Fabric Identity Provider application

**Applies to:** Microsoft Fabric on a delegated deployment. Skip for Local Docker Fabric, which uses the ambient Azure CLI identity in the Studio container.

Current Studio uses **Org Settings → Identity Providers** for downstream OAuth/OIDC registrations. Registering an Entra Identity Provider requires:

- a display name in Studio;
- Entra tenant ID;
- client ID;
- client secret.

Studio validates the candidate before saving it and then assigns a stable provider ID. The callback URL is derived from that provider ID and displayed in the Identity Providers panel:

```text
https://<studio-origin>/api/auth/oauth2/callback/<identity-provider-id>
```

Because the provider ID is allocated by Studio, the practical setup is:

1. Create the Entra application and client secret.
2. In Studio, open **Org Settings → Identity Providers** and register it.
3. Copy the callback URL Studio displays.
4. Add that exact callback URL to the Entra application registration.
5. If the first registration attempt cannot validate until the callback exists, add the callback and retry the Studio registration.

The Identity Provider is **link-only**. It never signs a person into Studio. A signed-in user later connects it from the downstream connection flow.

### Entra authority

Use the real tenant GUID. Do not use `common`, `organizations`, or `consumers`. Current Studio normalizes the Identity Provider to a concrete Entra tenant authority.

### Delegated permissions

The application must be allowed to obtain the Fabric resource tokens Studio requests for interactive operations. Grant the delegated Microsoft/Fabric permissions required by your organization's policy and consent model.

Studio acquires audience-specific access tokens. A token for Fabric REST is not assumed to be valid for SQL, storage, Graph, Key Vault, or ARM.

## C. Fabric Domain service principal

**Applies to:** Microsoft Fabric Domains that require unattended work.

Create a service principal for Domain automation. Return:

- tenant ID;
- client ID;
- client secret;
- service principal object ID.

The object ID is not the application/client ID. Fabric role APIs may require the service principal object ID when granting access.

The Domain service credential is stored on the Domain. It is used for unattended data-platform work, GitHub Actions profile material, verification, and ephemeral resource operations where the provider requires it.

### Reusing the Fabric Identity Provider application

Current Studio can expose a **reuse Identity Provider application** service-authentication option when the selected Identity Provider is eligible for service use. If the UI does not offer this option, use a separate service principal.

Do not assume that an interactive OAuth application can act as the Domain service credential merely because it has the same tenant or client ID.

## Redirect URI rule

For the downstream Fabric Identity Provider, use the callback URL Studio displays. Do not use the old fixed paths:

```text
/api/auth/fabric/callback
/api/v1/data-platforms/validation/callback
```

Those belonged to the earlier data-platform-registration flow and are not the current Identity Provider contract.

## Secrets and handoff

Send client secrets through your normal secret-management channel. Do not send them in ordinary email or chat.

Return these values to the Studio operator:

| Purpose | Values |
| --- | --- |
| Studio SSO | tenant ID, client ID, client secret |
| Fabric Identity Provider | tenant ID, client ID, client secret; callback is copied from Studio back into Entra |
| Fabric Domain service identity | tenant ID, client ID, client secret, service principal object ID |

The same administrator may own all three registrations, but Studio treats the identities as separate trust relationships.

---

_Applies to: studio/main (unreleased snapshot). Verified against `studio@5c9d2bbf339a` on 2026-08-22._
