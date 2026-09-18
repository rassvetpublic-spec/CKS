# Antigravity Event Contract v1

## Назначение

Контракт обмена состояниями между KAT9I_OS Runtime и GUI-слоем Antigravity.

## События

- SYSTEM_READY
- SYSTEM_IDLE
- TASK_CREATED
- TASK_RUNNING
- TASK_COMPLETED
- TASK_FAILED
- QA_RUNNING
- QA_PASS
- BLOCKED
- MERGE_READY
- EVIDENCE_READY

## Ограничения

GUI может отображать состояние.

GUI не принимает архитектурные решения и не изменяет канон CKS.

## Связь QA

Поддерживается привязка:

QA_CONTEXT = PR_HEAD + BASE_REFERENCE

для отображения проверяемого состояния.
