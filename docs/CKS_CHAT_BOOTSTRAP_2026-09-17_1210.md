# CKS — BOOTSTRAP ДЛЯ НОВОГО ЧАТА

**Дата фиксации:** 2026-09-17 12:10 (+03:00)  
**Репозиторий:** `rassvetpublic-spec/CKS`  
**Ветка:** `main`  
**Live main перед созданием bootstrap:** `36c41a8545984a75f667190a7fa852d38fca05e7`  
**Назначение:** восстановить рабочий контекст без перечитывания старого чата и без потери незавершённых решений/ограничений.  
**Статус документа:** recovery/bootstrap, не Canon и не Decision.

---

# 1. ПЕРВОЕ ПРАВИЛО НОВОГО ЧАТА

Перед **любым** изменением:

1. заново прочитать live `main`;
2. считать GitHub `main` единственным актуальным SSOT;
3. проверить, не было ли параллельной записи после SHA из этого bootstrap;
4. не откатывать и не перезаписывать чужую параллельную работу;
5. не делать force rollback;
6. не повторять уже закрытые аудиты без новых противоречащих доказательств;
7. не выдавать CI/защиту/этап за VERIFIED без фактического read-back.

Этот bootstrap — только точка восстановления. Если `main` ушёл вперёд, новое состояние `main` имеет приоритет.

---

# 2. НЕИЗМЕННАЯ ГРАНИЦА CKS

```text
CKS =
контекст
+ знания
+ решения
+ доказательства
+ история изменений

KAT9I_OS =
исполнение
+ процессы
+ операционные действия
```

CKS не превращать в исполнительный слой KAT9I_OS.

Canon / Frozen Core v1.2 без отдельного формального Decision **НЕ МЕНЯТЬ**.

Канонический путь изменения:

```text
GAP
→ Evidence
→ Proposal
→ Decision
→ Minimal Change
```

Постоянные ограничения:

- Proposal ≠ Decision;
- Experiment ≠ Canon;
- исследование не становится архитектурой автоматически;
- Graph ≠ SSOT;
- представление ≠ Canon;
- метрика ≠ решение;
- автоматизация ≠ утверждение;
- Obsidian ≠ SSOT;
- Project = динамическая проекция графа знаний, а не контейнер файлов.

---

# 3. ТЕКУЩЕЕ СОСТОЯНИЕ ОСНОВНОЙ GOVERNANCE-ВЕТКИ

По live GitHub на момент bootstrap:

```text
E1–E3.4    CLOSED / VERIFIED

E4.1       VERIFIED
E4.2       VERIFIED
E4.3       VERIFIED
E4.4       VERIFIED
E4.5       READY / EXTERNAL ADMIN AUTH BLOCKED / NOT APPLIED

Canon      UNCHANGED
Worker A   ownership/lock ACTIVE до успешного read-back E4.5
```

Ключевой Issue:

- **Issue #43** — `[E4][AUTONOMOUS] Repository governance + Package 003 execution ledger`
- **Issue #56** — `E4.5 admin handoff: apply main branch protection`

Issues #57 и #58 — случайные VOID / `not_planned`, не использовать как рабочие ветки.

## E4.5 — что именно осталось

Последний подтверждённый read-back:

```text
main.protected = false
required status-check enforcement = off
required contexts = []
```

То есть branch protection **не включена** и E4.5 нельзя называть VERIFIED.

Целевая политика для `main`:

1. требовать Pull Request до merge;
2. 0 обязательных approving reviews;
3. required status checks включены;
4. `strict = true` / branch must be up to date;
5. enforce administrators;
6. force push запрещён;
7. deletion запрещена;
8. не добавлять новые требования signed commits / linear history / deployments / code-owner review / last-push approval / conversation resolution.

Точные required checks:

1. `Package 003 integrated automation gate`
2. `boundary`
3. `canon-guard`
4. `traceability`
5. `governance`
6. `validate-control-plane`
7. `validate-bootstrap`

Bare `validate` специально исключён из-за двух производителей одинакового check-run name.

Безопасный helper:

```text
tools/cks_apply_branch_protection.py
```

Regression test:

```text
tests/test_cks_branch_protection_helper_e4.py
```

Исправление опасного раннего варианта helper:

```text
dd2b176d92f342d20fb14deb5bf5a531217c5995
```

Проверенный functional head:

```text
932e1984a7779cd0492989d944a0200ff539a7c8
```

Package 003 aggregate evidence:

```text
run: 35193442906
job: 105111018790
conclusion: success
```

## E4.5 — безопасное продолжение

Не вставлять admin token в чат и не коммитить его.

На машине с admin-capable GitHub token:

```powershell
$env:CKS_GITHUB_ADMIN_TOKEN = "<admin-capable-token>"
python tools/cks_apply_branch_protection.py
python tools/cks_apply_branch_protection.py --apply
Remove-Item Env:CKS_GITHUB_ADMIN_TOKEN
```

После применения обязательно сделать GitHub settings read-back и только если он доказывает целевую политику:

1. создать финальный E4.5 VERIFIED checkpoint;
2. перевести E4 в CLOSED / VERIFIED;
3. обновить Issues #43 и #56;
4. опубликовать `WORKER A RELEASE` в Issue #43.

---

# 4. DURABLE RECOVERY-ДОКУМЕНТЫ E4

Читать их перед восстановлением E4:

```text
docs/CKS_E4_FULL_RECOVERY_SNAPSHOT_2026-09-17.md
docs/CKS_POST_SNAPSHOT_CURRENT_WORK.md
docs/CKS_E4_AUTONOMOUS_EXECUTION_LEDGER_2026-09-17.md
docs/CKS_POST_SNAPSHOT_E4_4_INTEGRATED_REGRESSION_VERIFIED_2026-09-17.md
docs/CKS_POST_SNAPSHOT_E4_5_BRANCH_PROTECTION_READY_BLOCKED_2026-09-17.md
docs/CKS_POST_SNAPSHOT_AUDIT_INDEX.md
```

Последняя persistence chain:

```text
0c39ee92582d0340437111e274d5eb16226f5530  full recovery snapshot
bd965a3b586c0a6ea3d7395beffd052b7deda114  CURRENT_WORK advanced to E4
3b61ea06412d4405578973cb7f8bddb629693807  audit index linked to E4
b99e6c68c0948bc984527df2b7ed2db2dbbc9395  final branch-protection blocker evidence
36c41a8545984a75f667190a7fa852d38fca05e7  complete E4.5 recovery state persisted
```

---

# 5. KNOWLEDGE RUNTIME + KNOWLEDGE INTELLIGENCE — ЧТО УЖЕ СДЕЛАНО

Отдельная ветка работы этого чата прошла этапы 1–7.

Рабочий roadmap:

```text
docs/CKS_KNOWLEDGE_RUNTIME_AND_INTELLIGENCE_ROADMAP_RU.md
```

Важно: roadmap — рабочий план, не Canon.

## Этап 1 — аудит модели

Цель: не создавать второй параллельный объект знания/схему.

Зафиксирован принцип:

- использовать существующий `schemas/cks-knowledge-object.schema.json`;
- не создавать конкурирующую схему Knowledge Object;
- развивать существующие Runtime/Graph/Traceability/Intelligence инструменты.

## Этап 2 — Knowledge Runtime

Ключевые изменения:

```text
tools/cks_knowledge_state_machine.py
validators/lifecycle_guard.py
control/lifecycle-state-model.yaml
tests/test_cks_knowledge_runtime_stage2.py
docs/CKS_KNOWLEDGE_RUNTIME_STAGE_2_EXECUTION_RU.md
```

Основные commits:

```text
79682e3d718e05561e43c9b17562b56f2a994735
3278dc4188728ca84217d582c1b27597282311d9
e09b13b1ceb2f37b785d5fffa7db00217cc6f3a9
17a7b7f14d2ebbc6cf787ca781e010095134af35
3b72960ef498b856799f8fc29e525f010370bc2e
```

Реализовано:

- state machine;
- допустимые переходы статусов;
- защита Canon-перехода;
- compatibility mapping старых статусов;
- lifecycle guard.

## Этап 3 — Obsidian

Ключевые файлы:

```text
tools/cks_obsidian_export.py
tests/test_cks_obsidian_stage3.py
docs/CKS_KNOWLEDGE_REPRESENTATIONS_AND_OBSIDIAN.md
docs/CKS_KNOWLEDGE_RUNTIME_STAGE_3_OBSIDIAN_RU.md
```

Commits:

```text
d864fcfea63d83d48953db4425035aad9ff94e75
438ee6ce2e32ba7c36eb902fd3a28a0b75a29cb7
7cd127b3de22f907eaf4ab627d1f3352aaaaa770
c13260324990ce9d60aa71cd8c48ca29eed23d15
```

Реализовано:

- Markdown projection;
- индексы;
- Wiki-links;
- кластеры/теги/проекты/статусы;
- Obsidian Canvas;
- производные представления с `derived_view_only`.

## Этап 4 — Dynamic Views

Ключевые файлы:

```text
tools/cks_dynamic_views.py
tests/test_cks_dynamic_views_stage4.py
schemas/cks-knowledge-view.schema.json
docs/CKS_KNOWLEDGE_RUNTIME_STAGE_4_DYNAMIC_VIEWS_RU.md
```

Подтверждённые commits:

```text
c3e8675a2ce47a68ebf92878b85182b88e2cec2f  tests
7aa97c73502612169c87ec981ca8486dbc7562b8  view schema
0b9170d370ac592dab571f9d6b29aafd30f381b2  stage checkpoint
```

Представления включают:

- по статусам;
- типам;
- кластерам;
- тегам;
- проектам;
- времени;
- уверенности;
- связности;
- проблемам;
- происхождению;
- funnel «материал → знание».

## Этап 5 — Knowledge Intelligence I

Основные commits:

```text
51c634468084469d653cd5a41836546ad966c600  structural intelligence
7cd2ae4b237557d0c44b4fcfede6b991cf811074  tests
efa5031d16e02ef5a1c2f878becc271c325f8779  CI stages 2–5
```

Реализована структурная аналитика:

- графовая связность;
- isolated / weak nodes;
- broken references;
- кластерное/теговое покрытие;
- explicit conflict links;
- disputed status;
- confidence / novelty / uncertainty / importance signals;
- аналитика не изменяет источник и не принимает Decision/Canon.

## Этап 6 — Evolution / Migration / Recovery

Основные commits:

```text
a294446c9ab1896553c6706648b1e656a6b954fc  evolution runtime
a66bac32e20c67fe603bc3563f7759e44b0647c9  tests
1421f8258f2c3ab2e98f16ea98183ea8a082f3c4  real version diff
a6661fe824279c42265f34c912a620b9ab214024  CI stage 6
33260839af90c41e4ebd8b510cdb52e7ff950cbf  version analyzer facade test
```

Файл:

```text
tools/cks_knowledge_evolution.py
```

Реально реализовано:

- migration старых Knowledge Objects;
- legacy status mapping;
- управляемая эволюция статуса;
- запись history event;
- version change;
- deterministic snapshot;
- SHA-256 snapshot integrity;
- snapshot tamper detection;
- isolated runtime recovery;
- object-set diff.

### ВАЖНЫЙ НЕЗАКРЫТЫЙ СМЫСЛОВОЙ GAP

Не считать этап 6 доказательством, что полностью реализованы все пункты исходного roadmap.

Остаточный технический долг, который необходимо отдельно проверить/реализовать:

1. **Relation History** — полная история изменения каждой связи, а не только history объекта.
2. **Graph Migration Engine** — миграция версии/формата самого графа как отдельная процедура.
3. **Graph Recovery System** — восстановление графового хранилища/структуры как отдельная система, а не только snapshot объектов KnowledgeRuntime.
4. Полная JSON Schema validation в Runtime должна быть отдельно перепроверена: существующая `KnowledgeRuntime.validate()` исторически была более узкой, чем полный JSON Schema validator.

Не закрывать эти пункты только потому, что Stage 6 CI зелёный.

## Этап 7 — Full Self Audit / Integral Regression

Основной test commit:

```text
37452234a19e7dca00eb1a1653033f88a93bb444
```

CI commit:

```text
a499436faa0fe86411962fcd6422357628a2b941
```

Проверенный GitHub Actions run:

```text
run: 35158961924
job: 105004991534
conclusion: success
```

В job фактически SUCCESS получили:

- syntax modules stages 2–7;
- stage 2;
- stage 3;
- stage 4;
- base runtime/intelligence regression;
- stage 5;
- stage 6;
- stage 7 integral test;
- CKS self-audit;
- governance integral check;
- diagnostic report artifact publish.

Artifact:

```text
cks-knowledge-runtime-stage7-reports
artifact id: 10472460501
sha256: f6ed5a8ff35af2cb54f52c5d44ae8b2c8539a38a24a80cec613a877af2554e75
```

Важное ограничение: GitHub Actions artifact — временный объект, не считать его постоянным knowledge storage.

---

# 6. КЛЮЧЕВЫЕ ФАЙЛЫ KNOWLEDGE-СЛОЯ

Перед продолжением читать фактический live `main`:

```text
schemas/cks-knowledge-object.schema.json
schemas/cks-knowledge-view.schema.json

tools/cks_knowledge_runtime.py
tools/cks_knowledge_state_machine.py
tools/cks_dynamic_views.py
tools/cks_obsidian_export.py
tools/cks_knowledge_intelligence.py
tools/cks_knowledge_evolution.py
tools/cks_knowledge_graph_runtime.py
tools/cks_knowledge_federation.py
tools/cks_traceability_engine.py
tools/cks_runtime_pipeline.py
tools/cks_self_audit.py

validators/lifecycle_guard.py

docs/CKS_KNOWLEDGE_OBJECT_MODEL_RU.md
docs/CKS_PROJECT_KNOWLEDGE_TRANSFORMATION_VIEW.md
docs/CKS_RUSSIAN_FIRST_DOCUMENTATION_RULE.md
docs/CKS_VISION_KNOWLEDGE_SYSTEM_NOT_PROJECT_SYSTEM.md
docs/CKS_KNOWLEDGE_GRAPH_EVOLUTION_PLAN.md
docs/CKS_KNOWLEDGE_RUNTIME_AND_INTELLIGENCE_ROADMAP_RU.md
```

---

# 7. ЧТО НЕЛЬЗЯ ДЕЛАТЬ В НОВОМ ЧАТЕ

Запрещено:

- создавать второй Knowledge Object schema;
- создавать второй параллельный Runtime/Intelligence engine без доказанного GAP;
- превращать аналитический сигнал в Decision;
- автоматически повышать объект до Canon;
- считать Graph SSOT;
- считать Obsidian SSOT;
- изменять Frozen Core v1.2 без Decision;
- повторно выполнять E1–E3.4 «на всякий случай»;
- переигрывать E4.1–E4.4 без нового противоречащего evidence;
- называть E4.5 VERIFIED до settings read-back;
- перезаписывать параллельную работу старым состоянием;
- делать force rollback;
- делать false-green отчёты;
- считать зелёный unit/CI тест доказательством функциональности, которую тест фактически не покрывает.

---

# 8. КАК ПРОДОЛЖИТЬ РАБОТУ ПОСЛЕ ОТКРЫТИЯ НОВОГО ЧАТА

Новый чат должен начать так:

```text
Работаем с:
https://github.com/rassvetpublic-spec/CKS

Сначала прочитай live main.
GitHub main = SSOT.
Никаких rollback и перезаписи параллельной работы.

Прочитай bootstrap:
docs/CKS_CHAT_BOOTSTRAP_2026-09-17_1210.md

Затем прочитай:
- Issue #43
- Issue #56
- docs/CKS_E4_AUTONOMOUS_EXECUTION_LEDGER_2026-09-17.md
- docs/CKS_KNOWLEDGE_RUNTIME_AND_INTELLIGENCE_ROADMAP_RU.md

Проверь, насколько main ушёл вперёд относительно bootstrap SHA.
Не повторяй закрытые этапы.

Главные незакрытые направления:
1. E4.5 branch protection — только через admin-auth и обязательный read-back.
2. Отдельно проверить/закрыть Relation History.
3. Отдельно проверить/закрыть Graph Migration Engine.
4. Отдельно проверить/закрыть Graph Recovery System.
5. Перепроверить полноту JSON Schema validation KnowledgeRuntime.
6. После этого сделать финальный full-knowledge audit: всё ли из bootstrap уже покрыто GitHub и нет ли новых GAP.
```

---

# 9. ПРАВИЛО РАБОЧИХ ПРОХОДОВ

Пользователь просил не пытаться делать слишком большой объём одним проходом.

Правило:

```text
1 проход = 1 ограниченный этап
```

В конце каждого прохода:

1. повторно прочитать затронутые файлы из live `main`;
2. проверить предыдущий этап на регрессии;
3. получить фактический CI/read-back;
4. зафиксировать commit SHA;
5. записать остаточный GAP;
6. только потом переходить дальше.

---

# 10. СОСТОЯНИЕ НА МОМЕНТ ЭТОГО BOOTSTRAP

```text
CKS main before bootstrap write
36c41a8545984a75f667190a7fa852d38fca05e7

Canon / Frozen Core v1.2
UNCHANGED

E1–E3.4
CLOSED / VERIFIED

E4.1–E4.4
VERIFIED

E4.5
READY / EXTERNAL ADMIN AUTH BLOCKED / NOT APPLIED

Knowledge Runtime / Intelligence implementation track
Stages 1–7 implemented/tested

Knowledge track CI reference
35158961924 = SUCCESS

Residual knowledge-engineering GAPs
- Relation History
- Graph Migration Engine
- Graph Recovery System
- verify full JSON Schema validation coverage

Deletion of old chat
Do not rely on chat after this bootstrap.
Use live GitHub + this bootstrap as recovery sources.
```

---

# 11. ПРИОРИТЕТ ИСТОЧНИКОВ ПРИ ПРОТИВОРЕЧИИ

```text
1. live GitHub main
2. formal Decisions / Canon / Frozen Core
3. current Issues + durable execution ledgers
4. verified CI/read-back evidence
5. this bootstrap
6. old chat text / recollection
```

Этот порядок нужен, потому что параллельные worker'ы могут изменить `main` после создания bootstrap.
