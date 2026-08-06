---
applies-to: vibedata v0.1.26
verified-against: studio@653beeced
verified-on: 2026-08-05
sources:
  - cli/vibedata/src/vibedata/commands/install.py
  - cli/vibedata/src/vibedata/templates/docker-compose.yml.j2
  - cli/vibedata/src/vibedata/templates/env.j2
---

# Deploy Studio: Local Docker

This whole page is about `Local Docker`. It applies the same way for all three data
platforms — `DuckDB`, `MotherDuck`, and `Microsoft Fabric` — so nothing here is scoped by
data platform. If you chose `Kubernetes on Azure`, skip this page.

This continues from
[02-prereqs-operator](02-prereqs-operator.md): you already have a working `vibedata`
binary and a signed-in `gh` session on this machine.

> **Applies to: Microsoft Fabric.** Skip if you chose DuckDB or MotherDuck. Confirm you also
> completed the `az login` step in [02-prereqs-operator](02-prereqs-operator.md) before
> continuing — Studio checks that identity's Fabric workspace access as part of creating
> your first domain, later in this doc set. Nothing below depends on it, but skipping it now
> surfaces as a `Failed` domain much later; see
> [90-troubleshooting](90-troubleshooting.md) if that happens.

## Bring Studio up

Run:

```bash
vibedata install compose
```

This is the only command you need. Three flags control how much observability tooling runs
alongside Studio; the default, with none of them, is lean:

- No flag: the lean default. No observability stack.
- `--with-observability`: adds Grafana, Loki, Tempo, and Prometheus (bundled as one
  container), plus the Alloy collector that feeds them.
- `--full-observability`: adds everything `--with-observability` adds, plus Langfuse, for
  LLM-call observability.
- `--no-observability`: removes the observability stack from an existing install.
  Collected data stays under `DATA_DIR`.

Pick whichever matches what you want now. You can add more later by reinstalling with a
different flag — see the note below on what that does to Grafana's and Langfuse's
credentials. Reinstalling with no flag does not take you back to lean if you already
installed with `--with-observability` or `--full-observability` — it blocks and asks you to
confirm, rather than silently removing anything you have running. `--no-observability` is
the flag that actually turns the stack off.

## What this command actually does

This is what `vibedata install compose` does, in order. It corrects an older description
that circulated for this step:

1. It renders Compose's YAML file and a `.env` file into `DATA_DIR` (the directory
   [02](02-prereqs-operator.md#where-studio-keeps-its-data) describes — `~/.vibedata/studio`
   by default).
2. It generates OAuth client credentials for three bundled companion apps — Grafana,
   Langfuse, and Obot — on your machine, and writes all three into `.env`, regardless of
   which observability flag you chose: the credential-generation step takes no
   observability parameter at all. These credentials are generated once and never rotated
   on a later reinstall — only their issuer URL updates if you set `--studio-url` (the flag
   for reaching Studio at this machine's LAN address instead of `localhost`). If you
   installed the lean default, Grafana's and Langfuse's companion services never start, so
   their credentials sit in `.env` unused until you reinstall with an observability flag.
3. It pulls the container images Compose needs, then brings every container up in one
   attempt — there is no separate second install phase, and it never restarts an
   already-running service. If containers take a while to report healthy, the CLI may
   reissue `docker compose up` a few times while it waits, for up to five minutes total.
   That is Compose settling in, not a second pass — if your install pauses partway through,
   let it run; it gives up and reports a failure only after that five minutes is up. That
   five-minute wait only applies while containers are still coming to health — a failure of
   another kind (a missing or already-broken service) is reported straight away, not held
   for five minutes.
4. Once containers are up, Studio reads those credentials from its own environment and
   seeds them into its database as it starts. This is how Grafana, Langfuse, and Obot end
   up able to sign in through Studio without you configuring anything by hand.

No browser opens at any point during this command. You open one yourself, afterward, to
sign in — see below.

If your `gh` session check fails at the very end of this command, see
[02](02-prereqs-operator.md#sign-in-to-github) for what that means: your containers are
already running, no service URLs get printed, and re-running `vibedata install compose`
once you've signed in is safe.
[90-troubleshooting](90-troubleshooting.md#install-reports-missing-cli-authentication) has
the same case as a symptom entry, with the exact `MISSING_CLI_AUTH` reason and exit code.

## Images

Every image `vibedata install compose` pulls is public — verified by anonymous registry
fetch on 2026-08-05, with no credentials of any kind. Which images that means depends on
the flag you chose:

- Pulled with every flag, including the lean default: Studio's backend, its frontend, Obot,
  and Postgres.
- `--with-observability` additionally pulls: the bundled Grafana/Loki/Tempo/Prometheus
  image, Alloy, and the Nginx Prometheus exporter.
- `--full-observability` additionally pulls: the Langfuse images, ClickHouse, Redis, and
  MinIO — none of these four are pulled under the lean default or `--with-observability`.

You do not need to log in to any registry first.

## The containers this starts

With no observability flag, four containers run: `postgres`, `api` (the Studio backend),
`frontend` (Studio's UI and reverse proxy, the one you open in your browser), and `obot`.

`--with-observability` adds three more: `nginx-exporter`, and the observability bundle
itself — one container running Grafana with Loki, Tempo, and Prometheus, plus the `alloy`
collector that feeds it.

`--full-observability` adds the Langfuse stack on top of that: `langfuse-web`,
`langfuse-worker`, a one-time `langfuse-db-init` container, `langfuse-clickhouse`,
`langfuse-redis`, `langfuse-minio`, and a one-time `langfuse-minio-init` container.

Only `frontend` is reachable from your network, on `5173` by default. Alloy also publishes
two ports, for OTLP ingest, but only on `localhost` — not reachable from other machines.
Every other container — Grafana, Langfuse, Alloy's collector UI — is reached through
`frontend`, not through a port of its own.

## Security posture: no password, reachable from your network

`frontend` binds to all network interfaces on your machine, not just `localhost`. This is
deliberate: it is what lets you reach Studio by this machine's IP address from another
device on your network, without an SSH tunnel.

`frontend` is the only container this exposure applies to. Postgres, the Studio backend,
and Obot publish no port to your machine at all — they're reachable only inside Studio's
own internal Docker network. The observability containers, when running, publish nothing
either, except the Alloy collector's two ingest ports, which bind to `localhost` only and
so are not reachable from your network. `frontend` is the single door.

Local Docker has no login screen and no password — in `.env`, this is the literal
`AUTH_ENABLED=false`. Studio takes your identity from this machine's `gh` session — the one
you set up in [02](02-prereqs-operator.md#sign-in-to-github) — and there is no bootstrap key
in this mode. Put those two facts together: **anyone who can reach that port over the network signs
in as you, with owner access, no credentials needed.**

Act on this, don't just note it. Run Local Docker on a machine you trust. If that machine
sits on a shared or untrusted network, restrict the port with your host firewall so only
the devices you choose can reach it.

## Sign in for the first time

Open Studio in your browser, at the URL `vibedata install compose` prints once it finishes
— `http://localhost:5173` unless you changed the port. Studio signs you in immediately,
using the same `gh` session from [02](02-prereqs-operator.md#sign-in-to-github). You become
`vibedata_owner`, the one operator this deployment has, automatically. There is nothing to
type — no password, no setup form.

You do not need to run `vibedata login` for this. That command exists for driving Studio's
API directly from the CLI — against a deployment that has a real login screen, or a remote
one — or for when the CLI's own stored credential is missing or has expired. A fresh
`vibedata install compose` does not need it.

## Confirm Studio is running

Run:

```bash
cd ~/.vibedata/studio && docker compose ps
```

If you set `DATA_DIR` to something other than the default in
[02](02-prereqs-operator.md#where-studio-keeps-its-data), `cd` there instead.

Every container should show as running (and healthy, once its health check has had time to
pass). This is the command to reach for — there is no `vibedata` command that reports
service status.
