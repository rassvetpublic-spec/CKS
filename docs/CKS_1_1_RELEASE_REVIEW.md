# CKS 1.1 Release Review

## Статус

CKS 1.1 — стабильная версия.

## Назначение

CKS 1.1 фиксирует минимальное ядро системы знаний.

## Входит

- Knowledge Object (объект знания)
- Lifecycle (жизненный цикл знания)
- Reference (ссылка на объект знания)
- Decision (запись решения)
- Evidence (доказательство)
- Relationships (связи)
- ADR Model (модель архитектурных решений)
- Traceability (прослеживаемость)
- Language Policy (языковая политика)

## Не входит

- Runtime (среда исполнения)
- Agent Platform (платформа агентов)
- Workflow Engine (движок процессов)
- Import Engine (движок импорта)

## Архитектурное правило

Новые компоненты Core (ядра) добавляются только через Problem → Analysis → Options → ADR → Implementation.
