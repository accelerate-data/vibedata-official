---
applies-to: vibedata v0.1.26
verified-against: studio@653beeced
verified-on: 2026-08-08
sources:
  - cli/vibedata/src/vibedata/commands/install.py
  - cli/vibedata/src/vibedata/compose/lifecycle.py
  - cli/vibedata/src/vibedata/release/build_image_set.py
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

> **Applies to: Microsoft Fabric.** Skip if you chose DuckDB or MotherDuck. You still owe
> the Azure sign-in step from [02-prereqs-operator](02-prereqs-operator.md), and it runs
> **after** the install on this page, because it signs Studio's `api` container in and that
> container has to exist first. Sign in on your own machine instead of in the container and
> Studio cannot see it. Come back to that step once the containers are up. That container's
> Azure session is how Studio acquires Fabric tokens. Nothing below depends on it, but
> skipping it means Studio cannot reach Fabric at all once you start using the domain — and
> it surfaces as a token failure, not as a permissions message. See
> [90-troubleshooting](90-troubleshooting.md) if that happens.

## Bring Studio up

Run:

```bash
vibedata install compose
```

This is the only command you need. Three flags control how much observability tooling runs
alongside Studio. Passing none of them is the fourth case, and it is the lean default:

- No flag: the lean default. No observability stack.
- `--with-observability`: adds Grafana, Loki, Tempo, and Prometheus (bundled as one
  container), plus the Alloy collector that feeds them.
- `--full-observability`: adds everything `--with-observability` adds, plus Langfuse, for
  LLM-call observability.
- `--no-observability`: removes the observability stack from an existing install.
  Collected data stays under `DATA_DIR`.

The two flags that add services also raise what Docker has to run. Before it pulls
anything, the installer checks that Docker Desktop is sized for the profile you asked for,
and stops if it is not — raise the CPU or memory limits under Settings > Resources, or
install without the flag. The lean default has no such check.

Pick whichever matches what you want now. You can add more later by reinstalling with a
different flag — see the note below on what that does to Grafana's and Langfuse's
credentials. Reinstalling with no flag does not take you back to lean if you already
installed with `--with-observability` or `--full-observability` — it blocks and asks you to
confirm, rather than silently removing anything you have running. `--no-observability` is
the flag that actually turns the stack off.

## What this command actually does

This is what `vibedata install compose` does, in order:

1. It checks that Docker is running, that Docker is sized for the profile you asked for,
   and that every host port the profile publishes is free. All of this happens before any
   image is pulled, so a failure here costs you nothing but the time to fix it.
2. It generates OAuth client credentials for three bundled companion apps — Grafana,
   Langfuse, and Obot — on your machine, regardless of which observability flag you chose:
   the credential-generation step takes no observability parameter at all. These
   credentials are generated once and never rotated on a later reinstall — only their
   issuer URL updates if you set `--studio-url` (the flag for reaching Studio at this
   machine's LAN address instead of `localhost`). If you installed the lean default,
   Grafana's and Langfuse's companion services never start, so their credentials sit unused
   until you reinstall with an observability flag.
3. It renders Compose's YAML file and a `.env` file into `DATA_DIR` (the directory
   [02](02-prereqs-operator.md#where-studio-keeps-its-data) describes — `~/.vibedata/studio`
   by default), writing those credentials into `.env` as part of the same pass. The render
   is the only thing that writes `.env`; nothing comes back to it afterward. So if OAuth
   values in `.env` look wrong, the cause is upstream of the render, not a later step that
   failed to run.
4. It pulls the container images Compose needs, then brings every container up in one
   attempt — there is no separate second install phase. A container whose image tag,
   environment or profile changed **is** stopped and recreated: the CLI runs `docker compose
   up` without `--no-recreate`, so Compose replaces anything whose definition moved. Expect
   this on a reinstall that adds a flag, because adding one rewrites the Compose file. Your
   data is not at risk — every service reads and writes inside the data directory on your
   own disk, so nothing lives only inside a container. If containers take a while to report
   healthy, the CLI may
   reissue `docker compose up` a few times while it waits, for up to five minutes total.
   That is Compose settling in, not a second pass — if your install pauses partway through,
   let it run; it gives up and reports a failure only after that five minutes is up. That
   five-minute wait only applies while containers are still coming to health — a failure of
   another kind (a missing or already-broken service) is reported straight away, not held
   for five minutes.
5. Once containers are up, Studio reads those credentials from its own environment and
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

One more image sits outside those three lines, because it is not a container in the stack:

- **The agent-server image.** Studio starts a container from it each time you run an
  intent, so it is fetched the first time you use an agent feature rather than during the
  install. A machine that can install Studio but cannot reach the registry later will fail
  at that point, not at install time.
- **`vibedata --json install compose` pulls a different set.** The machine-readable form
  pulls from an explicit image list rather than from the rendered Compose file, and that
  list includes the agent-server image even under the lean default. If you script the
  install with `--json`, or pre-seed a mirrored registry from the list above, account for
  it.
- **`--skip-pull` installs from images you already hold.** It tells the install not to fetch
  anything from the registry, so every image in the list above must already be present
  locally or the install fails. Use it when you have loaded the images by another route;
  leave it off for a normal install. `vibedata update compose` accepts it too.

## The containers this starts

With no observability flag, four containers run: `postgres`, `api` (the Studio backend),
`frontend` (Studio's UI and reverse proxy, the one you open in your browser), and `obot`.

`--with-observability` adds three more: `nginx-exporter`, and the observability bundle
itself — one container running Grafana with Loki, Tempo, and Prometheus, plus the `alloy`
collector that feeds it.

`--full-observability` adds the Langfuse stack on top of that: `langfuse-web`,
`langfuse-worker`, a one-time `langfuse-db-init` container, `langfuse-clickhouse`,
`langfuse-redis`, `langfuse-minio`, and a one-time `langfuse-minio-init` container.

Only `frontend` is reachable from your network, on port `5173`. Alloy also publishes two
ports, for OTLP ingest, but only on `localhost` — not reachable from other machines. Every
other container — Grafana, Langfuse, Alloy's collector UI — is reached through `frontend`,
not through a port of its own.

**Port `5173` is fixed from the command line.** `vibedata install compose` has no flag to
change it, and `--studio-url` does not change it either — that flag sets the address Studio
advertises, not the port it binds. So `5173` has to be free before you install: the pre-flight check
stops the install with a port-conflict message if something else holds it. `5173` is also
Vite's default port, which is the usual reason it is taken. Stop the other service, then
run the install again.

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
`AUTH_ENABLED=false`. Studio takes your identity from the GitHub token the installer
imported into its `api` container — the session you set up in
[02](02-prereqs-operator.md#sign-in-to-github) — and there is no bootstrap key in this mode.
Put those two facts together: **anyone who can reach that port over the network signs in as
you, with owner access, no credentials needed.**

Act on this, don't just note it. Run Local Docker on a machine you trust. If that machine
sits on a shared or untrusted network, restrict the port with your host firewall so only
the devices you choose can reach it.

## Sign in for the first time

Open Studio in your browser, at the URL `vibedata install compose` prints once it finishes
— `http://localhost:5173`. Studio signs you in immediately, using the GitHub token it
imported in [02](02-prereqs-operator.md#sign-in-to-github). You become `vibedata_owner`, the
one operator this deployment has, automatically. There is nothing to type — no password, no
setup form.

That first sign-in needs outbound access to `api.github.com`: Studio calls GitHub to
resolve who you are. On a network that blocks it, Studio shows "Run `gh auth login`, then
refresh Studio" — advice that will not help, because your token is fine. Check outbound
access before you go back to `gh`.

The installer prints more than the Studio URL. Read the whole block:

- The Obot URL, always — `http://localhost:5173/obot/`.
- Under an observability flag, the Grafana, Alloy, and Langfuse URLs, all as paths under
  the same address, plus where their passwords live in `.env`.
- Under the lean default, the path to Studio's log files under `DATA_DIR`. With no
  observability stack running, those logs are your main diagnostic.
- A reminder that Studio listens on all interfaces, and the exact `--studio-url` command to
  reinstall with if you want to use it over the network.

**Take that last one seriously if you plan to reach Studio from another device.** Studio
itself works over the LAN without `--studio-url`, but the companion apps do not: Grafana,
Langfuse, and Obot sign in through Studio, and their sign-in addresses are built from
`localhost` unless you set the flag. Reinstalling with `--studio-url http://<host-ip>:5173`
sets one address for all of them. Without it, Studio loads from another machine and the
companion logins fail.

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

Every long-running container should show as running, and healthy once its health check has
had time to pass.

Two containers are the exception, and only under `--full-observability`:
`langfuse-db-init` and `langfuse-minio-init` are the one-time set-up containers named
earlier on this page. They do their work and stop, so `Exited (0)` is the correct result
for both. The install treats a clean exit from those two as success rather than as a
container that died, so it does not hold up the install. Do not tear the stack down or force
a rebuild over those two lines.

**Studio does not come back on its own after a reboot.** No service in the generated Compose
file sets a restart policy, so restarting Docker or the host leaves every container stopped.
Bring Studio back with `vibedata compose up` from the same data directory. If you want Studio
to start automatically, that is yours to arrange on the host — a service unit or a login item
that runs the same command.

This is the command to reach for — there is no `vibedata` command that reports service
status.
