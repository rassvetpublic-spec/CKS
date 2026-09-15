# CKS Bootstrap Snapshot

Статус документа:

BOOTSTRAP CONTEXT

Источник:
- CKS 1.1 Chat Distillation
- Repository Alignment Audit

Назначение:
быстро восстановить рабочий контекст CKS после закрытия рабочего чата.

---

# Текущее состояние

## CKS 1.1

Статус по подтверждённым материалам:

- архитектура: подтверждена
- Core: зафиксирован как минимальная модель
- граница CKS / KAT9I_OS: подтверждена
- Runtime внутри CKS: не допускается

---

# Главный принцип

CKS:

слой знаний.

Хранит:
- Knowledge Object (объект знания)
- Decision (решение)
- Evidence (доказательство)
- Reference (ссылка)
- Relationships (связи)
- Lifecycle (состояние знания)

KAT9I_OS:

слой исполнения.

Не является владельцем знаний CKS.

---

# Core Rules

1. Один источник истины для знаний.
2. Reference не является копией знания.
3. Evidence подтверждает знание, но не является архивом.
4. Lifecycle не является Workflow.
5. Новые Core-компоненты только через ADR.
6. Идея не становится компонентом ядра без доказанной проблемы.

---

# CKS 1.2

Статус:

Discovery only.

Исследовательские области:

- Context Passport
- Worker Manifest
- External Adapter Contract
- Import Pipeline
- Advanced Validation
- Promotion Workflow

Они не являются частью CKS 1.1 Core.

---

# Открытые проверки

- синхронизация статуса README и Release-документов;
- полный ADR audit;
- проверка схем объектов;
- проверка примеров Knowledge Object.

---

# Правило продолжения работы

Не расширять архитектуру от идеи.

Последовательность:

Problem

↓

Analysis

↓

Options

↓

ADR

↓

Implementation

---

# После восстановления контекста

Сначала проверить GitHub-состояние.

Не считать данные из старого чата подтверждёнными без проверки репозитория.
