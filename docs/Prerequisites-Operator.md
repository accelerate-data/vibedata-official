# Operator prerequisites

Install Studio through your cloud marketplace. You need a browser, access to the target cloud account, and the administrator handoffs below.

## Prepare the cloud account

For the [Microsoft Marketplace listing](https://marketplace.microsoft.com/en-us/product/vibedata-by-acceleratedata.vd-sol-01), confirm:

- your Azure account can access the intended subscription;
- your organisation permits the marketplace purchase and selected plan;
- you have permission to deploy the managed application;
- the selected region has sufficient capacity and quota for the size you choose;
- the subscription's policies permit the deployment.

Microsoft documents the purchase requirements in [Purchase an Azure Application](https://learn.microsoft.com/marketplace/purchase-azure-app-in-azure-portal) and [Enable Marketplace purchases](https://learn.microsoft.com/azure/cost-management-billing/manage/enable-marketplace-purchases).

## Choose the address

The marketplace form offers **Give me an Azure address** or **Use my own name**.

If you use your own name, prepare the **Hostname** and access to the DNS record. Under **Who holds the DNS**, select the option that matches your DNS provider. If you select **Somewhere else, I will add the record**, arrange for the DNS owner to complete the requested record.

## Collect administrator handoffs

- Identity-provider application details for Studio sign-in. For Entra, use [[Prerequisites Entra Administrator]].
- A customer-owned GitHub App, installed on the intended repositories. Use [[Prerequisites GitHub Organisation Owner]].
- Fabric or MotherDuck resources and credentials when you use that platform. Use [[Prerequisites Fabric Administrator]] or [[Prerequisites MotherDuck Administrator]].
- Access to the secret store you intend to select for the Domain.
- Access to an LLM provider, including any endpoint and credentials its Studio profile requires.

Keep credential values in your approved secret-management channel. Do not put them in agent chat or a repository.

Continue to [Install from your cloud marketplace](Deploy-via-Cloud-Marketplace.md).

---

_Release scope and source-review limits: [Home](README.md#release-and-verification-scope)._
