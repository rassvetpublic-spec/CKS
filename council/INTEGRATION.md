# Подготовка внешних интеграций

## QA Worker (внешний проверяющий исполнитель)

В исходном CKS нет реализации QA Worker. Подключение выключено, адрес репозитория
и имя workflow не заданы. Это подготовленный контракт, не работающая интеграция.
При подключении существующий QA Worker остаётся во внешней системе, например KAT9I_OS.

Вход должен соответствовать `schemas/agent_task_v1.yaml`:
id, source, objective, expected_artifacts, status; дополнительные ограничения
и требования к Evidence передаются через существующие поля.
В контексте задания: PR_HEAD и BASE_REFERENCE как полные SHA,
CURRENT_DECISION_STATE, proposal_ref, proposal_revision, relevant knowledge_refs.
Не пересылайте полные чаты или память агента.

Выход использует `schemas/agent_report_v1.yaml`: agent, task, artifacts, status,
evidence. reviewed_head и proposal_revision относятся к внешнему конверту,
не к расширению схемы CORE. Ссылка на отчёт должна указывать на неизменяемый артефакт.

| Вердикт Council | protocols/review_protocol.md |
|---|---|
| PASS | PASS |
| FAIL | REJECT |
| NEEDS_REVISION | NEEDS_REVIEW |

Неизвестный результат отклоняется. Новый PR_HEAD или новая ревизия аннулируют
прошлый PASS. Внешний обработчик должен отклонять дубликаты, старые события,
чужой task ID и попытки автора предложения выдать себя за владельца.

## Project lifecycle (жизненный цикл задачи)

Источник истины: `config/project_states.yaml` и `docs/PROJECT_LIFECYCLE_SPEC.md`.
Council PROPOSAL соответствует ANALYSIS; REVIEW, REVISION, VALIDATION и DECISION
остаются в DESIGN. VALIDATION здесь проверяет предложение, а не реализацию.
APPROVE позволяет IMPLEMENTATION, REJECT направляет в GRAVEYARD_REVIEW.
Далее: IMPLEMENTATION → QA → ACCEPTED → COMPLETED. Для ACCEPTED обязательны
артефакт реализации, актуальный QA PASS и доказательства.

Project ID, ID поля статуса и ID его вариантов следует получить из реального
Project перед включением интеграции. Не создавайте параллельные статусы Council
в существующем lifecycle. Сопоставление статусов задано в `.csk/integrations.yaml`.

## Условия включения автоматических workers — фаза 2

- Установлены фактические адрес и контракт существующего QA Worker.
- Получены ID Project и статусов; проверены права внешнего обработчика.
- Заполнены authorized_github_logins; пустой список запрещает APPROVE.
- Проверены текущий SHA, повторы, устаревший результат, лимит циклов и отказ QA.
- Личность владельца берётся из аутентифицированного GitHub-события.
- Ни Issue-текст, ни payload исполнителя не исполняются как команды оболочки.
- Финальный объект проходит текущие Validation → Evidence check → candidate.

Автоматическое принятие в canon и изменение CORE не входят в этот контракт.
