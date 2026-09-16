# CKS — система контекста и знаний (Context Knowledge System)

Независимая система работы с контекстом, знаниями и решениями.

## CKS v1.2 Status

```yaml
version: CKS_v1.2
status: archived
architecture: stable
core: frozen
development: gap_driven
```

## Принцип границы

CKS не является исполнительным компонентом KAT9I_OS.

CKS отвечает за:

- контекст;
- знания;
- решения;
- доказательства;
- историю изменений.

Исполнительные процессы и операционные действия относятся к внешним системам.

## Архитектурные слои

- Core Engine — замороженное ядро;
- Context Split Modes;
- Knowledge Objects;
- Decision System;
- Evidence Layer;
- External Storage Adapters;
- Protocol Contracts.

## Режимы работы

- SPLIT;
- AUDIT;
- REVIEW;
- RESEARCH;
- MIGRATION;
- CLEANUP;
- MERGE;
- CANON CHECK.

## Правила развития

1. Расширение Core запрещено без подтверждённого GAP.
2. Proposal не является Decision.
3. Experiment не является Canon.
4. Исследовательские материалы хранятся отдельно от канона.

## Текущий режим

CKS v1.2 находится в режиме закрытой стабильной архитектуры.

Дальнейшее развитие выполняется только через обнаруженные архитектурные разрывы (GAP).