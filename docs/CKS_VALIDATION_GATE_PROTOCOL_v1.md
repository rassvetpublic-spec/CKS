# Протокол гейта валидации CKS v1 (CKS Validation Gate Protocol v1)

## Назначение (Purpose)

Определяет независимую проверку изменений перед слиянием (`Merge`).

Поток валидации:

```text
Worker (исполнитель)
→ PR (рабочий объект)
→ QA Request (запрос тестирования)
→ QA (независимая верификация)
→ Review Request (запрос ревью)
→ Review (архитектурный аудит)
→ Merge Ready (готовность к слиянию)
→ Merge (слияние)
```

## Роли и ответственность (Roles and Responsibilities)

### Воркер (Worker / Исполнитель)

Ответственность:
- выполнить задачу;
- создать PR;
- подготовить проверяемые доказательства (`Evidence`);
- запросить проведение QA и архитектурного ревью (`Review`).

Запрещено:
- проведение QA собственного PR;
- проведение Review собственного PR;
- подтверждение собственного слияния (`Self-Merge`).

### Контроллер качества (QA Controller)

Проверяет:
- модульные и интеграционные тесты;
- статус рабочих процессов CI;
- отсутствие регрессий;
- соответствие критериям приёмки задачи.

Результат проверки:
- `PASS` (пройдено);
- `FAIL` (ошибка);
- `BLOCKED` (заблокировано).

### Архитектурный ревьюер (Review Controller)

Проверяет:
- архитектурную целостность;
- границы ответственности CKS и KAT9I_OS;
- неизменность инвариантов канона (`Canon`);
- правила управления репозиторием (`Governance`);
- соответствие принципам проекта CKS.

Результат ревью:
- `APPROVED` (одобрено);
- `REQUEST_CHANGES` (требуются изменения);
- `BLOCKED` (заблокировано).

## Принцип независимости (Independence Invariant)

```text
Author PR != QA
Author PR != Review
```

Проверки QA и архитектурное ревью не могут выполняться автором изменения.

## Поля передачи состояния (HANDOFF Fields)

```yaml
QA:
  REQUIRED: true
  REQUESTED: true
  ASSIGNEE: [логин / роль]
  RESULT: PASS | FAIL | BLOCKED

REVIEW:
  REQUIRED: true
  REQUESTED: true
  ASSIGNEE: [логин / роль]
  RESULT: APPROVED | REQUEST_CHANGES | BLOCKED

CHANNEL: GitHub PR conversation
```

## Условия допуска к слиянию (Merge Gate)

Слияние ветки (`Merge`) разрешено строго при выполнении условий:

- `QA = PASS`
- `REVIEW = APPROVED`
- `Evidence = PRESENT`
- `Blockers = NONE`

## Будущее развитие (Future Extensions)

Автоматический контроллер слияния (`Merge Controller`) может быть добавлен в последующих версиях протокола.
