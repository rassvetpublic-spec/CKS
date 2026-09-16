# CKS v1.3 PASS 5 — Research/Core Boundary

## Цель

Закрепить автоматический контроль границы между исследовательским слоем и стабильным ядром.

## Правила

Запрещено:

```
Research -> Core
Proposal -> Canon
Draft -> Core Rule
```

Разрешённый путь:

```
Research
  -> Evidence
  -> Proposal
  -> Decision
  -> Review Gate
  -> Core change
```

## CI

Добавлен workflow:

```
.github/workflows/cks-boundary-check.yml
```

Проверка использует существующий CKS validator.

## Аудит

Проверено:

- отчёты не являются SSOT;
- индекс знаний не заменяет исходные объекты;
- автоматизация проверяет правила, но не принимает решения.
