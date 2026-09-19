# CKS 1.2 Validation Coverage Matrix

## Purpose

Map existing CKS mechanisms to semantic validation coverage.

## Validation chain

```
Workflow
  -> Protocol
  -> Schema
  -> Validator
  -> Test
```

## Coverage

| Area | Existing layer | Validation target |
|---|---|---|
| Knowledge | knowledge/ | acceptance and provenance checks |
| Evidence | evidence/ | traceability checks |
| Decisions | decisions/ | lifecycle checks |
| Graveyard | graveyard/ | rejection lifecycle checks |
| Protocols | protocols/ | execution consistency |
| Workflows | .github/workflows/ | automation coverage |

## Current gaps

- Semantic validation implementation is separate from structural checks.
- Lifecycle integration tests need explicit mapping.
- Evidence linkage needs automated verification.

## Constraints

- CORE remains unchanged.
- Discovery artifacts are not canon.
- Human Gate remains required for promotion.
