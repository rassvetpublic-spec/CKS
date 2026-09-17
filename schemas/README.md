# Реестр схем CKS

Статус: рабочий реестр выбора контрактов для Issue #51. Этот файл **не является Canon** и не меняет Frozen Core v1.2.

## Зачем нужен этот реестр

Каталог `schemas/` содержит одновременно машинно-проверяемые JSON Schema и исторические/интеграционные YAML-контракты. Наличие файла само по себе не означает, что его следует использовать для нового объекта.

Для выбора используются роли:

- `ACTIVE` — текущий контракт для указанной сущности/представления;
- `COMPATIBILITY` — версионный или интеграционный контракт, который сохраняется для совместимости и не удаляется без regression evidence (регрессионного доказательства);
- `LEGACY` — исторический контракт, который не следует выбирать для нового объекта;
- `REVIEW` — обнаружено расхождение или недостаточно доказательств; использовать как новый контракт нельзя до отдельного решения.

`ACTIVE` в этой таблице означает **роль выбора контракта**, а не автоматическое повышение содержимого до Canon. Для YAML-описаний это также не означает наличие исполняемого JSON Schema-валидатора.

## Главное правило для Knowledge Object

Для **нового канонического knowledge object (объекта знания)** используется только:

`schemas/cks-knowledge-object.schema.json`

`tools/cks_ci.py` загружает именно эту JSON Schema и отклоняет YAML knowledge object как `KNOWLEDGE_OBJECT_YAML_NONCANONICAL`.

`schemas/knowledge_object_v1.yaml` — исторический Bootstrap 1.0 контракт с явным `bootstrap_scope_only: true`. Для новых knowledge object его выбирать нельзя. Старые данные не удаляются автоматически: при миграции они переводятся в JSON и должны пройти `cks-knowledge-object.schema.json`.

## Матрица контрактов

| Файл | Роль | Назначение / правило выбора |
|---|---|---|
| `agent_report_v1.yaml` | ACTIVE | Контракт `agent_report`; отдельная сущность. |
| `agent_task_v1.yaml` | ACTIVE | Контракт `agent_task`; отдельная сущность. |
| `artifact_contract_v1.yaml` | ACTIVE | Контракт артефакта и его lifecycle-ограничений. |
| `audit_report_v1.yaml` | ACTIVE | Контракт результата аудита. |
| `candidate_object_v1.yaml` | ACTIVE | Контракт объекта-кандидата. |
| `canon_registry_v1.yaml` | ACTIVE | Контракт записи canon registry; сам файл не даёт права повышать объект до Canon. |
| `cks-ci-report.schema.json` | REVIEW | Schema требует `schema_version=1.0`, тогда как текущий `tools/cks_ci.py` формирует `1.1`; до сверки потребителей не считать активным валидатором отчёта. |
| `cks-document-metadata.schema.json` | ACTIVE | JSON Schema метаданных; наличие и базовая сила схемы проверяются `schema_checks()` в `tools/cks_ci.py`. |
| `cks-knowledge-object.schema.json` | ACTIVE | Единственный контракт для новых канонических knowledge object; исполняемо выбран `tools/cks_ci.py`. |
| `cks-knowledge-view.schema.json` | ACTIVE | Контракт производного динамического представления; `authority=derived_view_only`, не SSOT. |
| `cks-v1.4-knowledge-graph.schema.json` | COMPATIBILITY | Версионный v1.4 контракт формы графа; сохраняется отдельно от более нового storage model, автоматической замены не выполнять. |
| `cks-v1.4-metrics.schema.json` | COMPATIBILITY | Версионный v1.4 контракт метрик; не удалять без доказанного migration path (пути миграции). |
| `cks_v1_6_event_model.yaml` | COMPATIBILITY | Версионная модель событий v1.6; события не меняют Canon автоматически. |
| `cks_v1_7_graph_storage_model.yaml` | ACTIVE | Текущая описательная модель хранения производного графа; `authority=derived_index_only`. |
| `context_package_kat9i_v1.yaml` | ACTIVE | Специализированный boundary-контракт для импорта из KAT9I_OS; не заменяет общий context package. |
| `context_package_v1.yaml` | ACTIVE | Общий контракт context package. |
| `decision_record_v1.yaml` | ACTIVE | Контракт decision record (записи решения). |
| `decision_reference_v1.yaml` | ACTIVE | Отдельный контракт ссылки на решение. |
| `distillate_object_v1.yaml` | ACTIVE | Контракт Distillate Worker → KAT9I_OS; `tools/cks_ci.py` имеет отдельную проверку `distillate_object`. |
| `evidence_record_v1.yaml` | ACTIVE | Контракт evidence record; не считать дублем `evidence_v1.yaml` без доказательства эквивалентности. |
| `evidence_v1.yaml` | ACTIVE | Отдельный evidence-контракт; автоматическая замена на `evidence_record_v1.yaml` запрещена. |
| `exchange_message_v1.yaml` | ACTIVE | Контракт exchange message. |
| `graveyard_item_v1.yaml` | ACTIVE | Контракт элемента Graveyard. |
| `knowledge_object_v1.yaml` | LEGACY | Bootstrap 1.0, `bootstrap_scope_only`; не использовать для новых knowledge object. |
| `knowledge_score_v1.yaml` | ACTIVE | Контракт knowledge score. |
| `project_state_v1.yaml` | ACTIVE | Контракт состояния проекта. |
| `promotion_request_v1.yaml` | ACTIVE | Контракт запроса на promotion; не является самим решением о Canon. |
| `reference_v1.yaml` | ACTIVE | Контракт reference. |
| `registry_v1.yaml` | ACTIVE | Общий registry-контракт. |
| `validation_result_v1.yaml` | ACTIVE | Контракт validation result. |

## Обнаруженный schema drift (дрейф схемы)

`cks-ci-report.schema.json` сейчас нельзя считать доказанно активным контрактом отчёта:

- JSON Schema требует `schema_version = 1.0`;
- текущий `tools/cks_ci.py` записывает `schema_version = 1.1`.

В этом проходе расхождение **не исправляется скрыто**: неизвестно, какой вариант является внешним контрактом для потребителей. Нужна отдельная сверка потребителей и решение, после которого роль `REVIEW` должна быть изменена на `ACTIVE`, `COMPATIBILITY` или `LEGACY` вместе с regression evidence.

## Правила изменения схем

1. Новая схема добавляется вместе с обновлением этой матрицы.
2. `COMPATIBILITY` нельзя удалить без теста/доказательства, что потребители мигрировали.
3. `LEGACY` не используется для создания новых объектов, но может сохраняться для чтения/миграции.
4. `REVIEW` нельзя молча использовать как default-контракт.
5. Изменение схемы не меняет Canon/Frozen Core автоматически.
6. Для Knowledge Object default всегда `cks-knowledge-object.schema.json`, пока отдельное формальное решение не изменит этот выбор.

## Migration path для legacy Knowledge Object

```text
knowledge_object_v1.yaml / старый Bootstrap-объект
→ прочитать без повышения статуса
→ преобразовать в JSON
→ заполнить обязательные поля активной cks-knowledge-object.schema.json
→ validate_instance / CKS CI
→ только после успешной проверки продолжать обычный lifecycle
```

Автоматическое удаление или повышение до Canon на этом пути запрещено.
