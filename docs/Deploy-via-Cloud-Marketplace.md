# Install Studio from your cloud marketplace

Install Studio from the [VibeData listing on Microsoft Marketplace](https://marketplace.microsoft.com/en-us/product/vibedata-by-acceleratedata.vd-sol-01). The deployment runs in your Azure subscription. Complete [Operator prerequisites](Prerequisites-Operator.md) before you start.

## Select the offer

1. Open the listing while signed in with the account that can purchase and deploy into your target subscription.
2. Select the plan available to your subscription.
3. Select **Create** to open the deployment form.

If your organisation supplies a private offer or preview link, use that link and its eligible account. If the plan is unavailable, check purchase policy and subscription eligibility with your administrator.

## Complete the deployment form

1. Select the subscription, resource group, and region for the deployment.
2. In **Address**, choose **Give me an Azure address** or **Use my own name**.
3. If you choose a custom name, fill in **Hostname**.
4. For a custom name, select the applicable option under **Who holds the DNS**.
5. In **Size**, select **Node size** from the options available to your subscription and region.
6. Set **Number of nodes**. The form requires at least three.
7. Choose **Core only** or **Core plus observability** under **Observability**. The latter adds Grafana, Loki, Prometheus, and Tempo and needs more capacity.
8. Complete **JIT Configuration** for publisher access.
9. Select **Review + create** to check the plan, terms, and validation results.
10. Select **Create** when the deployment details are correct and you accept the terms.

Follow the deployed offer's fields if a later release changes them. Do not copy resource identifiers or sizing from another installation.

## Open Studio

1. Wait for the deployment to finish.
2. Open the deployment outputs and copy **studioAddress**.
3. Open that address in your browser.
4. Complete the first-owner access procedure supplied with the deployment.
5. Continue to [Configure the Studio instance](Configure-the-Studio-Instance.md).

If deployment fails, retain the managed application and its diagnostics. Use [Troubleshooting](Troubleshooting.md) before starting another deployment.

## Check the delivered release

Record the Studio version delivered by the deployment. Use its matching release notes and wiki publication before configuring the first Domain. The latest GitHub Release can differ from the version already installed in your subscription.

---

_Release scope and source-review limits: [Home](README.md#release-and-verification-scope)._
