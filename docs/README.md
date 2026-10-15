# VibeData Studio onboarding

Install Studio from your cloud marketplace into your own subscription. Start with [Operator prerequisites](Prerequisites-Operator.md), then [Install from your cloud marketplace](Deploy-via-Cloud-Marketplace.md).

## Choose the Domain's data platform

A Domain connects a GitHub repository to a persistent data resource. Select its data platform, authentication, resource, and secret store when you create the Domain.

| Platform | Interactive identity | Unattended identity | Domain resource |
| --- | --- | --- | --- |
| DuckDB | No external credential | No external credential | Studio-managed database file and schema |
| MotherDuck | Each user's PAT | Domain service PAT | Database and schema; the acting identity must own the database for Intent activation |
| Microsoft Fabric | Connected Microsoft Entra ID provider | Reused provider application or dedicated service principal, where offered | Workspace, Lakehouse, and schema, with capacity for ephemeral workspaces |

## Prepare administrator prerequisites

| Administrator | What to prepare |
| --- | --- |
| Cloud subscription administrator | Marketplace purchase and deployment permission, region, capacity quota, and an address choice; see [Operator prerequisites](Prerequisites-Operator.md) |
| Identity administrator | An eligible provider for Studio sign-in; for Entra and Fabric, see [Microsoft Entra prerequisites](Prerequisites-Entra-Administrator.md) |
| GitHub organisation owner | A customer-owned GitHub App and repository access; see [GitHub prerequisites](Prerequisites-GitHub-Organisation-Owner.md) |
| Fabric administrator, when using Fabric | Persistent resources, ephemeral capacity, and service access; see [Fabric prerequisites](Prerequisites-Fabric-Administrator.md) |
| MotherDuck administrator, when using MotherDuck | User and service PATs, database ownership, and schema; see [MotherDuck prerequisites](Prerequisites-MotherDuck-Administrator.md) |

## Configure and use Studio

1. [Install from your cloud marketplace](Deploy-via-Cloud-Marketplace.md).
2. [Configure the Studio instance](Configure-the-Studio-Instance.md).
3. [Create your first Domain](Create-Your-First-Domain.md).
4. [Verify the first Domain](Verify-the-First-Domain.md).
5. [Start as a contributor](Getting-Started-as-a-Contributor.md).
6. [Add a Salesforce source](Worked-Example-Salesforce.md).

## Identity and secrets

**Org settings → Identity providers** manages provider registrations. Eligible providers can sign users in when **Allow sign-in** is selected. A provider can also serve downstream delegation, such as Fabric access. Users connect their own downstream accounts under **User Settings → Connections**. Domain service authentication is a separate policy for unattended work.

Choose **Secret store type** in the Domain's **Secret store** step. Use the saved store's entry method for source credentials. **Internal** exposes a **Secrets** tab after saving; external stores use their own secret-management surface, and **Local File** requires operator access outside Studio. Never enter credential values in agent chat or Git.

## Operate the deployment

Use [Update Studio](update.md), [Recovery and rollback](rollback.md), and [Troubleshooting](Troubleshooting.md) after onboarding.

## Release and verification scope

Use the documentation for the Studio release delivered by your marketplace deployment. The wiki's generated **Release** page, when present, identifies the release tag and Studio commit for that publication; it does not select or upgrade your installed release. A documentation-only publication may have no Release page.

This content was reviewed against Studio source `a4df79ffcd5dc9d71697887804626a8ae4983177` and its pinned data-engineering plugin `16f90f637d1617f89dab74661857f914caccd106` on 15 October 2026 (GST). Source review is not a completed marketplace deployment, provider login, or Intent run. Before publishing for a release, check these instructions against that release and complete the deployment and first-Domain checks.
