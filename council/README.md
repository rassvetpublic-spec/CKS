# CKS Council v0.1

`Council` (совместная подготовка и проверка решения) — вспомогательный процесс
через GitHub Issue и проверяемые артефакты. Версия 0.1 создаёт формы, роли,
контракты и автоматическую проверку конфигурации. Исполнители и автоматический
обмен между чатами в эту фазу не входят.

## Быстрый старт

1. Создайте Proposal (предложение) по `proposals/TEMPLATE.md` с ID `CKS-XXXX`.
2. Откройте Issue через форму «Council — предложение», свяжите его с артефактом.
3. Reviewer (проверяющий) получает ссылку и инструкцию `roles/reviewer.md`,
   сохраняет `reviews/CKS-XXXX-review-rN.md` и заполняет форму проверки.
4. При FAIL или NEEDS_REVISION автор исправляет предложение, повышает ревизию.
   После третьей проверки передайте нерешённые вопросы владельцу.
5. При PASS проверьте наличие доказательств и совпадение ревизии/PR_HEAD.
   Владелец фиксирует APPROVE, REJECT или REQUEST_CHANGE по `decisions/TEMPLATE.md`.
6. После APPROVE исполнитель может перейти к IMPLEMENTATION. Приёмка результата
   отдельно требует QA и Evidence (доказательств). Закрытие Issue не создаёт canon.

В фазе 1 переходы выполняет координатор; `.csk/workflow.yaml` описывает контракт,
но не запускает агентов. Файлы `TEMPLATE.md` и `*.example.*` — образцы, не решения.
Итоговые артефакты храните с историей Git, рабочие очереди и счётчики — снаружи.

## Состав

- `.csk/council.yaml`: настройки и ссылки на существующие контракты.
- `.csk/roles.yaml`: роли и будущая проверка полномочий владельца.
- `.csk/workflow.yaml`: допустимые переходы внешнего процесса.
- `.csk/integrations.yaml`: подготовка QA Worker и Project lifecycle.
- `.csk/state.json`: указатель на внешнее состояние; не база задач.
- `.github/ISSUE_TEMPLATE/council-*.yml`: новые формы рядом с существующими.
- `.github/workflows/council-check.yml`: проверка контрактов и регрессионные тесты.

Шаблоны GitHub появятся после попадания файлов в основную ветку.
Метки `council`, `decision`, `review-required` можно создать и назначать отдельно;
формы не зависят от их существования и не меняют имеющиеся шаблоны.
Формат сверялся с [документацией Issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms).

## Граница модели знания

CORE, schemas, protocols и config остаются прежними.
`council/decisions/` содержит результаты согласования; `decisions/` — записи знания.
Переносится только кандидат по `schemas/decision_record_v1.yaml`: id, title,
context, options, selected_option, rationale, evidence_refs, status.
Owner, approval chain, состояние задачи и метрики не добавляются в схему знания.
Пример кандидата намеренно имеет `status: draft` и пустые доказательства:
он не готов к принятию, пока реальные основания не заполнены и не проверены.

## Проверка локально

Из корня репозитория, Python 3.10+:

```powershell
python -m pip install -r council/requirements-check.txt
python scripts/validate_council.py
python -m unittest discover -s tests/council -v
python scripts/validate_structure.py
python scripts/validate_objects.py
python scripts/validate_bootstrap.py
```

Проверка Council обнаруживает несовместимые конфиги, но не доказывает истинность
Evidence, не подтверждает личность автора и не заменяет проверку содержания.

## Интеграции

Подробности: [INTEGRATION.md](INTEGRATION.md), [BRIDGE_DESIGN.md](BRIDGE_DESIGN.md).
Исходная проверка репозитория: [BASELINE.md](BASELINE.md).

Первый пилот на двух беседах: [Memory Pack](pilot/README.md).
Ограничение контекста и ответов: [TOKEN_POLICY.md](TOKEN_POLICY.md).
