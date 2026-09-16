#!/usr/bin/env python3
"""Совместимый вход для построения графа происхождения CKS.

Основная реализация находится в cks_traceability_engine.py.
"""
from __future__ import annotations

from typing import Any

from cks_traceability_engine import TraceabilityEngine


def build_trace_graph(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Построить реальный производный граф и вернуть диагностику ссылок."""
    engine = TraceabilityEngine()
    result = engine.ingest(records)
    payload = engine.export()
    payload["status"] = result["status"]
    payload["summary"] = result
    return payload
