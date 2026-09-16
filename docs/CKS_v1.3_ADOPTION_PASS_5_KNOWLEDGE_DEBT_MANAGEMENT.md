# CKS v1.3 ADOPTION PASS 5 — Knowledge Debt Management

## Назначение

Модель управления долгом знаний.

Knowledge Debt — это накопленные состояния, которые снижают качество и управляемость знаний:

- устаревшие объекты;
- отсутствующие Evidence;
- разорванные связи Traceability;
- конфликтующие определения;
- объекты без владельца.

## Категории долга

| Тип | Описание |
|---|---|
| Freshness Debt | знание требует пересмотра |
| Evidence Debt | отсутствуют подтверждения |
| Traceability Debt | нарушена цепочка связей |
| Ownership Debt | нет ответственного |
| Consistency Debt | есть конфликтующие объекты |

## Правило обработки

Knowledge Debt не изменяет Canon напрямую.

Поток:

Knowledge Object
↓
Health Metrics
↓
Debt Detection
↓
Review Gate
↓
Decision

## Связь с автоматизацией

Debt Management использует:

- Knowledge Health Metrics;
- Traceability Validator;
- Review Gate.

Отчёт о долге является диагностическим артефактом и не является SSOT.
