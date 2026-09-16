# CKS Object Registry v1

## Назначение

Единый реестр объектов CKS.

Цель: связать объект, его схему, расположение, состояние и роль в жизненном цикле знаний.

## Реестр объектов

| Объект | Схема | Путь | Версия | Статус | Назначение |
|---|---|---|---|---|---|
| контекст (Context) | пакет контекста (Context Package) | `schemas/context_package_v1.yaml` | v1 | активно | исходный материал и границы анализа |
| контекст KAT9I (Context Package KAT9I) | пакет контекста KAT9I (Context Package KAT9I) | `schemas/context_package_kat9i_v1.yaml` | v1 | активно | специальный формат обмена контекстом |
| решение (Decision) | запись решения (Decision Record) | `schemas/decision_record_v1.yaml` | v1 | активно | принятое решение и его основание |
| ссылка решения (Decision Reference) | ссылка решения (Decision Reference) | `schemas/decision_reference_v1.yaml` | v1 | активно | связь решений и объектов |
| доказательство (Evidence) | запись доказательства (Evidence Record) | `schemas/evidence_record_v1.yaml` | v1 | активно | подтверждение решения |
| доказательство (Evidence) | доказательство v1 (Evidence v1) | `schemas/evidence_v1.yaml` | v1 | активно | дополнительный формат подтверждающих данных |
| артефакт (Artifact) | договор артефакта (Artifact Contract) | `schemas/artifact_contract_v1.yaml` | v1 | активно | результат изменения или работы |
| объект выделенных знаний (Distillate) | объект выделенных знаний (Distillate Object) | `schemas/distillate_object_v1.yaml` | v1 | активно | результат обработки контекста |
| кандидат объекта (Candidate Object) | кандидат объекта (Candidate Object) | `schemas/candidate_object_v1.yaml` | v1 | активно | промежуточный объект до принятия решения |
| реестр канона (Canon Registry) | реестр канона (Canon Registry) | `schemas/canon_registry_v1.yaml` | v1 | активно | связь с правилами канона |
| задача исполнителя (Agent Task) | задача исполнителя (Agent Task) | `schemas/agent_task_v1.yaml` | v1 | активно | описание рабочей задачи |
| отчёт исполнителя (Agent Report) | отчёт исполнителя (Agent Report) | `schemas/agent_report_v1.yaml` | v1 | активно | результат выполнения задачи |
| отчёт аудита (Audit Report) | отчёт аудита (Audit Report) | `schemas/audit_report_v1.yaml` | v1 | активно | результаты проверки |
| снимок состояния (Snapshot) | снимок состояния (Snapshot) | `schemas/` | v1 | проектируется | восстановление состояния системы |

## Основные связи

```
контекст (Context)
    ↓
предложение (Proposal)
    ↓
решение (Decision)
    ↓
доказательство (Evidence)
    ↓
изменение (Change)
    ↓
результат (Result)
    ↓
снимок состояния (Snapshot)
```

## Правила

- объект решения должен иметь основание;
- доказательство должно иметь источник;
- изменение должно ссылаться на решение;
- снимок состояния должен ссылаться на актуальные объекты.

## Источник данных

Пути схем подтверждаются реестром схем CKS.

Следующий шаг:
проверка связей объектов с решениями, каноном и задачами GitHub.
