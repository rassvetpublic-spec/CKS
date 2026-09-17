# CKS Post-Snapshot Integrity Audit — Stage E3.4 FINAL

Date: 2026-09-17
Status: **VERIFIED / CLOSED**
Repository SSOT: `rassvetpublic-spec/CKS`, branch `main`
Functional verification head: `6ec4945f890ae6c1815d27511be6dc5dfa4ba0a1`

## Scope and invariant

This checkpoint closes the post-snapshot integrity chain through E3.4. E1 and E2 were retained as previously verified and were not needlessly re-run as separate audit stages. Their protected regression surfaces continued to execute inside the later runtime/compatibility checks where applicable.

Throughout E3, Canon and Frozen Core v1.2 were not modified.

## Closed chain

### E3.1 — workflow inventory

All 17 workflows present at the start of E3.1 were inventoried in three passes. The inventory found:

- Bootstrap false-green exit semantics;
- Control Plane false-green exit semantics;
- missing `tools/cks_ci.py` dependency trigger in the knowledge-runtime integral workflow;
- shallow and duplicate workflow surfaces requiring separate analysis.

### E3.2 — structural and integration repairs

Completed and verified:

1. `scripts/validate_bootstrap.py` now fails closed with a non-zero exit code on validation failure.
2. `validators/control_plane_validator.py` now fails closed with a non-zero exit code on validation failure.
3. Direct regression coverage protects both exit-semantic repairs and is wired into their workflows.
4. `tools/cks_ci.py` is present in both push and pull-request path triggers for `cks-knowledge-runtime-intelligence.yml`.
5. Redundant `cks-preflight.yml` was removed after proving it was a strict subset with no required-status dependency.
6. Redundant `cks-release-check.yml` was removed after proving it was a strict subset of Knowledge Check.
7. KAT9I_OS -> CKS context-package validation was rebuilt against the active repository contract.
8. The integration runner no longer returns a hard-coded PASS: it executes real tests, fails on zero discovered tests and propagates test failures through process exit status.
9. The first executable Integration Test correctly failed on a real unittest-discovery defect, proving fail-closed behavior; the defect was repaired and the automatic gate then passed.
10. The stale KAT9I repository example was aligned with the active contract and is now itself validated by the executable integration suite.
11. The Integration Test workflow watches the schema, importer, runner, adapters, relevant contract documentation, regression test and repository example on both push and pull request.

Latest integration-surface verification head: `e224bd24c7183f13250da5b95d34a38b5339d968`.

Automatic Integration Test run: `35172013962` — SUCCESS.

No integration-surface file was changed after that head during E3.4; therefore the path-filtered Integration Test was correctly not re-triggered by the final E3.4-only validation wiring.

### E3.3 — GitHub Actions Node.js runtime debt

The GitHub runner exposed concrete Node.js-20 deprecation warnings. The repository was migrated with the minimum selected Node.js-24 action majors:

- `actions/checkout@v4` -> `actions/checkout@v5`;
- `actions/setup-python@v5` -> `actions/setup-python@v6`;
- `actions/upload-artifact@v4` -> `actions/upload-artifact@v6`.

Migration head: `2d268b032966ada64a917ee5c8ce4d6d8984f4e4`.

A permanent regression guard now scans all workflow YAML files and fails if any retired Node.js-20 major returns. The guard is wired into `CKS Validation`.

Compatibility evidence after migration includes successful automatic runs of:

- Integration Test — `35171200158`;
- v1.4 Validation — `35171200220`;
- v1.6 Intelligence Runtime — `35171200230`;
- full Knowledge Runtime & Intelligence — `35171200175`.

### E3.4 — final post-snapshot regression

Added `tests/test_cks_post_snapshot_final_regression_stage_e3_4.py` and wired it into the main `CKS Validation` workflow.

The final meta-regression protects the combined E3 invariants:

- workflow inventory remains at 15 after intentional removal of Preflight and Release Check;
- removed duplicate workflows do not return;
- Bootstrap and Control Plane fail-closed repairs remain in place and their direct regression is still wired;
- KAT9I Integration Test executes the real runner and watches the complete proven contract surface;
- the real KAT9I repository example still passes the active validator;
- `tools/cks_ci.py` remains in both knowledge-runtime dependency trigger surfaces;
- Node.js-20 GitHub Action majors do not return;
- the Node.js-24 regression guard remains wired into main validation.

E3.4 implementation head:

`6ec4945f890ae6c1815d27511be6dc5dfa4ba0a1`

## Final automatic CI evidence on E3.4 head

Eight automatic push workflows ran on `6ec4945f890ae6c1815d27511be6dc5dfa4ba0a1`; all completed successfully and no failure or in-progress run remained:

- CKS Validation — `35172291306` — SUCCESS;
- CKS Bootstrap Check — `35172291219` — SUCCESS;
- CKS Knowledge Check — `35172291187` — SUCCESS;
- CKS Control Plane Validation — `35172291331` — SUCCESS;
- CKS Runtime Governance — `35172291352` — SUCCESS;
- CKS Boundary Check — `35172290906` — SUCCESS;
- CKS Traceability Check — `35172291002` — SUCCESS;
- CKS Canon Evidence Guard — `35172290879` — SUCCESS.

The `CKS Validation` job explicitly completed all of these steps successfully:

1. `actions/checkout@v5`;
2. `actions/setup-python@v6`;
3. `Guard GitHub Actions Node.js 24 migration`;
4. `Run E3.4 final post-snapshot regression`;
5. `Validate CKS structure and contracts` (`tools/cks_ci.py --mode all`);
6. validation report upload through `actions/upload-artifact@v6`.

The Runtime Governance job on the same head also completed all substantive steps successfully, including syntax checks, knowledge JSON-schema validation, runtime-core integration tests, stages 2–4, CKS self-audit and governance-runner validation.

## Retained workflow surfaces — not classified as false-green defects

The final review intentionally retains the following overlaps because they currently expose different operational trigger interfaces. They are governance/maintenance debt, not evidence of a broken validation result:

- `cks-compliance.yml` and `cks-knowledge-check.yml` both perform shallow structure-existence checks, but have different trigger interfaces;
- `cks-review-gate.yml` and `cks-boundary-check.yml` both invoke `tools/cks_ci.py --mode review-gate`, but expose different trigger interfaces;
- `cks-governance-runner.yml` remains PR/manual only rather than an ordinary push-to-main workflow.

Any consolidation of these interfaces should be a separate cleanup decision, not silently folded into integrity repair.

## Repository-governance debt outside this audit scope

During E3.2 dependency analysis, `main` was observed as unprotected and no required status checks were configured; repository rulesets were empty. This audit did not change branch-protection policy.

That remains an explicit future governance task because enabling required checks changes repository operating policy rather than repairing the validator implementation itself.

## Final result

**Post-snapshot integrity audit E1–E3.4: CLOSED.**

The audited system now has:

- fail-closed validation where false-green behavior was found;
- executable rather than existence-only KAT9I integration validation;
- regression protection for the active KAT9I exchange boundary;
- removal of two proven redundant workflow gates;
- repaired dependency-trigger coverage;
- Node.js-24-compatible GitHub Actions with regression protection;
- a final E3 meta-regression wired into the main validation gate;
- persistent repository checkpoints/index/current-work documents so the audit can be recovered without chat memory.

Canon / Frozen Core v1.2: **UNCHANGED**.
