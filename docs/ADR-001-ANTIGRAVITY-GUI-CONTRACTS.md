# ADR-001: Antigravity GUI contracts for KAT9I_OS

## Статус

Proposed (предложение)

## Контекст

Antigravity Electron становится визуальным слоем KAT9I_OS.

CKS сохраняет независимость и отвечает за:

- контекст;
- знания;
- решения;
- доказательства;
- историю изменений.

KAT9I_OS отвечает за исполнение и операционные процессы.

## Решение

Вводится граница через контракт событий:

```
KAT9I_OS Runtime
        |
        v
Event Contract
        |
        v
Antigravity GUI Layer
        |
        v
Electron Interface
```

GUI не содержит бизнес-логики исполнения и не становится источником решений.

## Правила

1. CKS не зависит от Electron.
2. Electron получает только подтверждённые состояния.
3. Решения проходят путь:

```
GAP
↓
Evidence
↓
Proposal
↓
Decision
↓
Minimal Change
```

4. UI-состояние не является каноном знаний.

## Следующие этапы

- Event Contract v1;
- State Adapter;
- QA_CONTEXT integration;
- Worker Dashboard.
