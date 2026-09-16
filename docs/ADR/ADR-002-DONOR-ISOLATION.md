# ADR-002: Donor Isolation Principle

## Status

Accepted

## Decision

External research projects can provide ideas, patterns and experiments, but cannot directly change the canon of the receiving system.

## Adoption pipeline

```text
Idea
 ↓
Research
 ↓
Audit
 ↓
ABC/XYZ evaluation
 ↓
Decision
 ↓
Canon update (only if accepted)
```

## Reason

This prevents accidental transfer of experimental assumptions into production systems.

## Scope

Applies to:

- CKS integrations;
- KAT9I_OS references;
- future donor projects.
