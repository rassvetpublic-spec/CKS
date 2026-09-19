# CKS 1.2 Execution Roadmap

## Current status

CKS 1.2 находится в стадии Discovery / Implementation Preparation.

Принцип:
- не создавать новые базовые слои;
- развивать существующие Knowledge, Evidence, Decisions, Graveyard;
- не менять CORE;
- не переводить Discovery в Canon без Human Gate.

## Completed

- Architecture audit.
- Проверка существующих слоёв.
- Semantic Validation направление.
- Decision Validator specification.
- Evidence Trace Validator specification.
- Graveyard Lifecycle Validator specification.
- Validation Coverage Matrix.
- GAP Report.
- GAP → Validation mapping.
- Implementation Proposal.
- Implementation Checklist.

## Remaining plan

### Phase 1 — Final Audit Freeze

Цель:
- сверить все CKS 1.2 документы;
- найти противоречия;
- подтвердить границы изменений.

Выход:
- CKS_1.2_FINAL_SELF_REVIEW.md

### Phase 2 — Validation Contract Design

Цель:
- определить входы/выходы валидаторов;
- определить форматы ошибок;
- связать валидаторы с существующими workflow.

Выход:
- validation contracts.

### Phase 3 — Minimal Implementation Preparation

Цель:
- определить минимальные изменения;
- не затрагивать CORE;
- подготовить отдельный implementation PR.

Выход:
- implementation package.

### Phase 4 — Human Gate Package

Цель:
- подготовить пакет принятия решения.

Состав:
- summary изменений;
- evidence map;
- risk analysis;
- review package.

## Estimated remaining

Документационная часть: около 20–30%.

Реализация кода валидаторов и интеграция workflow: отдельный этап после подтверждения пакета.

## Current constraints

CORE: unchanged.
Canon: unchanged.
Discovery: active.
Human Gate: required.
