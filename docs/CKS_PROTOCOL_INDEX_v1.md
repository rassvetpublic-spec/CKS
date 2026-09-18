# CKS Protocol Index v1

## Purpose

Unified map of CKS lifecycle protocols.

CKS stores knowledge, context, evidence, decisions and history.
Execution remains external and compatible with KAT9I_OS.

## Lifecycle

```
TASK CONTRACT
      |
      v
HANDOFF
      |
      v
WORKER LOOP
      |
      +---- QA
      |
      +---- REVIEW
      |
      v
VALIDATION GATE
      |
      v
MERGE DECISION
      |
      v
KNOWLEDGE GRAPH
      |
      v
DISTILLATION
      |
      v
KNOWLEDGE OBJECT
```

## Protocol layers

| Layer | Purpose |
|---|---|
| Task Contract | stable task definition |
| Handoff | transfer between actors |
| Worker Report | execution result format |
| Task Routing | classification and metrics |
| Validation Gate | QA and Review separation |
| PR Intake | direct PR tracking |
| Harvester | discovery of hidden knowledge |
| Knowledge Graph | relations between objects |
| Distillation | raw knowledge transformation |

## Boundary

CKS:
- what
- why
- context
- evidence
- decisions

KAT9I_OS:
- who
- how
- tools
- workflow
- runtime

## Rules

- Worker cannot QA own PR.
- Worker cannot Review own PR.
- Harvester cannot modify Canon directly.
- Distillation creates candidates, not final decisions.
- Protocol changes require versioning.
