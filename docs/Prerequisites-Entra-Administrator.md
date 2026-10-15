# Request for your Microsoft Entra administrator

Prepare Entra applications for the access your Studio deployment needs. Keep these purposes distinct:

- Studio sign-in through an eligible Identity Provider with **Allow sign-in** selected;
- delegated Fabric access through a provider connected by each user;
- unattended Fabric work through the Domain's service-authentication policy.

One eligible Entra provider can serve both sign-in and downstream delegation. The Domain can reuse its application for service authentication where Studio offers that option, or use a dedicated service principal.

## Prepare the provider application

Return the tenant ID, client ID, and client secret through your approved credential channel. Use the concrete tenant GUID, rather than a shared authority such as `common`.

Coordinate the redirect configuration with the Studio operator:

1. In Studio, open **Org settings → Identity providers**.
2. Select **Register identity provider**.
3. Choose **Microsoft Entra ID** under **Provider type**.
4. Fill in **Display name** to obtain the previewed **Callback URL**.
5. Register that exact callback URL on the Entra application.
6. Complete **Tenant ID**, **Client ID**, and **Client secret** in Studio.
7. Select **Allow sign-in** if the provider will sign users into Studio.
8. Select **Create**.
9. Run **Test** on the saved provider row to activate it.

Do not guess a callback path. Changing the provider name before saving can change the previewed URL. A saved provider stays **Pending test** until a successful test activates it.

Use **Automatically approve new users** only when your organisation wants new users from that provider to enter without manual approval. It does not grant roles, Domain membership, or approval to users already pending.

## Enable Fabric user access when required

Grant the delegated Microsoft/Fabric permissions required for the interactive operations and your organisation's consent policy. Studio requests audience-specific tokens; a Fabric REST token is not a substitute for a token for SQL, storage, Graph, Key Vault, or ARM.

The operator can use the sign-in provider for Fabric when it meets those requirements, or register a separate delegation-only provider with **Allow sign-in** cleared. Each user must connect the downstream provider under **User Settings → Connections** before it can be selected during Domain creation.

## Prepare Fabric service authentication

For **Dedicated identity**, return:

- tenant ID;
- application/client ID;
- client secret;
- service principal object ID.

The object ID is different from the application/client ID. Fabric role grants can require the service principal object ID.

If Studio offers **Reuse user identity provider**, the Domain references that provider's active application credentials and follows their rotation. Reuse does not give the application any additional Fabric permissions. Confirm its service principal has the access listed in [[Prerequisites Fabric Administrator]].

Do not assume that an interactive application is eligible for service use merely because it is in the same tenant.

## Handoff

| Purpose | Handoff |
| --- | --- |
| Sign-in or Fabric delegation provider | Tenant ID, client ID, client secret; exact callback copied from Studio back into Entra |
| Dedicated Domain service identity | Tenant ID, client ID, client secret, service principal object ID, and confirmation of Fabric access |
| Reused service identity | Confirmation that the selected provider's application is eligible and has the required service access |

Send secrets through a secret manager or another approved credential channel. Never put them in agent chat, Domain instructions, or Git.

---

_Release scope and source-review limits: [Home](README.md#release-and-verification-scope)._
