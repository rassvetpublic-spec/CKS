# CKS Open Items

## Назначение

Этот документ фиксирует незакрытые вопросы после аудита CKS 1.1 и подготовки Bootstrap Snapshot.

Статус документа:

- не изменяет Core;
- не является архитектурным решением;
- используется как список проверки и передачи контекста.

---

# Текущее состояние

```
CKS 1.1

Architecture: Approved
Core: Frozen
Mode: Maintenance + Observation
```

CKS 1.2:

```
Discovery only
```

---

# OPEN-001 — Синхронизация статуса документации

Статус:

UNRESOLVED

Описание:

Проверить соответствие между текущими формулировками README и эксплуатационным статусом CKS 1.1.

Проверка:

- README;
- release documents;
- operational reports.

---

# OPEN-002 — ADR Audit

Статус:

UNRESOLVED

Проверить:

- расположение ADR;
- связь Decision → Evidence → ADR;
- соответствие архитектурным правилам.

---

# OPEN-003 — Schema Audit

Статус:

UNRESOLVED

Проверить:

- Knowledge Object schema;
- Decision schema;
- Evidence schema;
- обязательные поля.

---

# OPEN-004 — Real Usage Collection

Статус:

PLANNED

Цель:

накопить реальные эксплуатационные объекты без изменения Core.

Первые кандидаты:

- Decision;
- Idea;
- Rule;
- Research;
- Conflict Case.

---

# OPEN-005 — CKS 1.2 Discovery

Статус:

BLOCKED UNTIL EVIDENCE

Правило:

Новое развитие начинается только от подтверждённого эксплуатационного ограничения.

---

# Правила продолжения

1. Не изменять Core без ADR.
2. Не добавлять компоненты "на будущее".
3. Разделять Knowledge Layer и Execution Layer.
4. Использовать GitHub как историю изменений.
5. Сохранять русский язык как основной язык архитектурного описания.
