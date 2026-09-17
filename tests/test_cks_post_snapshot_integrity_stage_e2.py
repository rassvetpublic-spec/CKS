#!/usr/bin/env python3
"""Этап E2: регрессия исторических compatibility-слоёв и Self Audit."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cks_compatibility_audit import run_compatibility_audit
from cks_self_audit import SelfAudit
from cks_v1_7_graph_validator import validate_graph, validate_graph_report
from cks_v1_7_orphan_node_detector import find_orphans
from cks_v1_7_relation_engine import RelationEngine


class PostSnapshotIntegrityStageE2Tests(unittest.TestCase):
    def test_compatibility_audit_has_no_false_green(self) -> None:
        result = run_compatibility_audit()
        self.assertEqual(result["status"], "PASS", result)
        self.assertEqual(result["failed_checks"], [], result)
        self.assertGreaterEqual(len(result["checks"]), 14)
        self.assertTrue(all(result["checks"].values()), result)
        self.assertEqual(result["authority"], "validation_only")

    def test_v17_validator_distinguishes_valid_broken_and_invalid_relation(self) -> None:
        nodes = [{"id": "A", "type": "knowledge"}, {"id": "B", "type": "evidence"}]
        self.assertEqual(validate_graph(nodes, [{"source": "A", "target": "B", "relation": "supports"}]), [])
        self.assertIn(
            "broken_edge_reference",
            validate_graph(nodes, [{"source": "A", "target": "MISSING", "relation": "supports"}]),
        )
        self.assertIn(
            "invalid_relation",
            validate_graph(nodes, [{"source": "A", "target": "B", "relation": "legacy_unknown"}]),
        )

    def test_v17_detailed_report_is_backed_by_current_runtime(self) -> None:
        report = validate_graph_report(
            [{"id": "A", "type": "knowledge"}, {"id": "B", "type": "evidence"}],
            [{"source": "A", "target": "B", "relation": "supports"}],
        )
        self.assertEqual(report["status"], "PASS", report)
        self.assertEqual(report["runtime"]["nodes"], 2)
        self.assertEqual(report["runtime"]["edges"], 1)
        self.assertEqual(report["authority"], "validation_only")

    def test_v17_orphan_detector_does_not_count_broken_edge_as_connectivity(self) -> None:
        nodes = [{"id": "A"}, {"id": "B"}, {"id": "C"}]
        edges = [
            {"source": "A", "target": "B", "relation": "supports"},
            {"source": "C", "target": "MISSING", "relation": "depends_on"},
        ]
        self.assertEqual({item["id"] for item in find_orphans(nodes, edges)}, {"C"})

    def test_v17_relation_engine_remains_real_graph_facade(self) -> None:
        engine = RelationEngine()
        engine.add_relation("A", "B", "supports")
        self.assertEqual(len(engine.find("supports")), 1)
        self.assertEqual(engine.graph.validate()["status"], "PASS")

    def test_repository_self_audit_now_checks_compatibility_layers(self) -> None:
        result = SelfAudit(ROOT).run()
        self.assertNotEqual(result["status"], "FAIL", result)
        self.assertEqual(result["summary"]["fail"], 0, result)
        self.assertEqual(result["schema_version"], "1.3")
        codes = {item["code"] for item in result["findings"]}
        self.assertNotIn("COMPATIBILITY_LAYER_INTEGRITY", codes)
        self.assertNotIn("COMPATIBILITY_LAYER_EXECUTION", codes)


if __name__ == "__main__":
    unittest.main()
