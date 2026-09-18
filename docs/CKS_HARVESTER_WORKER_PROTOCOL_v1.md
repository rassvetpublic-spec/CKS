# Протокол воркера-сборщика знаний CKS v1 (CKS Harvester Worker Protocol v1)

## Назначение (Purpose)

Воркер-сборщик знаний (`Harvester Worker`) отвечает за обнаружение, извлечение и структурирование скрытого знания.

Он не заменяет роли Исполнителя (`Executor`), Тестировщика (`QA`), Архитектурного ревьюера (`Review`) или Управления (`Governance`).

Миссия сборщика:
- выявление скрытых знаний;
- восстановление утерянных идей и контекста;
- связывание существующих доказательств (`Evidence`);
- формирование объектов знаний (`Knowledge Objects`) для последующего ревью.

## Границы ответственности (Boundary)

CKS хранит:
- намерения и цели (`Intent`);
- контекст (`Context`);
- доказательства (`Evidence`);
- решения (`Decisions`);
- историю изменений (`History`).

KAT9I_OS отвечает за:
- исполнение (`Execution`);
- тела агентов (`Agents`);
- инструменты (`Tools`);
- рабочие процессы (`Workflows`);
- среду выполнения (`Runtime`).

Сборщик (`Harvester`) не должен создавать исполнительных зависимостей внутри CKS.

## Роли воркеров (Worker Roles)

```text
Executor (Исполнитель)
- вносит изменения в систему

QA (Контроллер качества)
- проверяет техническое качество и тесты

Review (Архитектурный ревьюер)
- проверяет смысл, границы и архитектуру

Harvester (Сборщик знаний)
- обнаруживает и структурирует знания

Controller (Координатор)
- координирует общий поток задач
```

## Источники знаний (Sources)

Сборщик может анализировать:

- открытые и закрытые задачи `Issue`;
- pull-реквесты (`PR`);
- комментарии к обсуждениям;
- отвергнутые идеи и кладбище гипотез (`Graveyard`);
- исследовательские заметки (`Research Notes`);
- исторические документы;
- отчёты воркеров (`Worker Reports`).

## Объекты знаний (Knowledge Objects)

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

## Кластеры знаний (Clusters)

Кластеры объединяют тематически связанные объекты знаний.

Пример:

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

## Теги и категории (Tags)

Обязательные измерения классификации:

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

## Правила работы (Rules)

Сборщик (`Harvester`):

- может обнаруживать (`discover`);
- может классифицировать (`classify`);
- может связывать (`link`);
- может предлагать (`propose`).

Сборщику запрещено:

- напрямую повышать найденные элементы до Канона (`Canon`);
- самостоятельно утверждать собственные находки;
- выполнять слияние изменений без прохождения валидационных гейтов.

## Формат отчёта сборщика (Report Format)

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

## Метрики эффективности (Metrics)

- Покрытие поиска (`Discovery Coverage`)
- Связывание знаний (`Knowledge Linking`)
- Обнаружение дубликатов (`Duplicate Detection`)
- Качество доказательств (`Evidence Quality`)

## Совместимость (Compatibility)

- Контракт CKS: `v1`
- Совместимость с KAT9I_OS: `YES`
- Исполнительный слой: `EXTERNAL` (внешний)
- Маршрутизация моделей: `OPTIONAL FUTURE` (опционально в v2)
