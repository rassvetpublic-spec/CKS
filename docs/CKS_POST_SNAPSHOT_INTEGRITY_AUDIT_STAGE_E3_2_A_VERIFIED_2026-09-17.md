# CKS POST-SNAPSHOT INTEGRITY AUDIT — E3.2-A VERIFIED

Дата: 2026-09-17

Статус: **E3.2-A VERIFIED + CI + GITHUB CHECKPOINT**

Назначение: минимальное исправление двух подтверждённых false-green дефектов, найденных в E3.1. Документ является validation/audit evidence, не Decision и не Canon. Frozen Core CKS v1.2 не изменялся.

## 1. Наследуемая проверенная база

Не переоткрывались и остаются контрольными точками:

- E2 checkpoint: `302660ecca9f039f274c73905235577fa27b0d41`;
- E3.1-A checkpoint: `5f6cbf6a61200b2b3054e6a4176ce3fe00d4b2f9`;
- E3.1-B checkpoint: `20d4263a0ff78701c73fffe2f0840f6fa6669b2d`;
- E3.1-C complete checkpoint: `195b62ce550f65012fa113ca0845ba74feff8696`.

E3.1 зафиксировал 17/17 workflow и два подтверждённых false-green:

1. `scripts/validate_bootstrap.py` печатал `FAIL`, но завершался кодом 0;
2. `validators/control_plane_validator.py` формировал `status: FAIL`, но завершался кодом 0.

## 2. Выполненные исправления

### 2.1 Bootstrap Validator

Файл: `scripts/validate_bootstrap.py`

Исправление:

- введён `main() -> int`;
- `PASS` возвращает exit code `0`;
- `FAIL` возвращает exit code `1`;
- запуск через `raise SystemExit(main())`.

Commit:

`c1dc29ad54904a54f56f8b6af874e6f8f4c7e78d`

### 2.2 Control Plane Validator

Файл: `validators/control_plane_validator.py`

Исправление:

- введён `main() -> int`;
- `status: PASS` возвращает exit code `0`;
- `status: FAIL` возвращает exit code `1`;
- запуск через `raise SystemExit(main())`.

Commit:

`eb82dddcf4b1a6e54f737c9ed82477d69e1c8382`

### 2.3 Регрессионный тест поведения процесса

Создан файл:

`tests/test_cks_workflow_exit_semantics_stage_e3_2_a.py`

Commit:

`7e6517dddbe92fc2b1bdd179f7858770b8cc3dea`

Тест проверяет валидаторы как отдельные процессы через `subprocess`, то есть именно ту семантику, которую видит GitHub Actions:

- Bootstrap FAIL → ненулевой exit code;
- Bootstrap PASS → exit code 0;
- Control Plane FAIL → ненулевой exit code;
- Control Plane PASS → exit code 0.

### 2.4 Bootstrap workflow

Файл: `.github/workflows/bootstrap-check.yml`

Перед реальным валидатором добавлен запуск E3.2-A regression test.

Commit:

`cc98a7cfce396d3bc3716f7ec032d971f2d45d56`

### 2.5 Control Plane workflow

Файл: `.github/workflows/cks-control-plane-validation.yml`

Перед реальным валидатором добавлен запуск E3.2-A regression test.

Commit / итоговый head SHA исправляющего набора:

`065afd887f0d015ab430fae364d22728ae32aad7`

## 3. Фактическая CI-проверка исправления

Все нижеуказанные runs относятся к head SHA:

`065afd887f0d015ab430fae364d22728ae32aad7`

### Целевые проверки

- Bootstrap Check
  - run: `35168545834`
  - status: `completed`
  - conclusion: `success`

- Control Plane Validation
  - run: `35168545871`
  - status: `completed`
  - conclusion: `success`

### Перекрёстная регрессия основного контура

- CKS Validation
  - run: `35168545882`
  - status: `completed`
  - conclusion: `success`

- CKS Runtime Governance
  - run: `35168545959`
  - status: `completed`
  - conclusion: `success`

Таким образом, исправлены не только сообщения `PASS/FAIL`, но и реальное поведение exit code, а основной validation/runtime контур после изменений остаётся зелёным.

## 4. Что намеренно НЕ менялось в E3.2-A

Чтобы не смешивать разные классы долга, в этом проходе не исправлялись:

- отсутствие фиксированной Python version в ранних простых workflow;
- shallow/duplicate workflow;
- trigger coverage debt;
- dependency trigger gap интегрального Knowledge Runtime;
- Node.js Actions debt.

Они остаются отдельными этапами.

## 5. Canon / Frozen Core

Canon не изменялся.

Frozen Core CKS v1.2 не изменялся.

Изменялись только validation/runtime support files, tests и GitHub Actions workflow.

## 6. Точка продолжения

```text
POST-SNAPSHOT INTEGRITY AUDIT

E1      v1.6 false-green                       ✅ VERIFIED + CI
E2      v1.7 + Self Audit + v1.4              ✅ VERIFIED + CI + CHECKPOINT
E3.1    all 17 workflows                      ✅ COMPLETE + CHECKPOINTS A/B/C
E3.2-A  repair 2 confirmed false-greens       ✅ VERIFIED + CI + CHECKPOINT
E3.2-B  integral trigger dependency gap       ← NEXT SMALL PASS
E3.2-C  shallow/duplicate workflow cleanup    ⏳
E3.3    Node.js Actions debt                   ⏳
E3.4    final post-snapshot regression         ⏳
```

После разрыва не повторять E1/E2/E3.1/E3.2-A. Продолжать с **E3.2-B**: минимально закрыть dependency trigger gap `tools/cks_ci.py` в `.github/workflows/cks-knowledge-runtime-intelligence.yml`, затем проверить реальный GitHub Actions run и записать новый checkpoint.
