# Vibedata Studio onboarding — current `main`

This is a deployment and first-use guide for the current `accelerate-data/studio` `main` branch, at the commit stamped on this page.

It is intentionally **not pinned to the latest public Vibedata release**. `main` may contain behavior that has not yet been published in `vibedata-official`. When installing a published build, use the version-matched `vibedata` binary for that release and re-check release-specific differences.

## The two choices

Choose one deployment style and one data platform.

### Deployment style

| Style | Authentication posture | GitHub identity | Best fit |
| --- | --- | --- | --- |
| **Local Docker** | Ambient, single operator (`AUTH_ENABLED=false`) | Host `gh` session imported into Studio | Local evaluation, demos, single-operator work |
| **Kubernetes on Azure** | Delegated, multi-user (`AUTH_ENABLED=true`) | Customer-owned GitHub App plus per-user authorization | Shared production-style deployment |

Local Docker is deliberately not the same security model as the Kubernetes deployment. It exposes no Studio login gate. Anyone who can reach its UI can use the instance, so network access must be restricted by the operator.

### Data platform

| Platform | Interactive identity | Service identity | Domain resource |
| --- | --- | --- | --- |
| **DuckDB-local** | None | None | Studio-managed `.duckdb` file + schema |
| **MotherDuck** | User PAT in delegated mode; shared Domain PAT in ambient mode | Domain PAT in delegated mode | Database + schema |
| **Microsoft Fabric** | Entra OAuth/OIDC in delegated mode; container `az` identity in ambient mode | Domain service principal | Workspace + Lakehouse + schema |

The most important architectural rule in current `main`: **Data Platform configuration belongs to the Domain.** There is no instance-level Data Platform registration step. A Domain chooses its Data Platform Type, user authentication, service authentication, and exact resource coordinates when it is created.

## Identity model

Current Studio has three different identity concepts. Do not combine them casually.

1. **SSO Provider** — signs a person into Studio. Used only in delegated deployments.
2. **Identity Provider** — lets an already-signed-in user obtain downstream OAuth/OIDC credentials, such as Fabric access. It does not sign the user into Studio.
3. **Domain service credential** — belongs to one Domain and is used for unattended work. For Fabric, this is a service principal. For MotherDuck, this is a PAT.

A GitHub App is a fourth, separate identity used for repository access in delegated deployments.

## Domain Secret Store behavior in current `main`

Every new Domain currently receives a **local Secret Store automatically**. Studio creates it under its data directory. The Domain create UI does not expose a Secret Store picker.

Legacy Secret Store administration still exists under Org Settings, including Azure Key Vault support. Do not mistake that registry surface for the current Domain-create path. This onboarding flow follows the currently executable Domain-create implementation.

For source connections, the agent tells the user the exact secret names to create. Secret values are entered out of band in the Domain's local secrets file; they are never given to the agent or committed to Git.

## Which prerequisite pages apply

| Combination | Read before deployment |
| --- | --- |
| Local Docker + DuckDB | [[Prerequisites Operator]] |
| Local Docker + MotherDuck | [[Prerequisites MotherDuck Administrator]], [[Prerequisites Operator]] |
| Local Docker + Fabric | [[Prerequisites Entra Administrator]], [[Prerequisites Fabric Administrator]], [[Prerequisites Operator]] |
| Kubernetes + DuckDB | [[Prerequisites Entra Administrator]] for Studio SSO, [[Prerequisites GitHub Organisation Owner]], [[Prerequisites Azure Infrastructure]], [[Prerequisites Operator]] |
| Kubernetes + MotherDuck | the Kubernetes pages above plus [[Prerequisites MotherDuck Administrator]] |
| Kubernetes + Fabric | all prerequisite pages |

`01a` contains separate sections for Studio SSO, Fabric user OAuth, and the Fabric service principal. Skip the sections that do not apply to your combination.

## Reading path

### 1. Collect administrator prerequisites

- [[Prerequisites Entra Administrator]] — Entra registrations for Studio SSO and Fabric identities.
- [[Prerequisites Fabric Administrator]] — Fabric tenant, capacity, workspace, Lakehouse, schema, and service-principal access.
- [[Prerequisites GitHub Organisation Owner]] — customer-owned GitHub App for delegated deployments.
- [[Prerequisites Azure Infrastructure]] — AKS, Azure Files, Key Vault, DNS/Front Door, and cluster identity.
- [[Prerequisites MotherDuck Administrator]] — MotherDuck user/service PAT and database preparation.

### 2. Prepare the operator

Read [[Prerequisites Operator]].

### 3. Deploy Studio

- Local Docker: [[Deploy with Local Docker]]
- Kubernetes on Azure: [[Deploy on Kubernetes on Azure]]

### 4. Configure the instance

Read [[Configure the Studio Instance]].

The current minimum delegated setup normally includes:

- an SSO Provider;
- a GitHub Commit Provider backed by the GitHub App;
- an LLM Profile;
- an Identity Provider when a downstream platform requires delegated OAuth/OIDC, such as Fabric;
- user and role setup.

There is no instance-level Data Platform registration step.

### 5. Create and verify the first Domain

- [[Create Your First Domain]]
- [[Verify the First Domain]]

### 6. Start data work

- [[Getting Started as a Contributor]]
- [[Worked Example Salesforce]]

Use [[Troubleshooting]] as a symptom-based reference.

## Current implementation boundaries to remember

- Local Docker is ambient/single-operator only. The supported installer does not turn it into the delegated SSO topology.
- Kubernetes install currently supports Azure as its cloud provider. AWS and GCP are not implemented in the current CLI.
- `vibedata install kubernetes` currently uses explicit CLI flags such as `--domain`, `--storage-url`, and `--vault-url`. Design documents describing a declarative `--config` installer are ahead of the executable CLI and are not used in this guide.
- A Domain can defer a supported service identity at creation, but current UI warns that Intents cannot activate until the required service identity is configured.
- Data-platform resource identity is immutable after Domain creation. Fabric ephemeral capacity and service credentials are mutable operational settings.
- Git repository binding is immutable after Domain creation.
- Domain readiness is not automatically re-checked just by opening settings. Use **Verify** on an Active Domain or **Retry provisioning** after a failure.

## Verification policy for this snapshot

This refresh treated current implementation and current rendered UI as authoritative when they conflicted with older or future-looking design documents. In particular:

- CLI command definitions were checked directly in `cli/vibedata/src/vibedata/commands/`.
- Domain-create behavior was checked against the current UI, request schemas, and persistence path.
- GitHub App permissions were checked against the current GitHub provider contract.
- image-signature policy was checked against the workflows that actually sign candidate images.
- data-engineering behavior was checked against the exact `ext/vd-data-engineering` submodule pinned by this Studio SHA.

This is therefore a **main-branch snapshot**, not a promise about an older released binary or a future design.

---

_Applies to: studio/main (unreleased snapshot). Verified against `studio@5c9d2bbf339a` on 2026-08-22._
