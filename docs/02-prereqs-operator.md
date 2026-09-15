---
applies-to: vibedata v0.1.33
verified-against: studio@a121fc466
verified-on: 2026-08-13
sources:
  - cli/vibedata/src/vibedata/main.py
  - cli/vibedata/src/vibedata/auth/github_container_auth.py
  - cli/vibedata/src/vibedata/commands/install.py
  - cli/vibedata/src/vibedata/commands/login.py
  - cli/vibedata/src/vibedata/commands/install_kubernetes.py
  - cli/vibedata/src/vibedata/core/credentials.py
  - cli/vibedata/src/vibedata/core/data_dir.py
  - cli/vibedata/src/vibedata/templates/docker-compose.yml.j2
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

Install the GitHub CLI, `gh`, as well. The sign-in section below uses it, and the install
depends on it. You do not need the Azure CLI on your machine for any data platform: Studio
carries `az` inside its own container, and the Azure sign-in section below runs it there.

Three more things the installer checks before it pulls any image, each of which stops the
install if it is not true:

- **Docker must be running**, not only installed. If the daemon is not up, the install
  stops and tells you to start Docker Desktop and wait for the whale icon to stop
  animating.
- **Port `5173` must be free.** This is the port Studio's web interface uses. It is also
  Vite's default port, so another local development server is the usual cause. Stop
  whatever holds the port, then run the install again.
- **Docker needs enough CPU and memory** if you plan to use an observability flag on
  [03-deploy-docker](03-deploy-docker.md). Installing with `--with-observability` or
  `--full-observability` stops if Docker Desktop is sized too small; raise the limits under
  Settings > Resources, or install without the flag.

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

Install `kubectl` and `helm`, and have your kubeconfig for the AKS cluster ready — the
`AKS_KUBECONFIG` value from
[01d-prereqs-azure-infra](01d-prereqs-azure-infra.md). The CLI checks for both tools on
`PATH` before it will proceed, and exits with a clear error naming whichever one it
cannot find.

`vibedata install kubernetes` asks you to confirm the kubeconfig path, even when you pass
`--kube-context`. If you script the install, pipe a newline into it — `yes "" | vibedata
install kubernetes …` — because a closed input stream makes the prompt read as `Aborted`
instead of accepting the default.

## Install the vibedata CLI

Run the public installer:

```bash
curl -fsSL https://github.com/accelerate-data/vibedata-official/releases/latest/download/install.sh | sh
```

It detects your platform and downloads the matching binary from the latest
`vibedata-official` release, into `~/.local/bin` by default — set `VIBEDATA_INSTALL_DIR`
before running it to install somewhere else. Binaries are published for `darwin-arm64`,
`linux-arm64`, `linux-x86_64`, and `windows-x86_64`.

**On an Intel Mac**, the installer still downloads the `darwin-arm64` binary — it maps every
macOS host to that one asset, and no Intel build is published. The download and the
`chmod +x` both succeed, so the first sign of trouble is `vibedata version` failing to run.
Use an Apple Silicon Mac, a Linux host, or Windows instead.

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

To check whether your binary is current, compare `vibedata version` against the
`vibedata-official` releases, and only those:

```bash
gh release list --repo accelerate-data/vibedata-official --limit 1
```

CLI releases carry a `v` prefix, such as `v0.1.26`. Do not compare against any other
repository's release list — they run on their own numbering, so a higher number elsewhere
does not mean your CLI is out of date.

## Sign in to Azure, for Microsoft Fabric on Local Docker

> **Applies to: Local Docker with Microsoft Fabric.** Skip if your data platform is DuckDB
> or MotherDuck, or your deployment style is Kubernetes on Azure.

Under Local Docker, Studio acts on Microsoft Fabric using the Azure CLI session inside its own
`api` container. That session is how Studio acquires tokens for Fabric.

It is also the identity Studio's workspace read check runs as. That check **does** run here, so
this identity needs at least Viewer access on the domain's workspace — without it the domain
lands `Failed` at binding validation. What is skipped under Local Docker is the separate
service-principal grant check described in
[01b-prereqs-fabric-admin](01b-prereqs-fabric-admin.md) step 5, and the per-user connect check,
neither of which applies when there is no signed-in Studio user.

**Sign in inside Studio's `api` container, not on this machine, and do it after you
deploy.** Studio's backend runs inside that container and calls `az` there. The container
reads its Azure sign-in state from `/data/azure-config`, which is Studio's own
`azure-config` folder under `DATA_DIR` — not from your `~/.azure`. Nothing copies one into
the other, so an `az login` run in your own shell never reaches Studio.

This means the step has to wait until [03-deploy-docker](03-deploy-docker.md) has brought
the containers up. Once it has, run:

```bash
docker compose -f ~/.vibedata/studio/docker-compose.yml exec -it api az login --use-device-code
```

Use `--use-device-code`. The container has no browser, so the normal interactive sign-in
cannot complete there. If you set a non-default `DATA_DIR`, point `-f` at that path instead.

Confirm the container is signed in:

```bash
docker compose -f ~/.vibedata/studio/docker-compose.yml exec api az account show --output table
```

If you have several Azure subscriptions, pick the right one without signing in again:

```bash
docker compose -f ~/.vibedata/studio/docker-compose.yml exec -it api az account set --subscription <subscription-id>
```

Tell your Fabric workspace administrator which identity this is, so they can grant it access to
the domain's workspace.

**If you sign in on this machine instead of inside the container, Studio cannot see the
session at all.** The sign-in succeeds and looks correct, but Studio acquires no token. That
appears as a token failure, not as a permissions problem — so run the `az account show` command
above before you go looking for a missing workspace grant. See
[90-troubleshooting](90-troubleshooting.md).

## Sign in to GitHub

> **Applies to: Local Docker.** Skip if you chose Kubernetes on Azure — Kubernetes on
> Azure signs users in through Microsoft Entra SSO instead, and `vibedata install
> kubernetes` never asks for a `gh` session.

Local Docker Studio has no separate sign-in step of its own: it takes your identity from a
GitHub CLI session. `vibedata install compose` makes sure Studio's `api` container has one.
Sign in before you install:

```bash
gh auth login --scopes repo,read:org,workflow
```

**What this step actually does.** It is a bridge, not a simple check. Studio's GitHub work
happens inside the `api` container, so the installer:

1. Looks for a GitHub token **inside the container** first. If one is there, the step
   passes and your own machine is never consulted.
2. Otherwise reads the token from your machine's `gh` session. Only a failure here produces
   the "not signed in" block.
3. Imports that token into the container, which keeps its own copy in the `gh-config`
   folder under `DATA_DIR`.
4. Configures git inside the container.

Two consequences worth knowing. First, a later install can pass with no `gh` session on
your machine at all, because step 1 finds the container's stored copy — so a green install
is not proof that your own session is still valid. Second, steps 3 and 4 can fail on their
own, and all three failures report the same `MISSING_CLI_AUTH` reason; read the message, not
just the reason, because "signed in on your machine" does not rule these out.

Because Studio uses the token stored in the container, replacing the token on your machine
changes nothing until a later install imports the new one.

The installer does not inspect which scopes your token
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
replaceable, but `DATA_DIR` is not — back it up the way you would any other data you cannot
regenerate.

Replaceable does not mean replaced every time. `vibedata install compose` and `vibedata
update compose` both run `docker compose up`, which recreates a container only when its
image or its rendered configuration changed. Re-running the install with nothing changed
leaves your running containers as they are. If you hand-edit
`~/.vibedata/studio/docker-compose.yml` or `.env` and re-run the install, the CLI rewrites
those files from its own stored state, so your edit does not survive and no container is
replaced on its account.

## Your CLI credential directory

Whichever deployment style you chose, the CLI keeps a small local directory of its own at
this same default path, `~/.vibedata/studio`: `vibedata login` and `vibedata logout` both
resolve it unconditionally, before looking at which deployment style or Studio instance you
are signing in to. This is separate from Studio's own durable storage — on Kubernetes on
Azure it holds nothing but this record, not any Studio data.

**The credential itself is not in that directory.** The file it writes,
`credentials.json`, records only which keyring entry to look in. The credential is stored
in your operating system's keyring — Keychain on macOS, Credential Manager on Windows, a
Secret Service provider on Linux.

Two things follow from that:

- **A usable keyring is a prerequisite for `vibedata login`**, on both deployment styles. A
  headless Linux host with no Secret Service running has none, and `vibedata login` stops
  with a message asking you to unlock or configure the OS keyring. Check before you need it:

  ```bash
  vibedata auth keyring-check
  ```

  It prints the backend it found and exits `0` when the keyring works.

- **Copying `~/.vibedata/studio` to another machine does not move your CLI credential.** It
  moves only the record pointing at a keyring entry that does not exist there. Nothing fails
  at copy time; the credential is simply missing at first use. Run `vibedata login` again on
  the new machine.
