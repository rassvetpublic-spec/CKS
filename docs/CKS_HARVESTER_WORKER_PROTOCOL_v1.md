# CKS Harvester Worker Protocol v1

## Purpose

Harvester Worker is a knowledge discovery worker.

It does not replace Executor, QA, Review or Governance roles.

Mission:
- find hidden knowledge;
- recover lost ideas;
- connect existing evidence;
- create knowledge objects for review.

## Boundary

CKS stores:
- intent;
- context;
- evidence;
- decisions;
- history.

KAT9I_OS stores:
- execution;
- agents;
- tools;
- workflows;
- runtime.

Harvester must not create execution dependencies inside CKS.

## Worker Roles

```text
Executor
- changes system

QA
- verifies quality

Review
- verifies meaning and architecture

Harvester
- discovers and structures knowledge

Controller
- coordinates flow
```

## Sources

Harvester may inspect:

- open and closed Issues;
- pull requests;
- comments;
- rejected ideas;
- research notes;
- historical documents;
- worker reports.

## Knowledge Objects

```yaml
knowledge_object:
  id: ""
  source: ""
  type: "idea|pattern|decision|failure|experiment"
  status: "raw|reviewed|accepted|archived"
  tags: []
  cluster: ""
  evidence: []
```

## Clusters

Clusters group related knowledge objects.

Example:

```yaml
cluster:
  id: "CKS-CLUSTER-001"
  name: "Autonomous Worker System"
  contains:
    - HANDOFF
    - Worker Loop
    - KPI
    - Validation Gate
```

## Tags

Required tag dimensions:

```yaml
tags:
  domain:
    - architecture
    - governance
    - qa
    - automation
    - research

  type:
    - idea
    - decision
    - pattern
    - failure
    - experiment

  status:
    - raw
    - reviewed
    - accepted
    - archived
```

## Rules

Harvester:

- may discover;
- may classify;
- may link;
- may propose.

Harvester cannot:

- promote findings directly to Canon;
- approve own discoveries;
- merge changes without validation.

## Report Format

```yaml
harvester_report:
  status: "DONE|BLOCKED"
  sources_checked: []
  objects_found: 0
  clusters_found: 0
  duplicates_found: 0
  evidence_links: []
  review_required: true
```

## Metrics

```text
Discovery Coverage
████████░░

Knowledge Linking
██████░░░░

Duplicate Detection
████░░░░░░

Evidence Quality
████████░░
```

## Compatibility

CKS Contract:
v1

KAT9I_OS compatibility:
YES

Execution layer:
EXTERNAL

Model routing:
OPTIONAL FUTURE
