# CKS POST-SNAPSHOT INTEGRITY AUDIT — E3.2-B VERIFIED

Дата: 2026-09-17

Статус: **E3.2-B VERIFIED + CI + GITHUB CHECKPOINT**

Назначение: минимально закрыть разрыв зависимостей в автоматическом запуске интегральной проверки Knowledge Runtime. Документ является validation/audit evidence, не Decision и не Canon. Frozen Core CKS v1.2 не изменялся.

## 1. Наследуемая проверенная база

Не переоткрывались и остаются контрольными точками:

- E2 checkpoint: `302660ecca9f039f274c73905235577fa27b0d41`;
- E3.1-A checkpoint: `5f6cbf6a61200b2b3054e6a4176ce3fe00d4b2f9`;
- E3.1-B checkpoint: `20d4263a0ff78701c73fffe2f0840f6fa6669b2d`;
- E3.1-C complete checkpoint: `195b62ce550f65012fa113ca0845ba74feff8696`;
- E3.2-A verified checkpoint: `788c948cc205ad50833caba81330f6adcced90f6`.

## 2. Исходный дефект

Workflow:

`.github/workflows/cks-knowledge-runtime-intelligence.yml`

выполняет:

`python tools/cks_governance_runner.py ...`

а Governance Runner транзитивно вызывает:

`tools/cks_ci.py --mode all`.

При этом `tools/cks_ci.py` отсутствовал в обоих списках путей, вызывающих интегральный workflow:

- `push.paths`;
- `pull_request.paths`.

Следствие: изменение основного CI-валидатора могло не запускать интегральную Knowledge Runtime regression автоматически.

## 3. Минимальное исправление

В `.github/workflows/cks-knowledge-runtime-intelligence.yml` добавлен ровно один зависимый путь:

```yaml
- 'tools/cks_ci.py'
```

Он добавлен в оба фильтра:

- `push.paths`;
- `pull_request.paths`.

Других изменений workflow в этом проходе не выполнялось.

Commit исправления:

`e9ba67f840fd5afe2d2e6a0661bdf0b6db85a18d`

## 4. Фактическое доказательство GitHub Actions

Все проверки ниже относятся к head SHA:

`e9ba67f840fd5afe2d2e6a0661bdf0b6db85a18d`

### 4.1 Интегральный Knowledge Runtime

- workflow: `CKS — рабочий контур и аналитика знаний`;
- run: `35168683058`;
- event: `push`;
- status: `completed`;
- conclusion: `success`.

Сам факт автоматического создания этого run после изменения workflow подтверждает, что интегральный контур запускается по новой зависимости; полный успешный результат подтверждает отсутствие регрессии в его содержательных проверках.

### 4.2 Общий CKS Validation

- run: `35168682966`;
- status: `completed`;
- conclusion: `success`.

### 4.3 Runtime Governance

- workflow: `CKS — проверка рабочего ядра и архитектуры`;
- run: `35168682968`;
- status: `completed`;
- conclusion: `success`.

Таким образом, E3.2-B закрыт не только статическим изменением YAML, но и фактическим автоматическим запуском зависимого интегрального workflow плюс перекрёстной регрессией двух основных контуров.

## 5. Что намеренно НЕ менялось

В E3.2-B не менялись:

- сами валидаторы и их логика;
- shallow/duplicate workflow;
- Node.js Actions versions;
- Canon;
- Frozen Core CKS v1.2.

## 6. Точка продолжения

```text
POST-SNAPSHOT INTEGRITY AUDIT

E1      v1.6 false-green                       ✅ VERIFIED + CI
E2      v1.7 + Self Audit + v1.4              ✅ VERIFIED + CI + CHECKPOINT
E3.1    all 17 workflows                      ✅ COMPLETE + CHECKPOINTS A/B/C
E3.2-A  repair 2 confirmed false-greens       ✅ VERIFIED + CI + CHECKPOINT
E3.2-B  integral trigger dependency gap       ✅ VERIFIED + CI + CHECKPOINT
E3.2-C  shallow/duplicate workflow cleanup    ← NEXT SMALL GROUP
E3.3    Node.js Actions debt                   ⏳
E3.4    final post-snapshot regression         ⏳
```

После разрыва не повторять E1/E2/E3.1/E3.2-A/E3.2-B. Продолжать с **E3.2-C**.

E3.2-C начинать не с удаления workflow, а с малого аналитического прохода: точно сопоставить shallow/duplicate проверки, их события запуска и уникальное покрытие, чтобы объединение или удаление не создало новую дыру CI.
