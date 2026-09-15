# CKS 1.2 Scope

## Purpose

CKS 1.2 is the transition from a knowledge model to controlled integration capabilities.

The goal is not to replace the CKS core, but to add safe interaction layers around the stable knowledge foundation.

## Stable foundation (from Bootstrap 1.0 and CKS 1.1)

Already established:

- Knowledge Object
- Storage model
- Version lifecycle
- References
- Decision Records
- Evidence traceability

These components remain the source of truth.

## Included in CKS 1.2

### Context Passport

Purpose:

- describe external context packages;
- identify origin;
- preserve traceability.

### Worker Manifest

Purpose:

- describe worker capabilities;
- define allowed interactions;
- avoid uncontrolled knowledge writes.

### External Adapter Contract

Purpose:

- connect external systems through validated exchange formats;
- prevent raw context ingestion.

### Import Pipeline

Purpose:

```
External Package
      ↓
Validation
      ↓
Candidate Object
      ↓
CKS Lifecycle
```

## Excluded from CKS 1.2 core

Not part of the mandatory foundation:

- autonomous agents;
- automatic canon promotion;
- knowledge graph platform;
- hidden runtime memory;
- direct context dumps.

## Architecture rule

```
External systems
        ↓
validated artifacts
        ↓
CKS objects
```

Not allowed:

```
External runtime memory
        ↓
CKS storage
```

## Success criteria

CKS 1.2 is complete when:

- external context can be imported safely;
- provenance is preserved;
- existing knowledge lifecycle remains unchanged;
- integrations cannot bypass validation.
