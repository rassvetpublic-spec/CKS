# CKS Knowledge Graph Protocol v1

## Purpose

Knowledge Graph слой связывает найденные знания, источники, решения и доказательства.

## Boundary

CKS stores:
- knowledge objects;
- relations;
- evidence;
- decisions;
- history.

KAT9I_OS stores:
- execution;
- agents;
- tools;
- runtime.

## Knowledge Object

```yaml
knowledge_object:
  id: ""
  type: idea|pattern|decision|failure|experiment
  status: raw|reviewed|accepted|archived
  source:
    - issue
    - pr
    - comment
  tags:
    - architecture
    - governance
    - qa
  cluster: ""
```

## Relations

```yaml
relation:
  from: ""
  to: ""
  type: supports|contradicts|extends|duplicates
```

## Cluster

Cluster groups related knowledge objects.

Example:

```yaml
cluster:
  id: "CKS-CLUSTER-001"
  name: "Autonomous Worker System"
  contains:
    - handoff
    - worker-loop
    - validation-gate
    - metrics
```

## Harvester Flow

```
Sources
  |
  v
Harvester
  |
  v
Knowledge Objects
  |
  v
Clusters
  |
  v
Review
  |
  v
Decision
```

## Rules

- Harvester does not modify Canon directly.
- Discovery is separated from approval.
- Every accepted knowledge object keeps source traceability.
- Tags and clusters are metadata, not execution commands.

## Metrics

- discovered objects;
- linked objects;
- duplicate detection;
- evidence coverage;
- traceability.
