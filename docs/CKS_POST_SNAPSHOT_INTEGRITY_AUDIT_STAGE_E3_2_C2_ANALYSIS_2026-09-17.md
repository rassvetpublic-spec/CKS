# CKS POST-SNAPSHOT INTEGRITY AUDIT — E3.2-C2 ANALYSIS

Дата: 2026-09-17

Статус: **E3.2-C2 ANALYSIS COMPLETE / CHECKPOINT**

Назначение: малая аналитическая часть cleanup для двух workflow: Integration Test и Release Check. Изменения рабочего CI в этом проходе не выполнялись. Документ — audit evidence, не Decision и не Canon. Frozen Core CKS v1.2 не изменялся.

## 1. Наследуемая база

Предыдущий исправляющий проход E3.2-C1F завершён успешно:

- удалён только `cks-preflight.yml`;
- commit удаления: `481304d2c11ea1121bb292eb89692851d47207c4`;
- `CKS Knowledge Check` run `35168853550`: `completed / success`;
- `CKS Validation` run `35168853621`: `completed / success`;
- checkpoint E3.2-C1F записан в `main` commit `ee6b04893b401974cfb055299029b35ce34b1080`.

## 2. `cks-release-check.yml`

События:

- `pull_request`;
- `push` в `main`.

Проверяет только наличие:

- `docs`;
- `schemas`;
- `protocols`.

Сохранённый `cks-knowledge-check.yml` запускается на тех же автоматических событиях и проверяет:

- `docs`;
- `schemas`;
- `protocols`;
- `evidence`;
- `decisions`;
- `graveyard`.

Следовательно, `CKS Release Check` — строгое функциональное подмножество `CKS Knowledge Check` и не имеет уникального trigger/coverage поведения.

Классификация: **safe redundant workflow candidate**.

Минимальный следующий шаг: удалить только `cks-release-check.yml`, затем проверить `CKS Knowledge Check` и `CKS Validation` на commit удаления.

## 3. `cks-integration-test.yml`

События:

- `pull_request`;
- `workflow_dispatch`.

Проверка сейчас состоит только из:

- `test -f schemas/context_package_kat9i_v1.yaml`;
- `test -f scripts/import_context_package.py`.

Фактической integration validation (интеграционной проверки поведения) нет.

При этом эта проверка относится к отдельной границе CKS ↔ KAT9I_OS и поэтому не является обычным дубликатом directory checks.

Классификация: **unique boundary intent, insufficient depth**.

Удалять workflow не следует; его нужно усиливать отдельным малым проходом.

## 4. Дополнительное расхождение схемы и импортёра

Схема `schemas/context_package_kat9i_v1.yaml` описывает пакет с полями:

- `id`;
- `source_system`;
- `source_reference`;
- `created_at`;
- `split_mode`;
- `artifacts`.

Она также задаёт:

- `raw_runtime_state: false`;
- `raw_chat_dump: false`;
- `requires_validation: true`.

Текущий `scripts/import_context_package.py` является placeholder/prototype и функция `validate_package()` проверяет только наличие:

- `id`;
- `source_system`;
- `artifacts`.

Она не проверяет:

- `source_reference`;
- `created_at`;
- `split_mode`;
- значение `source_system == KAT9I_OS`;
- ограничения `raw_runtime_state` / `raw_chat_dump`.

Поиск по default branch не обнаружил тестов `validate_package()`.

Это не исправляется вместе с удалением Release Check, чтобы не смешивать cleanup и protocol validation.

## 5. Разделение дальнейшей работы

```text
E3.2-C2      analysis Integration + Release      ✅ CHECKPOINT
E3.2-C2F1    remove redundant Release Check       ← NEXT
E3.2-C2F2    strengthen Integration Test           ⏳
E3.2-C3      remaining overlap/trigger cleanup     ⏳
E3.3         Node.js Actions debt                  ⏳
E3.4         final regression                      ⏳
```

### E3.2-C2F1

Удалить только `.github/workflows/cks-release-check.yml`.

Не менять Integration Test.

Проверить после удаления:

- `CKS Knowledge Check`;
- `CKS Validation`;
- один основной runtime/governance контур.

### E3.2-C2F2

Отдельно определить минимально корректный контракт входного context package и добавить реальные тесты поведения импортёра + запуск тестов в Integration Test.

Не изменять Canon и Frozen Core v1.2 без отдельного доказанного решения.

## 6. Правило восстановления

После разрыва продолжать с **E3.2-C2F1**. Не повторять E1/E2/E3.1/E3.2-A/B/C1/C1F/C2 с нуля; только быстро подтвердить последний checkpoint перед изменением.
