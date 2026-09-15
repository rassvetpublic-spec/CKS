# CKS 1.1 ADR Model v1

## Purpose

Minimal decision record model for linking knowledge objects with architectural and project decisions.

## Scope

Included:
- decision identity;
- context;
- decision statement;
- source;
- version;
- lifecycle status.

Excluded:
- autonomous decisions;
- agent decisions;
- automatic canon promotion.

## Decision object

```yaml
id:
title:
context:
decision:
source:
version:
status:
```

## Lifecycle

```
draft
  ↓
accepted
  ↓
archived
```
