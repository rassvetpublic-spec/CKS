# CKS v1.5 PACKAGE 004 — Multi-repository Knowledge Index

## Назначение

Единый индекс знаний для нескольких репозиториев без нарушения границ SSOT.

## Модель

```
Repository A
Repository B
Repository C
      ↓
Knowledge Index
      ↓
Traceability Layer
```

## Правила

- индекс не заменяет источник истины;
- ссылки на объекты сохраняют владельца и происхождение;
- конфликты требуют Review Gate.

## Метаданные

- repository;
- object_id;
- version;
- relations;
- evidence_links;
- lifecycle_state.
