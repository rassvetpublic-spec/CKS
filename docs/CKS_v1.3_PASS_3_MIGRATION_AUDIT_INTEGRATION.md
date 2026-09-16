# CKS v1.3 PASS 3 — Migration Audit Integration

## Назначение

Migration Audit проверяет состояние перехода к CKS v1.3.

## Принцип

Audit не изменяет источники истины.

Он только формирует отчёт:

- возможные дубли;
- документы без metadata header;
- кандидаты на нормализацию.

## Поток

```text
Repository
  ↓
Migration Audit
  ↓
JSON Report
  ↓
Review
```

## Ограничения

- WARN не является ошибкой;
- автоматическое удаление запрещено;
- решения проходят через Review Gate.
