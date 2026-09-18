# Формат отчёта воркера CKS v1 (CKS Worker Report Format v1)

## Назначение (Purpose)

Единый формат ответа воркера (`Worker`) для системы CKS.

Формат имеет два уровня представления:

1. **YAML** — структурированный машинно-читаемый контракт для автоматического обмена между системами.
2. **Human View** — компактный экран состояния для человека и оператора.

## Совместимость с внешними системами (Compatibility)

CKS отвечает за контракт задачи, контекст, доказательства (`Evidence`) и архитектурные решения.

KAT9I_OS выступает внешним исполнительным слоем:
- тело и инструкции агента;
- инструменты исполнения;
- рабочие процессы (`Workflows`);
- среда выполнения (`Runtime`).

## Машинный контракт YAML (YAML Contract)

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

## Экранное представление для человека (Human Worker View)

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

## Правила оформления (Rules)

- Полоса прогресса визуализирует величину показателя.
- Значение `UNKNOWN` не приравнивается к нулю.
- Проверки QA и архитектурное ревью независимы от автора изменения.
- Воркер (`Worker`) не выполняет QA и ревью собственного PR.
- Если канал отчёта не указан, создаётся комментарий в целевом обсуждении `GitHub Issue / PR`.

## Значения статусных индикаторов (Status Icons)

- 🟢 `PASS` / `DONE` — успешно пройдено / завершено
- 🟡 `IN_PROGRESS` / `WAITING` — в процессе / ожидание
- 🔴 `BLOCKED` / `FAIL` — заблокировано / ошибка
- ⚪ `UNKNOWN` — не определено
- 🟣 `REVIEW` — на архитектурном ревью
