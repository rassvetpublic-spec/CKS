#!/usr/bin/env python3
"""Совместимый оркестратор CKS v1.6 Intelligence Runtime.

Исторический интерфейс ``IntelligenceRuntime`` сохранён, но пустой запуск больше
не является успешной заглушкой. Если внешние модули не переданы, оркестратор
использует актуальные рабочие реализации Knowledge Runtime / Intelligence,
детектора конфликтов и оценки качества.

Модуль диагностический: он не принимает Decision и не изменяет Canon.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

from cks_canon_conflict_detector import detect_conflicts
from cks_knowledge_health_score import calculate_health
from cks_knowledge_intelligence import KnowledgeIntelligence
from cks_knowledge_runtime import KnowledgeRuntime


@dataclass
class IntelligenceEvent:
    event_type: str
    object_id: str
    payload: dict[str, Any] = field(default_factory=dict)


def _extract_records(context: Any) -> list[dict[str, Any]]:
    if isinstance(context, list):
        return list(context)
    if isinstance(context, tuple):
        return list(context)
    if isinstance(context, dict):
        if isinstance(context.get("records"), list):
            return list(context["records"])
        if isinstance(context.get("objects"), list):
            return list(context["objects"])
        if context.get("id"):
            return [dict(context)]
    raise TypeError("context должен быть объектом знания или содержать records/objects")


class IntelligenceRuntime:
    """Старый интерфейс v1.6 поверх актуального рабочего слоя."""

    def __init__(self, modules: Iterable[Any] | None = None):
        # None означает актуальный встроенный стек. Явный [] сохраняет старый
        # режим внешней оркестрации и не подменяется встроенными модулями.
        self.modules = None if modules is None else list(modules)
        self.events: list[IntelligenceEvent] = []

    def run(self, context: Any) -> dict[str, Any]:
        if self.modules is not None:
            results: dict[str, Any] = {}
            for module in self.modules:
                if not hasattr(module, "run"):
                    raise TypeError(f"Модуль {module!r} не имеет метода run(context)")
                results[module.__class__.__name__] = module.run(context)
        else:
            records = _extract_records(context)
            runtime = KnowledgeRuntime()
            validation = runtime.ingest(records)
            if validation["status"] == "FAIL":
                raise ValueError(f"Некорректные объекты знаний: {validation['errors']}")
            intelligence = KnowledgeIntelligence(runtime)
            results = {
                "validation": validation,
                "KnowledgeIntelligence": intelligence.full_report(),
                "CanonConflictDetector": detect_conflicts(records),
                "KnowledgeHealthScore": calculate_health(records),
                "authority": "analysis_and_suggestions_only",
            }

        object_id = "unknown"
        if isinstance(context, dict):
            object_id = str(context.get("id") or context.get("run_id") or "unknown")
        self.events.append(IntelligenceEvent("runtime.completed", object_id, results))
        return results


def _self_check_records() -> list[dict[str, Any]]:
    return [
        {
            "id": "CKS-KNW-9601",
            "title": "Проверяемый объект A",
            "type": "knowledge",
            "status": "disputed",
            "owner": "CKS",
            "lifecycle": "knowledge",
            "clusters": ["runtime"],
            "tags": ["cks", "intelligence"],
            "projects": ["CKS"],
            "relations": [{"target": "CKS-KNW-9602", "type": "conflicts_with"}],
            "evidence": ["CKS-EVD-9601"],
            "history": [{"status": "validated"}],
            "signals": {"confidence": 0.7, "novelty": 0.4, "uncertainty": 0.3, "importance": 0.8},
        },
        {
            "id": "CKS-KNW-9602",
            "title": "Проверяемый объект B",
            "type": "knowledge",
            "status": "knowledge",
            "owner": "CKS",
            "lifecycle": "knowledge",
            "clusters": ["runtime"],
            "tags": ["cks", "intelligence"],
            "projects": ["CKS"],
            "relations": [],
            "evidence": ["CKS-EVD-9602"],
            "history": [{"status": "clustered"}, {"status": "validated"}],
            "signals": {"confidence": 0.8, "novelty": 0.5, "uncertainty": 0.2, "importance": 0.7},
        },
    ]


def self_check() -> dict[str, Any]:
    runtime = IntelligenceRuntime()
    result = runtime.run({"run_id": "v1.6-compat-self-check", "records": _self_check_records()})
    intelligence = result.get("KnowledgeIntelligence") or {}
    conflicts = result.get("CanonConflictDetector") or []
    health = result.get("KnowledgeHealthScore")
    checks = {
        "validation_pass": (result.get("validation") or {}).get("status") == "PASS",
        "real_intelligence_report": intelligence.get("kind") == "cks_knowledge_intelligence",
        "explicit_conflict_detected": len(conflicts) >= 1,
        "health_is_computed": isinstance(health, (int, float)) and float(health) > 0.0,
        "event_recorded": bool(runtime.events) and runtime.events[-1].event_type == "runtime.completed",
        "diagnostic_authority": result.get("authority") == "analysis_and_suggestions_only",
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema_version": "1.0",
        "kind": "cks_v1_6_compatibility_self_check",
        "status": status,
        "checks": checks,
        "health_score": health,
        "conflicts": conflicts,
        "event": asdict(runtime.events[-1]) if runtime.events else None,
        "authority": "validation_only",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CKS v1.6: совместимый запуск реального Intelligence Runtime")
    parser.add_argument("--input", help="JSON с объектом, массивом объектов либо records/objects")
    parser.add_argument("--output", help="Куда записать JSON-результат")
    parser.add_argument("--self-check", action="store_true", help="Выполнить детерминированную самопроверку совместимости")
    args = parser.parse_args(argv)

    if args.input:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        result: dict[str, Any] = IntelligenceRuntime().run(payload)
        exit_code = 0
    else:
        # Пустой CLI-вызов исторически использовался в CI. Теперь он обязан
        # выполнить реальную проверку, а не просто импортировать определения.
        result = self_check()
        exit_code = 0 if result["status"] == "PASS" else 1

    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    print(text, end="")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
