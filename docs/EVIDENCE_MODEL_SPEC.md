# CKS Evidence Model Specification

## Purpose

Evidence is the verification layer of CKS. Knowledge and decisions must reference evidence when they move beyond candidate status.

## Evidence Object

Required fields:

- id
- source
- type
- reference
- created
- related_objects

## Evidence Types

- document
- commit
- issue
- experiment
- external_reference

## Lifecycle

```text
Captured
  ↓
Validated
  ↓
Accepted
  ↓
Archived
```

## Rule

A decision without evidence remains a proposal. A canon object requires validated evidence.
