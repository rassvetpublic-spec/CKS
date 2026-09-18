# Реестр схем CKS

Статус: рабочий реестр выбора контрактов для Issue #51. Этот файл **не является Canon** и не меняет Frozen Core v1.2.

## Зачем нужен этот реестр

Каталог `schemas/` содержит несколько поколений технических контрактов (машинно-проверяемые JSON Schema и исторические/интеграционные YAML-контракты). Наличие файла в `schemas/` само по себе не означает, что его следует выбирать для создания нового объекта.

Для выбора используются статусы и роли:

- `ACTIVE` — действующий контракт для новых объектов или текущих отчётов/представлений соответствующего типа.
- `COMPATIBILITY` — версионный или интеграционный контракт, который сохраняется для совместимости с существующими производителями, потребителями и историческими данными. Не заменяется и не удаляется без отдельного migration/regression evidence (доказательства миграции и регрессии).
- `LEGACY` — исторический контракт. Сохраняется для чтения/проверки старых данных, но не выбирается для новых объектов.
- `REVIEW` — обнаружено расхождение или недостаточно доказательств; использовать как новый контракт нельзя до отдельного решения.

`ACTIVE` в этой таблице означает **роль выбора контракта**, а не автоматическое повышение содержимого до Canon. Для YAML-описаний это также не означает наличие исполняемого JSON Schema-валидатора.

## Однозначное правило для нового объекта знания

```text
NEW_KNOWLEDGE_OBJECT_CONTRACT = schemas/cks-knowledge-object.schema.json
LEGACY_KNOWLEDGE_OBJECT_CONTRACT = schemas/knowledge_object_v1.yaml
```

Для **любого нового универсального объекта знания CKS** использовать только `schemas/cks-knowledge-object.schema.json`.

`tools/cks_ci.py` загружает именно эту JSON Schema и отклоняет YAML knowledge object как `KNOWLEDGE_OBJECT_YAML_NONCANONICAL`.

`schemas/knowledge_object_v1.yaml` — исторический минимальный контракт Bootstrap 1.0 с явным `bootstrap_scope_only: true`. Он остаётся доступным для совместимости со старыми данными, но **не является альтернативным контрактом для новых объектов знания**. Старые данные не удаляются автоматически: при миграции они переводятся в JSON и должны пройти `cks-knowledge-object.schema.json`.

Правило выбора определяется назначением объекта, а не расширением файла, номером версии в имени или порядком файлов в каталоге.

## Матрица контрактов

| Файл | Роль | Назначение / правило выбора |
|---|---|---|
| `agent_report_v1.yaml` | ACTIVE | Контракт `agent_report`; отдельная сущность. |
| `agent_task_v1.yaml` | ACTIVE | Контракт `agent_task`; отдельная сущность. |
| `artifact_contract_v1.yaml` | ACTIVE | Контракт артефакта и его lifecycle-ограничений. |
| `audit_report_v1.yaml` | ACTIVE | Контракт результата аудита. |
| `candidate_object_v1.yaml` | ACTIVE | Контракт объекта-кандидата. |
| `canon_registry_v1.yaml` | ACTIVE | Контракт записи canon registry; сам файл не даёт права повышать объект до Canon. |
| `cks-ci-report.schema.json` | ACTIVE | Действующая JSON Schema отчёта CI (версия контракта 1.1, формируется и валидируется `tools/cks_ci.py`). |
| `cks-document-metadata.schema.json` | ACTIVE | JSON Schema метаданных; наличие и базовая сила схемы проверяются `schema_checks()` в `tools/cks_ci.py`. |
| `cks-knowledge-object.schema.json` | ACTIVE | **Единственный контракт для нового универсального объекта знания**; исполняемо выбран `tools/cks_ci.py`. |
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
| `knowledge_object_v1.yaml` | LEGACY | Исторический минимальный Knowledge Object Bootstrap 1.0, `bootstrap_scope_only: true`; не использовать для новых knowledge object. |
| `knowledge_score_v1.yaml` | ACTIVE | Контракт knowledge score. |
| `project_state_v1.yaml` | ACTIVE | Контракт состояния проекта. |
| `promotion_request_v1.yaml` | ACTIVE | Контракт запроса на promotion; не является самим решением о Canon. |
| `reference_v1.yaml` | ACTIVE | Контракт reference. |
| `registry_v1.yaml` | ACTIVE | Общий registry-контракт. |
| `validation_result_v1.yaml` | ACTIVE | Контракт validation result. |

## Разрешение schema drift (дрейф схемы)

Ранее обнаруженное расхождение версий в `cks-ci-report.schema.json` успешно разрешено:
- `schemas/cks-ci-report.schema.json` зафиксирована на версии `1.1` (`const: "1.1"`, `enum: ["1.1"]`);
- `tools/cks_json_schema_validator.py` расширен поддержкой ключевого слова `const`;
- `tools/cks_ci.py` формирует машиночитаемый отчёт с `schema_version = "1.1"` и валидирует его по схеме;
- Статус схемы переведён в `ACTIVE`.

## Правила изменения схем

1. Новая схема добавляется вместе с обновлением этой матрицы.
2. `COMPATIBILITY` нельзя удалить без теста/доказательства, что потребители мигрировали.
3. `LEGACY` не используется для создания новых объектов, но может сохраняться для чтения/миграции.
4. `REVIEW` нельзя молча использовать как default-контракт.
5. Изменение схемы не меняет Canon/Frozen Core автоматически.
6. Для Knowledge Object default всегда `cks-knowledge-object.schema.json`, пока отдельное формальное решение не изменит этот выбор.

## Путь совместимости и миграции Knowledge Object

```text
knowledge_object_v1.yaml / старый Bootstrap-объект
→ прочитать без повышения статуса
→ преобразовать в JSON
→ заполнить обязательные поля активной cks-knowledge-object.schema.json
→ validate_instance / CKS CI
→ только после успешной проверки продолжать обычный lifecycle
```

1. Существующие данные, созданные по `knowledge_object_v1.yaml`, не переписывать автоматически.
2. Старый контракт не удалять, пока существуют старые производители/данные или пока regression evidence не докажет безопасное удаление.
3. Новые универсальные объекты создавать по `cks-knowledge-object.schema.json`.
4. При явной миграции старого объекта добавить обязательные поля текущей схемы (`owner`, `lifecycle`, `relations`, `evidence`, `history`) и сопоставить старое состояние с допустимым текущим состоянием по действующим правилам жизненного цикла.
5. Поля старого payload (набора данных), не конфликтующие с текущей схемой, могут сохраняться: действующая JSON Schema допускает дополнительные свойства.
6. Изменение статуса схемы или удаление compatibility/legacy-контракта требует отдельного решения и регрессионного доказательства. Автоматическое удаление или повышение до Canon на этом пути запрещено.

## Границы Issue #51, этап исполнителя B

Этот этап изменяет только документацию выбора схемы и тест её контракта. Workflow wrappers (оболочки автоматических проверок), E4.5, Canon и Frozen Core не входят в область этого изменения.
