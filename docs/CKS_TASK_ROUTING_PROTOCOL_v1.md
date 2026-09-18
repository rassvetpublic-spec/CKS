# Протокол маршрутизации задач и метрик CKS v1 (CKS Task Routing Protocol v1)

## Назначение (Purpose)

Этот документ фиксирует классификацию задач, метрики выполнения и контракт воркера (`Worker`) для CKS.

## Принцип v1

Классификаторы `ABC` и `XYZ` используются для описания задачи и оценки риска.

Они **не** ограничивают выбор модели или исполнителя.

Любой воркер (`Worker`) может взять любую задачу при наличии доступа.

## Классификация задач (Task Classification)

Каждый отчет `HANDOFF` должен содержать:

```yaml
ABC: A|B|C
XYZ: X|Y|Z
COMPLEXITY: 1-10
RISK: LOW|MEDIUM|HIGH|CRITICAL
TOKEN_ESTIMATE: ~
```

## Категории ценности ABC

- **A** — высокая ценность или влияние.
  Примеры: архитектура, `governance` (управление репозиторием), решения `Canon`.
- **B** — стандартные изменения и доработки.
- **C** — потоковые сервисные операции.

## Категории неопределённости XYZ

- **X** — повторяемая задача с понятным детерминированным результатом.
- **Y** — задача со средним уровнем неопределённости.
- **Z** — исследовательская задача (`Research`) или новая архитектура.

## Контракт канала связи (Channel Contract)

Каждый `HANDOFF` обязан содержать:

```yaml
REPOSITORY: full github url
TARGET: issue/pr/branch
CHANNEL: return channel
REPORT_FORMAT: expected report
```

Если `CHANNEL` (канал обратной связи) отсутствует:
Воркер (`Worker`) создаёт комментарий в целевой задаче `GitHub Issue` и фиксирует используемый канал.

## Метрики отчёта воркера (Worker Report Metrics)

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

## Группы метрик (Metric Groups)

### Качество (Quality)

- Покрытие доказательствами (`Evidence Coverage`)
- Трассируемость (`Traceability`)
- Соответствие протоколам (`Protocol Compliance`)

### Затраты (Cost)

- Оценка токенов (`Token Estimate`)
- Фактический расход токенов (`Actual Tokens`)
- Доработка / исправления (`Rework`)

### Поток исполнения (Flow)

- Обнаружено (`Discovered`)
- Взято в работу (`Claimed`)
- Исполняется (`Running`)
- На проверке (`Review`)
- Верифицировано (`Verified`)
- Слито (`Merged`)

## Будущее расширение (Future Extension)

Слой рекомендации моделей (`Model Recommendation Layer`, выбор модели по соответствию требованиям) является отдельной опцией v2.

В v1 автоматического ограничения моделей нет.
