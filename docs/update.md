# Update Studio

Use the management app for your existing marketplace deployment. The update runs through that managed application's operation path in your subscription.

## Apply an update

1. Open the existing installation in its management app.
2. Open **Actions**.
3. Select **Upgrade** for the available target release.
4. Review the proposed release and plan, including backup and verification.
5. Approve the plan when its changes are correct.
6. Wait for the operation's final result.
7. Confirm the installed version and public Studio address.
8. Repeat [[Verify the First Domain]] for a representative Domain.

The upgrade takes a backup before changing the release and checks the result before serving again. A backup failure must be resolved before the update can continue.

For a marketplace operation, the cloud application's template status alone does not prove the operation completed. Read the operation's final result in the management app. If you do not have management access to the existing installation, ask its deployment administrator to provide that access before starting maintenance.

Use [Recovery and rollback](rollback.md) if the update fails. Use the documentation matched to the installed release after a successful update.

---

_Release scope and source-review limits: [Home](README.md#release-and-verification-scope)._
