# Recovery and rollback

Use the existing marketplace installation's management app and operation results to recover a deployment. Changing a public release listing does not roll back a running installation.

## After a failed upgrade

1. Read the failed upgrade's final result and recovery diagnostics.
2. Record the previous and attempted Studio versions.
3. Retain the backup identity and the failing operation's evidence.
4. Confirm whether the operation restored service before taking another action.
5. Escalate an incomplete rollback with that evidence to the deployment administrator or support.

The upgrade recovery path restores the previous release and, when required after a new backend has started, restores that run's backup. Release and durable data must remain compatible. Do not replace application images independently of the managed operation.

## Recover from a backup

1. Open the existing installation in its management app.
2. Review **Last backup** and confirm it is the recovery point you intend to use.
3. Open **Actions**.
4. Select **Recover**.
5. Review the recovery plan, including replacement resources and address cutover.
6. Approve only after accepting the recovery point and planned changes.
7. Wait for the final result and verify Studio at its public address.
8. Repeat [[Verify the First Domain]].

Recovery creates replacement resources, restores the backup, verifies the result, and moves the address. Changes after the recovery point can be lost. Preserve the installation's original encryption-key material; a backup alone does not replace it.

This guide does not define a standalone downgrade to an arbitrary release. Ask the deployment administrator or support for a release-specific recovery procedure when the managed operation does not resolve the fault.

---

_Release scope and source-review limits: [Home](README.md#release-and-verification-scope)._
