# CKS Knowledge Validation Protocol v1

## Purpose

Define the lifecycle from discovered information to validated knowledge.

## Principle

Discovery is not knowledge.

Harvester finds candidates.
Distillation structures candidates.
Review validates meaning.
Decision authority accepts changes.

## Knowledge states

```
RAW
  |
  v
FOUND
  |
  v
STRUCTURED
  |
  v
VALIDATED
  |
  v
CANON
```

## Roles

### Harvester

Can:
- discover sources;
- collect evidence;
- create knowledge objects;
- assign tags.

Cannot:
- approve knowledge;
- modify Canon;
- make final decisions.

### Distiller

Can:
- merge duplicates;
- extract patterns;
- create clusters.

Cannot:
- bypass review.

### Reviewer

Checks:
- evidence quality;
- consistency;
- architecture boundaries;
- conflicts.

## Knowledge Object

```yaml
knowledge_object:
  id:
  source:
  type:
    idea|pattern|decision|failure|experiment
  status:
    raw|found|structured|validated|canon
  evidence:
  tags:
  cluster:
```

## CKS / KAT9I_OS boundary

CKS stores:
- knowledge;
- evidence;
- decisions;
- history.

KAT9I_OS executes:
- agents;
- workflows;
- tools;
- runtime actions.

## Validation gate

Required before Canon:

- evidence exists;
- source traceable;
- review completed;
- conflicts resolved.
