"""Сравнение версий объектов знаний CKS.

Совместимый фасад поверх рабочего механизма этапа 6. Модуль не изменяет
объекты и возвращает только диагностическую разницу.
"""
from __future__ import annotations

from typing import Any

from cks_knowledge_evolution import KnowledgeEvolution


def compare_versions(old: Any, new: Any) -> dict[str, Any]:
    """Сравнить одну пару объектов или два набора объектов по id.

    Сохраняются исторические ключи added/removed/changed, но теперь они
    содержат реальную вычисленную разницу.
    """
    if isinstance(old, dict) and isinstance(new, dict):
        return KnowledgeEvolution.compare_record_sets([old], [new])
    if isinstance(old, (list, tuple)) and isinstance(new, (list, tuple)):
        return KnowledgeEvolution.compare_record_sets(old, new)
    raise TypeError("old и new должны быть объектами dict или наборами list/tuple")
