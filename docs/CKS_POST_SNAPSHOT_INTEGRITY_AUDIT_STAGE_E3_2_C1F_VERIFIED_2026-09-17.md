# CKS POST-SNAPSHOT INTEGRITY AUDIT — E3.2-C1F VERIFIED

Дата: 2026-09-17

Статус: **E3.2-C1F VERIFIED + CI + GITHUB CHECKPOINT**

Назначение: минимальное удаление одного полностью дублирующего структурного workflow после отдельного анализа покрытия. Документ — validation/audit evidence, не Decision и не Canon. Frozen Core CKS v1.2 не изменялся.

## 1. Наследуемая проверенная база

Контрольные точки не переоткрывались:

- E2: `302660ecca9f039f274c73905235577fa27b0d41`;
- E3.1-A: `5f6cbf6a61200b2b3054e6a4176ce3fe00d4b2f9`;
- E3.1-B: `20d4263a0ff78701c73fffe2f0840f6fa6669b2d`;
- E3.1-C: `195b62ce550f65012fa113ca0845ba74feff8696`;
- E3.2-A: `788c948cc205ad50833caba81330f6adcced90f6`;
- E3.2-B: `f8ef6a4a` — verified checkpoint in main;
- E3.2-C1 analysis: `5c4287a9` — structural overlap analysis checkpoint in main.

## 2. Доказанное дублирование

Удалённый workflow:

`.github/workflows/cks-preflight.yml`

До удаления он запускался на:

- `pull_request`;
- `push` в `main`.

И проверял наличие 5 каталогов:

- `protocols`;
- `schemas`;
- `decisions`;
- `evidence`;
- `graveyard`.

Сохранённый `.github/workflows/cks-knowledge-check.yml` имеет те же автоматические события и проверяет все эти 5 каталогов плюс `docs`.

Следовательно, Preflight был строгим подмножеством Knowledge Check и не давал уникального автоматического покрытия.

## 3. Проверка внешних зависимостей

Перед удалением было подтверждено:

- внутренних ссылок на `cks-preflight.yml` и имя `CKS Preflight` не найдено;
- repository rulesets отсутствуют;
- ветка `main` возвращает `protected: false`;
- обязательные status checks для main не настроены.

Таким образом, имя удаляемого workflow не было внешним обязательным merge gate.

## 4. Выполненное изменение

Удалён только файл:

`.github/workflows/cks-preflight.yml`

Commit удаления:

`481304d2c11ea1121bb292eb89692851d47207c4`

После удаления повторное чтение файла из `main` подтверждает его отсутствие.

Другие workflow в этом исправляющем проходе не менялись.

## 5. Фактическая CI-регрессия

Для head SHA:

`481304d2c11ea1121bb292eb89692851d47207c4`

GitHub Actions зарегистрировал 9 push-runs.

### Замещающее структурное покрытие

- workflow: `CKS Knowledge Check`
- run: `35168853550`
- status: `completed`
- conclusion: `success`

Это подтверждает, что оставшийся более широкий структурный workflow продолжает работать после удаления Preflight.

### Общая регрессия

- workflow: `CKS Validation`
- run: `35168853621`
- status: `completed`
- conclusion: `success`

Дополнительно на том же SHA успешно завершились:

- Runtime Governance — run `35168853594`;
- Traceability Check — run `35168853530`;
- Control Plane Validation — run `35168853620`;
- Release Check — run `35168853658`;
- Boundary Check — run `35168853676`;
- Canon Evidence Guard — run `35168853664`;
- Bootstrap Check — run `35168853782`.

Новой CI-регрессии после удаления Preflight не обнаружено.

## 6. Canon / Frozen Core

Canon не изменялся.

Frozen Core CKS v1.2 не изменялся.

## 7. Точка продолжения

```text
E3.2-A   false-green repair                    ✅ VERIFIED
E3.2-B   dependency trigger repair             ✅ VERIFIED
E3.2-C1  structural overlap analysis           ✅ CHECKPOINT
E3.2-C1F remove redundant Preflight             ✅ VERIFIED + CI + CHECKPOINT
E3.2-C2  Integration Test + Release Check      ← NEXT SMALL ANALYSIS PASS
E3.2-C3  remaining overlap/trigger cleanup      ⏳
E3.3     Node.js Actions debt                   ⏳
E3.4     final regression                       ⏳
```

После разрыва продолжать с **E3.2-C2**. Сначала только анализ `cks-integration-test.yml` и `cks-release-check.yml`; никаких массовых удалений.
