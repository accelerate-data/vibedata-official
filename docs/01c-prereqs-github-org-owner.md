---
applies-to: vibedata v0.1.33
verified-against: studio@a121fc466
verified-on: 2026-08-13
sources:
  - docs/functional/github-user-auth-flow/github-app.md
  - src/server/modules/external-services/github-commit-provider.service.ts
  - src/server/modules/external-services/github-commit-provider.router.ts
  - src/server/modules/external-services/external-services.schemas.ts
  - src/server/modules/auth/providers/github.ts
  - src/server/modules/user-service-links/connect-github-commits.router.ts
  - src/server/lib/auth/github-app-metadata.ts
  - src/server/lib/auth/frontend-redirect.ts
  - src/features/settings/components/Settings/OrgSettingsPanel.tsx
  - src/features/settings/components/Settings/panels/GitHubProviderPanel.tsx
  - src/shared/schemas.ts
  - src/server/config/auth-enabled.ts
  - cli/vibedata/src/vibedata/templates/docker-compose.yml.j2
  - src/server/modules/credential-broker/credential-broker.github-minting.ts
  - src/server/modules/github/services/github-installations.service.ts
  - src/server/modules/github/services/__tests__/github-installations.service.local-mode.test.ts
  - src/server/modules/git-config/git-config.openapi.ts
  - src/server/lib/github-api.ts
  - src/server/modules/domains/helpers/domain-repository-values.ts
---

# Request for your GitHub organisation owner: create a GitHub App

This request applies only if you chose **Kubernetes on Azure**. If you chose **Local
Docker**, skip this page. Studio uses the operator's own GitHub sign-in instead, and no
organisation owner action is needed.

Forward this page to the owner of your GitHub organisation. If you have no GitHub organisation,
this page is for you to do yourself — see "Why a GitHub App" below. Either way it takes about 10
minutes in GitHub's own settings. Nothing here requires access to Studio or to any Accelerate Data
system — only to your organisation's GitHub settings.

## What this page consumes

This page needs one value before its step 4 can be done: the **Studio domain**, the DNS name
Studio will be reached at. It comes from your Azure infrastructure owner — see
[01d-prereqs-azure-infra](01d-prereqs-azure-infra.md) — and it must be settled before this
request is sent, because the callback URL in step 4 is built from it. Send it along with this
page.

## What is being asked

Create a GitHub App in your own GitHub organisation, install it, and send back the values listed
under "Values to send back" at the end of this page.

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

**If you have no GitHub organisation**, register the App under your personal GitHub account
instead. There is then nobody to forward this page to: you are both the App owner and the
person setting up Studio. Everything below still applies, with two differences, each called out
where it occurs — step 7 must be set to **Any account**, and you install the App on your
personal account rather than on an organisation.

## Create the App

1. Sign in to GitHub as an owner of your organisation.
2. Go to your organisation's **Settings → Developer settings → GitHub Apps**, and select
   **New GitHub App**.
3. Give it a name and a homepage URL. Neither needs to be public-facing, and GitHub validates
   both, so they are not free text. The homepage URL is never read again. **The name is.**
   Studio derives the App's slug from the name when your operator saves the provider, stores it,
   and matches installations against that stored value. Renaming the App on GitHub afterwards
   makes the stored slug stale, and Studio stops finding the installation until your operator
   saves the provider again. Choose a name you are willing to keep.

   | Field | What GitHub requires |
   | --- | --- |
   | **GitHub App name** | Unique across all of GitHub, and at most 34 characters. The obvious names are often already taken, so qualify the name with your organisation — for example `VibeData Studio - Acme`. GitHub shows this name, lowercased and hyphenated, every time the App acts on a repository. |
   | **Homepage URL** | A complete, well-formed URL. If you have no page for this App, use your organisation's own GitHub URL: `https://github.com/<your-org>`. |

4. Under **Identifying and authorizing users**, register this callback URL. Build it by
   appending the path to your Studio domain, in full. If your Studio domain is
   `studio.example.com`, the URL is:

   ```
   https://studio.example.com/api/v1/connect/github-commits/callback
   ```

   **This one URL is the whole requirement.** It is the only path Studio ever sends GitHub as a
   `redirect_uri`, and it belongs to the flow where a person links their own GitHub account
   inside Studio. Your operator saving the connection in Org Settings does not use it: that save
   is non-interactive, validating the App from its Client ID and private key without any browser
   redirect. So there is no second URL to find, and no second visit to this page.

   Register the complete URL, not the path alone. `STUDIO_DOMAIN` — the DNS name for it —
   comes from your Azure infrastructure owner; see
   [01d-prereqs-azure-infra](01d-prereqs-azure-infra.md).

   Leave **Request user authorization (OAuth) during installation** unchecked. Studio starts
   the authorisation flow itself and names the callback URL it needs each time.
5. Under **Webhook**, uncheck **Active**. Studio does not need webhook events for this setup.
6. Under **Repository permissions**, set exactly these seven permissions:

   | Permission | Access |
   | --- | --- |
   | Contents | Read and write |
   | Metadata | Read-only |
   | Pull requests | Read and write |
   | Workflows | Read and write |
   | Variables | Read and write |
   | Secrets | Read and write |
   | Administration | Read-only |

   Leave every other permission, and every organisation and account permission, at **No
   access**.

   **Read-only is right for `Administration` — do not grant it write.** Studio uses this
   permission for one thing: reading the domain repository's default-branch protection, so it can
   report whether the recommended branch rules are in place. Reading branch protection is what
   GitHub gates behind `Administration`; nothing Studio does needs to change a repository's
   settings. Granting write hands the App the ability to alter repository configuration for no
   benefit.

   **Three permissions people commonly add here are not needed.** `Actions`, `Issues`, and
   `Administration: write` are all outside what Studio uses. Adding them widens the App without
   fixing anything.

   **`Secrets` is required, not optional.** Studio writes GitHub Actions secrets into each
   domain repository: `MOTHERDUCK_TOKEN` if your data platform is MotherDuck, and `LLM_API_KEY`
   on MotherDuck and Microsoft Fabric once the operator sets a default LLM profile. GitHub
   treats **Variables** and **Secrets** as two separate permissions, so granting Variables does
   not cover this. Without `Secrets`, creating a domain fails at the secret-write step with a
   GitHub 403. Studio reports it as `repository_secret_permission_denied`: "A GitHub Actions
   repository secret could not be written — the calling account lacks permission." The message
   names the cause, so the failure is recognisable; the fix is this permission.

   **`Administration` is the one you can safely leave out, and you will see the cost.** Without
   it, every domain your team creates on MotherDuck or Microsoft Fabric finishes with a warning:
   *"GitHub repository `<org>/<repo>` is missing recommended branch rules: cannot verify
   default-branch protection (insufficient permission)."* Nothing is blocked — the check is
   advisory and the domain still works. But the message reads as though the caller's own access
   is wrong, and it does not name this permission, so it costs a diagnosis every time somebody
   new sees it. Granting `Administration: read` removes it permanently.

   **Adding a permission later is not finished until an owner approves it.** GitHub does not
   extend an existing installation automatically. Changing the App's permission set raises a
   **request**, and until an organisation owner approves that request on the installation, the
   App keeps running with its old permissions — no error, no prompt, no sign anything is
   pending. So if you created this App with a narrower set and are adding to it now, do two
   things: change the permissions on the App, then go to the installation and approve the
   request. Checking only the App's settings page will show the new permissions and tell you
   nothing about whether the installation has them.

   This is worth care because the failure it produces looks like the permission was never
   granted. An App whose settings list `Secrets` but whose installation has not been approved
   fails the secret-write step exactly as an App without `Secrets` does.
7. Under **Where can this GitHub App be installed?**, choose the option that matches who will
   use Studio. This is the App's **visibility**, and it controls two separate things: which
   accounts can **install** the App, and which people can **authorize** it.

   Authorization is the one that decides whether your colleagues can work. Every person who
   uses Studio to work on a domain repository authorizes this App from inside Studio, so that
   Studio can act on GitHub as them. GitHub documents the rule directly: a public App can be
   installed and authorized by any GitHub user, while a private App "can only be installed on
   the account that owns the app. Only members of the organization that owns it can authorize
   it."

   | Your situation | Choose |
   | --- | --- |
   | The App is owned by a GitHub organisation, and everyone who will use Studio is a member of that organisation | **Only on this account** |
   | The App is owned by a personal GitHub account | **Any account** |
   | The App is owned by an organisation, but someone who will use Studio is not a member of it | **Any account** — or add those people to the organisation and keep **Only on this account** |

   A private App owned by a personal account can be authorized by that one person and nobody
   else. Every other Studio user's **Connect GitHub** then fails at GitHub, with nothing wrong
   in Studio's own configuration and no setting in Studio that can fix it.

   If you are not certain that every future Studio user will be a member of the owning
   organisation, choose **Any account**. Visibility can be changed later on the App's own
   settings page, but each blocked person stays blocked until it is.

   **What Any account does not do.** It does not publish the App to GitHub Marketplace — that
   is a separate, deliberate submission. It does not give anyone access to your organisation's
   repositories: every installation reaches only the repositories that installation's own owner
   selected. It does not let anyone into Studio; who can sign in to Studio is decided by the SSO
   provider your operator registers, which on this deployment style is Microsoft Entra. What
   this setting does do is give the App a landing page with an **Install**
   button, so a GitHub user who finds that page can install the App on their own repositories.
8. Save the App.

If the callback URL is missing or does not match, GitHub rejects the sign-in with
`redirect_uri_mismatch`. This surfaces when a person links their own GitHub account, not when
your operator saves the connection — that save never uses the callback URL, so it succeeds
either way. You can add or correct the URL later on the same settings page.

## Install the App

After saving, GitHub prompts you to install the App, or shows an **Install App** option in
the App's own settings page. Install it on the account that owns the repositories your domains
will use: your organisation account in the normal case, or your personal account if you
registered the App there because you have no organisation. Do not install an
organisation-owned App on a personal account — the repositories it must reach are the
organisation's.

Installing the App and authorizing it are two different grants, and installing does not cover
your colleagues. The installation you make here gives Studio access to the repositories you
select. Each person who later works on a domain repository still authorizes the App for
themselves, from inside Studio, and step 7's visibility setting is what decides whether they
can.

When GitHub asks which repositories the App can access, choose either:

- **All repositories**, or
- **Only select repositories** — in this case, include every repository that will become a
  Studio Domain's repository, now or later.

Note which choice you made. If you choose select repositories and a new Domain's repository
is not on the list later, add it from the same install screen before that Domain is created.

## Values to send back

Find these values on the App's own settings page, under **General**:

| Value | Where to find it |
| --- | --- |
| `GITHUB_APP_CLIENT_ID` | **General → Client ID**. |
| `GITHUB_APP_CLIENT_SECRET` | **General → Client secrets** — select **Generate a new client secret** and copy it immediately. GitHub shows it only once. |
| `GITHUB_APP_PRIVATE_KEY` | **General → Private keys** — select **Generate a private key**. GitHub downloads a `.pem` file; send its full contents. |

**Three values, and the App ID is not one of them.** Studio authenticates as the App using the
Client ID and the private key, then asks GitHub for the App's own identity — its numeric ID and
its slug — from that authenticated session. Sending the App ID separately is unnecessary, and
Studio's form has no field for it. If you are working from an older copy of this request that
asked for a fourth value, sending it does no harm; it will simply not be used.

Send all of them back to the person setting up Studio, together with which repositories
the App can access. The client secret and the private key are credentials — send them
through a secret manager, password vault, or another channel your organisation already
trusts for this kind of handoff, not by email or chat. GitHub downloads the private key as a
`.pem` file and will not show it again, so keep a copy until it is safely delivered.

**There is no installation ID to send.** Studio finds the installation itself, by matching the
App's slug against the installations it can see. Nothing asks you for the installation's numeric
ID, and Studio's GitHub panel has no field for one.

This is worth stating because it changes what "the App is installed" has to mean. Studio locates
the installation by the App's **slug**, which GitHub derives from the App's name — so the name
you chose in step 3 is what ties the two together. Rename the App later and Studio stops finding
the installation until your operator saves the provider again. That is the same warning as step
3, and this is why it matters.

## Where this goes

Studio stores these values in **Org Settings → GitHub**, which configures the GitHub
Commit Provider. The three do two different jobs, which is why all three are needed:

- **Client ID and private key.** Together these let Studio act *as the App*. It signs a token
  with the private key, presents the Client ID as the App's identity, and mints a
  repository-scoped installation token whenever it needs to act on a domain repository without
  a person driving. This pair is also how Studio discovers the App's numeric ID and slug, and
  through the slug, the installation you created above.
- **Client ID and client secret.** These drive GitHub's user authorisation flow — the
  browser redirect that sends a person to GitHub and back to the callback URL in step 4, so
  each person can link their own GitHub account. Without the callback URL registered, this
  pair cannot be used at all.

The Client ID appears in both because it identifies the same App in both roles. What separates
them is the credential it is paired with: the private key proves the App to itself, and the
client secret proves it during a person's browser sign-in.

**Saving the connection does not use the callback URL.** Your operator's save validates the
Client ID and private key directly against GitHub, with no browser redirect. A missing or wrong
callback URL therefore passes at save time and fails later, the first time somebody links their
own account.

The operator enters these values during organisation setup — see
[05-configure-org](05-configure-org.md).
