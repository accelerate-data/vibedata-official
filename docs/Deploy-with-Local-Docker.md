# Deploy Studio with Local Docker

> **Applies to: Local Docker.** Skip if you chose Kubernetes on Azure.

Local Docker is a single-operator, ambient-auth deployment. The supported installer renders `AUTH_ENABLED=false`; there is no Studio browser-login gate.

Restrict network access to the machine accordingly.

## 1. Sign in to GitHub on the host

Before installation:

```bash
gh auth login --scopes repo,read:org,workflow
```

The installer imports this session into the Studio API container.

## 2. Install Studio

Run:

```bash
vibedata install compose
```

The CLI and Studio version are paired. The installer renders its state under `DATA_DIR`, pulls images, starts the stack, applies migrations, and verifies readiness.

A fresh installation uses frontend port `5173`. If that port is not available:

```bash
vibedata install compose --frontend-port 5174
```

The selected port is persisted.

## 3. Choose observability

The default install is core-only.

| Flag | Adds |
| --- | --- |
| none | Studio core only |
| `--with-observability` | LGTM/Grafana + Alloy |
| `--full-observability` | LGTM + Alloy + Langfuse and its supporting services |
| `--no-observability` | Explicitly removes the optional observability topology |

Forgetting the flag on a later run does not silently remove an installed observability profile.

The full profile is materially larger than core. Size Docker Desktop resources before enabling it.

### Current memory caps

Current Compose files apply per-container caps. Core is approximately 2.1 GB of capped service memory before Intent agent containers. LGTM adds approximately 2.8 GB, and full observability adds several more GB.

Treat the rendered Compose files as authoritative if exact numbers change.

## 4. Set the address users will open

Studio's UI listens on all host interfaces. If you use it only on the same machine, the default localhost address is enough.

If another machine will open Studio and you need Obot, Grafana, or Langfuse OAuth callbacks to work, install with the externally used HTTP origin:

```bash
vibedata install compose --studio-url http://192.0.2.10:5173
```

or a local hostname:

```bash
vibedata install compose --studio-url http://studio.lan:5173
```

The supported Local Docker installer does not manage HTTPS termination.

## 5. Fabric only: sign in to Azure inside the API container

> **Applies to: Microsoft Fabric.** Skip for DuckDB and MotherDuck.

After Studio is up:

```bash
docker compose -f ~/.vibedata/studio/docker-compose.yml exec -it api az login --use-device-code
```

Confirm:

```bash
docker compose -f ~/.vibedata/studio/docker-compose.yml exec api az account show --output table
```

If `DATA_DIR` is not the default, use the Compose file under your chosen data directory.

This ambient Azure identity is the interactive Fabric identity for Local Docker. It must be able to reach the Fabric resources the Domain binds.

## 6. Verify the imported GitHub session

```bash
docker compose -f ~/.vibedata/studio/docker-compose.yml exec api gh auth token >/dev/null
```

If this fails, sign in again on the host and rerun `vibedata install compose` so the installer imports the current host session.

## 7. Protect `DATA_DIR`

`DATA_DIR` contains durable application data and credential caches, including generated `.env` and `state.json` files.

On POSIX systems the installer writes sensitive state files owner-only. Do not commit, share, or broaden access to this directory.

Back up the data directory using the supported `vibedata` backup flow before upgrades or host migration.

## 8. Understand the network boundary

Local Docker has no Studio login gate. Anyone who can reach the UI can operate the instance.

Use the host firewall, LAN segmentation, VPN, or another network control to restrict access. Do not expose a Local Docker evaluation instance directly to the public Internet as though it were the delegated Kubernetes deployment.

## 9. Update later

Use:

```bash
vibedata update compose
```

The updater reuses installer state and takes a backup before replacing containers.

## Next step

Continue to [[Configure the Studio Instance]]. Local Docker skips SSO and GitHub App setup, but still needs an LLM Profile before normal Intent work.

---

_Applies to: studio/main (unreleased snapshot). Verified against `studio@5c9d2bbf339a` on 2026-08-22._
