# CKS v1.3 Knowledge Graph Model

## Purpose

Define the object relationship model for CKS v1.3 research.

## Core objects

- Knowledge Object
- Evidence Record
- Decision Record
- Proposal
- GAP
- Owner
- History Entry

## Relations

```
GAP -> Proposal -> Evidence -> Decision -> Change -> History
```

## Boundary

Research objects cannot become Core objects without Decision Gate.
