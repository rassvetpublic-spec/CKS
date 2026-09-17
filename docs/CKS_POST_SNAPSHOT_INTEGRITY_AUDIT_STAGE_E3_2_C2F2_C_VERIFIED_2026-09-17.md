# CKS Post-Snapshot Integrity Audit — Stage E3.2-C2F2-C

Date: 2026-09-17
Status: VERIFIED

## PREV-VERIFY

C2F2-A established the active KAT9I_OS -> CKS contract. C2F2-B implemented the validator and direct regression tests without changing Canon, Frozen Core v1.2 or the active contract schema.

## Executable gate implementation

The prior Integration Test workflow only checked for file existence and the prior `scripts/run_integration_tests.py` returned a hard-coded PASS.

C2F2-C changed that behavior:

- `scripts/run_integration_tests.py` now discovers and executes the dedicated integration regression suite;
- zero discovered tests is a FAIL;
- test failures/errors cause a non-zero process exit;
- `.github/workflows/cks-integration-test.yml` runs the real test runner on Python 3.12;
- push/PR path filters cover the active schema, importer, runner, adapter layer, relevant ingestion/split contract docs and the regression test itself.

Workflow implementation commit: `9871c3ba1067eb685fee8fcce5f6d58b78ba72a5`.

## First real run caught a real runner defect

Automatic run `35170728397` failed as designed. The workflow no longer produced a false green.

Root cause:

`unittest.discover(..., top_level_dir=ROOT)` required `tests/` to be importable as a Python package, while this repository intentionally does not make `tests/` a package.

The defect was repaired minimally by keeping repository root on `sys.path` while discovering directly from the non-package test directory.

Repair commit: `c0717d79d888dc2743715564d8c0866d72571295`.

## Verification evidence on repair commit

All listed runs were automatic push runs for `c0717d79d888dc2743715564d8c0866d72571295` and completed successfully:

- CKS Integration Test — run `35170769965` — SUCCESS
- CKS Validation — run `35170769927` — SUCCESS
- CKS Boundary Check — run `35170769975` — SUCCESS
- CKS Runtime Governance — run `35170769917` — SUCCESS
- CKS Knowledge Check — run `35170769885` — SUCCESS
- CKS Control Plane Validation — run `35170769909` — SUCCESS
- CKS Traceability Check — run `35170769946` — SUCCESS
- CKS Canon Evidence Guard — run `35170769872` — SUCCESS
- CKS Bootstrap Check — run `35170769863` — SUCCESS

## Result

The KAT9I_OS context-package integration gate is no longer an existence-only check and no longer depends on a hard-coded PASS runner.

The first executable run demonstrated genuine fail-closed behavior; the corrected runner then passed the same automatic gate.

Canon / Frozen Core v1.2 / active context-package schema: UNCHANGED.

## Newly exposed debt

The failed-run log also supplied direct runtime evidence that GitHub is forcing actions that target Node.js 20 to run under Node.js 24. This becomes Stage E3.3 and is handled separately from the integration-contract repair.
