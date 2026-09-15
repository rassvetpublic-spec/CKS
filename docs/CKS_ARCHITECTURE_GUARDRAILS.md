# CKS Architecture Guardrails

## Core rule

CKS stores knowledge. External systems use references and validated artifacts.

## Allowed

- Knowledge Objects
- References
- Decision Records
- Evidence
- Version history

## Not allowed in core

- Runtime state
- Agent memory
- Direct chat dumps
- External execution logic
- Platform-specific dependencies

## KAT9I_OS boundary

```
KAT9I_OS
= execution layer

CKS
= knowledge layer
```

KAT9I_OS integration must happen through contracts, not by embedding runtime behavior into CKS.

## Extension rule

Every new subsystem must answer:

1. Does it protect or extend knowledge?
2. Does it create external dependency?
3. Can it be delayed?

If the answer increases platform complexity without improving the knowledge lifecycle, defer it.
