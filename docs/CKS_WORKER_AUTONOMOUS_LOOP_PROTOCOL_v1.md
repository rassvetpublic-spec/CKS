# Протокол автономного цикла воркера CKS (CKS WORKER AUTONOMOUS LOOP PROTOCOL v1)

## Назначение (Purpose)

Определение автономного цикла `Worker` (воркера / исполнителя) для поиска задач, их выполнения и формирования отчётности на базе GitHub.

## Репозиторий (Repository)

REPOSITORY:
https://github.com/rassvetpublic-spec/CKS

## Автономный цикл (Loop)

READ PROJECT (чтение проекта)
↓
SCAN ISSUES (сканирование задач)
↓
CLAIM TASK (взятие задачи)
↓
EXECUTE (выполнение)
↓
REPORT (отчётность)
↓
CHECK CHANGES (проверка изменений)
↓
RESTART LOOP (перезапуск цикла)

## Поиск задач (Issue discovery)

`Worker` проверяет открытые задачи `Issue` на наличие заданий без назначенного исполнителя.

Если задача существует и исполнитель не назначен:

- взять задачу в работу (`claim`);
- зафиксировать идентификатор воркера (`Worker identity`);
- начать выполнение (`execute`).

## Формат отметки о взятии (Claim format)

CLAIMED:

Worker:

Repository:
https://github.com/rassvetpublic-spec/CKS

Task:

Started:

## Правило канала связи (Channel rule)

Каждая задача воркера обязана объявлять:

REPOSITORY:
TARGET:
CHANNEL:
RETURN FORMAT:

Если `CHANNEL` (канал обратной связи) не указан:

`Worker` обязан оставить комментарий в задаче с указанием, что обсуждение задачи на GitHub (`GitHub Issue conversation`) используется в качестве резервного канала связи.

## Формирование отчёта (Reporting)

Если существует шаблон отчёта (`report template`), использовать его.

Если специализированного шаблона нет:

STATUS:
PASS / FAIL / BLOCKED

DONE:
-

EVIDENCE:
-

BLOCKERS:
-

NEXT:
-

## Отслеживание изменений (Change detection)

После завершения задачи `Worker` повторяет сканирование `Issue`.

Появление новой задачи, обновление существующей задачи или релевантные изменения в GitHub перезапускают цикл с этапа `READ PROJECT` (чтение проекта).
