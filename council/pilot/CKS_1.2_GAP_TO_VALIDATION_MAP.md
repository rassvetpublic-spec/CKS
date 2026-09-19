# CKS 1.2 Gap to Validation Map

## Purpose

Map identified CKS 1.2 gaps to existing mechanisms and required validation coverage.

## GAP-001 Semantic Validation Layer

Existing:
- schemas
- protocols
- workflows

Required validation:
- object semantics
- allowed state transitions
- prohibited field checks

## GAP-002 Lifecycle Integration Coverage

Flow:

Proposal
→ Review
→ Evidence
→ Decision
→ Knowledge / Graveyard

Required validation:
- every transition has evidence
- rejected objects remain separated from active knowledge

## GAP-003 Traceability Automation

Flow:

Object
→ Evidence
→ Source
→ Validation Result

Required validation:
- provenance completeness
- source linkage
- validation record preservation

## Implementation Boundary

This document is discovery material only.

Rules:
- CORE unchanged
- Canon unchanged
- no automatic promotion
- Human Gate remains required
