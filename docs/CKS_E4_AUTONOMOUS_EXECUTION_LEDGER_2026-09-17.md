# CKS E4 autonomous execution ledger

Date: 2026-09-17
Repository: `rassvetpublic-spec/CKS`
Branch: `main`
Tracking issue: #43
Administrative handoff issue: #56
Related QA issue: #34

## Invariants

- E1–E3.4: CLOSED / VERIFIED.
- Original E4 baseline: `1ff433d7605ea5b8c3af3081436d25df7e746450`.
- Canon / Frozen Core v1.2: DO NOT MODIFY.
- Continue from live `main`; preserve concurrent work; no force update/rollback.
- E4.5 may not be called VERIFIED without GitHub protection read-back.

## Worker coordination

- Worker A / this lane: E4.4 integrated verification + E4.5 branch protection.
- Parallel worker: Package 003 internal consolidation / duplicate cleanup.
- Before every repository write, re-read live `main`.
- Worker A lock is released only after E4.5 protection read-back and final checkpoint.

## E4 chain

| Stage | State | Evidence |
|---|---|---|
| E4.1 shared structural/review gates | VERIFIED | shared composite gates + regression coverage |
| E4.2 Governance Runner v2 | VERIFIED | fail-closed runner + push/PR/manual CI |
| E4.3 Package 003 executable completion | VERIFIED | canonical `cks-package-003-automation.yml`; PR/main evidence green |
| E4.4 integrated regression | VERIFIED | `CKS_POST_SNAPSHOT_E4_4_INTEGRATED_REGRESSION_VERIFIED_2026-09-17.md` |
| E4.5 branch protection | READY / EXTERNAL ADMIN AUTH BLOCKED | exact policy + fail-safe helper + tests green; GitHub settings mutation still unavailable |

## E4.3 canonical Package 003 state

Canonical aggregate:

`.github/workflows/cks-package-003-automation.yml`

The parallel worker removed only duplicate Package 003 workflow/test files. The canonical aggregate remains active and green.

Package 003 remains 10/10 component-complete: Actions automation, real schema validation, derived Knowledge Index, Traceability, Canon Guard, Issue/PR automation, Research/Core boundary, advisory Migration Audit, full tests/integration with zero-test guard, and real Review/Governance execution plus evidence artifacts.

## E4.4 live-main integrated verification

Verified live head before E4.4 checkpoint:

`3414630eda64a23eaa032db0a0601c4c73a51c64`

All 10 push workflows on that exact head completed SUCCESS:

- Package 003 Automation `35192113935`
- Validation `35192113941`
- Boundary `35192113974`
- Canon `35192113858`
- Traceability `35192113966`
- Governance `35192113867`
- Runtime Governance `35192113918`
- Knowledge Check `35192113938`
- Control Plane `35192113899`
- Bootstrap `35192113900`

Package 003 job `105106786775` passed its complete integrated chain. Validation job `105106786940` passed Node24, E3.4, Issue #34 false-green and full contracts validation.

Durable E4.4 checkpoint commit:

`da199b804e5fffaa4f40cb0afbfa50186d3dfdd8`

## E4.5 exact protection specification

Unique required PR checks selected from actual GitHub check-run names:

1. `Package 003 integrated automation gate`
2. `boundary`
3. `canon-guard`
4. `traceability`
5. `governance`
6. `validate-control-plane`
7. `validate-bootstrap`

Bare `validate` is deliberately excluded because two workflows emit that same check name.

All seven selected checks were re-read from live `main` and each source workflow has a `pull_request` trigger. This avoids an impossible required-check state on PRs.

Desired protection:

- pull request required before merge;
- 0 mandatory approving reviews;
- required status checks enabled;
- branch must be up to date before merge (`strict = true`);
- seven unique checks above required;
- administrators are subject to the rule;
- force pushes disabled;
- branch deletion disabled;
- do not newly require signed commits, linear history, deployments, code-owner review, last-push approval, conversation resolution or mandatory approvals.

## E4.5 helper and regression

Fail-safe helper:

`tools/cks_apply_branch_protection.py`

Tests:

`tests/test_cks_branch_protection_helper_e4.py`

The initial helper draft was audited before use. A defect was found: `required_pull_request_reviews = null` would disable the PR requirement. No repository-settings mutation had occurred.

The helper was corrected to enable the PR requirement with `required_approving_review_count = 0` and to verify this condition in read-back.

Correction chain:

- initial helper: `2ba14bacb5e25f75a65cefde328c3def0d0d6871`;
- PR-requirement fix: `dd2b176d92f342d20fb14deb5bf5a531217c5995`;
- corrected regression tests / verified functional head: `932e1984a7779cd0492989d944a0200ff539a7c8`.

On `932e1984...` all 10 automatic push workflows completed successfully with no failure and no unfinished run.

Canonical aggregate on the corrected helper head:

- run `35193442906`;
- job `105111018790` (`Package 003 integrated automation gate`);
- conclusion `success`;
- workflow contract, zero-test guard, full unittest suite, integration, Knowledge Index, Migration Audit, Traceability, Canon, Review/Research-Core Boundary, Governance Runner v2 and evidence upload all PASS.

## E4.5 current platform state

Latest read-back before this ledger update still shows:

- `main.protected = false`;
- required status-check enforcement = off;
- required contexts = empty;
- repository rulesets = `[]`.

Mutation attempts/capability audit:

- installed GitHub connector exposes protection/rulesets read-only and has no administration-write action;
- browser automation with the normal profile had no authenticated GitHub session; no mutation occurred;
- browser automation with vault enabled had no stored GitHub credentials; no mutation occurred;
- local execution environment has no authenticated administrator GitHub CLI/token path available to Worker A;
- no second GitHub-admin plugin is available.

No false claim of protection was made.

Durable blocker/spec checkpoint:

`docs/CKS_POST_SNAPSHOT_E4_5_BRANCH_PROTECTION_READY_BLOCKED_2026-09-17.md`

Latest handoff-spec update commit:

`32aee40e6cc24a1d7d13c1992e5b82fe14ab855a`

## One-shot admin handoff

Do not place a token in chat or repository content.

PowerShell procedure from a repository checkout:

```powershell
$env:CKS_GITHUB_ADMIN_TOKEN = "<admin-capable-token>"
python tools/cks_apply_branch_protection.py
python tools/cks_apply_branch_protection.py --apply
Remove-Item Env:CKS_GITHUB_ADMIN_TOKEN
```

First invocation is a live dry-run. `--apply` performs the mutation only after the live check surface passes preflight. A different pre-existing protection rule causes a fail-closed exit unless `--replace-existing` is deliberately supplied after review.

## E4.5 acceptance condition

Change E4.5 to VERIFIED only after GitHub read-back proves:

```text
main.protected = true
required status checks = enabled
strict / branch-up-to-date = true
required contexts = exactly the seven unique checks
pull request before merge = enabled
required approving review count = 0
enforce administrators = true
force pushes = disabled
deletions = disabled
```

After that read-back:

1. create final E4.5 VERIFIED checkpoint;
2. mark the E4 chain CLOSED / VERIFIED;
3. update Issue #43 and #56;
4. publish `WORKER A RELEASE` in Issue #43.

Until then E4 is functionally verified through E4.4, with one external repository-administration action outstanding.

## Canon / Frozen Core

UNCHANGED throughout E4.

This ledger + Issue #43 + Issue #56 are the recovery SSOT; chat history is not required.
