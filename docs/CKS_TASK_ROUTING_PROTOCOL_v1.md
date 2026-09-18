# CKS Task Routing Protocol v1

## Назначение

Этот документ фиксирует классификацию задач, метрики выполнения и контракт Worker для CKS.

## Принцип v1

ABC/XYZ используются для описания задачи и оценки риска.

Они НЕ ограничивают выбор модели или исполнителя.

Любой Worker может взять любую задачу при наличии доступа.

## Task Classification

Каждый HANDOFF должен содержать:

```yaml
ABC: A|B|C
XYZ: X|Y|Z
COMPLEXITY: 1-10
RISK: LOW|MEDIUM|HIGH|CRITICAL
TOKEN_ESTIMATE: ~
```

## ABC

A — высокая ценность или влияние.

Примеры:
- архитектура;
- governance;
- Canon решения.

B — стандартные изменения.

C — потоковые операции.

## XYZ

X — повторяемая задача с понятным результатом.

Y — задача со средним уровнем неопределённости.

Z — исследование или новая архитектура.

## Channel Contract

Каждый HANDOFF обязан содержать:

```yaml
REPOSITORY: full github url
TARGET: issue/pr/branch
CHANNEL: return channel
REPORT_FORMAT: expected report
```

Если CHANNEL отсутствует:
Worker создаёт комментарий в целевой GitHub Issue и фиксирует используемый канал.

## Worker Report Metrics

Минимальный отчёт:

```yaml
STATUS: PASS|FAIL|BLOCKED
TASK:
EVIDENCE:
BLOCKERS:
NEXT:
```

Расширенный отчёт:

```yaml
DURATION:
ITERATIONS:
EVIDENCE_COVERAGE:
TRACEABILITY:
PROTOCOL_COMPLIANCE:
TOKEN_ESTIMATE:
ACTUAL_TOKENS:
REWORK:
```

## Metric Groups

### Quality

- Evidence Coverage
- Traceability
- Protocol Compliance

### Cost

- Token Estimate
- Actual Tokens
- Rework

### Flow

- Discovered
- Claimed
- Running
- Review
- Verified
- Merged

## Future Extension

Model Recommendation Layer (выбор модели по соответствию требованиям) является отдельной опцией v2.

В v1 автоматического ограничения моделей нет.
