# CKS-XXXX — итог Council

Это запись согласования; объект знания создаётся отдельно по существующей схеме.

- proposal_ref: ссылка на конкретный коммит
- proposal_revision: 1
- review_ref: ссылка на актуальную проверку
- reviewed_head: полный SHA
- outcome: APPROVE / REJECT / REQUEST_CHANGE (выбрать одно)
- owner: GitHub login владельца
- approval_ref: ссылка на проверенное решение владельца
- date: дата ISO 8601

## Проблема и контекст

## Решение и альтернативы

## Доказательства

## Последствия и откат

## Связи

Issue → Project item → PR → QA result → candidate Decision Record.
Для REJECT сохранить основания и при необходимости ссылку на graveyard.
Для REQUEST_CHANGE сохранить запись, увеличить ревизию и повторить проверку.
