---
applies-to: vibedata v0.1.26
verified-against: studio@653beeced
verified-on: 2026-08-08
sources:
  - docs/functional/data-platform/motherduck-backend.md
  - docs/functional/data-platform/README.md
  - src/server/modules/data-platforms/providers/motherduck.descriptor.ts
  - src/server/modules/data-platforms/providers/motherduck.provider.ts
  - src/server/modules/data-platforms/data-platforms.schemas.ts
  - src/features/data-platforms/components/data-platform-editors/motherduck-editors.tsx
  - deploy/docker/Dockerfile.backend
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
deployment style is **Local Docker** or **Kubernetes on Azure** — but two of the asks below
work differently depending on which one you chose: the Share (step 4) and seats (step 5).
Read both sections carefully. Seats is the most consequential part of this page.

## The five things this page asks for

The one hard dependency: the organisation account (step 1) must exist before the token
(step 2) can be issued, since a token is issued against an account. Steps 3 and 4 need step 1's
account to hold the database and Share. Otherwise, the order below is a suggestion, not a
requirement.

**A note on names before you start.** Studio calls the token it stores a **Service PAT**. That
is Studio's own label, and you will not find it in the MotherDuck console. In MotherDuck's own
terms, what this page asks for is a **service account** with a **read/write token**. Where this
page says "Service PAT", read "the read/write token issued for that service account".

### 1. Provide an organisation account

Give your operator the name of the MotherDuck organisation account to use. Your operator
enters this name once, when registering your MotherDuck connection in Studio, and **Studio
stores it write-once** — there is no field to change it afterward. To point Studio at a
different account later, your operator registers a new connection rather than editing this
one.

### 2. Issue a read/write token for a service account

In your MotherDuck console: create a **service account** in the organisation account from
step 1, then issue a **read/write token** for it. Hand that token back to your operator. This
is the value Studio's connection form labels **Service PAT**.

**Issue a read/write token, not a read scaling token.** MotherDuck does publish a read scaling
token, which permits `SELECT` and blocks writes. Studio has no field for one: its MotherDuck
connection holds exactly one token, and that token must be able to write. A read scaling token
entered in that single field will fail as soon as Studio needs to write.

This token is rotatable: if it needs to be replaced later, your operator can update it in
Studio without re-entering the account name.

### 3. Create or nominate the database

Create a new MotherDuck database for this domain, or nominate an existing one, and return
its name. Your operator enters this later, when the domain is created and bound to your
account — not at the point the account and token above are registered.

**Record which identity owns this database.** It decides whether step 4 is optional or
required, and it is easy to get wrong: a database created under your own personal MotherDuck
identity is not owned by the service account from step 2. Creating it under the service
account is the simpler path, because it makes the Share optional.

### 4. Create a Share and grant READ

**Studio never creates a MotherDuck Share and never grants READ on one.** If more than one
person will work against the database — anyone other than the database's own owner — create
a Share on the database and grant READ to the identities that need it.

**Name the Share exactly after the database it carries.** Studio's operator has no field to
type a Share name into. On `v0.1.26` the domain form binds a database and a schema — both
required — and it has **no Share field at all**. Studio looks for a Share arriving under the
same name as the bound database. A Share called anything else is
invisible to Studio, however correctly you granted READ on it. (Builds after `v0.1.26` add a
Share picker to the domain form and lift this naming constraint. Match the database name
anyway — it is correct on both.)

**Skipping this step is safe in one case only: the service account from step 2 owns the
database itself.** Under Kubernetes on Azure, Studio runs a check on every MotherDuck domain
asking whether the **service account's token** — not any human's — can reach the bound
database. It is satisfied by either of:

- The service account **owns** that database, or
- The service account holds a **Share of the same name** as that database, with READ.

So if you created the database under your personal identity and skipped the Share, the check
fails and the domain lands in `Pending` — even though only one person will ever use it. Either
create the Share and grant the service account READ, or make the service account the database
owner in step 3.

Under Local Docker one of the two checks is skipped, but **not** the one that matters here.
The service-PAT read probe that produces `Pending` does not run without delegated
authentication. Binding validation still runs on both deployment styles, and it still resolves
the bound database — through a Share if one exists, otherwise by the database's own name. So a
database the credential cannot reach still fails on Local Docker; it fails at binding
validation with `Failed`, rather than sitting in `Pending`.

**Grant READ to every person's identity as well, under Kubernetes on Azure.** The check above
is the Service PAT's, and satisfying it grants nobody else anything. Each contributor connects
with their own MotherDuck identity (step 5), and that identity needs its own READ on the
database or Share to work in the domain. These are distinct identities, the same way Microsoft
Fabric's operating identity and service principal are distinct in
[01b-prereqs-fabric-admin](01b-prereqs-fabric-admin.md#5-confirm-the-service-principals-read-access-to-the-domain-workspace).
Granting one does not grant the other. Under Local Docker there is only the Service PAT to
grant, since one operator drives every operation through it.

**Get this right before the domain is created.** The database a domain binds is frozen at
creation, so a Share that has to be renamed to match it means recreating the domain, not
editing it.

### 5. Provision seats — read this section before your team commits to a plan

> The MotherDuck plan you choose bounds how many people can work in a domain — and the rule
> is different depending on your deployment style. This is a planning and cost decision, not
> a technical detail to skim.

**Under Kubernetes on Azure**, each person who signs in and works on a domain connects with
their **own** MotherDuck identity — not the Service PAT above. Studio stores one MotherDuck
credential per user, and it has no fallback to the Service PAT for a contributor who has not
connected their own account: that person simply cannot use the domain. **Under Kubernetes on
Azure, every contributor needs their own seat in your MotherDuck organisation.**

This is a constraint in how Studio connects, not a limit in MotherDuck. MotherDuck does have
sharing primitives that cross account boundaries — an unrestricted share, for example, is
readable by any user signed into any MotherDuck organisation in the same cloud region. Studio
does not use them as a substitute for per-user identity, so they do not remove the seat
requirement.

**Each contributor also needs their own MotherDuck token, not only a seat.** A seat lets them
exist in your organisation; the token is what they paste into Studio to connect their account.
Plan for issuing one per contributor, through the same secure channel you use for the Service
PAT.

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
| `api.motherduck.com` | Studio's REST call that checks the Service PAT is accepted (`/v1/active_accounts`). |
| `extensions.duckdb.org` | Where the DuckDB engine Studio runs on fetches the MotherDuck extension. |
| `*.motherduck.com` | MotherDuck's data-serving connection, the one that carries queries. Recommended starting point, not vendor-confirmed — see the note below this table. |

**The DuckDB MotherDuck extension is fetched over the network the first time Studio opens a
MotherDuck connection — it is not built into Studio's container image.** That first
connection happens during domain creation itself: creating a domain validates that the
bound database is reachable, and that validation is what opens
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

Studio has no fixed environment-variable names for these. Each value goes into a named field
on a screen, so this table gives the field label your operator will be looking at.

| Value | Studio's field | Comes from |
| --- | --- | --- |
| Organisation account name | **MotherDuck account** | Step 1 |
| Read/write token | **Service PAT** | Step 2 |
| Database name | **Database**, on the domain form | Step 3 |

If you created a Share in step 4, there is nothing to send back for it: on `v0.1.26` the
domain form has no Share field — it collects a database and a schema, and nothing else — and
Studio finds the Share by the bound database's own name. Tell
your operator it exists so they know the Pending check in
[06-first-domain](06-first-domain.md) should pass.

**Check the account name carefully before you send it.** Studio stores it write-once, and its
connection test does not verify it. The test only confirms that MotherDuck accepts the token;
it then reports success in a message that repeats whatever account name was typed in. A token
issued against a different MotherDuck organisation passes that test, and the mismatch does not
surface until a domain fails later. Correcting it means registering a new connection, not
editing the existing one.

The only fixed name in this flow appears later and is not something you supply: when a domain
runs GitHub Actions setup, Studio writes the token into that domain's repository as a CI
secret named `MOTHERDUCK_TOKEN`.

## Where this goes

The account name and the token are entered by the operator during organisation setup — see
[05-configure-org](05-configure-org.md). The database name is entered only in
[06-first-domain](06-first-domain.md), when the domain is created and bound to your account.
The Share, if you created one, is never entered anywhere — Studio resolves it from the
database name.
