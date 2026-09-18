# CKS Worker Report Format v1

## Purpose

Единый формат ответа Worker для CKS.

Формат имеет два уровня:

1. YAML — машинный обмен между системами.
2. Human View — компактный экран состояния для человека.

## Compatibility

CKS хранит контракт задачи, контекст, доказательства и решения.

KAT9I_OS остаётся внешним исполнительным слоем:
- агент;
- инструменты;
- workflow;
- runtime.

## YAML Contract

```yaml
task:
  id: ""
  version: "v1"
  repository: ""
  intent: ""
  objective: ""

classification:
  abc: "A|B|C"
  xyz: "X|Y|Z"
  complexity: 1
  risk: "LOW|MEDIUM|HIGH|CRITICAL"

compatibility:
  cks_contract: "v1"
  kat9i_os_compatible: true
  breaking_change: false

handoff:
  channel: ""
  report_format: "worker_report_v1"

execution:
  status: "DISCOVERED|CLAIMED|RUNNING|DONE|BLOCKED"

metrics:
  evidence_coverage: 0
  traceability: 0
  protocol_compliance: 0
  token_estimate: ""

validation:
  qa:
    required: true
    requested: false
    result: "WAITING"
  review:
    required: true
    requested: false
    result: "WAITING"

result:
  status: "PASS|FAIL|BLOCKED"
  evidence: []
  blockers: []
  next_action: ""
```

## Human Worker View

```text
🤖 CKS WORKER REPORT

TASK:

📌 Classification
ABC: A/B/C
XYZ: X/Y/Z
Complexity: 1-10
Risk: LOW/MEDIUM/HIGH/CRITICAL

⚙️ Execution
Status:
Progress:

📊 Metrics
Evidence Coverage:
Traceability:
Protocol Compliance:

🔍 Validation
QA:
Review:

📦 Result
STATUS:
Evidence:
Blockers:
Next:
```

## Rules

- Полоса показывает величину показателя.
- UNKNOWN не считается нулём.
- QA и Review независимы от автора изменения.
- Worker не выполняет QA своего PR.
- Если канал отчёта отсутствует, создаётся комментарий в целевом Issue/PR.

## Status Icons

🟢 PASS / DONE
🟡 IN PROGRESS / WAITING
🔴 BLOCKED / FAIL
⚪ UNKNOWN
🟣 REVIEW
