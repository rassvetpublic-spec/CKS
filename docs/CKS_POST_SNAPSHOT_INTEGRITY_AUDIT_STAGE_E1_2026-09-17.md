# CKS — пост-снимочный аудит целостности, этап E1

**Дата:** 17.09.2026  
**Статус:** ЗАВЕРШЁН И ПОДТВЕРЖДЁН CI.  
**Тип документа:** рабочий audit report (отчёт аудита), не Decision и не Canon.

## Зачем появился этап E1

После закрытия операции FULL KNOWLEDGE SNAPSHOT был выполнен дополнительный проход по предыдущим результатам, пока рабочий контекст ещё был доступен. Цель — искать не новые функции, а слабые места и ложноположительные проверки в уже существующих слоях.

## Найденный дефект

Обнаружен реальный **false-green CI** — ложноположительный зелёный CI — в историческом контуре `CKS v1.6 Intelligence Runtime`.

До исправления:

- `.github/workflows/cks-v1-6-intelligence-runtime.yml` выполнял только `python tools/cks_v1_6_intelligence_runtime.py`;
- `tools/cks_v1_6_intelligence_runtime.py` лишь объявлял классы и при прямом запуске фактически ничего не проверял;
- `tools/cks_canon_conflict_detector.py` всегда возвращал пустой список;
- `tools/cks_knowledge_health_score.py` всегда возвращал `0`.

Следовательно, workflow мог завершаться успешно даже при отсутствии реальной проверки Intelligence Runtime. Этот дефект не был выявлен предыдущим FULL KNOWLEDGE SNAPSHOT и показывает, что успешный общий CI нельзя автоматически трактовать как доказательство содержательности каждого исторического workflow.

## Исправление

Исторический v1.6 слой не превращён во второй независимый Runtime. Он сохранён как **compatibility facade — слой совместимости** поверх актуального рабочего контура.

Изменения:

1. `tools/cks_canon_conflict_detector.py`
   - теперь использует `KnowledgeIntelligence.conflict_signals()`;
   - учитывает только явные конфликтные отношения и статус `disputed`;
   - не интерпретирует свободный текст;
   - сохраняет старый тип результата — список конфликтов.

2. `tools/cks_knowledge_health_score.py`
   - для объектов знаний использует реальный `KnowledgeIntelligence.quality_audit()`;
   - для исторического интерфейса нормализованных метрик считает тот же взвешенный диагностический score 0..100;
   - не создаёт Decision и не изменяет Canon.

3. `tools/cks_v1_6_intelligence_runtime.py`
   - при обычном встроенном запуске использует актуальные `KnowledgeRuntime` и `KnowledgeIntelligence`;
   - сохраняет режим внешних legacy-модулей;
   - прямой CLI-запуск больше не является пустой операцией;
   - добавлен детерминированный `self_check()`.

4. `tests/test_cks_v1_6_compatibility_runtime.py`
   - 7 исполняемых регрессионных тестов;
   - проверяется реальный конфликт, отсутствие выдуманных конфликтов, health score, legacy metrics, текущий Intelligence stack, legacy module mode и CLI self-check.

5. `.github/workflows/cks-v1-6-intelligence-runtime.yml`
   - добавлен `push` trigger по релевантным файлам;
   - добавлен Python 3.12;
   - py_compile;
   - исполняемые unittest;
   - обязательный реальный self-check.

## Коммиты

- `857c812f911eee0870eff1000abe4d0c49f8f99f` — реальный compatibility detector конфликтов;
- `c7c8ad54195af67e87a43aaa976e87b833ae1454` — реальная compatibility оценка качества;
- `1730909d92a0647b5a7ea90ae5837c61bdf214c9` — рабочий v1.6 compatibility runtime и self-check;
- `2df184135b8b988eb7e894c40b9d616a4dc882e8` — 7 регрессионных тестов;
- `2ac56bb898a1dc4c54a221b2fe0f56765e88dd09` — исполняемый CI вместо false-green workflow.

## Подтверждённый GitHub Actions run

- workflow: `CKS v1.6 Intelligence Runtime`;
- run id: `35163494312`;
- job id: `105019319966`;
- head commit: `2ac56bb898a1dc4c54a221b2fe0f56765e88dd09`;
- Python: `3.12.14`;
- conclusion: `success`.

Фактически выполнено:

- синтаксис трёх compatibility-модулей — success;
- 7 unittest — все `ok`;
- self-check — `PASS`;
- `validation_pass: true`;
- `real_intelligence_report: true`;
- `explicit_conflict_detected: true`;
- `health_is_computed: true`;
- `event_recorded: true`;
- `diagnostic_authority: true`;
- вычисленный health score эталонного набора: `63.3`;
- явно обнаружены два конфликтных сигнала: `status:disputed` и `relation:conflicts_with`.

## Что перепроверено из предыдущих результатов

Этот проход не отменяет успешный интегральный run FULL KNOWLEDGE SNAPSHOT `35162449046`, но уточняет его смысл: он действительно подтвердил основной Knowledge Runtime / Intelligence, этапы B/D, Self Audit и Governance, однако отдельный исторический v1.6 workflow до E1 был содержательно слабым и давал false-green.

То есть предыдущий итог «основной рабочий контур проходит интегральную регрессию» остаётся подтверждённым, а более сильная формулировка «каждый исторический CI-контур содержательно проверяет заявленную функцию» была бы неверной.

## Следующие цели пост-снимочного аудита

Этап E1 специально ограничен v1.6 false-green контуром. Следующий отдельный проход должен проверить:

- исторические v1.7 вспомогательные модули на дублирование или слишком слабые проверки;
- глубину `cks_self_audit.py`: способен ли он обнаруживать пустые/ложноположительные compatibility-реализации, а не только основной Runtime;
- остальные workflows на pattern «скрипт запускается и возвращает 0, но содержательной проверки нет»;
- P2-долг внешних GitHub Actions с предупреждением Node.js 20.

## Архитектурные границы

- compatibility facade ≠ новый SSOT;
- метрика качества ≠ Decision;
- conflict signal ≠ автоматическое решение конфликта;
- успешный CI ≠ Canon;
- этот audit report ≠ изменение frozen Core v1.2.
