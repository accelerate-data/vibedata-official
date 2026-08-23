# Configure the Studio instance

Studio is now running. This page covers instance-level configuration before creating the first Domain.

The current architecture does **not** register Microsoft Fabric or MotherDuck as instance-level Data Platforms. Data Platform configuration happens on the Domain in [[Create Your First Domain]].

## Local Docker

> **Applies to: Local Docker.**

Local Docker uses ambient auth and a single operator.

Skip:

- SSO Provider setup;
- downstream Identity Provider administration for user OAuth;
- GitHub App setup;
- multi-user role provisioning.

Your host `gh` session and, for Fabric, the container's `az` session provide the ambient user identities.

You still need an LLM Profile.

## Kubernetes on Azure

> **Applies to: Kubernetes on Azure.**

Complete these instance-level items as the first real `vibedata_owner`.

### 1. SSO Provider

Open **Org Settings → SSO Providers**.

Register the provider users will use to sign in to Studio. Current UI supports provider-specific registrations and shows the callback URL for the provider.

For an Entra deployment, use the tenant/client/secret supplied by the administrator and register the exact callback URL Studio displays in the Entra application.

SSO Provider means **Studio login**. It is not the downstream Fabric Identity Provider.

### 2. GitHub

Open **Org Settings → GitHub**.

Enter the GitHub App:

- Client ID;
- client secret;
- private key PEM.

Studio validates the App identity and the required permission map before accepting the provider.

No App ID or installation ID is entered here. Installations are selected later as part of Domain repository binding.

### 3. Downstream Identity Provider, when required

Open **Org Settings → Identity Providers**.

> **Applies to: Microsoft Fabric on Kubernetes on Azure.**

Register a Microsoft Entra ID Identity Provider with:

- name;
- tenant ID;
- client ID;
- client secret.

This provider exists only for downstream user access. It does not sign users into Studio.

After registration, copy the callback URL Studio displays and make sure that exact URL is registered on the Entra application.

MotherDuck does not require an OAuth Identity Provider; its users connect PAT credentials. DuckDB needs no downstream identity.

## Configure LLM Profiles

Open **Org Settings → LLM Profiles**.

Current Studio supports these curated provider types:

- Anthropic;
- OpenAI;
- OpenRouter;
- Azure AI Foundry;
- plus a `custom` OpenAI-compatible profile type.

The old onboarding rule that every installation must use Azure AI Foundry is no longer correct.

Create at least one usable profile. The core connection fields are:

| Field | Meaning |
| --- | --- |
| Profile name | Stable human-readable profile name |
| Provider | Curated provider or custom |
| API base | Provider endpoint/base URL |
| API key | Secret, write-only after save |
| Model | Model identifier or Azure deployment name |

Studio runs a real connection test when a profile is created or its connection fields change. A failed test prevents that connection change from being saved.

Choose one profile as the instance default. New Intents can inherit the default profile and users can change the bound profile through the supported Intent flow. There is no Domain-level LLM override.

Advanced sampling, reasoning, caching, capability, and cost metadata can stay at defaults until you have a reason to tune them.

## Users and roles

> **Applies to: Kubernetes on Azure.**

Open **Org Settings → Users** and add the people who should use Studio with the minimum required role.

The main onboarding roles are:

- `vibedata_owner` — instance administration;
- `domain_owner` — administration within a Domain;
- `domain_contributor` — work within a Domain;
- `user_access_administrator` — user/access administration without broad product ownership.

Domain membership is configured after a Domain exists.

## Secret Stores: current-main caveat

Org Settings still exposes a **Secret Stores** administration surface, including Azure Key Vault support.

However, the current executable Domain-create path automatically initializes a local Domain secret store and does not present a Secret Store picker on the Domain form. For this onboarding snapshot, do not add a Secret Store merely because older documentation told you it was a required pre-Domain registry step.

The local Domain secrets file is created when the Domain is created and is used by the source-connection flow in this guide.

## Settings you can leave alone for first onboarding

The following current Org Settings surfaces are not prerequisites for the first Domain unless your organization has a specific requirement:

- OAuth Clients;
- MCP Catalog;
- Plugins;
- Service Principals;
- Connector Sources;
- Automations;
- Budgets;
- Action Confirmation;
- Capacity;
- Announcements.

Bundled product capabilities do not need to be manually installed as marketplace plugins for a basic first Domain.

## Checklist before creating the first Domain

For Local Docker:

- Studio is reachable;
- GitHub ambient session works;
- Fabric ambient Azure login works if Fabric is used;
- at least one LLM Profile is usable.

For Kubernetes on Azure:

- real owner signs in through SSO;
- GitHub provider validates;
- Fabric Identity Provider is registered when Fabric is used;
- users/roles needed for the first Domain exist;
- at least one LLM Profile is usable.

Continue to [[Create Your First Domain]].

---

_Applies to: studio/main (unreleased snapshot). Verified against `studio@5c9d2bbf339a` on 2026-08-22._
