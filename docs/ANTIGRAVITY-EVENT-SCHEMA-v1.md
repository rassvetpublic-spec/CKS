# Antigravity Event Schema v1

## Назначение

Описание событийного слоя между KAT9I_OS Runtime и Antigravity GUI.

## Событие

Каждое событие содержит:

```
event
 ├── type
 ├── timestamp
 ├── source
 ├── payload
 └── evidence_reference
```

## Базовые события

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

Event Contract передаёт состояние.

Он не передаёт:

- решения CKS;
- внутреннюю логику worker;
- изменение канона.

## Расширение

Новые события добавляются только через:

```
GAP
↓
Evidence
↓
Proposal
↓
Decision
```
