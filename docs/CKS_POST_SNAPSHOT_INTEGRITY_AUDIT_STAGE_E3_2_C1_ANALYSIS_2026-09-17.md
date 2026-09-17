# CKS POST-SNAPSHOT INTEGRITY AUDIT — E3.2-C1 ANALYSIS

Дата: 2026-09-17

Статус: **E3.2-C1 ANALYSIS COMPLETE / CHECKPOINT**

Назначение: малая аналитическая часть cleanup shallow/duplicate workflows. Изменения CI в этом проходе не выполнялись. Документ — audit evidence, не Decision и не Canon. Frozen Core CKS v1.2 не изменялся.

## 1. Проверенная группа

Только три структурных workflow:

1. `.github/workflows/cks-compliance.yml`
2. `.github/workflows/cks-knowledge-check.yml`
3. `.github/workflows/cks-preflight.yml`

## 2. Точное покрытие

### `CKS Compliance`

События:

- `pull_request`
- `workflow_dispatch`

Проверяет наличие 6 каталогов:

- `protocols`
- `schemas`
- `docs`
- `evidence`
- `decisions`
- `graveyard`

### `CKS Knowledge Check`

События:

- `pull_request`
- `push` в `main`

Проверяет те же 6 каталогов:

- `docs`
- `schemas`
- `protocols`
- `evidence`
- `decisions`
- `graveyard`

Порядок команд отличается, множество проверок идентично Compliance.

### `CKS Preflight`

События:

- `pull_request`
- `push` в `main`

Проверяет только 5 каталогов:

- `protocols`
- `schemas`
- `decisions`
- `evidence`
- `graveyard`

Каталог `docs` не проверяет.

## 3. Отношения покрытия

`CKS Preflight` является строгим подмножеством `CKS Knowledge Check`:

- события автоматического запуска одинаковы;
- все 5 проверок Preflight присутствуют в Knowledge Check;
- Knowledge Check дополнительно проверяет `docs`.

Следовательно, удаление `cks-preflight.yml` не уменьшает автоматическое структурное покрытие PR/main.

`CKS Compliance` по содержимому дублирует Knowledge Check, но сохраняет уникальное событие `workflow_dispatch` (ручной запуск). Поэтому в C1 он не удаляется.

## 4. Проверка внешних зависимостей перед удалением

Внутренний поиск default branch не нашёл ссылок на:

- `cks-preflight.yml`
- `CKS Preflight`
- `CKS Compliance`
- `CKS Knowledge Check`

Проверено состояние GitHub repository rulesets: список пуст.

Проверен объект ветки `main`:

- `protected: false`;
- branch protection disabled;
- required status checks отсутствуют.

Прямой endpoint полной branch protection конфигурации недоступен интеграции с HTTP 403, однако обычный branch endpoint возвращает явное состояние `protected: false` и пустые required checks. В сочетании с пустыми rulesets этого достаточно, чтобы исключить зависимость обязательного merge gate от имени `CKS Preflight` в текущей конфигурации.

## 5. Решение малого прохода

Безопасный минимальный следующий шаг:

- удалить только `.github/workflows/cks-preflight.yml`;
- `CKS Knowledge Check` оставить как автоматическую структурную проверку PR/main;
- `CKS Compliance` оставить до отдельного анализа ручного запуска;
- после удаления проверить фактический `CKS Knowledge Check` run и общий `CKS Validation`.

Никаких других shallow workflows в этом проходе не менять.

## 6. Точка продолжения

```text
E3.2-A   false-green repair                    ✅ VERIFIED
E3.2-B   dependency trigger repair             ✅ VERIFIED
E3.2-C1  structural overlap analysis           ✅ CHECKPOINT
E3.2-C1F remove redundant Preflight             ← NEXT
E3.2-C2  integration/release shallow checks    ⏳
E3.2-C3  remaining overlap/trigger cleanup      ⏳
E3.3     Node.js Actions debt                   ⏳
E3.4     final regression                       ⏳
```

После разрыва продолжать с **E3.2-C1F**. Не повторять предыдущие этапы с нуля.
