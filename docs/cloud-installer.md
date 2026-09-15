# Install Studio in the cloud (Vibedata Cloud Installer)

The Vibedata Cloud Installer builds the cloud estate for you and installs Studio into it. You sign in to Azure once, choose the target, and approve one plan; it creates the network, cluster, storage, vault, edge, and DNS, deploys Studio, verifies it, and only then puts the address into service.

It runs entirely on your own machine. Your cloud credentials never leave it, and there is no hosted service in the middle.

For an estate you have already built yourself, use `vibedata install kubernetes` instead — that path is documented in the Kubernetes install guide.

## Prerequisites

- An Azure subscription, and permission to create resources in it.
- The Azure CLI installed. You do not need to sign it in yourself: the provisioning engine authenticates only through the CLI, and the installer runs that sign-in itself when it reaches the point of needing it.
- A supported platform: macOS (Apple Silicon), Linux (x86-64 or ARM64), or Windows (x86-64).

You do **not** need Node, Pulumi, `kubectl`, Helm, or the `vibedata` CLI. The bundle carries all of them, pinned to the release it installs.

## Install

macOS and Linux:

```bash
curl -fsSL https://github.com/accelerate-data/vibedata-official/releases/latest/download/install-cloud-installer.sh | sh
```

The script downloads the bundle for your platform, checks it against the sha256 we published beside it, unpacks it into `~/.vibedata-cloud-installer`, and puts the `vibedata-cloud-installer` command on your `PATH` in `~/.local/bin`. If that directory is not on your `PATH`, the script tells you.

If something else already owns that name, the script leaves it alone and prints the full path to this release's own copy instead.

On Windows, download `vibedata-cloud-installer-win32-x64.zip` from the [latest release](https://github.com/accelerate-data/vibedata-official/releases/latest), extract it, and run `bin\vibedata-cloud-installer.cmd`.

The bundle brings everything it runs — Node, Pulumi, kubectl, Helm and cosign — so you install none of them yourself. The one thing it does not bring is the Azure CLI, which it checks for before offering you a plan.

The bundle is distributed unsigned, the way `kubectl`, Helm, and Pulumi are. The published checksum is what proves you received what we built.

## Run it

```bash
vibedata-cloud-installer
```

It prints the address it is serving and opens its own window. Everything happens there: sign in, choose the subscription and region, run the checks, review the plan, approve it, and watch it run.

To continue in a normal browser, use the **Open in browser** button in the window's top-right corner. It opens your usual browser on this installation; both windows then work on the same one. Click it again any time — each click makes a fresh link, so it still works after you close the tab.

Expect twenty-five to thirty-five minutes for a first installation. The cluster is about half of that and the Studio install most of the rest.

## After the installation

The same app manages the installation from then on. It offers upgrade, backup, pause and resume, recovery onto a replacement cluster, and teardown — each one planned, shown to you, and approved before anything changes.

Two more actions matter for teams:

- **Hand off to another machine** exports the installation into one encrypted file, with a password shown once. Restoring it on a second machine takes over management there. Use it when the original machine is being replaced.
- **Share state with your team** moves the installation's record into a storage container you own, so several operators can manage it. Each of them restores a handoff file once, and from then on they work against the shared record. Only one operator can change the installation at a time; the others see what is running and can inspect it.

## Where state lives

Under `~/.vibedata-installer`:

| Path                               | Holds                                                           |
| ---------------------------------- | --------------------------------------------------------------- |
| `installations.json`               | Which installations exist and where their authorities are       |
| `installations/<id>/journal.jsonl` | What each operation did                                         |
| `pulumi/`                          | The infrastructure state, until you move it to a shared backend |
| `auth-record.json`                 | Your Azure account coordinates — no secret in it                |

Azure tokens are not in that list on purpose: they stay in the Azure Identity cache, inside your operating system's credential store.

Keep this directory. Losing it does not damage the cloud estate, but it does lose the installer's record of what it built.
