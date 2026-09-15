# CKS 1.2 Implementation Checklist

## Purpose

Минимальный контроль перехода от Discovery к реализации без изменения CORE.

## Matrix

| GAP | Artifact | Test | Workflow | Evidence |
|---|---|---|---|---|
| Semantic validation | validator specification | semantic object test | validation workflow | validation result |
| Lifecycle integration | lifecycle rules | transition test | integration workflow | trace record |
| Traceability | evidence rules | evidence chain test | compliance workflow | source reference |

## Constraints

- CORE remains unchanged.
- Discovery is not Canon.
- Human Gate is required before promotion.
- Runtime state is not stored as knowledge.

## Implementation order

1. Define validation contracts.
2. Add tests.
3. Connect workflows.
4. Review results.
5. Prepare Council decision package.
