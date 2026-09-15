# CKS Dependency Map

## Core dependencies

Bootstrap 1.0 and CKS 1.1 depend only on internal knowledge models:

```
Knowledge Object
 ↓
Storage
 ↓
Lifecycle
 ↓
Reference
 ↓
Decision
 ↓
Evidence
```

## Future dependencies

CKS 1.2 candidates:

| Area | Depends on |
|---|---|
| Context Passport | artifact provenance |
| Worker Manifest | external execution model |
| Adapter Contract | validated exchange format |
| Import Pipeline | validation layer |
| Advanced Validation | quality rules |
| Promotion Workflow | decision/evidence model |

## Forbidden dependency direction

```
CKS core → external runtime
CKS core → specific agent
CKS core → KAT9I_OS implementation
```

External systems may use CKS, but cannot define the knowledge model.
