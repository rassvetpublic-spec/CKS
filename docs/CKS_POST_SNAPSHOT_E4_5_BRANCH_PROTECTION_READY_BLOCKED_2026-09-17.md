# CKS Post-Snapshot E4.5 — Branch Protection Ready / External Admin Blocker

Date: 2026-09-17
Repository: `rassvetpublic-spec/CKS`
Branch: `main`
Status: READY / EXTERNAL ADMIN AUTH BLOCKED / NOT APPLIED

## Scope

E4.5 is the final repository-governance action after E4.4 integrated verification.

E4.1–E4.4 are VERIFIED. Canon / Frozen Core v1.2 remain unchanged.

This checkpoint is a fail-closed handoff: it records the exact protection policy, executable helper, CI evidence, and acceptance read-back. It is **not** evidence that branch protection is already enabled.

## Current GitHub state

Latest read-back before this update:

- live `main` head: `932e1984a7779cd0492989d944a0200ff539a7c8`;
- `main.protected = false`;
- branch protection enforcement = off;
- required status-check contexts = empty;
- repository rulesets = `[]`.

Therefore branch protection is **not** currently active.

## Exact required-check set

Use exactly these unique PR check-run names:

1. `Package 003 integrated automation gate`
2. `boundary`
3. `canon-guard`
4. `traceability`
5. `governance`
6. `validate-control-plane`
7. `validate-bootstrap`

### Deliberate exclusion: `validate`

Do **not** require a bare check named `validate`.

Two separate workflows emit that same check-run name, so the context is ambiguous. The seven selected contexts above are unique.

## PR-trigger reachability audit

All seven selected required checks were re-read from live `main` and each source workflow has a `pull_request` trigger:

- `.github/workflows/cks-package-003-automation.yml`
- `.github/workflows/cks-boundary-check.yml`
- `.github/workflows/cks-canon-evidence-guard.yml`
- `.github/workflows/cks-traceability-check.yml`
- `.github/workflows/cks-governance-runner.yml`
- `.github/workflows/cks-control-plane-validation.yml`
- `.github/workflows/bootstrap-check.yml`

This prevents a protection rule that would wait forever for a required check which never runs on pull requests.

## Desired protection semantics

Target: branch `main`.

Required behavior:

- require a pull request before merging;
- require **0 mandatory approving reviews**;
- require status checks to pass;
- require the branch to be up to date before merging (`strict = true`);
- require exactly the seven unique checks listed above;
- enforce the rule for repository administrators;
- block force pushes;
- block branch deletion;
- do not newly require signed commits, linear history, deployments, code-owner review, last-push approval, conversation resolution, or mandatory approvals.

### Corrected API semantics

The first helper draft incorrectly used:

`required_pull_request_reviews = null`

GitHub defines `null` as disabling the pull-request review/protection requirement. That draft was never used to mutate repository settings.

The corrected helper now uses an object with:

```json
{
  "dismiss_stale_reviews": false,
  "require_code_owner_reviews": false,
  "required_approving_review_count": 0,
  "require_last_push_approval": false
}
```

This keeps pull-request-only merging enabled while requiring zero approving reviews.

Correction commits:

- helper fix: `dd2b176d92f342d20fb14deb5bf5a531217c5995`;
- regression tests / current verified head: `932e1984a7779cd0492989d944a0200ff539a7c8`.

## Fail-safe helper

Executable handoff helper:

`tools/cks_apply_branch_protection.py`

Regression tests:

`tests/test_cks_branch_protection_helper_e4.py`

Safety properties:

- default mode is dry-run; no mutation without `--apply`;
- requires an explicit admin-capable token from `CKS_GITHUB_ADMIN_TOKEN` or `GITHUB_TOKEN`;
- validates all seven required check names against the current branch head before mutation;
- rejects missing or duplicate required contexts;
- ignores the unrelated duplicate bare `validate` because it is not in the required set;
- refuses to overwrite a different existing protection rule unless `--replace-existing` is explicitly supplied;
- enables PR-only merge with zero approving reviews;
- performs branch/protection read-back after mutation;
- exits non-zero unless the read-back exactly matches the intended policy.

## CI evidence for corrected helper

Current verified helper/test head:

`932e1984a7779cd0492989d944a0200ff539a7c8`

All 10 automatic push workflows on this exact head completed successfully, with no failure and no unfinished run.

Canonical aggregate evidence:

- workflow: `CKS Package 003 Automation`;
- run: `35193442906`;
- job: `105111018790` (`Package 003 integrated automation gate`);
- conclusion: `success`.

The job passed the workflow contract regression, zero-test guard, full unittest suite (including the E4.5 helper regression), integration suite, Knowledge Index, Migration Audit, Traceability, Canon Guard, Review/Research-Core Boundary, Governance Runner v2, and evidence upload.

## One-shot application procedure

Do not paste an administrator token into chat or commit it to the repository.

### PowerShell

```powershell
$env:CKS_GITHUB_ADMIN_TOKEN = "<admin-capable-token>"
python tools/cks_apply_branch_protection.py
python tools/cks_apply_branch_protection.py --apply
Remove-Item Env:CKS_GITHUB_ADMIN_TOKEN
```

The first command invocation is a live dry-run. The second mutates protection only if the live check surface passes preflight.

If GitHub already has a different protection rule, the helper fails closed. `--replace-existing` must not be used without reviewing the existing rule first.

## Why it has not been applied automatically

Available mutation paths were exhausted without weakening verification:

1. Installed GitHub connector: repository/files/issues/PR/actions writes are available, but branch-protection/ruleset administration is exposed read-only; no administration-write action is available.
2. Browser automation with the normal profile reached GitHub but had no authenticated GitHub session; no mutation occurred.
3. Browser automation with vault enabled also found no stored GitHub credentials; no mutation occurred.
4. Local execution environment has no authenticated administrator GitHub CLI/token path available to this worker.

No false claim of protection was made.

Administrative handoff issue: **#56**.

Accidental placeholder issues #57 and #58 were immediately marked VOID and closed as `not_planned`; they carry no work.

## Acceptance condition for E4.5 VERIFIED

E4.5 may change from READY/BLOCKED to VERIFIED only after GitHub read-back proves all of the following:

```text
main.protected = true
required status checks = enabled
strict / branch-up-to-date = true
required contexts = exactly the seven unique checks above
pull request before merge = enabled
required approving review count = 0
enforce administrators = true
force pushes = disabled
deletions = disabled
```

After that read-back:

1. create the final E4.5 VERIFIED checkpoint;
2. update the E4 ledger to CLOSED / VERIFIED;
3. update Issue #43 and Issue #56;
4. publish `WORKER A RELEASE` in Issue #43.

## Worker coordination

E4.5 remains owned by Worker A. The parallel Package 003 worker should not alter this protection specification unless a required check is intentionally renamed or removed; such a change requires re-running the reachability audit before applying protection.

## Final persistence update — browser/API retry

Additional evidence captured after the fail-safe handoff:

- live `main` before this persistence pass had advanced through concurrent documentation work; the last read before the write was `bd965a3b586c0a6ea3d7395beffd052b7deda114`;
- browser automation run `10fa0b7d-3070-4847-98ae-0889a112e8df` opened the repository branch-settings URL but GitHub presented an unauthenticated state (`Sign in` / settings URL not accessible); **no branch-protection mutation was saved**;
- independent branch read-back still returned `main.protected = false`, required status-check enforcement off, and empty required contexts;
- repository rulesets read-back remained `[]`;
- direct branch-protection endpoint access through the installed integration returned `403 Resource not accessible by integration`, confirming the connector lacks the administration surface needed for the mutation/read-back endpoint;
- plugin-directory verification found only the already-installed GitHub connector and no separate GitHub administration connector;
- therefore there is no evidence of partial configuration and E4.5 remains `READY / EXTERNAL ADMIN AUTH BLOCKED / NOT APPLIED`.

The authoritative continuation remains Issue #56 plus `tools/cks_apply_branch_protection.py`. Worker A lock remains active until an admin-capable execution applies the policy and GitHub read-back satisfies every acceptance condition above.
