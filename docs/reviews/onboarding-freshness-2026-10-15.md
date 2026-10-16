# Onboarding freshness review

Reviewed on 15 October 2026 at 11:29 GST (Asia/Dubai; workstation zone `+04`).

## Current status

The corrections are implemented on `docs/onboarding-freshness-review`. Installation guidance is **cloud marketplace only**, as instructed by the operator after the review. The complete local Python suite, coverage gate, lint, and formatting checks pass. Release-specific and live verification remain open; see **Correction verification and limits** below.

The original review and baseline evidence below describe `aee3c19`, before these edits. Its file line numbers and test counts are historical references, not the corrected working tree.

## Original review verdict

**Requires corrections before publication as current onboarding.** The review found four P1 blockers and five P2 issues. All 15 onboarding pages were read. The pages still describe the `studio@5c9d2bbf339a` snapshot verified on 22 August 2026. Current implementation differs in cloud installation, sign-in, Domain secret stores, MotherDuck access, observability, and agent workflow.

At the end of the review phase, this report was the only repository change. The subsequent correction phase is recorded below.

## Evidence boundary

| Item | Reviewed revision |
| --- | --- |
| Documentation | `accelerate-data/vibedata-official@aee3c19ba64b217a8f4b79ae7df81d1a42dd80f7` |
| Studio | `accelerate-data/studio@a4df79ffcd5dc9d71697887804626a8ae4983177`, remote `main` captured for this review; commit time 15 October 2026, 11:14 GST |
| Data-engineering plugin | `accelerate-data/vibedata-data-engineering@16f90f637d1617f89dab74661857f914caccd106`, the exact `ext/vd-data-engineering` gitlink in the Studio revision above |
| Worktree | `/Users/shwetanksheel/.codex/worktrees/e2dc/vibedata-official` |
| Branch | `docs/onboarding-freshness-review` |

The local Studio checkout was stale and had unrelated changes. Evidence was read through authenticated GitHub API requests at the pinned revisions. Its working files were not used as current implementation evidence. Source files, including UI string definitions, were inspected; no Studio instance, installation, cloud account, or Salesforce connection was exercised. Source links below are immutable.

P1 means that a documented path cannot complete, or promises access that the current implementation rejects. P2 means that instructions, contracts, or verification need correction without blocking every onboarding path.

## Findings

### F01 — P1: The Kubernetes installation path calls a removed command

**Documentation:** `docs/Deploy-on-Kubernetes-on-Azure.md:24` and `:34`; `docs/Prerequisites-Operator.md:79`; `docs/Prerequisites-Azure-Infrastructure.md:5`, `:19`, and `:141`; `docs/README.md:109`; `docs/Troubleshooting.md:76`. The supporting `docs/cloud-installer.md:7` also recommends it.

The guide sends operators to `vibedata install kubernetes --cloud azure`, describes the installer as requiring an already-created AKS estate, and states that AWS is unimplemented. Current Python CLI help identifies it as the local Docker operator CLI; its install group registers `compose`, with no Kubernetes command. The current Cloud Installer provisions or adopts an estate and has Azure and AWS paths. Following the guide reaches a missing command before deployment can start.

**Evidence:** [CLI scope and command registration][cli-main], [install command][cli-install], [Cloud Installer behavior][cloud-intro], and [Azure/AWS input validation][cloud-providers].

**Original correction proposal (superseded):** Route cloud onboarding through the current Cloud Installer. The operator subsequently required marketplace-only installation, so the corrections do not expose either a standalone Cloud Installer or a local Docker alternative. See the disposition below.

### F02 — P1: Sign-in setup points to a removed SSO Providers surface

**Documentation:** `docs/Prerequisites-Entra-Administrator.md:15` and `:52`; `docs/Configure-the-Studio-Instance.md:32`; `docs/Deploy-on-Kubernetes-on-Azure.md:97`; `docs/Troubleshooting.md:113`; the identity model in `docs/README.md:30`.

The pages require **Org Settings → SSO Providers** and assert that an Identity Provider never signs a user into Studio. Current Org settings has **Identity providers**, with an **Allow sign-in** control for eligible provider kinds. The Entra adapter passes the saved `allowSignIn` policy to the authentication provider. There is no separate SSO Providers entry in the current settings navigation. The documented first-owner flow therefore asks for a missing screen and teaches the wrong provider model.

**Evidence:** [Org settings navigation][org-navigation], [sign-in policy control][identity-policy], and [Entra sign-in adapter][entra-adapter]. The [registration form][identity-register] also previews the callback URL before creation; the old copy-after-save sequence should be updated.

**Correction:** Explain sign-in and delegation as policies/capabilities of the current Identity Provider types. Use the actual registration controls and callback preview. Keep Studio login, downstream access, and Domain service credentials conceptually distinct without requiring obsolete separate registries.

### F03 — P1: Domain creation now requires an explicit Secret store step

**Documentation:** `docs/Create-Your-First-Domain.md:135`; `docs/Configure-the-Studio-Instance.md:118`; `docs/README.md:40`; `docs/Getting-Started-as-a-Contributor.md:108`; `docs/Worked-Example-Salesforce.md:25` and `:81`; `docs/Troubleshooting.md:149`.

The guide states that there is no Secret Store picker and that each new Domain automatically gets a local secrets file. Current creation has **Basics**, **Data platform**, and **Secret store** steps, and an explicit **Secret store type** selector. Persistence configures the selected typed candidate; local-file initialization is conditional on the selected descriptor's creation hook. The registered store types include Local File, Azure Key Vault, Internal, and GCP Secret Manager; individual availability is descriptor-controlled. A file under the Studio data directory is not a universal credential destination.

**Evidence:** [creation steps][create-steps], [Secret store type selector][store-selector], [typed persistence][domain-persistence], and [store registry][store-registry]. The [current Domain settings design][domain-secret-settings] describes the Internal store's Secrets tab and separate handling for external stores.

**Correction:** Add store selection and any required connection/resource setup to Domain creation. Make the contributor and Salesforce instructions depend on the saved store type. Explain Local File editing only for Local File, and use the current store-specific entry method for other stores. Update the obsolete **Add Data Domain** and **Create Domain** labels: the current screen is **Create domain**, with **Continue to secret store** and **Create** controls ([header][create-header], [footer][create-footer]).

### F04 — P1: A MotherDuck Share no longer enables non-owner Intent activation

**Documentation:** `docs/Prerequisites-MotherDuck-Administrator.md:48`–`:58`, `:74`, and `:95`; `docs/Create-Your-First-Domain.md:123` and `:163`; `docs/Verify-the-First-Domain.md:52`; `docs/Troubleshooting.md:212`.

The guide promises that a Share permits a non-owner to use the bound database as an Intent clone source and says a new Share association can be configured later. Current creation rejects Share state in the strict candidate schema. Clone-source resolution requires the acting identity to own the bound database and explicitly ignores legacy Share configuration. Operators can satisfy every published Share instruction and still be refused activation.

**Evidence:** [MotherDuck create schema][motherduck-schema] and [owner-only clone-source resolver][motherduck-clone]. The [settings design][motherduck-settings] confirms there is no Share picker; legacy state can only be cleared.

**Correction:** State the current ownership limitation and remove Share-based onboarding and repair instructions. Keep historical Share state distinct from supported new setup. Do not promise a different sharing model without an implemented and verified change.

### F05 — P2: Full observability and Langfuse installation instructions are retired

**Documentation:** `docs/Deploy-with-Local-Docker.md:45`; `docs/Deploy-on-Kubernetes-on-Azure.md:55`; `docs/Prerequisites-Azure-Infrastructure.md:23`, `:49`, and `:152`; `docs/Troubleshooting.md:79` and `:91`. Local Docker re-run behavior also needs clarification at `docs/Deploy-with-Local-Docker.md:49`.

The pages describe `--full-observability` as a supported LGTM-plus-Langfuse installation. The current CLI retains the flag only to return a controlled error: **Removed: Langfuse is no longer provisioned by Vibedata.** Its profile resolver blocks the removed value and directs the operator to `--with-observability` or `--no-observability`. On an existing observability installation, omitting a profile choice can also block for explicit selection; it is not simply a successful reinstall with an inherited topology.

**Evidence:** [retired flag help][observability-flags] and [profile resolution and blocking][observability-resolution].

**Correction:** Remove Langfuse/full-profile setup, sizing, vault, and readiness claims. Document supported profiles and explicit re-run choices for each current installer.

### F06 — P2: Contributor routing and durable artifacts describe an older plugin

**Documentation:** `docs/Getting-Started-as-a-Contributor.md:5`, `:54`, `:67`, and `:79`; `docs/Worked-Example-Salesforce.md:122`.

The guide presents `build`, `fix`, and `detect` as selectable sibling agents and names `capturing-intent` and `intent.md`. The pinned plugin has `build` and `detect`; `build` also owns the `fix` kind for a defect in one shipped product. Product work starts at `capturing-requirements`. Its Requirement artifact defaults to `intents/<slug>/requirement.md`, with Plan and Certification in the same Intent root, subject to the repository/existing-artifact precedence rules. Detect also supports bounded, read-only reconciliation between already-readable sources, which the guide omits.

**Evidence:** [Build routing][build-routing], [Detect routing][detect-routing], [requirement capture][requirement-capture], [kind registry][kind-registry], and [artifact paths][artifact-paths].

**Correction:** Update the agent/task mapping, skill names, and artifact locations. Preserve the valid distinctions between questions, bounded changes, product changes, and certified shipping. Keep the separate `fix` task kind without presenting it as an available agent identity.

### F07 — P2: LLM setup presents an obsolete exhaustive provider list

**Documentation:** `docs/Configure-the-Studio-Instance.md:77`–`:102` and `:107`.

The guide presents four curated providers plus Custom as the current supported set. The current shared provider catalogue also exposes providers such as DeepSeek and Ollama, and the Azure label is **Azure Foundry**. The profile editor derives connection controls from the selected provider and also shows **Canonical model**, used for capabilities, limits, and price; Custom and Ollama offer a catalogue association picker. That association is not universally required, so the replacement guide must not invent a mandatory field.

**Evidence:** [provider catalogue][llm-providers], [provider-driven profile fields][profile-fields], and [Canonical model control][canonical-model].

**Correction:** Explain how to choose from the actual Provider control and complete its displayed fields. Describe Canonical model when shown. Prefer this stable procedure over another exhaustive copied provider inventory. The reviewed source contains no basis for changing the named LLM models in external provider documentation, which was not audited.

### F08 — P2: The prior integration left two wiki tests failing

**Evidence:** A focused run from this clean worktree ran **21 tests: 19 passed, 2 failed, 0 errors**:

```text
test_publish_wiki.RenderSidebarTests.test_lists_onboarding_and_operate_pages
test_publish_wiki.TextTransformTests.test_real_home_page_renders_cleanly
```

`tests/test_publish_wiki.py:155` still requires the old numbered sidebar page names. `tests/test_publish_wiki.py:115` requires the Home page to contain a rendered `](update)` link, which the imported Home page no longer contains. These failures are present at `aee3c19` and come from the previous integration, not from this report. The test run publishes only to temporary local bare repositories; it did not contact or change the GitHub wiki.

**Correction:** Align the navigation test with the approved page names, retaining meaningful coverage of required entries. Restore the intended Home operations link or explicitly resolve that contract before adjusting its test. Keep the existing assertions that every published page is reachable and every sidebar target exists. No tests were edited during this review.

### F09 — P2: The public operator source now explicitly disclaims release matching

**Documentation:** `docs/README.md:3`–`:5` and the verification footer on all 15 onboarding pages.

The Home page tells operators the guide intentionally follows an unreleased `main` snapshot and may not match the public CLI they just downloaded. The accepted operator-documentation contract defines a release-coupled wiki that describes the released build. The publisher can stamp a generated Release page with the release identity, but it does not rewrite or validate behavioral claims in the onboarding pages. Publishing the current set with a new release would leave the August snapshot and the generated release identity side by side.

**Evidence:** [operator documentation contract][operator-contract] and this repository's `.github/workflows/wiki.yml` plus `scripts/publish_wiki.py:190`–`:265`.

**Correction:** Use this main-source audit to prepare corrections, then verify the publication set against the specific Studio revision/release being published. Distinguish a development snapshot from the released operator path. Refresh verification stamps only after the corresponding claims are checked; do not replace the SHA/date globally and call it verified.

## Page coverage

Every row represents a page read in full. A checked source contract is not a live installation or vendor permission test.

| Page | Result and retained evidence |
| --- | --- |
| `docs/README.md` | Corrections: F01–F03, F09. Ambient versus delegated deployment remains a useful distinction. |
| `docs/Prerequisites-Entra-Administrator.md` | Corrections: F02. A concrete tenant and the displayed provider-specific callback remain relevant; sign-in policy and callback acquisition steps changed. |
| `docs/Prerequisites-Fabric-Administrator.md` | Core bindings and ephemeral-workspace behavior were compared with the Fabric descriptor/provider. Workspace/Lakehouse/schema binding and an ephemeral capacity remain relevant. Live tenant consent, exact role sufficiency, endpoint policy, and federation repair were not exercised. F09 applies to its publication stamp. |
| `docs/Prerequisites-GitHub-Organisation-Owner.md` | The listed repository permission baseline still matches `github-permission-contract.ts:130`–`:188`. Customer App versus ambient `gh` remains relevant. No live App, installation approval, or authorization callback was tested. F09 applies. |
| `docs/Prerequisites-Azure-Infrastructure.md` | Corrections: F01, F05, F09. Re-scope the page around the current installer's provisioning/adoption path before accepting its sizing, storage, edge, and secret handoff checklist. |
| `docs/Prerequisites-MotherDuck-Administrator.md` | Corrections: F04, F09. PAT authentication and isolated clones remain implemented. No vendor entitlement or retention probe was run. |
| `docs/Prerequisites-Operator.md` | Corrections: F01, F09. The local Docker CLI remains; cloud prerequisites must follow the Cloud Installer rather than its removed Python CLI path. |
| `docs/Deploy-with-Local-Docker.md` | Corrections: F05, F09. `compose`, `--frontend-port`, `--studio-url`, and `AUTH_ENABLED=false` remain in current installer source/template. Container login, memory totals, and a real install were not exercised. |
| `docs/Deploy-on-Kubernetes-on-Azure.md` | Corrections: F01, F02, F05, F09. The documented command path cannot be followed on current main. |
| `docs/Configure-the-Studio-Instance.md` | Corrections: F02, F03, F07, F09. Current navigation also differs from its optional-settings inventory; update that inventory from the actual settings list. |
| `docs/Create-Your-First-Domain.md` | Corrections: F03, F04, F09. Domain-owned platform configuration and immutable bound resource identity remain consistent with the reviewed design/source. Exact wizard controls changed. |
| `docs/Verify-the-First-Domain.md` | Corrections: F04, F09, plus the cloud-install dependency in F01. Keep separate checks for runtime activation, external access, an LLM turn, and CI configuration. No completed activation, LLM call, or CI run is claimed. |
| `docs/Getting-Started-as-a-Contributor.md` | Corrections: F03, F06, F09. Bounded source setup and approved PR shipping remain in the pinned plugin. |
| `docs/Worked-Example-Salesforce.md` | Corrections: F03, F06, F09. The agent-driven entry and verification-before-config-persistence remain supported by the pinned source skill. No Salesforce credential shape, live source, or row count was verified. |
| `docs/Troubleshooting.md` | Corrections: F01–F05, F09. Reuse the confirmed current platform/provider errors when rewriting the affected sections. |

Supporting files `docs/cloud-installer.md`, `docs/update.md`, `docs/rollback.md`, the wiki workflow, publisher, and publisher tests were also inspected. This was not a full audit of backup, restore, rollback, release delivery, or external infrastructure security guidance.

## Countercheck: do not copy an unimplemented source form from the functional spec

The current source-connection functional spec describes an **Add Source** modal and `/add-source`. That conflicts with the inspected implementation: the [frontend harness-command registry][harness-commands] does not register `/add-source`, the source-connections router manages connector-source registries, and the pinned [add-or-update-source skill][source-skill] carries out conversational connector setup, verification, and commit/push. No corresponding Add Source form was found in the complete pinned source tree. The guide's conversational entry was therefore retained as supported, rather than marked stale solely because a spec describes a different surface. This is an upstream spec/implementation discrepancy, not permission to add that UI to the guide.

## Verification and limits

- Verified the worktree branch and base revision, and the remote Studio SHA and pinned plugin gitlink.
- Ran the existing `test_publish_wiki.py` suite only: 21 tests, 19 passed, 2 failed. Expected negative-path error messages in that suite are not additional failures.
- No runtime startup, installer execution, cloud changes, provider login, LLM request, Salesforce request, or external vendor documentation audit was performed.
- Microsoft portal permissions and third-party commercial terms are not certified by this code review. Check them through their approved documentation routes if those instructions are revised.
- No onboarding verification footer was refreshed, and no claim of current live behavior was added to a public guide.

## Correction disposition — 15 October 2026 (GST)

Used the authoring-user-guide workflow, the supporting concise-writing rules, the Vibedata source map, and the repository's top-level wiki layout. The operator's instruction to make the remaining changes authorised editing without another draft approval.

| Finding | Implemented correction |
| --- | --- |
| F01 | Added `docs/Deploy-via-Cloud-Marketplace.md` and routed Home, operator prerequisites, and sidebar to it. Removed the Kubernetes, local Docker, manual Azure infrastructure, and downloadable-installer pages. Removed the CLI installer download from the sidebar. No cluster, chart, or manual vault-bootstrap instructions remain in published source pages. |
| F02 | Replaced the obsolete SSO registry with **Identity providers**, **Allow sign-in**, callback preview, and save-then-**Test** activation. Kept sign-in, downstream user connections, and service identities distinct. |
| F03 | Documented **Basics**, **Data platform**, and **Secret store**; explicit store selection; availability-dependent types; and entry through Internal **Secrets**, external vaults, or an operator-managed Local File. Contributor and Salesforce instructions follow the saved store. |
| F04 | Removed Share-based activation and repair promises. Stated the bound-database ownership requirement and separate user/service PATs. |
| F05 | Removed retired local profiles and Langfuse instructions. Documented the marketplace form's actual **Core only** and **Core plus observability** choices. |
| F06 | Updated selectable roles to Build and Detect, `fix` ownership, bounded read-only reconciliation, **capturing-requirements**, and default `intents/<slug>/` artifact paths with repository/existing-path precedence. |
| F07 | Replaced the exhaustive provider list with a provider-driven procedure, exact **Azure Foundry** label, and the optional Custom/Ollama catalogue association. |
| F08 | Updated sidebar expectations, restored useful Home operation links, and added guards for retired installation paths and unresolved internal page links. Preserved page mapping, sidebar coverage, release gating, and local publication tests. |
| F09 | Removed obsolete August verification footers and the policy of following an unreleased main snapshot. All published pages point to Home's release and source-review scope. The current source audit is identified without claiming a live deployment or a release-specific acceptance run. Publication checks remain open. |

The correction pass also checked the actual Domain workspace: entry is **Domains → Add domain**, instructions are edit-only under **General**, delegated service authentication offers eligible provider reuse or **Dedicated identity**, and the readiness action is **Reconcile** under **Resources**. Obsolete Auto/Manual discovery and defer-at-create instructions were removed. Evidence: [Domain create flow][domain-create-flow], [workspace entry][domain-workspace], [Basics fields][domain-basics], [service-auth presentation][domain-auth], and [Reconcile button][domain-reconcile].

Supporting update and recovery pages now describe maintenance of the existing marketplace deployment, rather than a local update command or hiding a public GitHub release. The [management UI][installation-screen], [marketplace operation channel][marketplace-routes], and [managed-app operations decision][marketplace-day2] ground the scope. No arbitrary-version downgrade or direct resource-edit procedure is claimed.

### Marketplace evidence

- The listing URL is copied from the [current website marketplace registry][site-marketplaces], read from authenticated GitHub source. Its revision is `vibedata-site@34a4ce47f1b17a1f5c559d1a9d107f4380567a35`; only the Microsoft entry has a listing URL. No AWS or GCP installation listing was invented.
- Address, sizing, observability, and JIT controls come from [the pinned offer form][marketplace-form]. The `studioAddress` output comes from [the pinned deployment template][marketplace-template].
- Purchase requirements and portal actions were checked through Microsoft Learn: [Purchase an Azure Application][purchase-app] and [Enable Marketplace purchases][enable-purchases].
- Reading the live listing through `read-website-fast` returned **HTTP 403**. No alternative request was made to bypass that response. The configured URL is source-backed; live listing access, plan availability, and deployed offer version were not verified.

### Correction verification and limits

- The focused publisher suite passes: **23 tests, 0 failures, 0 errors**. Its temporary bare repositories are local and do not contact the real wiki.
- The new guards failed against the pre-correction source set, then passed with the corrected pages and navigation. The original 21-test baseline above is retained separately.
- Internal page targets resolve, all 15 published source pages are reachable from the sidebar, and no sidebar target names a missing page.
- The failed [main CI run](https://github.com/accelerate-data/vibedata-official/actions/runs/38696472222) tested `aee3c19ba64b217a8f4b79ae7df81d1a42dd80f7`: 112 tests ran with the two failures recorded in F08. Both failures were reproduced on clean main, and both pass in this corrected worktree.
- The complete suite passes under Python 3.12 using `requirements-dev.txt`: `python -m coverage run -m unittest discover -s tests` (**114 tests, 0 failures, 0 errors**) and `python -m coverage report --fail-under=70` (**90% total coverage**, above the 70% gate). Temporary coverage data was removed after the run.
- Final checks passed: `ruff check scripts tests`, `ruff format --check scripts tests` (12 files), `scripts/validate-marketplace.py --base-ref origin/main`, `scripts/check-plugin-version-bump.py --base-ref origin/main`, and `git diff --check`. The catalogue freshness and external theme-contract workflow checks were not rerun locally against the corrected tree; their inputs are unchanged. No plugin, manifest, catalogue, or release workflow changed.
- Studio remote `main` was rechecked during correction and still resolved to `a4df79ffcd5dc9d71697887804626a8ae4983177`. The dirty, stale local Studio checkout was not modified or used as current source.
- No live marketplace purchase/deployment, bootstrap login, identity-provider test, connector verification, Intent activation, LLM turn, CI deployment, maintenance operation, backup restore, or release-specific acceptance run was performed. The first-owner handoff and management access must be confirmed on the selected released deployment.
- Removed pages will no longer be published. Existing direct links to the retired installation pages will stop resolving after publication; navigation and source-page links now use the marketplace page.

## Next action

Validate the marketplace deployment and first-Domain flow against the release selected for publication before publishing this documentation.

[cli-main]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/cli/vibedata/src/vibedata/main.py#L22-L55
[cli-install]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/cli/vibedata/src/vibedata/commands/install.py#L436-L437
[cloud-intro]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/cli/cloud-installer/README.md#L1-L32
[cloud-providers]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/cli/cloud-installer/src/server/headless/inputs.ts#L93-L115
[org-navigation]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/features/settings/components/Settings/OrgSettingsPanel.tsx#L49-L102
[identity-policy]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/features/identity-providers/components/identity-provider-register-policy-fields.tsx#L30-L46
[entra-adapter]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/server/lib/auth/better-auth-providers/entra-oidc.ts#L13-L41
[identity-register]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/features/identity-providers/components/identity-provider-register-form.tsx#L65-L76
[create-steps]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/features/domain/components/domain-create/domain-create-tabs.tsx#L13-L18
[store-selector]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/features/domain/components/domain-create/domain-secret-store-candidate-section.tsx#L64-L94
[domain-persistence]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/server/modules/domains/services/create-domain.service.ts#L76-L94
[store-registry]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/server/modules/secret-store-types/providers/registry.ts#L12-L24
[domain-secret-settings]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/docs/design/domain/domain-settings.md#L146-L174
[create-header]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/features/domain/components/domain-create/domain-create-header.tsx#L4-L11
[create-footer]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/features/domain/components/domain-create/domain-create-dialog-footer.tsx#L23-L40
[motherduck-schema]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/server/modules/data-platform-types/providers/motherduck.descriptor.ts#L21-L31
[motherduck-clone]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/server/modules/data-platform-types/providers/motherduck-clone-source.ts#L9-L23
[motherduck-settings]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/docs/design/domain/domain-settings.md#L125-L128
[observability-flags]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/cli/vibedata/src/vibedata/commands/install.py#L447-L466
[observability-resolution]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/cli/vibedata/src/vibedata/commands/install.py#L226-L263
[build-routing]: https://github.com/accelerate-data/vibedata-data-engineering/blob/16f90f637d1617f89dab74661857f914caccd106/agents/build.md#L28-L62
[detect-routing]: https://github.com/accelerate-data/vibedata-data-engineering/blob/16f90f637d1617f89dab74661857f914caccd106/agents/detect.md#L22-L27
[requirement-capture]: https://github.com/accelerate-data/vibedata-data-engineering/blob/16f90f637d1617f89dab74661857f914caccd106/plugins/vibedata-data-engineering/skills/capturing-requirements/SKILL.md#L8-L20
[kind-registry]: https://github.com/accelerate-data/vibedata-data-engineering/blob/16f90f637d1617f89dab74661857f914caccd106/plugins/vibedata-data-engineering/lib/kinds/registry.json
[artifact-paths]: https://github.com/accelerate-data/vibedata-data-engineering/blob/16f90f637d1617f89dab74661857f914caccd106/plugins/vibedata-data-engineering/_shared/references/conventions/artifact-paths.md#L5-L23
[llm-providers]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/shared/llm-providers.ts#L24-L357
[profile-fields]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/features/model-catalog/components/profile-connection-fields.tsx#L125-L155
[canonical-model]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/features/model-catalog/components/profile-canonical-model-field.tsx#L31-L86
[operator-contract]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/docs/design/operator-documentation/README.md#L64-L80
[harness-commands]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/features/chat/lib/harness-commands.ts#L26-L45
[source-skill]: https://github.com/accelerate-data/vibedata-data-engineering/blob/16f90f637d1617f89dab74661857f914caccd106/plugins/vibedata-data-engineering/skills/add-or-update-source/SKILL.md#L28-L114
[site-marketplaces]: https://github.com/accelerate-data/vibedata-site/blob/34a4ce47f1b17a1f5c559d1a9d107f4380567a35/src/lib/marketplaces.ts
[marketplace-form]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/deploy/marketplace/azure/createUiDefinition.json
[marketplace-template]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/deploy/marketplace/azure/mainTemplate.json
[purchase-app]: https://learn.microsoft.com/marketplace/purchase-azure-app-in-azure-portal
[enable-purchases]: https://learn.microsoft.com/azure/cost-management-billing/manage/enable-marketplace-purchases
[domain-create-flow]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/docs/functional/domain/create-flow.md
[domain-workspace]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/features/domain/components/domain-workspace/DomainWorkspace.tsx#L130
[domain-basics]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/features/domain/components/domain-create/domain-create-basics-tab.tsx
[domain-auth]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/features/domain/components/domain-create/domain-data-platform-candidate-section.tsx#L245-L251
[domain-reconcile]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/src/features/settings/components/Settings/panels/domain-settings/DomainProvisioningSection.tsx#L140-L148
[installation-screen]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/cli/cloud-installer/src/ui/screens/InstallationScreen.tsx
[marketplace-routes]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/cli/cloud-installer/src/server/marketplace/routes.ts
[marketplace-day2]: https://github.com/accelerate-data/studio/blob/a4df79ffcd5dc9d71697887804626a8ae4983177/docs/adr/0137-marketplace-managed-app-day-2-runs-inside-the-managed-group-and-waits-for-approval.md
