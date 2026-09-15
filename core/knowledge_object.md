# Knowledge Object v1

## Purpose

Minimal object model for CKS Bootstrap 1.0.

CKS Bootstrap 1.0 stores knowledge objects. It does not implement graphs, agents, or advanced automation.

## Required fields

- id
- type
- title
- content
- source
- version
- status

## Lifecycle

```
draft
  ↓
accepted
  ↓
archived
```

## Bootstrap rule

A knowledge object is the smallest unit that CKS can create, store, read and version.
