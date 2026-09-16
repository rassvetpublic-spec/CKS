#!/usr/bin/env python3
"""Совместимый Knowledge Health Score (оценка качества знаний) CKS v1.6.

Исторический модуль сохранён как фасад совместимости. Для наборов объектов
используется реальный ``KnowledgeIntelligence.quality_audit``. Для старого
входа в виде нормализованных метрик применяется та же весовая модель качества.

Результат является диагностической метрикой и не является Decision/Canon.
"""
from __future__ import annotations

from typing import Any, Iterable

from cks_knowledge_intelligence import KnowledgeIntelligence
from cks_knowledge_runtime import KnowledgeRuntime


_WEIGHTS = {
    "completeness": 0.25,
    "evidence": 0.25,
    "connectivity": 0.20,
    "classification": 0.15,
    "history": 0.15,
}


def _score_metrics(metrics: dict[str, Any]) -> float:
    missing = [name for name in _WEIGHTS if name not in metrics]
    if missing:
        raise ValueError("Не хватает метрик качества: " + ", ".join(missing))
    total = 0.0
    for name, weight in _WEIGHTS.items():
        value = metrics[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"Метрика {name} должна быть числом 0..1")
        value = float(value)
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"Метрика {name} должна быть в диапазоне 0..1")
        total += weight * value
    return round(total * 100.0, 1)


def calculate_health(metrics: Any) -> float:
    """Вычислить реальную диагностическую оценку качества 0..100.

    Поддерживаются два совместимых режима:
    - dict с пятью нормализованными метриками старого интерфейса;
    - список/кортеж объектов знаний либо dict с ключом ``objects``.
    """
    if isinstance(metrics, dict) and all(name in metrics for name in _WEIGHTS):
        return _score_metrics(metrics)

    if isinstance(metrics, dict) and isinstance(metrics.get("objects"), list):
        records: Iterable[dict[str, Any]] = metrics["objects"]
    elif isinstance(metrics, (list, tuple)):
        records = metrics
    else:
        raise TypeError(
            "Ожидается словарь нормализованных метрик, список объектов знаний "
            "или словарь {'objects': [...]}"
        )

    runtime = KnowledgeRuntime()
    validation = runtime.ingest(list(records))
    if validation["status"] == "FAIL":
        raise ValueError(f"Некорректные объекты знаний: {validation['errors']}")
    report = KnowledgeIntelligence(runtime).quality_audit()
    return float(report["average_score"])
