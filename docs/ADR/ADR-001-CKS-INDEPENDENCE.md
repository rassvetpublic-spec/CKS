# ADR-001: CKS Independence

## Status

Accepted

## Decision

CKS remains an independent system and repository.

CKS is not a subsystem of KAT9I_OS.

## Context

Knowledge lifecycle and execution lifecycle have different requirements.

Combining them would create coupling between storage, decisions and runtime execution.

## Consequences

Positive:

- CKS can evolve independently.
- CKS can support multiple execution systems.
- KAT9I_OS keeps its own canon.

Negative:

- Integration requires explicit contracts.
- Adoption requires review.

## Rule

External knowledge systems must not automatically become canonical sources.
