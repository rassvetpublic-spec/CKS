# CKS ASYNC HANDOFF PROTOCOL v1.2

## Назначение

Протокол передачи состояния между WORKER и QA+REVIEW CONTROLLER.

FLOW:

WORKER -> HANDOFF -> QA+REVIEW -> VERDICT -> HISTORY

## Принципы

- commit = состояние кода
- HANDOFF = передача состояния
- VERDICT = решение проверки
- HISTORY = история решений

## SHA boundary

HANDOFF и VERDICT привязаны к SHA и BASE_SHA.

Если SHA изменился, предыдущий VERDICT недействителен.

## HANDOFF != EVIDENCE

HANDOFF описывает состояние.
EVIDENCE содержит подтверждение:
- tests
- workflow
- artifacts
- read-back

## Ограничения

1 PR = 1 active HANDOFF.

HANDOFF должен быть коротким и содержать только текущее состояние.
