#!/usr/bin/env python3
"""Тесты этапа 5: структурная аналитика знаний CKS."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cks_knowledge_intelligence import KnowledgeIntelligence
from cks_knowledge_runtime import KnowledgeRuntime


class KnowledgeIntelligenceStage5Tests(unittest.TestCase):
    def _runtime(self) -> KnowledgeRuntime:
        runtime = KnowledgeRuntime()
        result = runtime.ingest(
            [
                {
                    "id": "CKS-EVD-501",
                    "title": "Проверенное основание",
                    "type": "evidence",
                    "status": "validated",
                    "owner": "tests",
                    "lifecycle": "validation",
                    "clusters": ["CKS"],
                    "tags": ["evidence"],
                    "projects": ["CKS"],
                    "relations": [],
                    "evidence": [],
                    "history": [],
                    "signals": {"confidence": 0.95},
                },
                {
                    "id": "CKS-KNW-501",
                    "title": "Знание с низкой уверенностью",
                    "type": "knowledge",
                    "status": "knowledge",
                    "owner": "tests",
                    "lifecycle": "knowledge",
                    "clusters": ["CKS", "Аналитика"],
                    "tags": ["graph", "analytics"],
                    "projects": ["CKS"],
                    "relations": [{"target": "CKS-EVD-501", "type": "supported_by"}],
                    "evidence": ["CKS-EVD-501"],
                    "history": [{"status": "validated", "timestamp": "2026-09-10T10:00:00Z"}],
                    "signals": {"confidence": 0.35, "importance": 0.9, "novelty": 0.4},
                },
                {
                    "id": "CKS-CAN-501",
                    "title": "Канонический объект с явным конфликтом",
                    "type": "knowledge",
                    "status": "canonical",
                    "owner": "tests",
                    "lifecycle": "knowledge",
                    "clusters": ["CKS", "Аналитика"],
                    "tags": ["graph", "canon"],
                    "projects": ["CKS"],
                    "relations": [{"target": "CKS-KNW-501", "type": "conflicts_with"}],
                    "evidence": ["CKS-EVD-501"],
                    "history": [{"status": "validated", "timestamp": "2026-09-11T10:00:00Z"}],
                    "signals": {"confidence": 0.6, "uncertainty": 0.5, "importance": 1.0},
                },
                {
                    "id": "CKS-DSP-501",
                    "title": "Оспариваемый объект",
                    "type": "knowledge",
                    "status": "disputed",
                    "owner": "tests",
                    "lifecycle": "knowledge",
                    "clusters": ["CKS"],
                    "tags": ["conflict"],
                    "projects": ["CKS"],
                    "relations": [{"target": "CKS-CAN-501", "type": "contradicts"}],
                    "evidence": ["CKS-EVD-501"],
                    "history": [],
                    "signals": {"confidence": 0.5, "uncertainty": 0.8},
                },
                {
                    "id": "CKS-IDEA-501",
                    "title": "Изолированная новая идея",
                    "type": "idea",
                    "status": "raw",
                    "owner": "tests",
                    "lifecycle": "research",
                    "clusters": [],
                    "tags": ["new"],
                    "projects": ["CKS"],
                    "relations": [{"target": "CKS-MISSING-501", "type": "related_to"}],
                    "evidence": [],
                    "history": [],
                    "signals": {"novelty": 0.9, "confidence": 0.3},
                },
            ]
        )
        self.assertEqual(result["status"], "PASS", result)
        return runtime

    def test_structure_detects_components_isolation_and_broken_target(self) -> None:
        analysis = KnowledgeIntelligence(self._runtime()).structure_analysis()
        self.assertEqual(analysis["nodes"], 5)
        self.assertEqual(analysis["components_count"], 2)
        self.assertIn("CKS-IDEA-501", analysis["isolated_nodes"])
        self.assertIn("CKS-EVD-501", analysis["weakly_connected_nodes"])
        self.assertEqual(
            analysis["broken_relation_targets"],
            [{"source": "CKS-IDEA-501", "target": "CKS-MISSING-501", "relation": "related_to"}],
        )
        self.assertEqual(analysis["authority"], "diagnostic_only")

    def test_weak_nodes_distinguish_isolated_and_single_connection(self) -> None:
        nodes = {item["id"]: item for item in KnowledgeIntelligence(self._runtime()).weakly_connected_nodes()}
        self.assertEqual(nodes["CKS-IDEA-501"]["degree"], 0)
        self.assertEqual(nodes["CKS-IDEA-501"]["broken_relation_targets"], 1)
        self.assertEqual(nodes["CKS-EVD-501"]["degree"], 1)
        self.assertEqual(nodes["CKS-DSP-501"]["degree"], 1)
        self.assertNotIn("CKS-CAN-501", nodes)

    def test_conflicts_use_only_explicit_relations_and_disputed_status(self) -> None:
        report = KnowledgeIntelligence(self._runtime()).conflict_signals()
        signals = {(item["source"], item["target"], item["signal"]) for item in report["conflicts"]}
        self.assertIn(("CKS-CAN-501", "CKS-KNW-501", "relation:conflicts_with"), signals)
        self.assertIn(("CKS-DSP-501", "CKS-CAN-501", "relation:contradicts"), signals)
        self.assertIn(("CKS-DSP-501", "CKS-DSP-501", "status:disputed"), signals)
        self.assertEqual(report["method"], "explicit_signals_only")
        self.assertEqual(report["authority"], "diagnostic_only")

    def test_signal_diagnostics_find_confidence_novelty_and_canon_risks(self) -> None:
        report = KnowledgeIntelligence(self._runtime()).signal_diagnostics()
        objects = {item["id"]: item for item in report["objects"]}
        self.assertIn("низкая уверенность", objects["CKS-KNW-501"]["warnings"])
        self.assertIn("важный объект с низкой уверенностью", objects["CKS-KNW-501"]["warnings"])
        self.assertIn("высокая новизна без доказательств", objects["CKS-IDEA-501"]["warnings"])
        self.assertIn("канонический объект с пониженной уверенностью", objects["CKS-CAN-501"]["warnings"])
        self.assertIn("канонический объект с заметной неопределённостью", objects["CKS-CAN-501"]["warnings"])
        self.assertEqual(report["status"], "WARN")

    def test_full_report_keeps_old_sections_and_adds_stage5_sections(self) -> None:
        report = KnowledgeIntelligence(self._runtime()).full_report(link_threshold=0.3)
        for key in (
            "скрытые_связи",
            "новые_кластеры",
            "что_стало_знанием",
            "карта_развития_проекта",
            "самоаудит_качества",
            "структура_знаний",
            "слабосвязанные_узлы",
            "конфликтные_сигналы",
            "сигналы_уверенности_и_новизны",
        ):
            self.assertIn(key, report)
        self.assertEqual(report["authority"], "analysis_and_suggestions_only")

    def test_analysis_is_deterministic_and_does_not_mutate_runtime(self) -> None:
        runtime = self._runtime()
        before = copy.deepcopy(runtime.records)
        intelligence = KnowledgeIntelligence(runtime)
        first = intelligence.full_report()
        second = intelligence.full_report()
        self.assertEqual(first, second)
        self.assertEqual(runtime.records, before)
        self.assertEqual(runtime.records["CKS-CAN-501"]["status"], "canonical")


if __name__ == "__main__":
    unittest.main()
