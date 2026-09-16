# CKS GAP Register

## Purpose

Единая точка входа для изменений CKS после v1.2.

Архитектурные изменения не начинаются с идеи. Они начинаются с подтверждённого GAP.

## Lifecycle

```text
GAP
 ↓
Evidence
 ↓
Proposal
 ↓
Decision
 ↓
Minimal Change
```

## Rules

- Нет GAP → нет изменения Core.
- Proposal не является Decision.
- Experiment не является Canon.
- Исторические материалы сохраняются отдельно.

## Current State

```yaml
CKS_v1_2:
  status: archived
  development: gap_driven
  core: frozen
```

## Active GAPs

| ID | Description | Status |
|---|---|---|
| GAP-001 | repository documentation alignment | confirmed |
| GAP-002 | decision traceability | confirmed |
| GAP-003 | evidence to decision links | confirmed |
