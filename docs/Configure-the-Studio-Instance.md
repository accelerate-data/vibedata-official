# Configure the Studio instance

After your marketplace deployment is running, complete these steps as a `vibedata_owner`. Data-platform and secret-store configuration belongs to each Domain; see [[Create Your First Domain]].

## Configure an identity provider for sign-in

1. Open **Org settings → Identity providers**.
2. Select **Register identity provider**.
3. Choose the appropriate **Provider type** and fill in **Display name**.
4. Copy the displayed **Callback URL** into the external application's redirect configuration.
5. Complete the provider-specific fields, including **Tenant ID**, **Client ID**, and **Client secret** for **Microsoft Entra ID**.
6. Select **Allow sign-in** if this provider must sign users into Studio.
7. Set **Automatically approve new users** according to your access policy.
8. Select **Create**.
9. Select **Test** on the saved provider row.

A new provider shows **Pending test** until its test succeeds. A successful test activates it. Saving a replacement for an active provider keeps the previous active configuration in use until the replacement passes its test.

An eligible provider can support both sign-in and downstream delegation. Clear **Allow sign-in** for a delegation-only provider. Automatic approval does not grant roles or Domain membership and does not approve existing pending users.

For Entra preparation, see [[Prerequisites Entra Administrator]].

## Configure GitHub

1. Open **Org settings → GitHub**.
2. Enter the customer-owned GitHub App's client ID, client secret, and private key PEM.
3. Save the configuration.

Studio validates the App identity and required permissions. It derives the App metadata; you do not enter an App ID or a global installation ID. The Domain repository picker selects the installation and repository later.

Use [[Prerequisites GitHub Organisation Owner]] if validation fails or an installation needs permission approval.

## Connect downstream user accounts

For Fabric, register and activate an eligible **Microsoft Entra ID** provider. It can be the provider used for sign-in if it has the required downstream configuration and permissions, or a separate delegation-only provider.

Each user then connects their own account under **User Settings → Connections**. Domain creation offers only active, compatible providers with a healthy connection for the signed-in user. Registering a provider alone does not complete that user's connection, and Domain creation does not start the OAuth flow.

MotherDuck uses user PATs. DuckDB needs no external data-platform credential.

## Configure an LLM profile

1. Open **Org settings → LLM profiles**.
2. Start a new profile.
3. Fill in **Profile name**.
4. Select **Provider**.
5. Complete the connection fields displayed for that provider.
6. Select or enter **Model**.
7. Review **Canonical model**.
8. Save the profile and resolve any connection-test failure.

Choose from the deployed provider list. For example, the Azure option is **Azure Foundry**; the list also includes providers such as DeepSeek and Ollama. Endpoint, credential, and model-discovery requirements depend on the provider.

**Canonical model** supplies capabilities, limits, and price metadata. For providers that identify their own models, Studio resolves it. **Custom (OpenAI-compatible)** and Ollama offer a catalogue association picker, including **None — not in the catalogue**. An association is not mandatory for every profile.

Connection-field changes run a real provider test. A failed test prevents that connection change from being saved. Choose an instance default profile, then verify it with an actual Intent turn. There is no Domain-level LLM override.

## Configure users and roles

Open **Org settings → Users** and grant the minimum required access. The main onboarding roles are:

- `vibedata_owner` — instance administration;
- `domain_owner` — administration within a Domain;
- `domain_contributor` — work within a Domain;
- `user_access_administrator` — user and access administration.

Configure Domain membership after the Domain exists.

## Prepare the Domain secret store

Choose the store during Domain creation. The **Secret store type** control shows which types your deployment offers and which are available.

- **Internal** needs no external store connection. Saving it exposes the Domain's **Secrets** tab.
- **Azure Key Vault** and other external stores need their displayed connection, identity, and resource configuration.
- **Local File**, when selected, requires an operator to supply secrets outside Studio.

There is no separate organisation-level Secret Stores registration prerequisite. See [[Create Your First Domain]] for the create flow and store-specific credential handling.

## Optional settings

Configure these only when your organisation requires them. Availability depends on permissions, deployment settings, and preview features:

- **OAuth clients**;
- **MCP catalog**;
- **Plugins**;
- **Action confirmation**;
- **Connector sources**;
- **Maintenance jobs**;
- **Capacity settings**;
- **Credit packs**;
- **Announcements**;
- **Preview features**;
- **Usage**;
- **Audit records**;
- **Archive**.

## Check before creating the first Domain

Confirm that a real owner can sign in, GitHub configuration validates, required users have access, and an LLM profile is usable. For Fabric, also confirm the creating user's downstream connection is healthy.

Continue to [[Create Your First Domain]].

---

_Release scope and source-review limits: [Home](README.md#release-and-verification-scope)._
