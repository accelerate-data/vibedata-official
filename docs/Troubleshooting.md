# Troubleshooting

Read the saved deployment or Domain diagnostic before changing resources. Keep identifiers and error messages, but redact credential values before sharing evidence.

## Marketplace deployment

### The offer or plan is unavailable

Confirm that you are using the intended marketplace listing and account. Ask your subscription administrator to check marketplace purchase policy and plan eligibility. For a private offer or preview, use the supplied link with its eligible account.

### Validation reports insufficient quota or capacity

Check the selected region, **Node size**, **Number of nodes**, and the form's quota message. Request the required quota or choose an available size and region that meet the offer's requirements. Re-run validation before creating the deployment.

### Deployment fails or the Studio address does not open

Inspect the failed deployment operation in the cloud portal. Retain the managed application identity, target subscription, region, and safe diagnostic. If you chose a custom hostname, confirm the requested DNS record is complete and the browser uses that hostname.

Do not create a second deployment until you understand the first failure. See [Install from your cloud marketplace](Deploy-via-Cloud-Marketplace.md).

## Sign-in and instance setup

### Provider callback is rejected

Open **Org settings → Identity providers** and use the **Callback URL** shown for the exact provider. It is previewed in the registration form before creation. Register that URL on the external application and confirm that its origin matches the public Studio address.

For Entra, use the concrete tenant GUID and the intended application. See [[Prerequisites Entra Administrator]].

### Provider is saved but users cannot sign in

Check whether the row shows **Pending test**. Run **Test** to activate a new registration. For an eligible sign-in provider, also check **Allow sign-in**.

A replacement candidate does not take over until its test succeeds. If users are pending approval, approve them under **Users**; enabling automatic approval later does not approve existing pending users or grant roles.

### GitHub configuration fails permission validation

Check the customer-owned GitHub App's required permission map in [[Prerequisites GitHub Organisation Owner]]. Then check the installation has approved any permission updates. Editing the App definition alone can leave an existing installation on its old grants.

## Domain creation and readiness

### I cannot find a data-platform registration page

Select **Data platform type** within **Domains → Add domain**. The Domain owns its platform configuration and persistent resource binding.

### The Identity provider selector is empty

Read the field's reason. An administrator may need to register, repair, or activate a compatible provider. If the message says the user is not connected, complete **User Settings → Connections**. A registered provider is not the same as the signed-in user's healthy connection. Domain creation does not start OAuth.

### I cannot complete Secret store

Select **Secret store type** in the third create step. Complete that type's required connection, service-authentication, and resource fields. Only available types can be selected.

**Internal** has no external connection fields; **Local File** requires secrets supplied outside Studio. An external store needs its own valid configuration. There is no separate organisation-level Secret Stores registration step.

### The Domain saved but an Intent cannot activate

Open the Domain's **Resources** tab and read the required checks. Repair the reported service credential, connection, permission, or resource failure. Select **Reconcile** after the repair.

For an older Domain with incomplete service authentication, configure the required service identity first. Do not treat persistence as proof of readiness.

### The Secrets tab is missing

The tab is available after **Internal** has been saved as the Domain's store and the user has the required access. An unsaved selection does not enable it. Other store types use their own entry mechanism. Switching stores does not copy secret values.

## Microsoft Fabric

### The user cannot discover or validate resources

Check that the Domain uses the intended Entra Identity Provider, that the user's downstream connection is healthy, and that the user can access the persistent workspace, Lakehouse, and schema.

### The service check cannot verify the persistent workspace

Grant the selected service identity the required persistent workspace access. Studio verifies that access; it does not silently grant the missing role.

### Intent activation fails while creating an ephemeral workspace

Check the selected ephemeral capacity, available capacity, service identity authorisation, Lakehouse SQL endpoint creation, and schema validity. Capacity exhaustion blocks activation.

### GitHub Actions reports a federated-credential mismatch

The expected subject uses the Domain repository's **recorded default branch**:

```text
repo:<org>/<repo>:ref:refs/heads/<default-branch>
```

Follow the remediation reported by Studio. If token exchange succeeds but deployment fails, check the service identity's Fabric permissions rather than changing a valid federated credential.

## MotherDuck

### A PAT authenticates but Intent activation fails

Confirm the acting MotherDuck identity owns the bound database. Read access through a Share does not satisfy the clone-source ownership requirement, and legacy Share state is ignored for activation. Do not try to add a Share as a repair.

Check the user PAT separately from the Domain service PAT. Studio does not use another person's credential as a fallback.

### Cloning fails after a plan change

Check the source database's retention setting against the acting identity's current plan entitlement. A valid PAT does not prove a plan-gated clone is permitted.

## DuckDB

### The database is locked or busy

Let the active writer complete, or stop a conflicting writer you control, then retry. Do not duplicate or replace the Studio-managed Domain file as a first repair.

## Source connections

### Verification reports a missing secret

Use the exact secret name the agent returned for the saved Domain store:

- **Internal**: add the value under the Domain's **Secrets** tab;
- **Azure Key Vault**: add it in the bound vault;
- **Local File**: ask the operator to update the Domain's secrets file outside Studio and Git.

Then tell the agent to retry. Never paste the value in chat. If the selected store is not supported by the deployed source workflow, resolve that compatibility before proceeding.

### The connector fields differ from an example

Use the current connector's introspection result. Authentication fields depend on the loaded connector version. See [[Worked Example Salesforce]].

## LLM profiles

### A profile will not save

Check **Provider**, its displayed credential and endpoint fields, and **Model** against the provider error. Connection-field changes run a real test; a failed edit preserves the previous saved profile.

**Canonical model** supplies capabilities, limits, and price metadata. Custom and Ollama can use **None — not in the catalogue**; do not treat a catalogue association as universally mandatory.

### A profile saves but an Intent turn fails

Check the Intent's bound profile, runtime connectivity, model capabilities, and the error from that turn. A connection test does not prove every tool or reasoning capability.

## Retain evidence before escalation

Record the deployment or Domain identity, installed Studio version, failed operation, readiness result, and safe diagnostic. Include relevant cloud deployment identifiers for an installation failure. Exclude secrets.

Use [Update Studio](update.md) or [Recovery and rollback](rollback.md) for deployment lifecycle failures. Deleting a Domain or deployment can remove evidence and data.

---

_Release scope and source-review limits: [Home](README.md#release-and-verification-scope)._
