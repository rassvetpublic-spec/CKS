# CKS v1.3 Knowledge Object Contract

## Purpose
Formal contract for all managed knowledge objects.

Required fields:

- id
- type
- status
- owner
- lifecycle
- relations
- evidence
- history

Object lifecycle:

Research -> Review -> Active -> Superseded -> Archived

Rules:

- Every object has a stable identifier.
- Canon objects require evidence and decision links.
- Research objects cannot directly modify Core.
