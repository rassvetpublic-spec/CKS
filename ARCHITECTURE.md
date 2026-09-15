# CKS Architecture v1

## Purpose

CKS is an independent Context Knowledge System.

## Storage separation

CKS may contain storage adapters and repositories, but KAT9I_OS remains an execution system, not a knowledge database.

## Core

```
CKS
├── core
├── modes
├── schemas
├── protocols
├── adapters
├── knowledge
├── decisions
├── graveyard
└── evidence
```

## Integration

Communication with KAT9I_OS happens through artifact contracts and schemas.

No direct internal dependency.
