# Verify the first Domain

Verify the saved Domain, an Intent run, and the separate CI prerequisites you intend to use. Saving a Domain does not prove that all external operations will succeed.

## Check the saved resources

1. Open **Domains**.
2. Select your Domain.
3. Open **Resources**.
4. Read the repository, data-platform, and secret-store checks.
5. Repair any reported configuration or access failure.
6. Select **Reconcile** to run the applicable checks again.

Reopening the page is not a replacement for an explicit readiness check. Keep the saved diagnostics while you investigate; do not recreate the Domain as a first response.

## Verify GitHub access

Confirm the repository binding is correct. Access is bounded by the selected App installation, its repository selection and approved permissions, and the acting user's GitHub authorisation for user-driven work.

A repository excluded from the App installation cannot be used by that Domain. See [[Prerequisites GitHub Organisation Owner]].

## Verify the data-platform resource

| Platform | Check |
| --- | --- |
| DuckDB | The selected Studio-managed database and schema can be opened. No external platform credential is required. |
| MotherDuck | The acting PAT reaches the bound database and its identity owns it; the schema exists; the service PAT supports unattended operations; plan and retention limits allow cloning. A Share is not an ownership workaround. |
| Microsoft Fabric | The user reaches the persistent workspace, Lakehouse, SQL endpoint, and schema; the service identity has its required persistent access; the selected ephemeral capacity exists and has room for temporary workspaces. |

Studio verifies persistent Fabric workspace access. It does not silently grant a missing role. See [[Prerequisites Fabric Administrator]] or [[Prerequisites MotherDuck Administrator]].

## Verify the secret store

Confirm **Resources** shows the store you intended to select and that any required connection and service checks pass. For **Internal**, confirm the saved Domain exposes **Secrets**. For an external store or **Local File**, confirm the responsible administrator can add values through that store's own mechanism.

A later connector verification must still prove that the runtime can use the required secret names. An available store type does not prove every connector-delivery path works.

## Verify an Intent can activate

1. Create an Intent in the Domain.
2. Wait for its runtime to become usable.
3. Read the data-platform diagnostic if activation fails.

This checks the ephemeral-resource path: a Fabric workspace and Lakehouse, an isolated MotherDuck clone, or a DuckDB runtime resource. Failure here can prevent chat even when an LLM profile is valid.

## Verify an LLM turn

Run a simple question with the intended LLM profile. Confirm that the profile is selectable, the runtime reaches the provider, and the model supports the requested behaviour.

Profile creation tests the connection. An actual Intent turn checks the runtime path.

## Verify GitHub Actions separately

For MotherDuck or Fabric Domains that use CI/CD, complete the Domain's GitHub Actions setup and inspect its platform-specific results. Core Domain readiness does not certify CI/CD setup.

Fabric's expected federated credential is tied to the repository and its **recorded default branch**:

```text
repo:<org>/<repo>:ref:refs/heads/<default-branch>
```

Use the remediation Studio reports to repair a missing or invalid credential on the Domain service principal's application. Do not assume the default branch is `main`.

Successful token exchange proves identity, not Fabric authorisation. If deployment fails after federation succeeds, check the service identity's workspace permissions and relevant tenant/API permissions.

## Check completion

Confirm that a real user can sign in, repository access works, required resource checks pass, an Intent activates, and an LLM turn succeeds. Complete the separate CI checks if you intend to use CI/CD.

Continue to [[Getting Started as a Contributor]].

---

_Release scope and source-review limits: [Home](README.md#release-and-verification-scope)._
