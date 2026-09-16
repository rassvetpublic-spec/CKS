"""Защита жизненного цикла CKS.

Старые системные состояния сохранены для обратной совместимости.
Для объектов знаний используется единая машина состояний из tools/cks_knowledge_state_machine.py.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cks_knowledge_state_machine import validate_status as _validate_knowledge_status
from cks_knowledge_state_machine import validate_transition as _validate_knowledge_transition


ALLOWED_STATES = [
    "DISCOVERED",
    "RESEARCHED",
    "PROPOSED",
    "REVIEWED",
    "ACCEPTED",
    "CANONICAL",
    "DEPRECATED",
    "ARCHIVED",
]


def validate_state(state: Any) -> dict[str, Any]:
    """Проверка старого системного жизненного цикла."""
    normalized = str(state or "").strip().upper()
    return {
        "status": "PASS" if normalized in ALLOWED_STATES else "FAIL",
        "state": normalized,
        "scope": "system_lifecycle",
    }


def validate_knowledge_status(state: Any) -> dict[str, Any]:
    """Проверка статуса развития объекта знания."""
    result = _validate_knowledge_status(state)
    result["scope"] = "knowledge_status"
    return result


def validate_transition(current: Any, target: Any, **kwargs: Any) -> dict[str, Any]:
    """Проверка перехода знания. Никаких изменений объекта не выполняет."""
    result = _validate_knowledge_transition(current, target, **kwargs)
    result["scope"] = "knowledge_status_transition"
    return result
