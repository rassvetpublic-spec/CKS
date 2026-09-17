# CKS POST-SNAPSHOT INTEGRITY AUDIT — E3.1-A

Дата: 2026-09-17

Статус: **E3.1-A COMPLETE / CHECKPOINT**

Назначение: первая малая часть инвентаризации остальных GitHub Actions workflow после подтверждённых E1/E2. Документ является validation/audit evidence, не Decision и не Canon. Frozen Core CKS v1.2 не изменяется.

## 1. Базовая точка подтверждена

Перед E3.1-A повторно проверено:

- checkpoint E2 существует в `main`: `docs/CKS_POST_SNAPSHOT_INTEGRITY_AUDIT_STAGE_E2_VERIFIED_2026-09-17.md`;
- commit checkpoint: `302660ecca9f039f274c73905235577fa27b0d41`;
- E1 run `35163494312`: `completed / success`, head `2ac56bb898a1dc4c54a221b2fe0f56765e88dd09`;
- E2 integral run `35164758487`: `completed / success`, head `e9e8c74e7372944fe985033de20fff89258c8ab4`;
- v1.4 validation run `35164728856`: `completed / success`, head `0996f3f42d6a5c207ba608b2a947629af51d373c`.

E1/E2 не переоткрываются.

## 2. Полная верхнеуровневая инвентаризация workflow

В `.github/workflows` на момент прохода обнаружено 17 workflow-файлов:

1. `bootstrap-check.yml`
2. `cks-boundary-check.yml`
3. `cks-canon-evidence-guard.yml`
4. `cks-compliance.yml`
5. `cks-control-plane-validation.yml`
6. `cks-governance-runner.yml`
7. `cks-integration-test.yml`
8. `cks-knowledge-check.yml`
9. `cks-knowledge-runtime-intelligence.yml`
10. `cks-preflight.yml`
11. `cks-release-check.yml`
12. `cks-review-gate.yml`
13. `cks-runtime-governance.yml`
14. `cks-traceability-check.yml`
15. `cks-v1-6-intelligence-runtime.yml`
16. `cks-v1.4-validation.yml`
17. `cks-validation.yml`

E3.1-A содержательно проверяет только позиции 1–6. Остальные оставлены для следующих малых частей.

## 3. Проверенная группа E3.1-A

### 3.1 `bootstrap-check.yml`

Триггеры: `push`, `pull_request`.

Команда: `python scripts/validate_bootstrap.py`.

Найден **CRITICAL false-green risk**:

`scripts/validate_bootstrap.py` вычисляет `True/False` и печатает `PASS/FAIL`, но не завершает процесс ненулевым кодом при `FAIL`. Следовательно, GitHub Actions step может быть зелёным даже при проваленной проверке.

Дополнительный долг: версия Python не фиксируется через `actions/setup-python`.

Классификация: `E3.2 candidate / false-green`.

### 3.2 `cks-boundary-check.yml`

Триггеры: `pull_request`, `push` в `main`.

Команда: `python tools/cks_ci.py --mode review-gate`.

`tools/cks_ci.py` возвращает exit code 1 при итоговом `FAIL`. Явного false-green по коду выхода не найдено.

Классификация: `PASS for exit semantics`, дальнейшая общая проверка покрытия остаётся в E3.1/E3.4.

### 3.3 `cks-canon-evidence-guard.yml`

Триггеры: `pull_request`, `push` в `main`, `workflow_dispatch`.

Команда: `python tools/cks_ci.py --mode canon`.

Код выхода содержательный: `FAIL → exit 1`.

Классификация: `PASS for exit semantics`.

### 3.4 `cks-compliance.yml`

Триггеры: `pull_request`, `workflow_dispatch`; обычного `push` в `main` нет.

Проверяет только наличие каталогов:

- `protocols`
- `schemas`
- `docs`
- `evidence`
- `decisions`
- `graveyard`

Команды `test -d` корректно падают при отсутствии каталога, то есть прямого false-green по exit semantics нет.

Риски:

1. слабая глубина проверки — только наличие директорий;
2. отсутствует автоматический запуск на `push` в `main`.

Классификация: `coverage/depth debt`, не подтверждённый false-green.

### 3.5 `cks-control-plane-validation.yml`

Триггеры: `pull_request`, `push`.

Команда: `python validators/control_plane_validator.py`.

Найден **CRITICAL false-green risk**:

`validators/control_plane_validator.py` формирует `status: PASS/FAIL` и печатает результат, но не возвращает ненулевой код процесса при `FAIL`. Поэтому workflow способен завершаться зелёным при отсутствующих обязательных control-plane файлах.

Дополнительный долг: Python version не фиксируется.

Классификация: `E3.2 candidate / false-green`.

### 3.6 `cks-governance-runner.yml`

Триггеры: `pull_request`, `workflow_dispatch`; обычного `push` в `main` нет.

Команда: `python tools/cks_governance_runner.py`.

`cks_governance_runner.py` агрегирует Self Audit и `cks_ci.py --mode all`, затем возвращает exit code 1 при итоговом `FAIL`. Прямого false-green по коду выхода не найдено.

Риск: отсутствие автоматического запуска на `push` в `main`.

Классификация: `trigger coverage debt`.

## 4. Итог E3.1-A

Проверено workflow: **6 / 17**.

Найдено:

- **2 подтверждённых false-green риска**:
  - `bootstrap-check.yml` → `scripts/validate_bootstrap.py`;
  - `cks-control-plane-validation.yml` → `validators/control_plane_validator.py`;
- **2 workflow с неполным push-покрытием**:
  - `cks-compliance.yml`;
  - `cks-governance-runner.yml`;
- **1 слабая структурная проверка**: `cks-compliance.yml`;
- `cks-boundary-check.yml` и `cks-canon-evidence-guard.yml` имеют корректную fail-семантику через `tools/cks_ci.py`.

Исправления в этом проходе намеренно не выполнялись. Они относятся к E3.2 после завершения инвентаризации.

## 5. Точка продолжения

```text
POST-SNAPSHOT INTEGRITY AUDIT

E1      v1.6 false-green                       ✅ VERIFIED + CI
E2      v1.7 + Self Audit + v1.4              ✅ VERIFIED + CI + CHECKPOINT
E3.1-A  workflows 1–6                         ✅ INVENTORIED + CHECKPOINT
E3.1-B  workflows 7–12                        ← NEXT SMALL PASS
E3.1-C  workflows 13–17                       ⏳
E3.2    fix confirmed risk groups             ⏳
E3.3    Node.js Actions debt                   ⏳
E3.4    final post-snapshot regression         ⏳
```

После разрыва продолжать с **E3.1-B**, одновременно быстро перепроверяя E1/E2 и предыдущий E3.1 checkpoint. Не повторять закрытые этапы с нуля.
