# CKS Issue #34 — remediation checkpoint

Дата: 2026-09-17
Статус: **PARTIAL / P0 remediation in progress**
Источник: GitHub Issue #34 — `[QA + REVIEW] Архитектурно-технический QA-аудит и ревью проекта CKS (v1.3–v1.7, Runtime, CI/CD)`

## Контрольная точка

- Repository: `rassvetpublic-spec/CKS`
- Base `main`: `bb79776c426c01a2dddd409e16a7a2052da02891`
- Исходная рабочая ветка: `fix/issue-34-false-green`
- Head исходной ветки при checkpoint: `a22b1307064b9c4de770253830ac598c91e5223b`
- Создана чистая ветка для переноса только remediation #34: `fix/issue-34-clean`
- Issue #34 проверял старую точку `1ff433d7605ea5b8c3af3081436d25df7e746450`; выводы перепроверяются по актуальному `main`.

## Подтверждённые живые дефекты

1. Исторический обход валидации knowledge objects через YAML.
2. Неполный diff для multi-commit push.
3. Сломанный архитектурный SSoT `architecture/` при наличии `ARCHITECTURE.md`.
4. Мёртвые/слабые тесты, не отражавшие реальную проверку.
5. Отсутствовавший `setup-python` в части workflows.
6. `main` остаётся `protected: false` — отдельный governance-риск.

## Уже подготовленные исправления в исходной ветке

- миграция проблемных канонических knowledge objects из YAML в JSON;
- усиление `tools/cks_ci.py` реальной schema-проверкой и fail-closed поведением;
- полный диапазон GitHub push diff;
- исправление `control/ssot-registry.yaml` на `ARCHITECTURE.md`;
- усиление `tools/cks_self_audit.py`;
- регрессионный тест `tests/test_cks_issue34_false_green_regression.py`;
- перевод исторических тестов на реальный `unittest` discovery;
- исправление E3.4 parser;
- перенос markdown-псевдотеста из `tests/` в `docs/testing/`;
- `actions/setup-python@v6` для недостающих workflows;
- `.gitignore`;
- удаление `datetime.utcnow()` из v1.4 dashboard compatibility layer.

## BLOCKER

Исходная ветка `fix/issue-34-false-green` содержит посторонние реконструкционные изменения. Прямой merge запрещён до изоляции remediation diff.

## Следующий шаг

Перенести только изменения Issue #34 в `fix/issue-34-clean`, открыть PR, проверить CI и только после PASS рассматривать merge.
