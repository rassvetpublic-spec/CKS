# CKS Post-Snapshot Integrity Audit — Stage E3.3

Date: 2026-09-17
Status: ANALYSIS COMPLETE
Scope: GitHub Actions Node.js runtime debt only

## PREV-VERIFY

E3.2-C2F2-C is VERIFIED. Its repair commit `c0717d79d888dc2743715564d8c0866d72571295` produced a successful automatic Integration Test (`35170769965`) together with successful Validation, Boundary, Runtime Governance, Knowledge Check, Control Plane, Traceability, Canon Guard and Bootstrap runs.

Canon / Frozen Core v1.2 remain unchanged.

## Direct runtime evidence

The executable Integration Test run before the discovery repair emitted GitHub runner warnings that:

- Node.js 20 is deprecated;
- actions targeting Node.js 20 are being forced to run on Node.js 24;
- specifically `actions/checkout@v4` and `actions/setup-python@v5` were identified in the run log.

GitHub's published deprecation notice, updated August 25, 2026, states that Node.js 20 will be removed from Actions runners on **2026-09-23**.

## Repository inventory

After removal of Preflight and Release Check, 15 workflow files remain.

All 15 use `actions/checkout@v4`.

10 use `actions/setup-python@v5`:

1. `cks-boundary-check.yml`
2. `cks-canon-evidence-guard.yml`
3. `cks-integration-test.yml`
4. `cks-knowledge-runtime-intelligence.yml`
5. `cks-review-gate.yml`
6. `cks-runtime-governance.yml`
7. `cks-traceability-check.yml`
8. `cks-v1-6-intelligence-runtime.yml`
9. `cks-v1.4-validation.yml`
10. `cks-validation.yml`

7 use `actions/upload-artifact@v4`:

1. `cks-boundary-check.yml`
2. `cks-canon-evidence-guard.yml`
3. `cks-knowledge-runtime-intelligence.yml`
4. `cks-review-gate.yml`
5. `cks-runtime-governance.yml`
6. `cks-traceability-check.yml`
7. `cks-validation.yml`

## Minimal migration targets

This audit intentionally does **not** chase the newest available major merely because it exists.

The minimum official Node.js 24 migration majors are:

- `actions/checkout@v5` — Node.js 24; minimum Actions runner `v2.327.1`;
- `actions/setup-python@v6` — Node.js 24; minimum Actions runner `v2.327.1`;
- `actions/upload-artifact@v6` — Node.js 24; minimum Actions runner `v2.327.1`.

The observed GitHub-hosted runner for CKS was `v2.337.0`, so it satisfies the common minimum version.

Current upstream majors are newer, but using the first Node.js-24 major minimizes unrelated behavioral change while removing the concrete deprecation risk.

## Implementation decision

E3.3 implementation will perform only these substitutions:

```text
actions/checkout@v4        -> actions/checkout@v5
actions/setup-python@v5    -> actions/setup-python@v6
actions/upload-artifact@v4 -> actions/upload-artifact@v6
```

No triggers, permissions, commands, test semantics, Python versions, artifacts, Canon/Core files or CKS contracts will be changed in the migration.

After replacement, E3.4 must prove both:

1. no legacy target remains in any workflow;
2. the substantive CKS gates still pass with the Node.js-24 action majors.
