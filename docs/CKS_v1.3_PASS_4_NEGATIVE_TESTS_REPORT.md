# CKS v1.3 PASS 4 — Negative Tests Report

## Цель

Проверка, что запрещённые состояния корректно обнаруживаются.

## Проверенные сценарии

- неверный формат CKS ID;
- Research lifecycle в Canon/Core контексте;
- Canon без полного набора Evidence + Decision + History + Owner.

## Правило

Тесты проверяют границы системы, а не создают новые правила.

## Следующий этап

- подключение тестов к CI;
- Research/Core boundary workflow;
- интеграционный Review Gate Run.
