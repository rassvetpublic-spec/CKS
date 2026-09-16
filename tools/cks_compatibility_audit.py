#!/usr/bin/env python3
"""Исполняемый аудит исторических compatibility-слоёв CKS.

Проверяет, что старые v1.4/v1.6/v1.7 интерфейсы не являются пустыми
заглушками и действительно выполняют заявленные диагностические операции.
Модуль не является Runtime, SSOT, Decision или Canon.
"""
from __future__ import annotations

import json
from typing import Any

from cks_canon_conflict_detector import detect_conflicts
from cks_knowledge_health_score import calculate_health as calculate_v16_health
from cks_v1_4_dashboard_runtime import build_dashboard
from cks_v1_4_graph_builder import build_graph
from cks_v1_4_metrics_calculator import KnowledgeMetrics, calculate_health as calculate_v14_health
from cks_v1_4_migration_adapter import migrate_object
from cks_v1_4_review_gate_runner import run_gate
from cks_v1_6_intelligence_runtime import self_check as v16_self_check
from cks_v1_7_graph_validator import validate_graph, validate_graph_report
from cks_v1_7_orphan_node_detector import find_orphans
from cks_v1_7_relation_engine import RelationEngine


def _knowledge(object_id: str, *, status: str = "knowledge", relations=None) -> dict[str, Any]:
    return {
        "id": object_id,
        "title": object_id,
        "type": "knowledge",
        "status": status,
        "owner": "CKS",
        "lifecycle": "knowledge",
        "clusters": ["compatibility"],
        "tags": ["audit", "compatibility"],
        "projects": ["CKS"],
        "relations": list(relations or []),
        "evidence": ["CKS-EVD-COMPAT"],
        "history": [{"status": "validated"}],
        "signals": {"confidence": 0.8, "novelty": 0.4, "uncertainty": 0.2, "importance": 0.7},
    }


def run_compatibility_audit() -> dict[str, Any]:
    checks: dict[str, bool] = {}
    details: dict[str, Any] = {}

    # v1.4: функции должны вычислять данные, а не только импортироваться.
    metrics = calculate_v14_health(KnowledgeMetrics(80, 90, 70, 60))
    checks["v1_4_metrics_computed"] = metrics.get("health_score") == 75

    legacy_objects = [
        {"id": "A", "type": "knowledge", "relations": [{"source": "A", "target": "B", "relation": "supports"}]},
        {"id": "B", "type": "evidence", "relations": []},
    ]
    legacy_graph = build_graph(legacy_objects)
    checks["v1_4_graph_built"] = len(legacy_graph.get("nodes", [])) == 2 and len(legacy_graph.get("edges", [])) == 1
    checks["v1_4_review_gate_meaningful"] = (
        run_gate({"schema": True, "evidence": True}).get("status") == "PASS"
        and run_gate({"schema": True, "evidence": False}).get("status") == "WARN"
    )
    source = {"id": "legacy"}
    migrated = migrate_object(source)
    checks["v1_4_migration_non_mutating"] = source == {"id": "legacy"} and migrated.get("version") == "1.4"
    dashboard = build_dashboard(metrics=metrics, graph=legacy_graph, review={"status": "PASS"})
    checks["v1_4_dashboard_derived_only"] = dashboard.get("is_source_of_truth") is False

    # v1.6: предыдущий false-green должен оставаться исправленным.
    first = _knowledge(
        "CKS-KNW-COMPAT-1",
        status="disputed",
        relations=[{"target": "CKS-KNW-COMPAT-2", "type": "conflicts_with"}],
    )
    second = _knowledge("CKS-KNW-COMPAT-2")
    conflicts = detect_conflicts([first, second])
    health = calculate_v16_health([first, second])
    v16 = v16_self_check()
    checks["v1_6_explicit_conflict_detected"] = any(item.get("signal") == "relation:conflicts_with" for item in conflicts)
    checks["v1_6_health_computed"] = isinstance(health, (int, float)) and 0.0 < float(health) <= 100.0
    checks["v1_6_self_check_passes"] = v16.get("status") == "PASS"

    # v1.7: helper-функции должны опираться на текущий KnowledgeGraph и
    # различать валидный граф, битую ссылку, недопустимую связь и orphan.
    nodes = [{"id": "N1", "type": "knowledge"}, {"id": "N2", "type": "evidence"}, {"id": "N3", "type": "knowledge"}]
    valid_edges = [{"source": "N1", "target": "N2", "relation": "supports"}]
    broken_edges = valid_edges + [{"source": "N1", "target": "MISSING", "relation": "depends_on"}]
    invalid_relation_edges = [{"source": "N1", "target": "N2", "relation": "not_allowed_relation"}]
    checks["v1_7_valid_graph_has_no_failures"] = validate_graph(nodes, valid_edges) == []
    checks["v1_7_broken_reference_detected"] = "broken_edge_reference" in validate_graph(nodes, broken_edges)
    checks["v1_7_invalid_relation_detected"] = "invalid_relation" in validate_graph(nodes, invalid_relation_edges)
    orphan_ids = {item.get("id") for item in find_orphans(nodes, valid_edges)}
    checks["v1_7_orphan_detected"] = orphan_ids == {"N3"}
    detailed = validate_graph_report(nodes, valid_edges)
    checks["v1_7_validator_uses_runtime_report"] = detailed.get("runtime", {}).get("edges") == 1

    relation_engine = RelationEngine()
    relation_engine.add_relation("R1", "R2", "supports")
    checks["v1_7_relation_engine_real_graph"] = (
        len(relation_engine.find("supports")) == 1
        and relation_engine.graph.validate().get("status") == "PASS"
    )

    details.update(
        {
            "v1_4_health": metrics,
            "v1_6_health": health,
            "v1_6_conflicts": conflicts,
            "v1_7_validation": detailed,
            "v1_7_orphans": sorted(orphan_ids),
        }
    )
    failed = sorted(name for name, passed in checks.items() if not passed)
    return {
        "schema_version": "1.0",
        "kind": "cks_compatibility_integrity_audit",
        "status": "FAIL" if failed else "PASS",
        "checks": checks,
        "failed_checks": failed,
        "details": details,
        "authority": "validation_only",
    }


def main() -> int:
    result = run_compatibility_audit()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
