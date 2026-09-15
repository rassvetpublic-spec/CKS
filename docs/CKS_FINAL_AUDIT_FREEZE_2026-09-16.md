# CKS Final Audit Freeze

Дата: 2026-09-16
Baseline main: `e0cdf523d9e14b2bb37855a1c37b37d9f182d6cb`

## Статус

`BLOCKED_NEEDS_ARCHITECTURE_DECISION`

Этот документ фиксирует результат финального технического аудита перед Human Gate. Он не выполняет APPROVE, MERGE, Stable promotion, Canon promotion и не изменяет CORE.

## Вход восстановления

1. `docs/CKS_BOOTSTRAP_SNAPSHOT.md` — CKS Bootstrap Context.
2. `council/pilot/CKS_BOOTSTRAP_SNAPSHOT_2026-09-15.md`.
3. `council/pilot/HUMAN_GATE_DECISION_BRIEF.md`.
4. `council/pilot/CKS_FINAL_STATUS_REPORT.md`.

## Сохранённые инварианты

- CKS остаётся слоем знаний, а не runtime-системой.
- KAT9I_OS остаётся слоем исполнения.
- CORE не расширяется автоматически.
- Council v0.1 не получает автоматический approval или promotion.
- CKS 1.2 остаётся Discovery only до отдельного решения.

## Findings

### P0-FAF-001 — коллизия ADR-0001

В `main` существуют два разных архитектурных решения с одинаковым ID `ADR-0001`:

- `decisions/ARCHITECTURE_DECISION_RECORD.md` — CKS как независимая система знаний;
- `decisions/ADR-0001-multi-worker-distillate.md` — Multi-Worker Distillate.

Автоматически переименовывать, отменять или менять статус одного из них нельзя: это затрагивает архитектурную историю и канон решений.

### P0-FAF-002 — конфликт модели Decision

`docs/ADR_MODEL_v1.md` задаёт поля:

`id, title, context, decision, source, version, status`.

`schemas/decision_record_v1.yaml` задаёт другую модель:

`id, title, context, options, selected_option, rationale, evidence_refs, status`.

`decisions/example_decision.yaml` соответствует первой модели, но не текущей YAML-схеме.

Нужен один явный SSoT для Decision Record.

### P0-FAF-003 — конфликт модели Evidence

Одновременно существуют несовместимые определения Evidence:

- `docs/EVIDENCE_MODEL_v1.md`;
- `docs/EVIDENCE_MODEL_SPEC.md`;
- `schemas/evidence_record_v1.yaml`.

Они используют разные поля и lifecycle. `evidence/example_evidence.yaml` также не соответствует `schemas/evidence_record_v1.yaml`.

Нужен один явный SSoT для Evidence Record.

### P1-FAF-004 — рассинхронизация статуса версии

Статус CKS 1.1 описан по-разному:

- `README.md`: `Architecture initialization stage`;
- `docs/CKS_CURRENT_STATE_REPORT.md`: `Release Candidate`;
- `docs/CKS_1_1_RELEASE.md`: `RELEASE CANDIDATE`;
- `docs/CKS_1_1_RELEASE_REVIEW.md`: стабильная версия.

Автоматически объявлять Stable нельзя, так как Stable promotion явно оставлен за управляемым решением владельца.

### P1-FAF-005 — зелёный CI не доказывает соответствие схемам

`scripts/validate_objects.py` сейчас проверяет только наличие директорий и прямо обозначен как placeholder.
`.github/workflows/cks-validation.yml` проверяет структуру репозитория, но не валидирует Decision/Evidence instances против их контрактов.

Следовательно, текущий зелёный CI подтверждает структурную целостность, но не устраняет P0-FAF-002/P0-FAF-003.

## Проверено без блокеров

- `knowledge/objects/example_object.yaml` соответствует обязательным полям `schemas/knowledge_object_v1.yaml`.
- Граница Knowledge / Runtime в bootstrap-артефактах сохранена.
- PR #3 `Add CKS Council v0.1` остаётся draft и Human Gate остаётся открытым.
- На head PR #3 (`df0a893e8a9aa96d97b4ec4b239a8ccae16fba61`) GitHub Actions для Bootstrap, Release, Council, Validation, Compliance, Schema, Preflight, Integration и Knowledge завершались SUCCESS.

## Freeze rule

До решения P0-FAF-001..003 запрещено считать пакет финально согласованным или использовать статус `Final Audit PASS`.

Разрешены без архитектурного решения:

- сбор дополнительного evidence;
- техническая проверка ссылок;
- подготовка вариантов миграции;
- подготовка impact-анализа без изменения канона.

Требуют решения владельца:

1. какой ADR сохраняет ID `ADR-0001` и какой новый ID/статус получает второй;
2. какая модель Decision становится SSoT;
3. какая модель Evidence становится SSoT;
4. отдельным решением после исправлений — остаётся ли CKS 1.1 Release Candidate или выполняется Stable promotion.

## Состояние после freeze

```yaml
core: unchanged
canon: unchanged
cks_1_2: discovery_only
council_v0_1:
  technical_review: complete
  human_gate: open
final_audit_freeze:
  status: blocked_needs_architecture_decision
  baseline: e0cdf523d9e14b2bb37855a1c37b37d9f182d6cb
```
