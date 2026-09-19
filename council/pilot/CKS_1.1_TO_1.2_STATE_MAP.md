# CKS 1.1 → CKS 1.2 State Map

Status: Discovery document

## Purpose

Describe allowed evolution paths without performing promotion.

## State model

| Current | Next | Automatic |
|---|---|---|
| Release Candidate | Stable review | No |
| Council draft | Human Gate review | No |
| Discovery artifact | Discovery artifact | Yes |
| Discovery artifact | Canon | No |
| Draft decision | Accepted decision | No |

## Protected boundaries

- CORE remains frozen.
- Knowledge storage does not become execution storage.
- Runtime state remains external.
- Technical validation is not owner approval.
- Rejected alternatives remain part of history.

## Current observed state

CKS 1.1:
- Council v0.1 technical preparation complete.
- Release status discrepancy remains unresolved by design.

CKS 1.2:
- Discovery artifacts prepared.
- Promotion not performed.

## Allowed automatic work

- validation
- audit
- documentation
- evidence indexing

## Human Gate required

- acceptance
- rejection
- promotion
- merge
