# CKS Post-Snapshot Integrity Audit — Stage E3.3

Date: 2026-09-17
Status: VERIFIED
Scope: GitHub Actions Node.js runtime debt

## PREV-VERIFY

E3.2 integration repairs remained green before this stage. Canon and Frozen Core v1.2 were not modified.

## Migration

The repository moved the GitHub Actions that were still targeting Node.js 20 to the minimum Node.js-24 majors selected in the analysis checkpoint:

- `actions/checkout@v4` -> `actions/checkout@v5`;
- `actions/setup-python@v5` -> `actions/setup-python@v6`;
- `actions/upload-artifact@v4` -> `actions/upload-artifact@v6`.

Five checkout-only workflows were updated first. The remaining workflow set was then migrated in tree commit:

`2d268b032966ada64a917ee5c8ce4d6d8984f4e4`.

No triggers, CKS validation commands, Python version, artifact paths, permissions, Canon/Core contracts or knowledge semantics were changed as part of the migration.

## Permanent regression guard

Added:

`tests/test_cks_github_actions_node24_stage_e3_3.py`

The test scans all `.github/workflows/*.yml|yaml` and fails if any of the retired majors return:

- `actions/checkout@v4`;
- `actions/setup-python@v5`;
- `actions/upload-artifact@v4`.

It also verifies that the Node.js-24 replacement majors are present.

The guard is executed by the main `CKS Validation` workflow.

Guard wiring commit:

`c3d72f93696d7b7d7f2119b75670581d2595aa7a`.

## CI evidence

On migration head `2d268b032966ada64a917ee5c8ce4d6d8984f4e4`, GitHub created 12 automatic runs and no failure was recorded. Representative migrated workflows passed, including:

- CKS Integration Test — run `35171200158` — SUCCESS, explicitly executing `checkout@v5` and `setup-python@v6`;
- CKS v1.4 Validation — run `35171200220` — SUCCESS.

On final integration head `e224bd24c7183f13250da5b95d34a38b5339d968`:

- CKS Validation — run `35172013953` — SUCCESS, including step `Guard GitHub Actions Node.js 24 migration`;
- CKS Integration Test — run `35172013962` — SUCCESS;
- Runtime Governance — run `35172014046` — SUCCESS;
- Traceability — run `35172013996` — SUCCESS;
- Knowledge Check — run `35172013951` — SUCCESS;
- Boundary Check — run `35172013955` — SUCCESS;
- Control Plane Validation — run `35172014010` — SUCCESS;
- Bootstrap Check — run `35172013970` — SUCCESS;
- Canon Evidence Guard — run `35172014148` — SUCCESS.

The validated jobs show the expected Node.js-24 majors in execution, including `checkout@v5`, `setup-python@v6` and `upload-artifact@v6` where applicable.

## Result

The concrete Node.js-20 deprecation debt identified by GitHub runner warnings has been removed from the workflow definitions and is now protected against regression by CI.

Canon / Frozen Core v1.2: UNCHANGED.
