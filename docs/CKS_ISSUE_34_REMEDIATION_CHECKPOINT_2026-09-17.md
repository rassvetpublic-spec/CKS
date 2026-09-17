# CKS Issue #34 — remediation checkpoint

Дата: 2026-09-17
Статус: **PARTIAL / P0 remediation in progress**
Источник: GitHub Issue #34 — `[QA + REVIEW] Архитектурно-технический QA-аудит и ревью проекта CKS (v1.3–v1.7, Runtime, CI/CD)`

## 1. Контрольная точка

- Repository: `rassvetpublic-spec/CKS`
- Base `main`: `bb79776c426c01a2dddd409e16a7a2052da02891`
- Working branch: `fix/issue-34-false-green`
- Branch head at checkpoint: `a22b1307064b9c4de770253830ac598c91e5223b`
- Branch delta vs base: 29 commits ahead, 0 behind.
- Issue #34 проверял старую точку `1ff433d7605ea5b8c3af3081436d25df7e746450`, поэтому его выводы перепроверяются по текущему состоянию, а не переносятся буквально.

## 2. Подтверждённые живые проблемы из Issue #34

1. `tools/cks_ci.py` исторически валидировал knowledge objects только по `*.json`, в то время как реальные объекты могли находиться в YAML и обходить каноническую схему.
2. Дифф на `push` был ориентирован на `HEAD^..HEAD`, что не покрывает надёжно multi-commit push.
3. `control/ssot-registry.yaml` указывал архитектурный SSoT на отсутствующий `architecture/`, хотя реальный документ — `ARCHITECTURE.md`.
4. Часть тестов была фактически несовместима с `unittest discover` либо проверяла слишком слабые/тафтологические условия.
5. `bootstrap-check.yml` и `cks-control-plane-validation.yml` не имели явной настройки Python.
6. `main` остаётся `protected: false`; этот риск не закрыт кодовыми изменениями текущей ветки.

## 3. Уже записанные исправления

### Knowledge-object false-green

- Проблемные канонические knowledge objects мигрированы из YAML в JSON:
  - `knowledge/objects/example_object.json`
  - `knowledge/objects/concept_multi_worker_sync.json`
  - `knowledge/examples/CKS-OBJ-001-rule-example.json`
- Старые YAML-версии удалены.
- `tools/cks_ci.py` усилен:
  - проверяет реальные JSON Schema constraints канонических knowledge objects;
  - учитывает обязательные поля, ID, enums и типы коллекций;
  - неизвестный/неразмеченный YAML в knowledge layer не должен молча считаться каноническим объектом;
  - отчёт фиксирует число реально проверенных knowledge objects.

### Differential validation

- Добавлена поддержка полного диапазона push через GitHub event (`before..after`) с fallback-механизмами.
- Workflow, использующие дифф, переведены на `fetch-depth: 0` там, где это требуется.

### SSoT

- `control/ssot-registry.yaml`: архитектурный указатель переведён на фактический `ARCHITECTURE.md`.
- `tools/cks_self_audit.py`: проверка архитектурного SSoT усилена.

### Tests / CI debt

- Добавлен `tests/test_cks_issue34_false_green_regression.py` для причин дефектов #34.
- `tests/test_cks_contracts.py`, `test_cks_v1_4_e2e.py`, `test_cks_v1_4_runtime_integration.py` переработаны под реальный `unittest` discovery.
- E3.4 parser KAT9I example переведён с хрупкого flat-parser на фактический контрактный parser.
- Неисполняемый `tests/test_governance_runner_failures.md` перенесён в `docs/testing/GOVERNANCE_RUNNER_FAILURE_CASES.md`.
- `bootstrap-check.yml` и `cks-control-plane-validation.yml` получили `actions/setup-python@v6`.
- `cks_v1_4_dashboard_runtime.py` очищен от устаревшего `datetime.utcnow()`.
- Создан корневой `.gitignore` для runtime/test artifacts.

## 4. Важное ограничение текущей ветки

Ветка `fix/issue-34-false-green` содержит также несколько реконструкционных артефактов, не относящихся напрямую к Issue #34, включая файлы под `docs/recon/`, `research/audits/` и отдельный knowledge object.

**Это блокирует прямой merge ветки целиком без предварительной изоляции diff.**

Перед merge требуется либо:

1. выделить чистую ветку только с remediation #34; либо
2. доказать, что дополнительные изменения относятся к отдельной согласованной операции и должны войти независимо.

Текущая политика: **не выполнять прямой merge этой ветки в `main` до очистки состава изменений.**

## 5. Ещё не закрыто

- Проверить все изменённые файлы #34 на текущей ветке повторным чтением.
- Запустить/проверить CI на чистой PR-ветке.
- Проверить, что новый validator действительно FAIL-ится на искусственно невалидном JSON/YAML и PASS-ится на текущем наборе.
- Проверить `scripts/cks_distiller_daemon.py` и внешний путь `C:\\Antigravity\\Common\\...` — наличие/актуальность на текущем `main` ещё требует отдельной перепроверки.
- Разобрать остаточное workflow-дублирование: общие composite actions уже существуют, поэтому #34 частично устарел; нужно отличить безопасные wrapper workflows от настоящего дублирования.
- Решить защиту `main` отдельным governance-шагом; она остаётся `protected: false` на момент checkpoint.

## 6. Правило восстановления

После разрыва контекста:

1. прочитать Issue #34;
2. прочитать этот checkpoint;
3. проверить текущие SHA `main` и `fix/issue-34-false-green`;
4. **не повторять аудит с нуля**;
5. сначала изолировать чистый remediation diff #34;
6. затем открыть PR и проверять CI;
7. merge только после подтверждённого PASS обязательных проверок.

## 7. Архитектурная граница

Эта работа является remediation/validation и не меняет Frozen Core автоматически, не создаёт новый Canon и не превращает результаты QA в Decision без отдельного процесса принятия решения.
