# CKS Post-Snapshot Integrity Audit — Stage E3.2-C2F2-A

Date: 2026-09-17
Status: ANALYSIS COMPLETE
Scope: KAT9I_OS -> CKS context-package integration contract

## PREV-VERIFY

Verified `main` before this pass. The latest completed checkpoint was E3.2-C2F1 (`db5d0e5f...`), after removal of the redundant Release Check workflow. E1/E2 were not repeated. Canon and Frozen Core v1.2 were not modified.

## SSOT used in this pass

The repository `main` branch remains the project SSOT.

Active contract evidence:

- `docs/registry/CKS_SCHEMA_REGISTRY_v1.md` marks `schemas/context_package_kat9i_v1.yaml` as **active** and describes it as the special exchange contract.
- `schemas/context_package_kat9i_v1.yaml` declares the context-package fields:
  - `id: string`
  - `source_system: KAT9I_OS`
  - `source_reference: string`
  - `created_at: datetime`
  - `split_mode: string`
  - `artifacts: []`
- the same schema declares:
  - `raw_runtime_state: false`
  - `raw_chat_dump: false`
  - `requires_validation: true`
- `docs/CONTEXT_SPLIT_MODES.md` defines the supported split modes:
  - `SPLIT`
  - `AUDIT`
  - `REVIEW`
  - `RESEARCH`
  - `MIGRATION`
  - `CLEANUP`
  - `MERGE`
  - `CANON CHECK`
- `adapters/kat9i_os_adapter.md` requires structured artifacts only and forbids importing raw runtime memory.
- `adapters/kat9i_mapping_rules.yaml` rejects `raw_runtime_state`, `hidden_memory` and `direct_canon_update`.
- `adapters/exchange_mapping.yaml` fixes the context-package source as `KAT9I_OS`, target as `CKS`, and requires validation.
- `adapters/adapter_validation.md` requires adapter validation before creation of a CKS object and rejects raw memory.
- `protocols/ingestion_protocol.md` states that raw context is not a knowledge object and promoted objects require source and validation.
- `core/ADAPTER_BOUNDARY_RULE.md`, ADR-001 and ADR-002 prohibit bypassing the CKS decision/evidence boundary and prohibit automatic Canon adoption from an external system.

## Proven contract for the validator

The next implementation pass may safely enforce only requirements already supported by the active repository contract:

1. Input must be a mapping/dictionary.
2. All six fields declared by the active KAT9I context-package contract must be present.
3. `id` is a string.
4. `source_system` must equal `KAT9I_OS`.
5. `source_reference` is a string.
6. `created_at` must represent a datetime value; the contract does not define a narrower timezone policy.
7. `split_mode` must be one of the modes explicitly listed as supported by `docs/CONTEXT_SPLIT_MODES.md`.
8. `artifacts` must be a list. The active contract does **not** prove that the list must be non-empty, therefore empty lists must not be rejected merely by assumption.
9. A package carrying prohibited raw/runtime indicators must be rejected when those indicators request/import prohibited material:
   - truthy `raw_runtime_state`;
   - truthy `raw_chat_dump`;
   - truthy `hidden_memory`;
   - `type: raw_context_dump` as represented by the existing negative integration fixture.
10. A request for `direct_canon_update` must be rejected.
11. Unknown extra metadata must not be rejected without a contract rule; the current YAML is a lightweight contract, not a formal `additionalProperties: false` schema.
12. Validation must not itself promote data into Canon/Core.

## Important inconsistency found

`examples/kat9i_os_import/context_package.yaml` is stale relative to the active KAT9I exchange contract:

- it uses `source` instead of `source_system`;
- it lacks `source_reference`, `created_at` and `artifacts`;
- it uses `CONTEXT_SPLIT`, while the active supported-mode document lists `SPLIT` rather than `CONTEXT_SPLIT`.

Therefore the example must **not** be used as the source of truth for validator behavior. It is recorded as migration/documentation debt and should be corrected only after the validator is protected by tests.

## Existing integration weakness reconfirmed

- `scripts/import_context_package.py` validates only the presence of `id`, `source_system` and `artifacts`.
- `.github/workflows/cks-integration-test.yml` checks only that the schema and importer files exist.
- `scripts/run_integration_tests.py` currently returns a hard-coded PASS result and therefore is not evidence of an executed integration test.

## Decision for C2F2-B/C

C2F2-B will strengthen the importer and add direct regression tests against the proven contract above.

C2F2-C will replace the existence-only workflow behavior with execution of those tests and will add focused push/PR path triggers so changes to the contract, validator, adapter boundary or tests cannot silently bypass the integration gate.

No schema, Canon or Frozen Core change is authorized or required by this finding.
