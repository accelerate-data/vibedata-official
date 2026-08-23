# Operator prerequisites

This page is for the person who will run the `vibedata` CLI.

## Install the Vibedata CLI

Published Vibedata CLI and Studio releases are paired 1:1. Install the CLI from `vibedata-official`:

```bash
curl -fsSL https://github.com/accelerate-data/vibedata-official/releases/latest/download/install.sh | sh
```

Then check:

```bash
vibedata version
```

This draft set is verified against `studio/main`, which may be ahead of the latest published CLI. When running a public release, follow the behavior of the version-matched binary rather than assuming every `main` feature has shipped.

`DATA_DIR` defaults to `~/.vibedata/studio` on macOS/Linux and the equivalent user-profile path on Windows.

## Local Docker prerequisites

> **Applies to: Local Docker.** Skip if you chose Kubernetes on Azure.

Install and start:

- Docker Engine or Docker Desktop;
- Docker Compose support;
- GitHub CLI (`gh`).

Before installing Studio, sign in to GitHub:

```bash
gh auth login --scopes repo,read:org,workflow
```

The Compose installer imports this session into Studio's API container. `GIT_PAT_TOKEN` and `GITHUB_PAT` are not the supported ambient-auth substitute.

### Frontend port

A new install defaults to host port `5173`. It is no longer a fixed requirement. If 5173 is occupied, choose another port:

```bash
vibedata install compose --frontend-port 5174
```

The chosen port is persisted in installer state.

### Remote access to Local Docker

The UI binds to all host interfaces. If people will open it by a hostname or LAN IP and need bundled companion-app OAuth to work, install with the address they will actually use:

```bash
vibedata install compose --studio-url http://<host-or-ip>:5173
```

Local Docker supports HTTP for this installer-managed URL. It is not a production SSO deployment.

### Fabric on Local Docker

> **Applies to: Local Docker + Microsoft Fabric.**

Do not run `az login` on the host and assume Studio can see it. After the containers are running, sign in inside the API container:

```bash
docker compose -f ~/.vibedata/studio/docker-compose.yml exec -it api az login --use-device-code
```

Confirm:

```bash
docker compose -f ~/.vibedata/studio/docker-compose.yml exec api az account show --output table
```

The Azure CLI state is persisted under Studio's `DATA_DIR`.

## Kubernetes on Azure prerequisites

> **Applies to: Kubernetes on Azure.** Skip if you chose Local Docker.

Install on the operator machine:

- `kubectl`;
- `helm`;
- the version-matched `vibedata` CLI.

Have the following from the Azure infrastructure owner:

- kubeconfig path and context;
- public Studio domain;
- Azure Files storage URL;
- Key Vault URL;
- vault identity client ID when needed;
- storage resource group when needed.

Check cluster access before installing:

```bash
kubectl --context <context> get nodes
```

The current Kubernetes installer supports `--cloud azure`. It verifies `kubectl` and `helm` before modifying the cluster.

### Know the required vault secrets before provisioning

Run:

```bash
vibedata install kubernetes --cloud azure --list-secrets
```

Add the same observability flag you plan to use. This command does not require the cluster and is the authoritative list for that CLI build.

## CLI login and keyring

The `vibedata` CLI stores login credentials in the operating system credential store, not directly in `credentials.json`.

You can check whether the machine has a usable keyring:

```bash
vibedata auth keyring-check
```

On a headless Linux host without a Secret Service provider, login can fail closed until a supported keyring is available.

## What not to install locally

- You do not need the Azure CLI on the operator machine for Local Docker Fabric runtime access; that login happens in the API container.
- You do not need a GitHub App for Local Docker.
- You do not need Docker for the Kubernetes installer.

## Next step

- Local Docker: [[Deploy with Local Docker]]
- Kubernetes on Azure: [[Deploy on Kubernetes on Azure]]

---

_Applies to: studio/main (unreleased snapshot). Verified against `studio@5c9d2bbf339a` on 2026-08-22._
