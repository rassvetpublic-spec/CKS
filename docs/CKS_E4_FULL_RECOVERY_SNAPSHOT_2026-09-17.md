# CKS E4 Full Recovery Snapshot

Date: 2026-09-17
Repository: `rassvetpublic-spec/CKS`
Branch: `main`
Purpose: durable recovery of the current work state without relying on chat history.

## 1. Governing invariants

- GitHub `main` is the SSOT.
- E1–E3.4 are CLOSED / VERIFIED and must not be repeated without contradictory evidence.
- Original E4 baseline: `1ff433d7605ea5b8c3af3081436d25df7e746450`.
- Canon / Frozen Core v1.2 remain unchanged.
- CKS remains independent from KAT9I_OS.
- Preserve concurrent work; no force-push/rollback recovery.
- Before every repository write, re-read live `main`.

## 2. Current E4 status

```text
E4.1 Shared structural/review gates   VERIFIED
E4.2 Governance Runner v2             VERIFIED
E4.3 Package 003 executable package   VERIFIED
E4.4 Integrated live-main regression  VERIFIED
E4.5 Main branch protection           READY / EXTERNAL ADMIN AUTH BLOCKED
```

E4 is functionally verified through E4.4. It is not fully CLOSED because E4.5 has not been physically applied to GitHub repository settings.

## 3. E4.1 — shared gates

Implemented state:

- Compliance and Knowledge Check use a common structural gate rather than duplicating directory logic.
- Review Gate and Boundary Check intentionally share the same review-gate engine while preserving separate workflow interfaces/triggers.
- Workflow inventory remains stable; consolidation did not delete public workflow interfaces unnecessarily.

Relevant reusable actions:

- `.github/actions/cks-structure-gate/action.yml`
- `.github/actions/cks-review-gate/action.yml`

## 4. E4.2 — Governance Runner v2

Governance Runner v2 is fail-closed and wired for:

- `push` to `main`;
- `pull_request`;
- `workflow_dispatch`.

Canonical workflow:

- `.github/workflows/cks-governance-runner.yml`

Canonical runner:

- `tools/cks_governance_runner.py`

## 5. E4.3 — CKS v1.3 Implementation Package 003

Canonical aggregate workflow:

- `.github/workflows/cks-package-003-automation.yml`

Package 003 is treated as 10/10 component-complete:

1. real GitHub Actions automation;
2. schema validation;
3. derived Knowledge Index generation;
4. automatic Traceability gate/reporting;
5. Canon Evidence Guard enforcement;
6. Issue/PR automation;
7. CI enforcement of Research/Core boundary;
8. advisory Migration Audit;
9. full unit/integration test surface with zero-test protection;
10. real Review/Governance execution with evidence artifacts.

The canonical aggregate currently runs:

- Package 003 workflow contract test;
- non-zero test-discovery guard;
- full unittest suite;
- integration suite;
- Knowledge Index generation;
- Migration Audit;
- Traceability gate;
- Canon gate;
- Review + Research/Core Boundary gate;
- Governance Runner v2;
- evidence artifact upload.

Do not recreate duplicate Package 003 workflows/tests that were already consolidated away.

## 6. E4.4 — integrated verification

Previously verified functional live-main head:

`3414630eda64a23eaa032db0a0601c4c73a51c64`

E4.4 durable checkpoint:

`da199b804e5fffaa4f40cb0afbfa50186d3dfdd8`

All 10 push workflows on the verified E4.4 head completed successfully.

The later E4.5 helper/test head:

`932e1984a7779cd0492989d944a0200ff539a7c8`

also completed all 10 automatic workflows successfully. The Package 003 aggregate run `35193442906`, job `105111018790`, completed SUCCESS through the full integrated chain.

The last repository head before creation of this recovery snapshot was:

`b4277a4496d4499a18b83c9869a39a4514156b78`

and its 10 automatic push workflows completed successfully with no failure and no unfinished run.

## 7. E4.5 — exact branch-protection policy

Target branch: `main`.

Required merge behavior:

- pull request required before merge;
- zero mandatory approving reviews;
- required status checks enabled;
- branch must be up to date before merge (`strict = true`);
- administrators are subject to the rule;
- force pushes disabled;
- branch deletion disabled;
- do not newly require signed commits, linear history, deployments, code-owner review, last-push approval, conversation resolution, or mandatory approvals.

Exact required status contexts:

1. `Package 003 integrated automation gate`
2. `boundary`
3. `canon-guard`
4. `traceability`
5. `governance`
6. `validate-control-plane`
7. `validate-bootstrap`

The bare check name `validate` is deliberately excluded because two workflows emit that same check-run name, making it ambiguous as a branch-protection context.

All seven selected contexts were verified to originate from workflows that have `pull_request` triggers, so requiring them will not create an impossible PR state.

## 8. E4.5 fail-safe helper

Helper:

- `tools/cks_apply_branch_protection.py`

Regression tests:

- `tests/test_cks_branch_protection_helper_e4.py`

Important audit finding and repair:

- initial helper draft used `required_pull_request_reviews = null`, which would disable the PR requirement;
- no GitHub settings mutation had occurred at that point;
- fixed in commit `dd2b176d92f342d20fb14deb5bf5a531217c5995`;
- tests updated and verified on head `932e1984a7779cd0492989d944a0200ff539a7c8`;
- corrected semantics use `required_approving_review_count = 0` while still requiring pull requests.

The helper is fail-safe:

- no mutation without `--apply`;
- validates the exact required check surface first;
- refuses to overwrite a different existing protection rule unless explicitly allowed;
- performs post-mutation read-back;
- fails if the resulting rule does not match the target policy.

## 9. Current external blocker

Latest verified platform state before this snapshot:

```text
main.protected = false
required status-check enforcement = off
required contexts = []
```

The rule has NOT been applied.

Exhausted mutation paths:

- installed GitHub connector: repository/files/issues/PR/actions writes available, but no branch-protection/ruleset administration write action;
- GitHub connector administration access is not available through the managed app;
- browser normal profile: no authenticated GitHub session;
- browser vault path: no stored GitHub credentials;
- no authenticated admin GitHub CLI/token path in the execution environment;
- no second GitHub-admin plugin available;
- repository workflows do not expose an existing admin-capable secret path that can safely be reused.

Therefore E4.5 must remain `READY / EXTERNAL ADMIN AUTH BLOCKED` until an administrator-capable credential is available in a safe execution environment.

## 10. One-shot E4.5 execution procedure

Do not place a token in chat or repository content.

From a repository checkout in PowerShell:

```powershell
$env:CKS_GITHUB_ADMIN_TOKEN = "<admin-capable-token>"
python tools/cks_apply_branch_protection.py
python tools/cks_apply_branch_protection.py --apply
Remove-Item Env:CKS_GITHUB_ADMIN_TOKEN
```

The first invocation is dry-run/preflight. The second performs the mutation only if the live check surface is safe.

## 11. E4.5 acceptance condition

E4.5 becomes VERIFIED only when GitHub read-back proves all of the following:

```text
main.protected = true
required status checks = enabled
strict / branch-up-to-date = true
required contexts = exactly the seven contexts listed above
pull request before merge = enabled
required approving review count = 0
enforce administrators = true
force pushes = disabled
deletions = disabled
```

Then perform, in order:

1. create final E4.5 VERIFIED checkpoint;
2. mark E4 chain CLOSED / VERIFIED;
3. update Issue #43;
4. update Issue #56;
5. publish `WORKER A RELEASE` in Issue #43.

## 12. Coordination / issue map

- Issue #43 — main E4 tracking / worker coordination.
- Issue #56 — canonical administrative handoff for E4.5.
- Issue #34 — related QA / false-green regression context.
- Issue #57 — accidental placeholder; CLOSED / VOID / not planned.
- Issue #58 — accidental dummy issue; CLOSED / VOID / not planned.

Do not attach work to #57 or #58.

## 13. Durable recovery sources

Primary recovery chain:

1. `docs/CKS_POST_SNAPSHOT_CURRENT_WORK.md`
2. `docs/CKS_E4_AUTONOMOUS_EXECUTION_LEDGER_2026-09-17.md`
3. `docs/CKS_POST_SNAPSHOT_E4_4_INTEGRATED_REGRESSION_VERIFIED_2026-09-17.md`
4. `docs/CKS_POST_SNAPSHOT_E4_5_BRANCH_PROTECTION_READY_BLOCKED_2026-09-17.md`
5. this file: `docs/CKS_E4_FULL_RECOVERY_SNAPSHOT_2026-09-17.md`
6. Issue #43
7. Issue #56

Chat history is not required to continue safely from this state.

## 14. Canon / Frozen Core

UNCHANGED throughout E4.
