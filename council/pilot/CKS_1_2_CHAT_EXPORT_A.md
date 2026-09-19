# CKS 1.2 — экспорт беседы A

Источник: «Продолжение CKS bootstrap». Это свидетельство содержания чата,
не подтверждение репозитория.

## Состояние

`CONFIRMED_IN_CHAT`: CKS 1.1 — APPROVED, CORE FROZEN, RELEASE STABLE,
OPERATION VALIDATED, PILOT COMPLETED, Maintenance + Observation.

Граница: CKS — система знаний; KAT9I_OS — исполнение; GitHub — история изменений.

## CKS 1.2

Все перечисленное имеет статус `PROPOSAL`, реализация не подтверждена:

- Context Passport — ссылки, происхождение и ограничения;
- Worker Manifest — возможности и ограничения агента;
- External Adapter Contract — обмен проверенными артефактами;
- Import Pipeline — Source → Validation → Candidate → Lifecycle;
- Advanced Validation;
- Promotion Workflow.

## Зафиксированные в чате решения

`CONFIRMED_IN_CHAT`: CKS не является runtime; изменения CORE требуют ADR;
не создавать новые сущности без доказанной проблемы; соблюдать Language Policy.

`REJECTED`: CKS как runtime, память агентов, архив сырых чатов и отдельное
«кладбище идей» как отдельное хранилище.

## Риски и проверка

Документация может расходиться с системой; Passport может стать копией знаний;
Manifest — менеджером агентов; Adapter — скрытым исполнителем.

`GITHUB_VERIFICATION_REQUIRED`: наличие CKS 1.2 документов, ADR, PR, KU-объектов
и соответствие документации текущему репозиторию.

`UNRESOLVED`: в чате одновременно встречаются завершённый CKS 1.1 и CKS 1.2
как будущий Discovery; это не означает, что CKS 1.2 реализован.
