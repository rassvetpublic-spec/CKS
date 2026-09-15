# CKS Bootstrap Snapshot v0.1

## Назначение

Снимок контекста для восстановления рабочего состояния после удаления чата.

Источник:
- рабочий анализ KAT9I_OS + CKS + Antigravity Manager;
- архитектурные решения, перенесённые в GitHub Issues.

## Системная модель

### CKS

Владелец:
- знания;
- решения;
- альтернативы;
- rationale (обоснование);
- learning history.

CKS не управляет исполнением задач.

### KAT9I_OS

Владелец:
- задачи;
- execution lifecycle;
- Worker;
- QA;
- operational Evidence;
- политика выполнения.

KAT9I не является хранилищем знаний.

### Antigravity Manager

Внешний execution layer:
- аккаунты;
- сессии;
- квоты;
- proxy;
- routing;
- execution capabilities.

KAT9I не владеет секретами и credential lifecycle.

## Главные инварианты

Не создавать внутри KAT9I:

- собственный AccountPool;
- Credential Authority;
- RefreshTokenStore;
- собственный execution scheduler;
- собственный provider routing.

Использовать adapter/control contracts.

## Поток данных

```
CKS
 |
 | Context Artifact / Decision Artifact
 v
KAT9I Context + Policy
 |
 v
Worker Adapter
 |
 v
Antigravity Manager
 |
 v
Provider execution
 |
 v
Execution Evidence
 |
 v
CKS Learning Event
```

## Связанные задачи

- KAT9I_OS #217 — общий план KAT9I v1 + CKS + Antigravity.
- KAT9I_OS #218 — Capability Matrix Antigravity Manager.
- KAT9I_OS #219 — Artifact Contracts.
- #216 — Distillate Pattern.
- #183 — Token Budget Router.
- #177 — RAW knowledge seed.
- #178 — Architecture Tournament.

## Следующие действия

1. Завершить Capability Matrix Antigravity Manager.
2. Создать минимальные Artifact Contracts.
3. Проверить Token Budget Router.
4. Выполнить первый экспериментальный цикл.

## Правило восстановления

Новый рабочий чат должен начинаться с чтения:

1. этого snapshot;
2. KAT9I_OS issues #217-#219;
3. актуальных CKS protocols.

Чат не является источником истины. Источник истины — GitHub + канонические документы.
