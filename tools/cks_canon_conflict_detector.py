#!/usr/bin/env python3
"""Совместимый детектор конфликтов CKS v1.6.

Исторический модуль оставлен как фасад совместимости. Реальная логика
конфликтных сигналов находится в ``cks_knowledge_intelligence.py``.

Модуль не интерпретирует свободный текст и не создаёт Decision/Canon:
учитываются только явные конфликтные отношения и статус ``disputed``.
"""
from __future__ import annotations

from typing import Any, Iterable

from cks_knowledge_intelligence import KnowledgeIntelligence
from cks_knowledge_runtime import KnowledgeRuntime


def detect_conflicts(objects: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Вернуть явные конфликтные сигналы для старого интерфейса v1.6.

    Историческая функция возвращала список, поэтому тип результата сохранён.
    В отличие от старого заглушечного варианта список теперь вычисляется
    рабочим Knowledge Intelligence (аналитикой знаний).
    """
    runtime = KnowledgeRuntime()
    records = list(objects)
    validation = runtime.ingest(records)
    if validation["status"] == "FAIL":
        raise ValueError(f"Некорректные объекты знаний: {validation['errors']}")
    report = KnowledgeIntelligence(runtime).conflict_signals()
    return list(report["conflicts"])
