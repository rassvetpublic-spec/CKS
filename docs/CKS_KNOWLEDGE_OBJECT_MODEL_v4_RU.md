# CKS — модель объекта знания v4

## Статус

```yaml
proposal: CKS-PROP-V4-001
status: CANON
layer: knowledge
core_impact: none
```

## Назначение

Этот документ канонизирует уже реализованную рабочую модель объекта знания CKS без изменения frozen Core v1.2 и без создания второго runtime.

Основания:
- Evidence Registry: #367;
- Decision Record и Decision Verification Protocol v3: #370;
- Promotion Gate v4: #371;
- исходная задача модели знаний: #349.

## Каноническая модель

Объект знания CKS имеет идентичность и состояние и может содержать следующие нормализованные поля рабочего контура:

- `id` — обязательный идентификатор;
- `title` — человекочитаемое имя;
- `type` — тип объекта;
- `status` — стадия жизненного цикла;
- `owner` — владелец;
- `lifecycle` — контур жизненного цикла;
- `version` — версия;
- `clusters` — кластеры;
- `tags` — теги;
- `projects` — проекции проектов;
- `relations` — связи;
- `evidence` — доказательства;
- `history` — история изменений;
- `signals` — диагностические сигналы;
- `obsidian` — метаданные производной Obsidian-проекции.

Источник фактического runtime-контракта: `tools/cks_knowledge_runtime.py`.

## Жизненный цикл

Канонический статус не назначается автоматически. Переход в `canonical` разрешён только после проверки жизненного цикла и требует:

1. минимум одного Evidence;
2. ссылки на Decision.

Источник проверки переходов: `tools/cks_knowledge_state_machine.py`.

## Связи

Граф знаний является производным индексом и не заменяет SSOT, Decision или Canon. Типизированные связи и их история обслуживаются рабочим графом `tools/cks_knowledge_graph_runtime.py`.

## Инварианты

- Knowledge ≠ Decision.
- Proposal ≠ Canon.
- Evidence не заменяет Validation.
- Canon Promotion требует явного Decision.
- CKS не становится исполнительным слоем KAT9I_OS.
- Производные представления и GUI не являются источником Canon.
- Frozen Core v1.2 этим Promotion не изменяется.

## Обратимость и история

Promotion сохраняет полную трассировку:

```text
#349
  ↓
#367 Evidence Registry
  ↓
#370 Decision Record
  ↓
#371 Promotion Gate
  ↓
CKS_KNOWLEDGE_OBJECT_MODEL_v4_RU.md
```

При последующей замене модель должна переходить через Decision/Promotion и фиксироваться как superseded, а не переписываться без истории.
