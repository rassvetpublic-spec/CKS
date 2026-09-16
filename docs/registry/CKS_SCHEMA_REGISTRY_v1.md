# CKS Schema Registry v1

## Назначение

Реестр схем объектов CKS.

Цель: зафиксировать существующие схемы, версии, расположение, статус и роль в системе.

## Правило

Не создавать новые схемы без проверки существующих.

## Реестр схем

| Схема | Версия | Путь | Статус | Назначение |
|---|---|---|---|---|
| решение (Decision Record) | v1 | `schemas/decision_record_v1.yaml` | активно | описание принятого решения |
| доказательство (Evidence Record) | v1 | `schemas/evidence_record_v1.yaml` | активно | описание подтверждающих данных |
| пакет контекста (Context Package) | v1 | `schemas/context_package_v1.yaml` | активно | перенос и границы контекста |
| пакет контекста KAT9I (Context Package KAT9I) | v1 | `schemas/context_package_kat9i_v1.yaml` | активно | специальный договор обмена |
| договор артефакта (Artifact Contract) | v1 | `schemas/artifact_contract_v1.yaml` | активно | описание результата и условий |
| объект выделенных знаний (Distillate Object) | v1 | `schemas/distillate_object_v1.yaml` | активно | результат выделения знаний |
| реестр канона (Canon Registry) | v1 | `schemas/canon_registry_v1.yaml` | активно | описание связей с каноном |
| ссылка решения (Decision Reference) | v1 | `schemas/decision_reference_v1.yaml` | активно | ссылка на принятое решение |
| обменное сообщение (Exchange Message) | v1 | `schemas/exchange_message_v1.yaml` | активно | обмен между системами |
| объект кандидата (Candidate Object) | v1 | `schemas/candidate_object_v1.yaml` | требует аудита | потенциальное знание или решение |
| задача исполнителя (Agent Task) | v1 | `schemas/agent_task_v1.yaml` | активно | описание задания |
| отчёт исполнителя (Agent Report) | v1 | `schemas/agent_report_v1.yaml` | активно | результат выполнения задания |
| отчёт аудита (Audit Report) | v1 | `schemas/audit_report_v1.yaml` | активно | результат проверки |

## Правила совместимости

- изменение существующей схемы требует проверки влияния;
- новые версии должны сохранять историю изменений;
- устаревшие схемы не удаляются без решения;
- каждая схема должна иметь назначение и владельца жизненного цикла.

## Следующий шаг

Провести аудит полей YAML-схем и добавить связи между объектами.