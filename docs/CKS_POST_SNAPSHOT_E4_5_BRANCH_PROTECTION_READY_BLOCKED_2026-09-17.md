# CKS Post-Snapshot E4.5 — Branch Protection Ready / Administrative Blocker

Date: 2026-09-17
Repository: `rassvetpublic-spec/CKS`
Branch: `main`
Status: READY, NOT APPLIED

## Scope

E4.5 is the final repository-governance action after E4.4 integrated verification.

E4.4 is VERIFIED on live main. Canon / Frozen Core v1.2 remain unchanged.

## Current GitHub state

Read-back before this checkpoint:

- `main.protected = false`;
- branch protection enforcement = off;
- required status-check contexts = empty;
- repository rulesets = `[]`.

Therefore branch protection is **not** currently active and this document must not be interpreted as evidence that it is.

## Exact required-check set

The exact live check-run names were read from commit:

`3414630eda64a23eaa032db0a0601c4c73a51c64`

Use these unique, stable PR checks:

1. `Package 003 integrated automation gate`
2. `boundary`
3. `canon-guard`
4. `traceability`
5. `governance`
6. `validate-control-plane`
7. `validate-bootstrap`

### Deliberate exclusion: `validate`

Do **not** require a bare check named `validate`.

Two separate workflows currently emit the same check-run name:

- CKS Knowledge Check -> `validate`;
- CKS Validation -> `validate`.

Using this ambiguous context as a required check would weaken the semantic guarantee because GitHub cannot distinguish the intended producer by the context string alone.

## Desired protection semantics

Target: branch `main`.

Required behavior:

- require a pull request before merging;
- do not require mandatory approvals (owner-operated autonomous repository);
- require status checks to pass;
- require branch to be up to date before merging;
- require exactly the seven unique checks listed above;
- block force pushes;
- block branch deletion;
- do not newly require signed commits, linear history, deployments, code-owner review, conversation resolution, or mandatory approvals.

## Why it was not applied automatically

Three mutation paths were evaluated:

1. Installed GitHub connector: repository/files/issues/PR/actions writes are available, but branch-protection/ruleset administration is exposed as GET/read only. The managed GitHub App connection does not expose administration-write operations.
2. Browser automation: the branch-settings run was rejected during tool preflight because strict agent mode is not enabled for the account. No GitHub page mutation occurred.
3. Local GitHub CLI: no authenticated `gh` session is available in the execution environment.

No weaker or unverified workaround was used, because claiming protection without API/UI read-back would itself be a false-green governance result.

## Acceptance condition for E4.5 VERIFIED

E4.5 may be changed from READY/BLOCKED to VERIFIED only after a GitHub read-back shows:

```text
main.protected = true
required status checks = enabled
required contexts include all seven unique checks above
force pushes = disabled
deletions = disabled
```

A final checkpoint must record the resulting GitHub protection/ruleset state.

## Worker coordination

This blocker belongs to the E4.5 lane of the current worker.
The parallel Package 003 worker should not alter this protection specification unless a check name is intentionally renamed, in which case this document must be reconciled before protection is enabled.
