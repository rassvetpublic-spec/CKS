# Antigravity Worker Dashboard Contract v1

## Назначение

Контракт отображения состояния worker-процессов KAT9I_OS в GUI Antigravity.

## Граница ответственности

Worker и KAT9I_OS являются источником состояния.

Antigravity GUI только отображает подтверждённое состояние.

CKS хранит знания, решения, доказательства и историю изменений.

## Модель данных

```
KAT9I_OS Runtime
        |
        v
Worker State Adapter
        |
        v
Event Contract
        |
        v
Antigravity Dashboard
```

## Состояния worker

- CREATED
- QUEUED
- RUNNING
- WAITING
- BLOCKED
- COMPLETED
- FAILED

## Ограничения

GUI не меняет состояние worker напрямую.

Любое изменение проходит через исполнительный слой KAT9I_OS.

## Связь QA_CONTEXT

Для отображения проверяемого состояния используется:

```
QA_CONTEXT = PR_HEAD + BASE_REFERENCE
```

## Будущие расширения

- очередь задач;
- метрики выполнения;
- история запусков;
- визуализация доказательств.
