# CKS POST-SNAPSHOT INTEGRITY AUDIT — E3.1-C COMPLETE

Дата: 2026-09-17

Статус: **E3.1 COMPLETE / ALL 17 WORKFLOWS INVENTORIED / CHECKPOINT**

Назначение: третья малая часть и завершение инвентаризации GitHub Actions workflow. Документ является validation/audit evidence, не Decision и не Canon. Frozen Core CKS v1.2 не изменяется.

## 1. Наследуемые checkpoints

Подтверждены и не переоткрываются:

- E2 checkpoint commit: `302660ecca9f039f274c73905235577fa27b0d41`;
- E3.1-A checkpoint commit: `5f6cbf6a61200b2b3054e6a4176ce3fe00d4b2f9`;
- E3.1-B checkpoint commit: `20d4263a0ff78701c73fffe2f0840f6fa6669b2d`.

В этой операции E1/E2/v1.4 run-объекты GitHub были повторно проверены и остаются `completed / success`.

## 2. Проверенная группа E3.1-C

Позиции 13–17 из общей карты 17 workflow.

### 2.1 `cks-runtime-governance.yml`

Триггеры: `pull_request`, `push` в `main`, `workflow_dispatch`.

Содержательно выполняет:

- checkout с полной историей;
- Python 3.12;
- `py_compile` рабочего контура;
- проверку JSON schemas;
- реальные integration/runtime tests;
- этапы Knowledge Runtime 2–4;
- Self Audit;
- Governance Runner;
- upload диагностических артефактов.

Проверен CLI Self Audit: при итоговом `FAIL` возвращает exit code 1. Governance Runner также возвращает exit code 1 при `FAIL`.

Классификация: `PASS / substantive workflow`.

### 2.2 `cks-traceability-check.yml`

Триггеры: `pull_request`, `push` в `main`, `workflow_dispatch`.

Команда: `python tools/cks_ci.py --mode traceability`.

Использует Python 3.12 и полную git history. `tools/cks_ci.py` возвращает exit code 1 при `FAIL`.

Классификация: `PASS exit semantics`.

### 2.3 `cks-v1-6-intelligence-runtime.yml`

Триггеры: path-filtered `push`, path-filtered `pull_request`, `workflow_dispatch`.

Содержательно выполняет:

- Python 3.12;
- syntax checks;
- regression test `test_cks_v1_6_compatibility_runtime.py`;
- реальный `--self-check` runtime.

Это исправленный в E1 workflow. Фактический run `35163494312` ранее в этой операции повторно подтверждён как `completed / success`.

Классификация: `PASS / E1 verified`.

### 2.4 `cks-v1.4-validation.yml`

Триггеры: path-filtered `pull_request`, path-filtered `push` в `main`.

Содержательно выполняет:

- Python 3.12;
- syntax checks v1.4 compatibility-модулей;
- содержательную E2 compatibility regression;
- Compatibility Audit без пустых заглушек.

Это исправленный в E2 workflow. Фактический run `35164728856` ранее в этой операции повторно подтверждён как `completed / success`.

Классификация: `PASS / E2 verified`.

### 2.5 `cks-validation.yml`

Триггеры: `pull_request`, `push` в `main`, `workflow_dispatch`.

Команда: `python tools/cks_ci.py --mode all`.

Использует checkout с полной историей, Python 3.12 и всегда публикует отчёт. `tools/cks_ci.py` возвращает exit code 1 при `FAIL`.

Классификация: `PASS exit semantics`.

## 3. Сводный итог полного E3.1

Проверено: **17 / 17 workflow**.

### Подтверждённые false-green риски

1. `bootstrap-check.yml` → `scripts/validate_bootstrap.py`:
   - печатает `FAIL`, но не возвращает ненулевой exit code.

2. `cks-control-plane-validation.yml` → `validators/control_plane_validator.py`:
   - формирует `status: FAIL`, но не возвращает ненулевой exit code.

Оба относятся к первому минимальному исправляющему проходу E3.2.

### Dependency trigger gap

3. `cks-knowledge-runtime-intelligence.yml`:
   - запускает Governance Runner;
   - Governance Runner вызывает `tools/cks_ci.py`;
   - но `tools/cks_ci.py` отсутствует в `push.paths` и `pull_request.paths` интегрального workflow.

Это также кандидат E3.2.

### Поверхностные/дублирующие workflow

4. `cks-compliance.yml` — existence-only directory check, нет push в main.
5. `cks-integration-test.yml` — existence-only двух файлов, фактической integration execution нет, нет push в main.
6. `cks-knowledge-check.yml` — existence-only directory check.
7. `cks-preflight.yml` — existence-only directory check.
8. `cks-release-check.yml` — existence-only directory check при сильном названии Release Check.
9. `cks-review-gate.yml` — корректный validator, но функционально пересекается с Boundary Check.
10. `cks-governance-runner.yml` — содержательный, но отдельный workflow не запускается на push в main; функциональное main-покрытие частично обеспечивается `cks-runtime-governance.yml`.

Эта группа требует проектного минимального решения в E3.2: не усиливать всё сразу, а исправлять только доказанные риски и отдельно решать, какие shallow checks должны быть удалены, объединены или усилены.

### Сильные workflow

- `cks-boundary-check.yml`;
- `cks-canon-evidence-guard.yml`;
- `cks-knowledge-runtime-intelligence.yml` — кроме trigger dependency gap;
- `cks-runtime-governance.yml`;
- `cks-traceability-check.yml`;
- `cks-v1-6-intelligence-runtime.yml`;
- `cks-v1.4-validation.yml`;
- `cks-validation.yml`.

## 4. Правило перехода к E3.2

E3.2 делить на отдельные малые исправляющие проходы:

- **E3.2-A** — исправить только два подтверждённых false-green validator exit codes + тесты;
- **E3.2-B** — закрыть dependency trigger gap `tools/cks_ci.py` в integral runtime;
- **E3.2-C** — отдельно решить shallow/duplicate workflows без смешивания с false-green repair.

Каждый проход заканчивать отдельным GitHub checkpoint и быстрой регрессией предыдущих результатов.

## 5. Точка продолжения

```text
POST-SNAPSHOT INTEGRITY AUDIT

E1      v1.6 false-green                       ✅ VERIFIED + CI
E2      v1.7 + Self Audit + v1.4              ✅ VERIFIED + CI + CHECKPOINT
E3.1-A  workflows 1–6                         ✅ INVENTORIED + CHECKPOINT
E3.1-B  workflows 7–12                        ✅ INVENTORIED + CHECKPOINT
E3.1-C  workflows 13–17                       ✅ INVENTORIED + CHECKPOINT
E3.1    all 17 workflows                      ✅ COMPLETE
E3.2-A  repair 2 confirmed false-greens       ← NEXT SMALL PASS
E3.2-B  integral trigger dependency gap       ⏳
E3.2-C  shallow/duplicate workflow cleanup    ⏳
E3.3    Node.js Actions debt                   ⏳
E3.4    final post-snapshot regression         ⏳
```

После разрыва продолжать с **E3.2-A**. Не повторять E1/E2/E3.1 с нуля; только быстро подтвердить checkpoints и выполнять регрессию после изменения.
