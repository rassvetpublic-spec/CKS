# CKS POST-SNAPSHOT INTEGRITY AUDIT — E3.1-B

Дата: 2026-09-17

Статус: **E3.1-B COMPLETE / CHECKPOINT**

Назначение: вторая малая часть инвентаризации GitHub Actions workflow. Это validation/audit evidence; не Decision и не Canon. Frozen Core CKS v1.2 не изменяется.

## 1. Наследуемая проверенная база

В этой же операции повторно подтверждены E1/E2/v1.4 run-объекты GitHub:

- E1 run `35163494312` — `completed / success`;
- E2 integral run `35164758487` — `completed / success`;
- v1.4 run `35164728856` — `completed / success`.

Checkpoint E3.1-A повторно прочитан из `main` после записи.

- E3.1-A commit: `5f6cbf6a61200b2b3054e6a4176ce3fe00d4b2f9`.
- E3.1-A зафиксировал два подтверждённых false-green риска: Bootstrap Validator и Control Plane Validator.

Закрытые результаты не переоткрываются; E3.1-B расширяет инвентаризацию.

## 2. Проверенная группа E3.1-B

Позиции 7–12 из общей карты 17 workflow.

### 2.1 `cks-integration-test.yml`

Триггеры: `pull_request`, `workflow_dispatch`.

Фактическая проверка:

- существует `schemas/context_package_kat9i_v1.yaml`;
- существует `scripts/import_context_package.py`.

Команды `test -f` корректно падают при отсутствии файлов, поэтому прямого false-green по exit semantics нет.

Риски:

1. workflow с названием Integration Test не выполняет импорт и не проверяет поведение интеграции — только наличие двух файлов;
2. нет автоматического `push`-запуска в `main`.

Классификация: `depth debt + trigger coverage debt`.

### 2.2 `cks-knowledge-check.yml`

Триггеры: `push` в `main`, `pull_request`.

Проверяет только наличие каталогов `docs`, `schemas`, `protocols`, `evidence`, `decisions`, `graveyard`.

Прямого false-green по exit semantics нет. Проверка структурно корректна, но очень поверхностна и частично дублирует `cks-compliance.yml`/`cks-preflight.yml`.

Классификация: `depth/duplication debt`.

### 2.3 `cks-knowledge-runtime-intelligence.yml`

Триггеры: path-filtered `push` и `pull_request`.

Workflow содержательный:

- фиксирует Python 3.12;
- компилирует рабочие модули;
- выполняет реальный набор unit/regression тестов этапов 2–7, B, D, E2;
- запускает Compatibility Audit;
- запускает Self Audit;
- запускает Governance Runner;
- публикует диагностические отчёты.

Подтверждённый ранее E2 run этого workflow: `35164758487`, `completed / success`.

Новый найденный риск: **dependency trigger gap**.

`tools/cks_governance_runner.py` внутри workflow вызывает `tools/cks_ci.py --mode all`, однако путь `tools/cks_ci.py` отсутствует в списке `push.paths` и `pull_request.paths` данного workflow. Следовательно, изменение базового CI validator не запускает этот интегральный workflow автоматически, хотя его поведение от валидатора зависит.

Классификация: `E3.2 candidate / dependency trigger gap`.

### 2.4 `cks-preflight.yml`

Триггеры: `pull_request`, `push` в `main`.

Проверяет только наличие каталогов `protocols`, `schemas`, `decisions`, `evidence`, `graveyard`.

Прямого false-green по коду выхода нет.

Классификация: `depth/duplication debt`.

### 2.5 `cks-release-check.yml`

Триггеры: `pull_request`, `push` в `main`.

Проверяет только наличие каталогов `docs`, `schemas`, `protocols`.

Название предполагает release validation, но содержательно проверяется лишь минимальная структура.

Классификация: `depth/semantic-name debt`; прямой false-green не подтверждён.

### 2.6 `cks-review-gate.yml`

Триггеры: `pull_request`, `workflow_dispatch`.

Использует:

- checkout с `fetch-depth: 0`;
- Python 3.12;
- `python tools/cks_ci.py --mode review-gate`;
- upload отчёта всегда.

`tools/cks_ci.py` возвращает exit code 1 при `FAIL`, поэтому прямой false-green не найден.

Отдельного push-триггера у Review Gate нет, однако аналогичный `review-gate` режим на push в `main` выполняет `cks-boundary-check.yml`. Поэтому здесь фиксируется прежде всего функциональное перекрытие/дублирование, а не подтверждённая дыра main-покрытия.

Классификация: `PASS exit semantics / overlap debt`.

## 3. Итог E3.1-B

Проверено дополнительно: **6 workflow**.

Суммарно после E3.1-A+B: **12 / 17 workflow**.

Новых подтверждённых false-green в группе B: **0**.

Найдено:

- **1 dependency trigger gap** — `cks-knowledge-runtime-intelligence.yml` не триггерится изменением `tools/cks_ci.py`, несмотря на транзитивную зависимость через Governance Runner;
- **4 слабых/поверхностных workflow**:
  - `cks-integration-test.yml`;
  - `cks-knowledge-check.yml`;
  - `cks-preflight.yml`;
  - `cks-release-check.yml`;
- существенное дублирование структурных directory/file existence checks;
- `cks-review-gate.yml` имеет корректную fail-семантику через `tools/cks_ci.py`.

Исправления отложены до E3.2 после полного E3.1.

## 4. Точка продолжения

```text
POST-SNAPSHOT INTEGRITY AUDIT

E1      v1.6 false-green                       ✅ VERIFIED + CI
E2      v1.7 + Self Audit + v1.4              ✅ VERIFIED + CI + CHECKPOINT
E3.1-A  workflows 1–6                         ✅ INVENTORIED + CHECKPOINT
E3.1-B  workflows 7–12                        ✅ INVENTORIED + CHECKPOINT
E3.1-C  workflows 13–17                       ← NEXT SMALL PASS
E3.2    fix confirmed risk groups             ⏳
E3.3    Node.js Actions debt                   ⏳
E3.4    final post-snapshot regression         ⏳
```

После разрыва продолжать с **E3.1-C**. Быстро подтвердить наличие E2/A/B checkpoints и не повторять их анализ с нуля.
