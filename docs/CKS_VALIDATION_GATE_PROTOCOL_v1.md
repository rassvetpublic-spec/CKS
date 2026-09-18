# CKS Validation Gate Protocol v1

## Назначение

Определяет независимую проверку изменений перед merge.

Поток:

Worker
→ PR
→ QA Request
→ QA
→ Review Request
→ Review
→ Merge Ready
→ Merge

## Роли

### Worker

Ответственность:
- выполнить задачу;
- создать PR;
- подготовить evidence;
- запросить QA и Review.

Запрещено:
- QA собственного PR;
- Review собственного PR;
- подтверждение собственного merge.

### QA

Проверяет:
- тесты;
- CI;
- регрессии;
- соответствие требованиям.

Результат:
- PASS;
- FAIL;
- BLOCKED.

### Review

Проверяет:
- архитектуру;
- границы CKS;
- Canon;
- governance;
- соответствие принципам проекта.

Результат:
- APPROVED;
- REQUEST CHANGES;
- BLOCKED.

## Независимость

Author PR != QA
Author PR != Review

QA и Review не могут выполняться автором изменения.

## Handoff поля

QA:
- REQUIRED
- REQUESTED
- ASSIGNEE
- RESULT

REVIEW:
- REQUIRED
- REQUESTED
- ASSIGNEE
- RESULT

CHANNEL:
GitHub PR conversation

## Merge Gate

Merge разрешён только если:

QA = PASS
REVIEW = APPROVED
Evidence = PRESENT
Blockers = NONE

## Future

Автоматический Merge Controller может быть добавлен позже.
