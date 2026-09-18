# Antigravity Contract Tests v1

## Цель

Проверка архитектурного контракта CKS, KAT9I_OS и Antigravity GUI.

## Проверки

PASS:

- CKS не зависит от Electron.
- GUI получает только подтверждённые состояния.
- События соответствуют Event Contract.
- Evidence имеет источник.
- QA_CONTEXT использует PR_HEAD + BASE_REFERENCE.

FAIL:

- GUI принимает решения.
- GUI изменяет Canon CKS.
- Worker обходит Runtime слой.
- UI становится источником знаний.
