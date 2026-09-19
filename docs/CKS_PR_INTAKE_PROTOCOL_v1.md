# Протокол приёма pull-реквестов CKS v1 (CKS PR Intake Protocol v1)

## Назначение (Purpose)

Определение порядка обработки pull-реквестов (`PR`), созданных без связанной задачи (`Issue`).

Работа, начатая с PR (`PR-first`), должна входить в тот же жизненный цикл, что и работа, начатая с задачи (`Issue-first`).

## Потоки исполнения (Flows)

### Начало с задачи (Issue-first)

```text
Issue → HANDOFF → Worker → PR → Decision → Merge
```

### Начало с PR (PR-first)

```text
PR → PR Intake → Связанная Issue → HANDOFF → Worker → Decision → Merge
```

## Обработка PR без связанной Issue (PR without Issue)

Если PR не имеет исходной задачи:

1. Создать задачу приёма PR (`PR Intake Issue`).
2. Связать PR и созданную Issue.
3. Добавить метаданные передачи состояния `HANDOFF`.
4. Классифицировать задачу (по шкале `ABC/XYZ`, сложности и риску).
5. Продолжить работу по стандартному жизненному циклу ревью.

## Шаблон приёма PR (PR Intake Template)

```md
# PR Intake

SOURCE:
Pull Request #

REPOSITORY:
https://github.com/rassvetpublic-spec/CKS

TYPE:
PR-first

PURPOSE:
-

CLASSIFICATION:

ABC:
-

XYZ:
-

COMPLEXITY:
-

RISK:
-

CHANNEL:
GitHub Issue conversation

REPORT FORMAT:
STATUS:
EVIDENCE:
BLOCKERS:
NEXT:
```

## Метрики (Metrics)

Обязательные показатели:

- Сложность (`Complexity`)
- Риск (`Risk`)
- Классификатор `ABC/XYZ`
- Покрытие доказательствами (`Evidence coverage`)
- Трассируемость (`Traceability`)
- Соответствие протоколам (`Protocol compliance`)

## Политика моделей (Model Policy)

Выбор конкретной модели остаётся опциональным.

Любой воркер (`Worker`) может взять любую задачу при наличии доступа.

Рекомендация моделей (`Model Recommendation`) выделена в отдельную функциональность v2.
