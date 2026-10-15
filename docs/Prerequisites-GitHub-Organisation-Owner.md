# Request for your GitHub organisation owner: create a GitHub App

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker. Local Docker uses the operator's `gh` CLI session instead.

Studio uses a customer-owned GitHub App for delegated deployments. There is no Accelerate Data-hosted Marketplace App to install instead.

## What the App does

The App has two identities:

- an **installation identity** for headless Domain repository work;
- a **per-user authorization flow** so Studio can act on GitHub as a signed-in user, bounded by both the user and the App installation.

Each GitHub account where the App is installed gets its own installation ID. The Domain repository binding stores the selected installation. Org Settings does not configure a global default installation.

## Create the App

Create a GitHub App under the organisation that owns the Domain repositories. If you use personal repositories, create or install it on the appropriate personal account instead.

Use a stable App name. Studio derives App identity metadata from GitHub and relies on the actual installation when resolving repositories.

### User authorization callback

Configure the callback URL used by Studio's GitHub connection flow. The current GitHub provider surface and user-auth flow expose the callback Studio expects. Use the exact URL shown by the deployed instance rather than copying a callback from an older onboarding guide.

Do not enable a webhook solely for this setup. Current Studio does not require GitHub webhooks for the documented onboarding path.

## Required repository permissions

Grant this exact baseline:

| Repository permission | Access |
| --- | --- |
| Administration | Read-only |
| Contents | Read and write |
| Metadata | Read-only |
| Pull requests | Read and write |
| Workflows | Read and write |
| Variables / Actions variables | Read and write |
| Secrets | Read and write |

Do not add the following just because they look related:

- Actions permission;
- Issues permission;
- Administration write.

`Administration: read` is used for branch-protection inspection. `Workflows: write` is required when Studio writes workflow files. Variables and Secrets are separate GitHub permissions and both are needed when Studio materializes repository configuration.

Studio validates the App's required permission map when the operator saves the GitHub provider. A missing permission blocks a clean provider save or later repository operation with a specific failure.

### Permission changes on an existing App

Changing an App's permission set is not enough. Existing installations may require an organisation owner to approve the new permission request. Until that approval happens, the installation continues with its older grants.

If Studio reports a repository permission failure after you added the permission on the App, check the installation's pending permission update.

## Install the App

Install it on every GitHub organisation or personal account that owns repositories Studio will use.

Choose either:

- **All repositories**, or
- **Only select repositories** and explicitly include every intended Domain repository.

A Domain cannot use a repository excluded from its selected installation.

## App visibility

Choose visibility based on who must authorize the App.

A private organisation-owned App is suitable when every Studio user who needs GitHub authorization is a member of the owning organisation. If users outside that organisation must authorize the App, the App's installation/authorization policy must permit them.

Visibility does not grant repository access by itself. Repository selection on each installation still defines what the App can reach.

## Values to send to the Studio operator

Under the App's settings, provide:

| Value | Studio use |
| --- | --- |
| Client ID | Identifies the App for both machine and user flows |
| Client secret | Per-user GitHub authorization |
| Private key PEM | App JWT and installation-token minting |

Studio does **not** ask the operator to enter:

- App ID;
- installation ID;
- App slug.

Studio validates the App and derives the required metadata. The Domain repository picker later selects the installation and repository.

Send the client secret and PEM through a secret manager or another approved credential channel.

## Where the operator enters the values

The operator configures them under **Org Settings → GitHub** after the first real Studio owner can sign in.

Provider Save validates the App identity and required permission map. User authorization is a separate flow that occurs later when a person connects GitHub.

## Local Docker comparison

> **Applies to: Local Docker.**

There is no GitHub App prerequisite. Run this on the operator machine before installing Studio:

```bash
gh auth login --scopes repo,read:org,workflow
```

The Compose installer imports that session into Studio's API container.

---

_Applies to: studio/main (unreleased snapshot). Verified against `studio@5c9d2bbf339a` on 2026-08-22._
