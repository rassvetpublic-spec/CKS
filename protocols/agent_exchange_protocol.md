# Agent Exchange Protocol v1

## Purpose

Defines safe exchange between agents and CKS.

## Flow

Agent receives task artifact.

Agent returns result artifact.

```
CKS -> Agent -> CKS
```

## Rules

- Agent does not own persistent knowledge.
- Agent cannot promote canon directly.
- Results require validation before becoming CKS objects.
