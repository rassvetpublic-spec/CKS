# Graveyard Distillation — Chat Session 2026-09-15

## Назначение

Этот файл сохраняет не только принятые решения, но и отброшенные варианты из архитектурного обсуждения KAT9I_OS + CKS + Antigravity Manager.

Цель: после удаления рабочего чата сохранить причины решений и не потерять исследовательский контекст.

---

# 1. Принятый архитектурный канон

## CKS

Владеет:

- знаниями;
- решениями;
- альтернативами;
- обоснованиями (rationale);
- историей обучения.

CKS не управляет исполнением.

## KAT9I_OS

Владеет:

- задачами;
- Worker lifecycle;
- QA;
- execution lifecycle;
- operational Evidence;
- политикой выполнения.

## Antigravity Manager

Внешний execution layer.

Владеет:

- аккаунтами;
- сессиями;
- квотами;
- proxy/routing возможностями;
- механизмами выполнения.

---

# 2. Отвергнутые варианты

## Собственный Token Manager внутри KAT9I

Статус: REJECTED

Не создавать:

- RefreshTokenStore;
- Credential Authority;
- AccountPool.

Причина:

создаёт второй источник состояния и смешивает control plane с execution layer.

---

## Полный Rust rewrite Antigravity Manager

Статус: GRAVEYARD

Причина:

нет доказанного функционального разрыва.

Возврат возможен только после Capability Matrix и реального эксперимента.

---

## Собственный Proxy Layer KAT9I

Статус: отложено.

Причина:

сначала использовать возможности внешнего Manager.

---

## Объединение CKS и KAT9I в один репозиторий

Статус: REJECTED.

Причина:

разные зоны ответственности.

---

# 3. Рассмотренные архитектуры

## Вариант A

KAT9I как полноценная AI OS.

Отклонён: слишком много ответственности.

## Вариант B

Тонкий control plane + внешние execution backends.

Текущий кандидат.

## Вариант C

Event-driven runtime.

Оставлен для исследования.

## Вариант D

Общее blackboard/shared state хранилище.

Отклонено.

Причина: риск потери владельца данных.

---

# 4. Поток знаний и исполнения

```
CKS
 ↓
Decision / Context Artifact
 ↓
KAT9I Policy
 ↓
Worker Adapter
 ↓
Antigravity Manager
 ↓
Execution
 ↓
Evidence
 ↓
CKS Learning Event
```

---

# 5. Следующие эксперименты

Приоритет A/X:

- Capability Matrix Antigravity Manager;
- Artifact Contracts;
- Context Packet;
- Token Budget Policy.

Приоритет A/Y:

- Manager Adapter;
- Decision mapping;
- Feedback loop.

Приоритет C/Z:

- собственный runtime;
- собственный credential слой;
- переписывание Manager.

---

# 6. Точки восстановления

Основные источники:

- KAT9I_OS #217 — общий план;
- KAT9I_OS #218 — Capability Matrix;
- KAT9I_OS #219 — Artifact Contracts;
- CKS Bootstrap Snapshot.

После удаления чата продолжение работы начинается с этих артефактов.
