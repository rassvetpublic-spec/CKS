#!/usr/bin/env python3
"""Машина состояний знаний CKS.

Назначение:
- проверять допустимость переходов между статусами развития знания;
- не допускать прямого попадания сырья в канон;
- сохранять совместимость со старыми статусами draft/review/active;
- не изменять объект автоматически: модуль только проверяет переход.
"""
from __future__ import annotations

from typing import Any

from cks_knowledge_runtime import COMPATIBLE_STATUSES, STATUS_ORDER, STATUS_RU


LEGACY_STATUS_MAP = {
    "draft": "raw",
    "review": "validated",
    "active": "knowledge",
}

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "raw": {"captured", "rejected", "archived"},
    "captured": {"normalized", "clustered", "rejected", "archived"},
    "normalized": {"deduplicated", "clustered", "researched", "rejected", "archived"},
    "deduplicated": {"clustered", "researched", "rejected", "archived"},
    "clustered": {"researched", "understood", "connected", "rejected", "archived"},
    "researched": {"understood", "connected", "validated", "rejected", "archived"},
    "understood": {"connected", "validated", "knowledge", "disputed", "archived"},
    "connected": {"validated", "knowledge", "disputed", "archived"},
    "validated": {"knowledge", "canonical", "disputed", "archived"},
    "knowledge": {"evolving", "canonical", "disputed", "superseded", "archived"},
    "canonical": {"evolving", "disputed", "superseded", "archived"},
    "evolving": {"validated", "knowledge", "canonical", "disputed", "superseded", "archived"},
    "disputed": {"researched", "validated", "knowledge", "canonical", "superseded", "archived"},
    "superseded": {"archived"},
    "archived": set(),
    "rejected": set(),
}


def canonical_status(status: Any) -> str:
    value = str(status or "").strip().lower()
    return LEGACY_STATUS_MAP.get(value, value)


def validate_status(status: Any) -> dict[str, Any]:
    raw = str(status or "").strip().lower()
    canonical = canonical_status(raw)
    valid = raw in COMPATIBLE_STATUSES and canonical in STATUS_ORDER
    return {
        "status": "PASS" if valid else "FAIL",
        "input": raw,
        "canonical": canonical,
        "label_ru": STATUS_RU.get(raw) or STATUS_RU.get(canonical) or raw,
        "legacy_alias": raw in LEGACY_STATUS_MAP,
    }


def validate_transition(
    current: Any,
    target: Any,
    *,
    reason: str | None = None,
    evidence_count: int = 0,
    decision_ref: str | None = None,
) -> dict[str, Any]:
    """Проверить переход статуса без изменения объекта."""
    source = canonical_status(current)
    destination = canonical_status(target)
    errors: list[str] = []
    warnings: list[str] = []

    if source not in STATUS_ORDER:
        errors.append(f"неизвестный исходный статус: {current}")
    if destination not in STATUS_ORDER:
        errors.append(f"неизвестный целевой статус: {target}")
    if errors:
        return {
            "status": "FAIL",
            "from": source,
            "to": destination,
            "errors": errors,
            "warnings": warnings,
        }

    if source == destination:
        warnings.append("статус не изменяется")
    elif destination not in ALLOWED_TRANSITIONS[source]:
        errors.append(f"переход {source} -> {destination} не разрешён")

    if source in {"archived", "rejected"} and destination != source:
        errors.append(f"статус {source} является терминальным")

    if destination == "canonical":
        if evidence_count < 1:
            errors.append("для canonical требуется хотя бы одно доказательство")
        if not str(decision_ref or "").strip():
            errors.append("для canonical требуется ссылка на решение")

    if source in STATUS_ORDER and destination in STATUS_ORDER:
        source_index = STATUS_ORDER.index(source)
        target_index = STATUS_ORDER.index(destination)
        if target_index < source_index and source != destination and not str(reason or "").strip():
            errors.append("обратный переход требует причины")

    return {
        "status": "FAIL" if errors else "PASS",
        "from": source,
        "to": destination,
        "from_ru": STATUS_RU.get(source, source),
        "to_ru": STATUS_RU.get(destination, destination),
        "errors": errors,
        "warnings": warnings,
        "authority": "validation_only",
    }


def validate_record_transition(record: dict[str, Any], target: Any, *, reason: str | None = None) -> dict[str, Any]:
    evidence = record.get("evidence") or []
    decision_ref = record.get("decision")
    traceability = record.get("traceability")
    if not decision_ref and isinstance(traceability, dict):
        decision_ref = traceability.get("decision") or traceability.get("decision_ref")
    return validate_transition(
        record.get("status"),
        target,
        reason=reason,
        evidence_count=len(evidence) if isinstance(evidence, list) else 0,
        decision_ref=str(decision_ref or ""),
    )
