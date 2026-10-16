# Getting started as a Domain contributor

Open an Intent in a ready Domain. Select the agent for the work you need.

## Choose the agent

| Agent | Use it for |
| --- | --- |
| `build` | New or changed data products, bounded operations, and a `fix` for an already-shipped product |
| `detect` | Read-only runtime-health investigation, triaged findings, and bounded reconciliation between sources it can already read |

`fix` is a task kind owned by the Build agent. For a defect in a shipped product, its flow retains **Explain**, **Investigate**, and **Remediate**, with a stop before writes. Use the Detect agent for investigation across the Domain; it does not change code or data. The Build agent does not monitor the Domain.

## Let the Build agent classify the request

### Question

If nothing changes, the agent answers using the relevant skill or tool. A technical question does not require a product-change workflow.

### Bounded operation

For a change inside an already-decided shape, the owning skill runs directly. Examples include adding a source connection, testing a connection, or making a bounded configuration change.

### Product change

If the request changes what a data product commits to deliver, the staged workflow begins. The product kinds are ingestion, transformation, orchestration, and semantic-model. One Intent can contain more than one kind.

## Follow the product-change workflow

1. **capturing-requirements** records the Requirement and resolves the ordered `kinds:` list.
2. **designing** records the design for the approved requirement.
3. **planning** records the implementation plan.
4. **executing-the-plan** carries out the approved plan.
5. **verifying** records evidence and certification.
6. **shipping** checks the ship gates and asks for final approval before producing the registered ship product.

A later stage does not start only because the previous stage finished. The agent proposes the next stage and follows its approval rules.

## Find the durable artifacts

Unless repository instructions or existing artifact locations specify otherwise, the default files are:

- `intents/<slug>/requirement.md` — requirement, kinds, scope, and success criteria;
- design records for the Intent;
- `intents/<slug>/plan.md` — implementation plan;
- `intents/<slug>/verify.md` — verification evidence, certification, and ship approvals.

Transformation work can also produce a data-slice artifact during requirement capture. The repository and these files are the durable record; the agent reads them when it resumes.

## Approve shipping only after verification

For product work, the ship product is an Intent PR. A `fix` produces its Intent PR on a case branch. Detect work remains read-only and can produce triaged issues.

Shipping requires certified verification, a clean diff, and explicit final ship approval. Breaking schema changes require their own approval. Runtime outputs, generated artifacts, and secrets must stay out of the PR. The clean-diff protection also checks pushes and PR creation.

## Add a source connection

Ask the Build agent in conversation. The source flow:

1. checks the Domain platform and saved secret-store type;
2. discovers and prepares an available connector;
3. introspects its authentication methods and required fields;
4. asks for non-secret configuration;
5. gives you the exact secret names for the selected store;
6. verifies the connection through the runtime path;
7. records the non-secret configuration only after verification succeeds.

Enter credential values outside the agent:

- for **Internal**, use the saved Domain's **Secrets** tab;
- for **Azure Key Vault**, use the vault's secret-management surface;
- for **Local File**, ask the operator to update the Domain's secrets file outside Git.

Use a store supported by the deployed source workflow. A store being offered in Domain creation does not by itself prove every connector-delivery path works with it. A missing required secret can cause the first verification to fail; add it through the correct store, then ask the agent to retry. Never paste the value in chat.

## Keep development work isolated

Work happens on an Intent branch and in the runtime-declared ephemeral data destination. The agent must use the Domain's declared platform and must not write to the persistent production resource during development.

Do not commit dbt `target/`, package directories, logs, `.env`, or secret files. Do not ask the agent to dump environment variables or read credential files.

Use `CONTEXT.md` and `docs/adr/` for durable Domain knowledge. Keep lasting terminology and architecture decisions there when relevant.

Continue to [[Worked Example Salesforce]].

---

_Release scope and source-review limits: [Home](README.md#release-and-verification-scope)._
