---
applies-to: vibedata v0.1.26
verified-against: studio@653beeced
verified-on: 2026-08-05
sources:
  - docs/wiki/install.md
  - cli/vibedata/src/vibedata/main.py
  - cli/vibedata/src/vibedata/auth/github_container_auth.py
  - cli/vibedata/src/vibedata/commands/install.py
  - cli/vibedata/src/vibedata/commands/login.py
  - cli/vibedata/src/vibedata/commands/install_kubernetes.py
  - cli/vibedata/src/vibedata/core/data_dir.py
  - cli/vibedata/src/vibedata/core/exit_codes.py
  - cli/vibedata/src/vibedata/k8s/cluster.py
  - cli/vibedata/src/vibedata/compose/lifecycle.py
  - scripts/generate-install-script.sh
  - src/server/modules/domains/services/domain-provisioning-diagnostic.ts
---

# Operator setup: the vibedata CLI and GitHub sign-in

From here on, this guide speaks to you, the person who will run the `vibedata` CLI and
deploy Studio. If you forwarded any of the admin request pages, you can start this page
before those requests come back — nothing here depends on them, except the one kubeconfig
noted below.

By the end of this page you have a working `vibedata` binary on your `PATH` and, if you
chose Local Docker, an authenticated `gh` CLI session.

## Install what your deployment style needs

> **Applies to: Local Docker.** Skip if you chose Kubernetes on Azure.

Install Docker Engine with the Compose plugin, so that `docker compose` works from your
shell. The CLI shells out to `docker compose` to bring Studio up; without the plugin,
`vibedata install compose` has nothing to drive.

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

Install `kubectl` and `helm`, and have your kubeconfig for the AKS cluster ready — the
`AKS_KUBECONFIG` value from
[01d-prereqs-azure-infra](01d-prereqs-azure-infra.md). The CLI checks for both tools on
`PATH` before it will proceed, and exits with a clear error naming whichever one it
cannot find.

## Install the vibedata CLI

Run the public installer:

```bash
curl -fsSL https://github.com/accelerate-data/vibedata-official/releases/latest/download/install.sh | sh
```

It detects your platform and downloads the matching binary from the latest
`vibedata-official` release, into `~/.local/bin` by default — set `VIBEDATA_INSTALL_DIR`
before running it to install somewhere else. Binaries are published for `darwin-arm64`,
`linux-arm64`, `linux-x86_64`, and `windows-x86_64`.

**On Windows**, the installer above needs a POSIX shell and does not run there. Download
`vibedata-windows-x86_64.exe` directly from the `vibedata-official` release page instead,
rename it to `vibedata.exe`, and put it on your `PATH` — the POSIX installer above renames
the downloaded asset to plain `vibedata` for the same reason, so `vibedata version` below
resolves; without the rename, Windows will not find a `vibedata` command on `PATH`.

**There is no Homebrew formula for the `vibedata` CLI.** The `accelerate-data/homebrew-tap`
repository describes itself as a tap for the VibeData CLI, but the only formula it
publishes is `ad-migration`. `brew install vibedata` fails — use the installer above
instead.

Confirm the install:

```bash
vibedata version
```

If your shell reports `vibedata: command not found`, the install directory
(`~/.local/bin`, unless you overrode it) is not on your `PATH` yet — add it and open a new
shell.

## Sign in to Azure, for Microsoft Fabric on Local Docker

> **Applies to: Local Docker with Microsoft Fabric.** Skip if your data platform is DuckDB
> or MotherDuck, or your deployment style is Kubernetes on Azure.

Under Local Docker, Studio has no signed-in Studio user to check Fabric workspace access
against, so it uses the Azure identity behind an `az login` session on this same machine
instead — see [01b-prereqs-fabric-admin](01b-prereqs-fabric-admin.md) for what that check
does and why it runs even on this deployment style. Sign in before you deploy:

```bash
az login
```

Tell your Fabric workspace administrator which identity this is, so they can grant it at
least Viewer access to the domain's workspace, as
[01b-prereqs-fabric-admin](01b-prereqs-fabric-admin.md) describes. Without that access,
your first domain's Provisioning status goes to `Failed` — see
[90-troubleshooting](90-troubleshooting.md) if that happens.

## Sign in to GitHub

> **Applies to: Local Docker.** Skip if you chose Kubernetes on Azure — Kubernetes on
> Azure signs users in through Microsoft Entra SSO instead, and `vibedata install
> kubernetes` never asks for a `gh` session.

Local Docker Studio has no separate sign-in step of its own: it takes your identity from
your own machine's GitHub CLI session. `vibedata install compose` checks for that session,
and stops if it cannot find one. Sign in before you install:

```bash
gh auth login --scopes repo,read:org,workflow
```

**What this check actually confirms, stated plainly:** the installer only checks that
`gh auth token` succeeds — nothing more. It does not inspect which scopes your token
carries, and it does not check whether you belong to any GitHub organisation. But Studio's
GitHub features do need the scopes above: `repo` for reading and pushing to your
repositories, `read:org` for listing the organisations you belong to, `workflow` for pushing
the CI files Studio seeds into a domain repository. A token missing one of these fails
quietly rather than with an error — for example, a repository dropdown that silently shows
only your personal repos — so grant all three now to avoid a confusing partial failure
later. A personal GitHub account with no organisation membership at all is enough to
complete this step and sign in to Studio.

**This check runs at the end of the install, not before it.** Compose brings your
containers up first; the GitHub session check runs only after they report ready, so a
blocked install still leaves Studio's containers running — it is not a pre-flight gate.
If it blocks, the CLI exits with code `3` (`BLOCKED`) and **prints no service URLs** — do
not go looking for them. Sign in with `gh`, then run `vibedata install compose` again.
Bringing up already-running containers is safe, so the whole flow — pull, up, readiness —
repeats without harm, and the service URLs print once the check passes.

## Where Studio keeps its data

> **Applies to: Local Docker.** Skip if you chose Kubernetes on Azure — there, durable
> storage is the Azure Files share from
> [01d-prereqs-azure-infra](01d-prereqs-azure-infra.md), not a local directory.

`vibedata install compose` writes durable state to a directory on your machine —
`DATA_DIR`. It defaults to `~/.vibedata/studio`, and you can point it elsewhere by setting
the `DATA_DIR` environment variable before you run the CLI. Make sure whichever path you
use is writable by your user.

Treat this directory as the durable part of your install: the containers themselves are
replaceable and get recreated on every `vibedata install compose` or `vibedata update
compose`, but `DATA_DIR` is not — back it up the way you would any other data you cannot
regenerate.

## Your CLI credential directory

Whichever deployment style you chose, the CLI keeps a small local directory of its own at
this same default path, `~/.vibedata/studio`, to hold your CLI credential: `vibedata
login` and `vibedata logout` both resolve it unconditionally, before looking at which
deployment style or Studio instance you are signing in to. This is separate from Studio's
own durable storage — on Kubernetes on Azure it holds only your CLI credential, not any
Studio data.
