#!/usr/bin/env python3
"""Регрессия совместимости исторического CKS v1.6 Intelligence Runtime.

Цель теста — не допустить возврата пустых заглушек и ложного зелёного CI.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cks_canon_conflict_detector import detect_conflicts
from cks_knowledge_health_score import calculate_health
from cks_v1_6_intelligence_runtime import IntelligenceRuntime, self_check


def _records():
    return [
        {
            "id": "CKS-KNW-9611",
            "title": "A",
            "type": "knowledge",
            "status": "disputed",
            "owner": "tests",
            "lifecycle": "knowledge",
            "clusters": ["runtime"],
            "tags": ["cks", "compat"],
            "projects": ["CKS"],
            "relations": [{"target": "CKS-KNW-9612", "type": "conflicts_with"}],
            "evidence": ["CKS-EVD-9611"],
            "history": [{"status": "validated"}],
            "signals": {"confidence": 0.7, "novelty": 0.4, "uncertainty": 0.3, "importance": 0.8},
        },
        {
            "id": "CKS-KNW-9612",
            "title": "B",
            "type": "knowledge",
            "status": "knowledge",
            "owner": "tests",
            "lifecycle": "knowledge",
            "clusters": ["runtime"],
            "tags": ["cks", "compat"],
            "projects": ["CKS"],
            "relations": [],
            "evidence": ["CKS-EVD-9612"],
            "history": [{"status": "clustered"}, {"status": "validated"}],
            "signals": {"confidence": 0.8, "novelty": 0.5, "uncertainty": 0.2, "importance": 0.7},
        },
    ]


class V16CompatibilityTests(unittest.TestCase):
    def test_conflict_detector_is_not_empty_stub(self):
        conflicts = detect_conflicts(_records())
        self.assertTrue(conflicts)
        self.assertTrue(any(item["signal"] == "status:disputed" for item in conflicts))
        self.assertTrue(any(item["signal"] == "relation:conflicts_with" for item in conflicts))

    def test_conflict_detector_does_not_invent_conflicts(self):
        records = _records()
        records[0]["status"] = "knowledge"
        records[0]["relations"] = []
        self.assertEqual(detect_conflicts(records), [])

    def test_health_score_uses_real_record_audit(self):
        score = calculate_health(_records())
        self.assertGreater(score, 0.0)
        self.assertLessEqual(score, 100.0)

    def test_health_score_supports_legacy_normalized_metrics(self):
        self.assertEqual(
            calculate_health(
                {
                    "completeness": 1.0,
                    "evidence": 1.0,
                    "connectivity": 1.0,
                    "classification": 1.0,
                    "history": 1.0,
                }
            ),
            100.0,
        )

    def test_default_runtime_executes_current_intelligence_stack(self):
        runtime = IntelligenceRuntime()
        result = runtime.run({"run_id": "test", "records": _records()})
        self.assertEqual(result["validation"]["status"], "PASS")
        self.assertEqual(result["KnowledgeIntelligence"]["kind"], "cks_knowledge_intelligence")
        self.assertTrue(result["CanonConflictDetector"])
        self.assertGreater(result["KnowledgeHealthScore"], 0.0)
        self.assertEqual(result["authority"], "analysis_and_suggestions_only")
        self.assertEqual(runtime.events[-1].event_type, "runtime.completed")

    def test_explicit_module_mode_remains_compatible(self):
        class LegacyModule:
            def run(self, context):
                return {"seen": context["id"]}

        runtime = IntelligenceRuntime([LegacyModule()])
        result = runtime.run({"id": "legacy"})
        self.assertEqual(result, {"LegacyModule": {"seen": "legacy"}})

    def test_cli_self_check_is_meaningful(self):
        result = self_check()
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(all(result["checks"].values()))
        self.assertGreater(result["health_score"], 0.0)
        self.assertTrue(result["conflicts"])


if __name__ == "__main__":
    unittest.main()
