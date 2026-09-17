# CKS Issue #34 — remediation checkpoint

Дата: 2026-09-17
Статус: **VERIFIED + MERGED / residual governance debt remains**
Источник: GitHub Issue #34 — `[QA + REVIEW] Архитектурно-технический QA-аудит и ревью проекта CKS (v1.3–v1.7, Runtime, CI/CD)`

## 1. Фактическая точка завершения remediation

- Repository: `rassvetpublic-spec/CKS`
- Issue #34 исходно проверял: `1ff433d7605ea5b8c3af3081436d25df7e746450`
- Remediation PR: **#38** — `fix: remediate Issue #34 false-green and QA blind spots`
- PR head: `a22b1307064b9c4de770253830ac598c91e5223b`
- Merge commit в `main`: `1234d5d86e40b4b18a184d5f2d111f2183889e00`
- PR #38 merged: 2026-09-17 06:25:33 UTC.

Промежуточное опасение, что вместе с #34 были влиты `docs/recon` / `research/audits`, повторной сверкой **не подтвердилось**: эти файлы уже находились в `main` до merge #38. Технический PR #37 синхронизировал три параллельных коммита `main` в remediation-ветку перед финальным PR.

## 2. Закрытые дефекты Issue #34

### Knowledge-object false-green

- канонические knowledge objects, ранее обходившие активную JSON Schema через YAML, мигрированы в JSON;
- `tools/cks_ci.py` применяет фактические ограничения `schemas/cks-knowledge-object.schema.json`;
- YAML в `knowledge/` работает fail-closed: отдельный YAML-контракт должен быть явно распознан; `knowledge_object` больше не может молча обойти каноническую схему;
- добавлена защита от нулевого числа реально проверенных канонических объектов;
- новый YAML object, появившийся параллельно (`solution_agy_standalone_db_restore_01`), также мигрирован в JSON до merge.

### Differential validation

- multi-commit push использует полный GitHub event range `before..after`;
- невозможность надёжно определить changed files в push/PR не превращается в PASS;
- workflows, которым требуется Git history, получают `fetch-depth: 0`.

### SSoT

- `control/ssot-registry.yaml`: `architecture.path` исправлен с отсутствующего `architecture/` на реальный `ARCHITECTURE.md`;
- `tools/cks_self_audit.py` проверяет этот указатель и физическое наличие целевого файла.

### Tests / compatibility / CI

- добавлен `tests/test_cks_issue34_false_green_regression.py`;
- исторические `test_cks_contracts.py`, `test_cks_v1_4_e2e.py`, `test_cks_v1_4_runtime_integration.py` переведены на реальный `unittest` discovery и содержательные проверки;
- E3.4 больше не зависит от магического `len(workflow_names) == 15`;
- ad-hoc flat parser KAT9I context package заменён активным fail-closed loader контрактного уровня;
- markdown-спецификация governance failure cases перенесена из `tests/` в `docs/testing/`;
- `bootstrap-check.yml` и `cks-control-plane-validation.yml` получили `actions/setup-python@v6`;
- создан корневой `.gitignore`;
- `datetime.utcnow()` устранён из v1.4 dashboard compatibility layer.

## 3. PR CI — подтверждение

Для PR head `a22b1307064b9c4de770253830ac598c91e5223b` успешно завершились обязательные проверки, включая:

- `CKS Validation` — run `35189694859` — SUCCESS;
- `CKS Integration Test` — run `35189694929` — SUCCESS;
- `CKS Control Plane Validation` — run `35189694955` — SUCCESS;
- `CKS Canon Evidence Guard` — run `35189694709` — SUCCESS;
- `CKS Governance Runner` — run `35189694890` — SUCCESS;
- `CKS Bootstrap Check` — run `35189694903` — SUCCESS;
- `CKS Boundary Check` — run `35189695012` — SUCCESS;
- `CKS Review Gate` — run `35189694668` — SUCCESS;
- `CKS Traceability Check` — run `35189694966` — SUCCESS;
- `CKS Knowledge Check` — run `35189694867` — SUCCESS;
- `CKS Compliance` — run `35189694816` — SUCCESS;
- `CKS v1.4 Validation` — run `35189695095` — SUCCESS;
- `CKS — рабочий контур и аналитика знаний` — run `35189695030` — SUCCESS.

`CKS Issue PR Automation` имел один ранний failure run `35189694953` на шаге metadata validation, после чего повторный run `35189716948` на том же head завершился SUCCESS. Это не было отказом кода/валидации CKS; финальное состояние automation зелёное.

## 4. Post-merge verification

Для merge commit `1234d5d86e40b4b18a184d5f2d111f2183889e00` GitHub Actions возвращает 17 связанных запусков. На момент checkpoint среди них нет `failure`, `cancelled` или незавершённых результатов.

Следовательно, remediation Issue #34 считается **MERGED + VERIFIED** на уровне кода и CI.

## 5. Остаточный долг — не скрывать

### HIGH governance risk

`main` по-прежнему имеет `protected: false`. Это относится к Issue #30 / настройкам репозитория и не закрывается изменениями #34.

### P2 архитектурный долг

- исторические schema-файлы по-прежнему требуют отдельной консолидации/compatibility migration;
- workflow wrappers `Review/Boundary` и `Compliance/Knowledge` сохранены. Исполняемая логика уже вынесена в shared composite actions, поэтому исходная формулировка #34 о полном дублировании устарела, но вопрос сокращения wrapper-workflows можно рассматривать отдельно.

### N/A / obsolete finding

`scripts/cks_distiller_daemon.py` из текста #34 отсутствует в отслеживаемом текущем репозитории; исправлять несуществующий tracked-файл не требуется.

## 6. Правило продолжения

Не повторять Issue #34 remediation с нуля.

Следующая работа:

1. сохранить этот checkpoint в `main` отдельным docs-only PR;
2. обновить Issue #39 фактическими PR/run ID;
3. Issue #34 можно закрывать как выполненный по подтверждённым code/CI дефектам, сохранив ссылки на отдельные остаточные governance/P2 задачи;
4. продолжать следующую операцию малыми пакетами с checkpoint после каждого крупного перехода.

## 7. Архитектурная граница

Remediation/validation не размораживает Frozen Core, не создаёт новый Canon и не превращает QA-наблюдения в Decision без отдельного процесса принятия решения.
