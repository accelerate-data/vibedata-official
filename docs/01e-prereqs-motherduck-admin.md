---
applies-to: vibedata v0.1.26
verified-against: studio@653beeced
verified-on: 2026-08-05
sources:
  - docs/functional/data-platform/motherduck-backend.md
  - docs/functional/data-platform/README.md
  - src/server/modules/data-platforms/providers/motherduck.descriptor.ts
  - src/server/modules/data-platforms/providers/motherduck.provider.ts
  - src/server/modules/data-platforms/data-platforms.schemas.ts
  - src/features/data-platforms/components/data-platform-editors/motherduck-editors.tsx
  - deploy/docker/Dockerfile.backend
  - src/server/modules/mcp/runtime/motherduck-mcp-proxy.service.ts
  - src/server/modules/data-platforms/helpers/probe.ts
  - src/server/modules/domains/types.ts
  - src/server/modules/domains/services/domain-provisioning-step.ts
  - src/features/settings/components/Settings/modals/domain-destination/motherduck.tsx
---

# Request for your MotherDuck organisation administrator: account, token, and database access

This page asks for access in your organisation's MotherDuck account. Nothing here requires
access to Studio or to any Accelerate Data system, only to your organisation's MotherDuck
account.

This whole page applies only if your data platform is **MotherDuck**. Skip it entirely if
you chose **DuckDB** or **Microsoft Fabric**. Everything on this page applies whether your
deployment style is **Local Docker** or **Kubernetes on Azure** — but one of the asks
below, seats, works differently depending on which one you chose. Read that section
carefully; it is the most consequential part of this page.

## The five things this page asks for

The one hard dependency: the organisation account (step 1) must exist before the Service PAT
(step 2) can be issued, since a PAT is issued against an account. Steps 3 and 4 need step 1's
account to hold the database and Share. Otherwise, the order below is a suggestion, not a
requirement.

### 1. Provide an organisation account

Give your operator the name of the MotherDuck organisation account to use. Your operator
enters this name once, when registering your MotherDuck connection in Studio, and **Studio
stores it write-once** — there is no field to change it afterward. To point Studio at a
different account later, your operator registers a new connection rather than editing this
one.

### 2. Issue a read-write Service PAT

Issue a **Service PAT** with read-write access, and hand it back to your operator. This is
the only kind of token Studio's MotherDuck connection accepts — there is no read-only option
and no read-scaling token slot. Do not offer a read-only PAT; Studio has nowhere to put one.

This PAT is rotatable: if it needs to be replaced later, your operator can update it in
Studio without re-entering the account name.

### 3. Create or nominate the database

Create a new MotherDuck database for this domain, or nominate an existing one, and return
its name. Your operator enters this later, when the domain is created and bound to your
account — not at the point the account and PAT above are registered.

### 4. Create a Share and grant READ, if your team plans to use one

**Studio never creates a MotherDuck Share and never grants READ on one.** If more than one
person will work against the database — anyone other than the database's own owner — create
a Share on the database and grant READ to the identities that need it. If the database will
only ever be driven by its owner, you can skip this step.

**Grant READ to two different kinds of identity, not just one, under Kubernetes on Azure.**
Picking a Share when a domain is created uses the operator's own personal MotherDuck
identity — Studio lists only Shares that identity can already read. Later, a separate,
retryable check confirms the registered **Service PAT** can also read that same Share; this
runs under the Service PAT's own identity, not the operator's. These are two distinct
identities, the same way Microsoft Fabric's operating identity and service principal are
two distinct identities in
[01b-prereqs-fabric-admin](01b-prereqs-fabric-admin.md#4-confirm-the-operating-identitys-own-read-access-to-the-workspace).
Granting the operator's identity READ does not also grant the Service PAT READ — grant both,
or domain creation can succeed while the domain still lands in `Pending` afterward. Under
Local Docker there is only the Service PAT to grant, since one operator drives every
operation through it.

**The Share choice is immutable after the domain is created.** Your operator picks the Share
(or picks none) when the domain is created in Studio, and there is no edit path afterward.
Changing your mind later means recreating the domain, not editing it. Decide before domain
creation, not after.

### 5. Provision seats — read this section before your team commits to a plan

> The MotherDuck plan you choose bounds how many people can work in a domain — and the rule
> is different depending on your deployment style. This is a planning and cost decision, not
> a technical detail to skim.

**Under Kubernetes on Azure**, each person who signs in and works on a domain connects with
their **own** MotherDuck identity — not the Service PAT above. There is no primitive in
MotherDuck for one identity to grant another identity access across account boundaries, and
there is no fallback to the Service PAT if a contributor has not connected their own account.
**Under Kubernetes on Azure, every contributor needs their own seat in your MotherDuck
organisation.**

**Under Local Docker**, there is one operator, and Studio always uses the Service PAT above
for every operation. Seats are not a constraint under this deployment style.

The MotherDuck tiers, and what they cap:

| Tier | Users | Service accounts | Cost |
| --- | --- | --- | --- |
| Lite | 3 | 2 | $0/mo |
| Business | 10 | unlimited | $250/mo plus usage |
| Enterprise | unlimited | unlimited | custom |

These figures are MotherDuck's own published pricing, current as of this page's verification
date above — confirm current pricing and terms with MotherDuck directly, since a vendor can
change either at any time.

Under Kubernetes on Azure, a ten-person contributor team sits exactly on the Business tier's
cap, with no headroom. The Business tier's ten seats are what the plan includes, not a hard
ceiling MotherDuck enforces — but per-seat pricing beyond ten is not publicly published, so
a team past ten contributors is a commercial conversation with MotherDuck, not a self-serve
upgrade. This is a fact to plan and budget around, not a reason to choose a different data
platform or deployment style.

## Network access

Allow outbound access (443/tcp) from wherever Studio runs to:

| Host | Purpose |
| --- | --- |
| `api.motherduck.com` | Studio's REST calls: checking the Service PAT is valid and reaches the named account, and its MotherDuck MCP relay. |
| `extensions.duckdb.org` | Where the DuckDB engine Studio runs on fetches the MotherDuck extension. |
| `*.motherduck.com` | MotherDuck's data-serving connection, the one that carries queries. Recommended starting point, not vendor-confirmed — see the note below this table. |

**The DuckDB MotherDuck extension is fetched over the network the first time Studio opens a
MotherDuck connection — it is not built into Studio's container image.** That first
connection happens during domain creation itself: creating a domain validates that the
bound database (and Share, if configured) is reachable, and that validation is what opens
the connection that loads the extension. In a network that blocks `extensions.duckdb.org`,
**domain creation fails right there** — not later, when someone runs a query. Allow this
host before your team creates its first MotherDuck domain, not only before installing
Studio.

Beyond the two confirmed hosts above, MotherDuck's own client library also opens a direct
connection to MotherDuck's data-serving infrastructure — separate from the REST host
above. This is the same connection used by the domain-creation validation above and by
every query afterward. **MotherDuck does not publish a fixed list of hostnames for this
connection** — which is why the table above lists `*.motherduck.com` as a recommendation,
not a confirmed host. Close the gap with either of these before relying on it in a
restricted network:

- Ask MotherDuck support for the current set of hosts this connection uses.
- Trace the connection through your firewall or proxy during a live test, and allowlist
  what you observe.

Do not treat `*.motherduck.com` as a confirmed, complete list — it is a reasonable starting
point, not a vendor-confirmed one.

## Sending the Service PAT back

Send the Service PAT through a secret manager, password vault, or another channel your
organisation already trusts for credential handoff — not by email or chat.

## Values to send back

| Token | Comes from |
| --- | --- |
| `MOTHERDUCK_ACCOUNT` | The organisation account name from step 1. |
| `MOTHERDUCK_SERVICE_PAT` | The Service PAT from step 2. |

Also send back the database name from step 3, and the Share name from step 4 if you created
one — your operator needs both when the domain is created, though neither is a fixed Studio
token name the way the two above are.

## Where this goes

`MOTHERDUCK_ACCOUNT` and `MOTHERDUCK_SERVICE_PAT` are entered by the operator during
organisation setup — see [05-configure-org](05-configure-org.md). The database name and the
optional Share name are entered only in [06-first-domain](06-first-domain.md), when the
domain is created and bound to your account.
