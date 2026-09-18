# Схемы CKS: статус и правило выбора

Этот каталог содержит несколько поколений технических контрактов. Наличие файла в `schemas/` само по себе не означает, что его следует выбирать для создания нового объекта.

## Статусы

- `ACTIVE` — действующий контракт для новых объектов соответствующего типа.
- `COMPATIBILITY` — совместимый контракт, который сохраняется для существующих производителей, потребителей и исторических данных. Не заменяется и не удаляется без отдельного migration/regression evidence (доказательства миграции и регрессии).
- `LEGACY` — исторический контракт. Он сохраняется для чтения/проверки старых данных, но не выбирается для новых объектов.

## Однозначное правило для нового объекта знания

```text
NEW_KNOWLEDGE_OBJECT_CONTRACT = schemas/cks-knowledge-object.schema.json
LEGACY_KNOWLEDGE_OBJECT_CONTRACT = schemas/knowledge_object_v1.yaml
```

Для **любого нового универсального объекта знания CKS** использовать только `schemas/cks-knowledge-object.schema.json`.

`schemas/knowledge_object_v1.yaml` — исторический минимальный контракт Bootstrap 1.0 с `bootstrap_scope_only: true`. Он остаётся доступным для совместимости со старыми данными, но **не является альтернативным контрактом для новых объектов знания**.

Правило выбора определяется назначением объекта, а не расширением файла, номером версии в имени или порядком файлов в каталоге.

## Инвентарь схем

| Схема | Статус | Назначение / правило |
|---|---|---|
| `agent_report_v1.yaml` | COMPATIBILITY | Совместимый контракт отчёта агента v1. |
| `agent_task_v1.yaml` | COMPATIBILITY | Совместимый контракт задачи агента v1. |
| `artifact_contract_v1.yaml` | COMPATIBILITY | Совместимый контракт артефакта v1. |
| `audit_report_v1.yaml` | COMPATIBILITY | Совместимый контракт аудиторского отчёта v1. |
| `candidate_object_v1.yaml` | COMPATIBILITY | Совместимый контракт объекта-кандидата v1. |
| `canon_registry_v1.yaml` | COMPATIBILITY | Совместимый контракт реестра канона v1; этот документ не меняет Canon. |
| `cks-ci-report.schema.json` | ACTIVE | Действующая JSON Schema (схема JSON) отчёта CI. |
| `cks-document-metadata.schema.json` | ACTIVE | Действующая JSON Schema метаданных документа. |
| `cks-knowledge-object.schema.json` | ACTIVE | **Единственный контракт для нового универсального объекта знания.** |
| `cks-knowledge-view.schema.json` | ACTIVE | Действующая схема производного представления знаний. |
| `cks-v1.4-knowledge-graph.schema.json` | ACTIVE | Действующая схема артефакта графа знаний v1.4, пока не введён заменяющий контракт. |
| `cks-v1.4-metrics.schema.json` | ACTIVE | Действующая схема метрик v1.4, пока не введён заменяющий контракт. |
| `cks_v1_6_event_model.yaml` | ACTIVE | Действующий версионированный контракт модели событий v1.6. |
| `cks_v1_7_graph_storage_model.yaml` | ACTIVE | Действующий версионированный контракт хранения графа v1.7. |
| `context_package_kat9i_v1.yaml` | COMPATIBILITY | Совместимый специализированный пакет контекста KAT9I v1. |
| `context_package_v1.yaml` | COMPATIBILITY | Совместимый общий пакет контекста v1. |
| `decision_record_v1.yaml` | COMPATIBILITY | Совместимый контракт записи решения v1. |
| `decision_reference_v1.yaml` | COMPATIBILITY | Совместимый контракт ссылки на решение v1. |
| `distillate_object_v1.yaml` | COMPATIBILITY | Совместимый контракт объекта-дистиллята v1. |
| `evidence_record_v1.yaml` | COMPATIBILITY | Совместимый контракт записи доказательства v1. |
| `evidence_v1.yaml` | COMPATIBILITY | Совместимый контракт доказательства v1. |
| `exchange_message_v1.yaml` | COMPATIBILITY | Совместимый контракт сообщения обмена v1. |
| `graveyard_item_v1.yaml` | COMPATIBILITY | Совместимый контракт элемента Graveyard v1. |
| `knowledge_object_v1.yaml` | LEGACY | Исторический минимальный Knowledge Object (объект знания) Bootstrap 1.0; только старые данные/совместимость. |
| `knowledge_score_v1.yaml` | COMPATIBILITY | Совместимый контракт оценки знания v1. |
| `project_state_v1.yaml` | COMPATIBILITY | Совместимый контракт состояния проекта v1. |
| `promotion_request_v1.yaml` | COMPATIBILITY | Совместимый контракт запроса продвижения v1. |
| `reference_v1.yaml` | COMPATIBILITY | Совместимый контракт ссылки v1. |
| `registry_v1.yaml` | COMPATIBILITY | Совместимый контракт реестра v1. |
| `validation_result_v1.yaml` | COMPATIBILITY | Совместимый контракт результата проверки v1. |

## Путь совместимости и миграции Knowledge Object

1. Существующие данные, созданные по `knowledge_object_v1.yaml`, не переписывать автоматически.
2. Старый контракт не удалять, пока существуют старые производители/данные или пока regression evidence не докажет безопасное удаление.
3. Новые универсальные объекты создавать по `cks-knowledge-object.schema.json`.
4. При явной миграции старого объекта добавить обязательные поля текущей схемы (`owner`, `lifecycle`, `relations`, `evidence`, `history`) и сопоставить старое состояние с допустимым текущим состоянием по действующим правилам жизненного цикла.
5. Поля старого payload (набора данных), не конфликтующие с текущей схемой, могут сохраняться: действующая JSON Schema допускает дополнительные свойства.
6. Изменение статуса схемы или удаление compatibility/legacy-контракта требует отдельного решения и регрессионного доказательства.

## Границы Issue #51, этап исполнителя B

Этот этап изменяет только документацию выбора схемы и тест её контракта. Workflow wrappers (оболочки автоматических проверок), E4.5, Canon и Frozen Core не входят в область этого изменения.
