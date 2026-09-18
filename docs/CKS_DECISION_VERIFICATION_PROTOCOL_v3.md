# Протокол проверки решений CKS v3 (CKS Decision Verification Protocol v3)

## Назначение (Purpose)

Протокол **CKS Decision Verification Protocol v3** устанавливает строгие правила, критерии верификации, конвейер валидации и инварианты аудита архитектурных и проектных решений (`Decision Records`) в системе CKS.

Протокол обеспечивает защиту базы знаний от невалидных предположений и галлюцинаций (Anti-Poisoning), гарантирует воспроизводимость доказательной базы и связывает цикл принятия решений с неизменяемым каноном CKS.

---

## Границы ответственности и закон физического размещения (Boundaries & Storage Law)

- **Физическая граница данных (`C:\GIT\` Boundary):**
  100% конфигураций агентов, состояний, профилей, телеметрии и рабочих данных физически располагаются **исключительно внутри каталога `C:\GIT\`**. Физическое сохранение за пределами `C:\GIT\` исключено.
  Отображение пользовательских каталогов Windows выполнено через архитектуру NTFS Junctions:
  - `~/.gemini` ➔ `C:\GIT\.gemini\` (глобальные политики, навыки, конфигурации, профили)
  - `~/.kat9i` ➔ `C:\GIT\.kat9i\` (локальное состояние платформы, блокировки совместной работы, базы телеметрии)

- **Разделение слоёв (Separation of Concerns):**
  - **CKS (Knowledge & Canon Layer):** Канонический уровень архитектурных решений, моделей знаний, реестров доказательств (`Evidence`) и неизменяемой истории изменений (`History`). CKS не зависит от сред выполнения или деталей интерфейса (Electron GUI).
  - **KAT9I_OS & Antigravity (Execution & Runtime Layer):** Внешний исполнительный слой (оркестрация задач, вызовы LLM, воркеры, рабочие процессы).
  - **Правило суверенитета:** Решение фиксирует архитектурный факт системы CKS, а не временное состояние конкретного агента.

---

## Конвейер жизненного цикла решения (Decision Lifecycle Flow)

Процесс принятия и подтверждения решения следует строгому циклу:

```text
[GAP / Проблема]
      ↓
[EVIDENCE / Доказательства]
      ↓
[PROPOSAL / Предложение решения]
      ↓
[VERIFICATION GATE / Аудит независимым контроллером]
      ↓
[DECISION ACCEPTED / Принято]
      ↓
[CANON PROMOTION / Включение в канон]
      ↓
[SUPERSEDED / Замещение новой ревизией]
```

### Запреты слоя решений:
```text
Proposal ≠ Decision
Draft ≠ Accepted
Worker Report ≠ Decision
Decision ≠ Canon (до прохождения Canon Promotion Gate)
```

---

## Критерии верификации решений (Verification Gates)

Каждое решение перед переводом в статус `ACCEPTED` проходит 7 обязательных проверочных шлюзов:

### Gate 1: Источник проблемы (Problem / GAP Gate)
- Решение обязано явно ссылаться на исходную проблему: идентификатор открытого GitHub Issue, запись в реестре разрывов (`GAP_REGISTER`) или архитектурный инцидент.
- Абстрактные решения без подтверждённого контекста и цели отклоняются (`REJECTED`).

### Gate 2: Доказательная база (Evidence Gate)
- Обязательно наличие списка проверяемых доказательств (`evidence_refs`).
- Доказательством признаются:
  - автоматические детерминированные тесты (pytest, unittest);
  - контрольные логи и дампы проверок CI (`tools/cks_ci.py`);
  - канонические ссылки на существующие схемы и спецификации.
- Предположения модели LLM без доказательств не допускаются в качестве основания для решения.

### Gate 3: Анализ альтернатив (Alternative Analysis Gate)
- В поле `options` должны быть представлены минимум две альтернативы (включая отвергнутые варианты).
- Для каждой отвергнутой альтернативы должно быть дано краткое техническое обоснование причин отказа в поле `rationale`.

### Gate 4: Независимость аудитора (Anti-Poisoning Law)
- Проверка решения осуществляется независимым агентом в роли аудитора решений (`Decision Auditor` / `WORKER QA`).
- Автор предложения (`Proposal Author`) категорически не имеет права утверждать собственное решение.

### Gate 5: Фиксация точного коммита (Exact SHA Boundary)
- Вердикт аудита валиден исключительно для точного хэша коммита (`Exact HEAD SHA`) и базового коммита (`BASE_SHA`).
- Любое изменение файлов или добавление нового коммита аннулирует предыдущий вердикт и возвращает решение на повторный аудит.

### Gate 6: Неизменяемость (Immutability & Superseding)
- Принятые решения неизменяемы по принципу Event Sourcing.
- Исправление или отмена принятого решения производится исключительно публикацией нового решения, ссылающегося на предыдущее с отношением `supersedes`.

### Gate 7: Канонический язык (Language Canon)
- Документация решений, спецификации и отчёты аудита оформляются на русском языке как основном каноническом слое CKS согласно общему правилу локализации.

---

## Машинный контракт верификации решений (YAML Contract)

```yaml
schema_name: cks_decision_verification_protocol_v3
version: "3.0"
purpose: Contract for automated verification and auditing of CKS decision records.

decision_states:
  - DRAFT
  - REVIEW
  - ACCEPTED
  - REJECTED
  - SUPERSEDED

verification_gates:
  - id: GATE_01_GAP
    name: "GAP & Context Verification"
    required: true
    rule: "Decision must reference a valid GAP, Issue ID, or architectural objective."

  - id: GATE_02_EVIDENCE
    name: "Evidence Traceability"
    required: true
    rule: "Field evidence_refs must contain at least one verifiable proof artifact."

  - id: GATE_03_ALTERNATIVES
    name: "Alternative Options Check"
    required: true
    rule: "At least 2 options must be documented with explicit selection rationale."

  - id: GATE_04_INDEPENDENCE
    name: "Anti-Poisoning Auditor Independence"
    required: true
    rule: "Auditor must not be the author of the decision proposal."

  - id: GATE_05_SHA_PINNING
    name: "Exact SHA Pinning"
    required: true
    rule: "Verdict binds strictly to exact commit SHA."

  - id: GATE_06_IMMUTABILITY
    name: "Append-Only Immutability"
    required: true
    rule: "Accepted decisions cannot be modified; superseded via new decision records only."

  - id: GATE_07_LANGUAGE
    name: "Russian Language Canon"
    required: true
    rule: "Decision documentation must adhere to Russian language canonical standard."

required_fields:
  - id
  - title
  - context
  - options
  - selected_option
  - rationale
  - evidence_refs
  - status
  - exact_sha
  - auditor_id
```

---

## Формат отчёта аудитора (WORKER_REPORT v1)

Результаты проверки решений оформляются по единому стандарту `WORKER_REPORT v1`:

```text
🤖 CKS WORKER REPORT

TASK: #350 (architecture: создать CKS Протокол проверки решений v3)

📌 Classification
ABC: A
XYZ: X
Complexity: 8/10
Risk: LOW

⚙️ Execution
Status: DONE
Progress: [██████████] 100%

📊 Metrics
Evidence Coverage: 100%
Traceability: 100%
Protocol Compliance: 100%

🔍 Validation
QA: PASS (tests/test_cks_decision_verification_protocol_v3.py)
Review: READY

📦 Result
STATUS: PASS
Evidence:
  - docs/CKS_DECISION_VERIFICATION_PROTOCOL_v3.md
  - schemas/cks_decision_verification_protocol_v3.yaml
  - tests/test_cks_decision_verification_protocol_v3.py
Blockers: []
Next: Create Pull Request, handoff to QA Controller
```

---

## Совместимость (Compatibility)

- **Версия протокола CKS:** `v3`
- **Базовый контракт решения:** `schemas/decision_record_v1.yaml`
- **Протокол воркера:** `docs/CKS_WORKER_STATE_PROTOCOL_v3.md`
- **Шлюз продвижения в канон:** `docs/CKS_CANON_PROMOTION_GATE_v1_RU.md`
- **Хранение данных:** Физически строго `C:\GIT\` через NTFS Junctions.
