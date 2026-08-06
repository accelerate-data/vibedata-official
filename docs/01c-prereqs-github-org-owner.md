---
applies-to: vibedata v0.1.26
verified-against: studio@653beeced
verified-on: 2026-08-05
sources:
  - docs/functional/github-user-auth-flow/github-app.md
  - src/server/modules/external-services/github-commit-provider.service.ts
  - src/server/modules/external-services/external-services.schemas.ts
  - src/features/settings/components/Settings/OrgSettingsPanel.tsx
  - src/features/settings/components/Settings/panels/GitHubProviderPanel.tsx
  - src/shared/schemas.ts
  - src/server/config/auth-enabled.ts
  - cli/vibedata/src/vibedata/templates/docker-compose.yml.j2
  - src/server/modules/credential-broker/credential-broker.github-minting.ts
  - src/server/modules/github/services/github-installations.service.ts
  - src/server/modules/github/services/__tests__/github-installations.service.local-mode.test.ts
  - src/server/modules/git-config/git-config.openapi.ts
---

# Request for your GitHub organisation owner: create a GitHub App

This request applies only if you chose **Kubernetes on Azure**. If you chose **Local
Docker**, skip this page. Studio uses the operator's own GitHub sign-in instead, and no
organisation owner action is needed.

Forward this page to the owner of your GitHub organisation. It takes about 10 minutes in
GitHub's own settings. Nothing here requires access to Studio or to any Accelerate Data
system — only to your organisation's GitHub settings.

## What is being asked

Create a GitHub App in your own GitHub organisation, install it, and send back four values
from the App's settings page.

## Why a GitHub App

Kubernetes on Azure supports multiple people signing in. Studio needs a way to act on
your team's domain repository — clone it, commit, open pull requests, write workflow files —
even when no person is signed in and driving. A GitHub App gives Studio that identity.

A GitHub App is not the same as:

- **A personal access token (PAT).** A PAT belongs to one person and disappears if that
  person leaves or revokes it. A GitHub App belongs to your organisation.
- **An OAuth app.** A classic OAuth app receives a token scoped to the signing-in user — it
  can reach every repository that person can see, across every organisation they belong to.
  A GitHub App is installed by an organisation owner onto specific repositories only. Any
  token it produces, whether acting as itself or on a signed-in user's behalf, can only touch
  the repositories you installed it on.

Create this App in your own organisation. There is no Accelerate Data-hosted App to install
instead, and no command-line tool creates it for you — an organisation owner must create it
directly in GitHub.

## Create the App

1. Sign in to GitHub as an owner of your organisation.
2. Go to your organisation's **Settings → Developer settings → GitHub Apps**, and select
   **New GitHub App**.
3. Give it a name and a homepage URL. Neither needs to be public-facing; any values work.
4. Under **Webhook**, uncheck **Active**. Studio does not need webhook events for this setup.
5. Under **Repository permissions**, set exactly these five permissions:

   | Permission | Access |
   | --- | --- |
   | Contents | Read and write |
   | Metadata | Read-only |
   | Pull requests | Read and write |
   | Workflows | Read and write |
   | Variables | Read and write |

   Leave every other permission, and every organisation and account permission, at **No
   access**.
6. Under **Where can this GitHub App be installed?**, choose **Only on this account**.
7. Save the App.

## Install the App on your organisation

After saving, GitHub prompts you to install the App, or shows an **Install App** option in
the App's own settings page. Install it on your organisation account — not a personal
account.

When GitHub asks which repositories the App can access, choose either:

- **All repositories**, or
- **Only select repositories** — in this case, include every repository that will become a
  Studio Domain's repository, now or later.

Note which choice you made. If you choose select repositories and a new Domain's repository
is not on the list later, add it from the same install screen before that Domain is created.

## Values to send back

Find all four values on the App's own settings page, under **General**:

| Value | Where to find it |
| --- | --- |
| `GITHUB_APP_ID` | **General → App ID**. |
| `GITHUB_APP_CLIENT_ID` | **General → Client ID**. |
| `GITHUB_APP_CLIENT_SECRET` | **General → Client secrets** — select **Generate a new client secret** and copy it immediately. GitHub shows it only once. |
| `GITHUB_APP_PRIVATE_KEY` | **General → Private keys** — select **Generate a private key**. GitHub downloads a `.pem` file; send its full contents. |

Send all four values back to the person setting up Studio, together with which repositories
the App can access. The client secret and the private key are credentials — send them
through a secret manager, password vault, or another channel your organisation already
trusts for this kind of handoff, not by email or chat. GitHub downloads the private key as a
`.pem` file and will not show it again, so keep a copy until it is safely delivered.

## Where this goes

Studio stores these four values in **Org Settings → GitHub**, which configures the GitHub
Commit Provider. From the App ID and private key, together with the installation you
created above, Studio mints a repository-scoped installation token whenever it needs to act
on a domain repository without a person driving. The operator enters these values during
organisation setup — see [05-configure-org](05-configure-org.md).
