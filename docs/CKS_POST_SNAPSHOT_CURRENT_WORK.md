# CKS Post-Snapshot Current Work

Updated: 2026-09-17
SSOT: GitHub `rassvetpublic-spec/CKS`, branch `main`

## Current stage

**E4 ACTIVE — functionally verified through E4.4; E4.5 branch protection is READY / EXTERNAL ADMIN AUTH BLOCKED.**

E1–E3.4 remain CLOSED / VERIFIED and must not be repeated without contradictory evidence.

Original E4 baseline:

`1ff433d7605ea5b8c3af3081436d25df7e746450`

## Current E4 chain

```text
E4.1  VERIFIED — shared structural/review gates
E4.2  VERIFIED — Governance Runner v2, push main + PR + manual
E4.3  VERIFIED — Package 003 executable completion
E4.4  VERIFIED — integrated live-main regression
E4.5  READY / EXTERNAL ADMIN AUTH BLOCKED — branch protection not yet applied
```

## Primary recovery documents

1. `docs/CKS_E4_FULL_RECOVERY_SNAPSHOT_2026-09-17.md`
2. `docs/CKS_E4_AUTONOMOUS_EXECUTION_LEDGER_2026-09-17.md`
3. `docs/CKS_POST_SNAPSHOT_E4_4_INTEGRATED_REGRESSION_VERIFIED_2026-09-17.md`
4. `docs/CKS_POST_SNAPSHOT_E4_5_BRANCH_PROTECTION_READY_BLOCKED_2026-09-17.md`
5. `docs/CKS_POST_SNAPSHOT_AUDIT_INDEX.md`

Coordination:

- Issue #43 — main E4 tracker / worker coordination.
- Issue #56 — canonical E4.5 administrative handoff.
- Issue #34 — related QA / false-green context.
- Issues #57 and #58 — accidental VOID issues; closed / not planned; do not use.

## Package 003 canonical state

Canonical aggregate workflow:

`.github/workflows/cks-package-003-automation.yml`

Package 003 is 10/10 component-complete:

1. GitHub Actions automation;
2. schema validation;
3. Knowledge Index generation;
4. Traceability;
5. Canon Guard;
6. Issue/PR automation;
7. Research/Core boundary CI;
8. Migration Audit;
9. full unit/integration tests with zero-test guard;
10. real Review/Governance execution + evidence artifacts.

Do not recreate duplicate Package 003 workflow/test implementations that were already consolidated away.

## Latest verified E4 functional evidence

Corrected E4.5 helper/test functional head:

`932e1984a7779cd0492989d944a0200ff539a7c8`

All 10 automatic push workflows on that head completed SUCCESS.

Package 003 aggregate:

- run `35193442906`;
- job `105111018790`;
- `Package 003 integrated automation gate` = SUCCESS.

The repository head immediately before the full recovery snapshot was:

`b4277a4496d4499a18b83c9869a39a4514156b78`

and its 10 automatic workflows also completed SUCCESS with no unfinished run.

Full recovery snapshot commit:

`0c39ee92582d0340437111e274d5eb16226f5530`

## E4.5 exact required checks

1. `Package 003 integrated automation gate`
2. `boundary`
3. `canon-guard`
4. `traceability`
5. `governance`
6. `validate-control-plane`
7. `validate-bootstrap`

Bare `validate` is deliberately excluded because two workflows emit the same check-run name.

All seven selected checks have a `pull_request` trigger.

## E4.5 exact target policy

- PR required before merge;
- 0 mandatory approving reviews;
- required status checks enabled;
- branch must be up to date before merge (`strict = true`);
- exactly the seven unique contexts above;
- enforce administrators;
- block force pushes;
- block branch deletion;
- do not newly require signed commits, linear history, deployments, code-owner review, last-push approval, conversation resolution, or mandatory approvals.

Fail-safe helper:

`tools/cks_apply_branch_protection.py`

Tests:

`tests/test_cks_branch_protection_helper_e4.py`

The helper was audited before use. An initial defect (`required_pull_request_reviews = null`, which would disable the PR requirement) was found before any settings mutation and fixed in `dd2b176d92f342d20fb14deb5bf5a531217c5995`; corrected tests passed on `932e1984...`.

## Current external blocker

Latest read-back still shows:

```text
main.protected = false
required status-check enforcement = off
required contexts = []
```

No false claim of protection is allowed.

Available GitHub connector/browser/local execution paths do not currently expose an authenticated repository-administration write surface. E4.5 remains blocked until an admin-capable credential is available in a safe environment.

## One-shot continuation

Do not put a token in chat or repository content.

```powershell
$env:CKS_GITHUB_ADMIN_TOKEN = "<admin-capable-token>"
python tools/cks_apply_branch_protection.py
python tools/cks_apply_branch_protection.py --apply
Remove-Item Env:CKS_GITHUB_ADMIN_TOKEN
```

After successful GitHub read-back:

1. create final E4.5 VERIFIED checkpoint;
2. mark E4 CLOSED / VERIFIED;
3. update Issues #43 and #56;
4. publish `WORKER A RELEASE` in Issue #43.

## Closed historical audit

E1–E3.4 remain CLOSED / VERIFIED. Historical final documents:

- `docs/CKS_POST_SNAPSHOT_INTEGRITY_AUDIT_STAGE_E3_4_FINAL_VERIFIED_2026-09-17.md`
- `docs/CKS_POST_SNAPSHOT_AUDIT_INDEX.md`

## Do not restart closed work

- do not repeat E1/E2/E3 merely to reconstruct chat context;
- use GitHub `main` and the recovery documents above;
- do not modify Canon / Frozen Core v1.2 as part of E4 administration;
- preserve the CKS/KAT9I_OS boundary: no raw runtime/history import and no direct external Canon mutation.
