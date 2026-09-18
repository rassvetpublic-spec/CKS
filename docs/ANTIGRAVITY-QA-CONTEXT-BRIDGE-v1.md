# Antigravity QA_CONTEXT Bridge v1

## Назначение

Определяет отображение проверочного состояния в GUI без переноса логики QA в интерфейс.

## Каноническая связь

QA_CONTEXT = PR_HEAD + BASE_REFERENCE

## Поток

PR_HEAD
↓
BASE_REFERENCE
↓
QA проверка
↓
Evidence
↓
GUI отображение

## Ограничения

- GUI показывает результат.
- GUI не выполняет роль QA двигателя.
- Evidence остаётся частью слоя доказательств.
