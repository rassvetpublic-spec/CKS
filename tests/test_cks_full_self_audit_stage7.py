#!/usr/bin/env python3
"""Этап 7: полный самоаудит и интегральная регрессия CKS.

Проверка связывает рабочий контур знаний, граф, трассировку происхождения,
аналитику, эволюцию/восстановление, федерацию проектов и управление.
Ни одна проверка не принимает Decision (решение) и не изменяет Canon (канон).
"""
from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cks_governance_runner import run_all
from cks_knowledge_evolution import KnowledgeEvolution
from cks_knowledge_federation import KnowledgeFederation
from cks_knowledge_graph_runtime import KnowledgeGraph
from cks_knowledge_intelligence import KnowledgeIntelligence
from cks_knowledge_runtime import KnowledgeRuntime
from cks_self_audit import SelfAudit
from cks_traceability_engine import TraceabilityEngine
from cks_version_change_analyzer import compare_versions


class FullSelfAuditStage7Tests(unittest.TestCase):
    @staticmethod
    def _records() -> list[dict[str, object]]:
        return [
            {
                "id": "CKS-EVD-701",
                "title": "Интеграционное доказательство",
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
                "id": "CKS-DEC-701",
                "title": "Интеграционное решение",
                "type": "decision",
                "status": "knowledge",
                "owner": "tests",
                "lifecycle": "adoption",
                "clusters": ["CKS"],
                "tags": ["decision"],
                "projects": ["CKS"],
                "relations": [],
                "evidence": ["CKS-EVD-701"],
                "history": [],
                "signals": {"confidence": 0.9},
            },
            {
                "id": "CKS-KNW-701",
                "title": "Рабочее знание A",
                "type": "knowledge",
                "status": "knowledge",
                "owner": "tests",
                "lifecycle": "knowledge",
                "version": "3",
                "clusters": ["архитектура", "CKS"],
                "tags": ["runtime", "knowledge"],
                "projects": ["CKS"],
                "relations": [],
                "evidence": ["CKS-EVD-701"],
                "decision": "CKS-DEC-701",
                "history": [{"status": "validated"}],
                "signals": {"confidence": 0.9},
            },
            {
                "id": "CKS-KNW-702",
                "title": "Рабочее знание B",
                "type": "knowledge",
                "status": "evolving",
                "owner": "tests",
                "lifecycle": "knowledge",
                "version": "2",
                "clusters": ["архитектура", "CKS"],
                "tags": ["runtime", "evolution"],
                "projects": ["CKS"],
                "relations": [],
                "evidence": ["CKS-EVD-701"],
                "decision": "CKS-DEC-701",
                "history": [{"status": "knowledge"}],
                "signals": {"confidence": 0.8, "novelty": 0.6},
            },
        ]

    def test_repository_self_audit_has_no_failures(self) -> None:
        result = SelfAudit(ROOT).run()
        self.assertNotEqual(result["status"], "FAIL", result)
        self.assertEqual(result["summary"]["fail"], 0, result)
        self.assertEqual(result["authority"], "diagnostic_only")

    def test_governance_runner_has_no_failures(self) -> None:
        result = run_all(ROOT)
        self.assertNotEqual(result["status"], "FAIL", result)
        self.assertEqual(result["checks"]["self_audit"]["summary"]["fail"], 0, result)
        self.assertEqual(result["authority"], "validation_only")

    def test_end_to_end_knowledge_lifecycle(self) -> None:
        records = self._records()
        originals = copy.deepcopy(records)

        runtime = KnowledgeRuntime()
        ingest = runtime.ingest(records)
        self.assertEqual(ingest["status"], "PASS", ingest)
        self.assertEqual(ingest["objects"], 4)

        views = runtime.dynamic_views()
        self.assertIn("архитектура", views["по_кластерам"])
        self.assertEqual(views["authority"], "derived_view_only")

        intelligence = KnowledgeIntelligence(runtime)
        candidates = intelligence.hidden_links(threshold=0.3)
        pair = {
            tuple(sorted((item["source"], item["target"])))
            for item in candidates
        }
        self.assertIn(("CKS-KNW-701", "CKS-KNW-702"), pair)
        self.assertTrue(all(item["authority"] == "suggestion_only" for item in candidates))

        trace = TraceabilityEngine()
        trace_result = trace.ingest(records)
        self.assertNotEqual(trace_result["status"], "FAIL", trace_result)
        self.assertEqual(trace_result["broken_references"], [])
        chain = trace.chain("CKS-KNW-701")
        relations = {edge["relation"] for edge in chain["outgoing"]}
        self.assertIn("evidenced_by", relations)
        self.assertIn("decided_by", relations)

        evolved = KnowledgeEvolution.evolve_record(
            runtime.records["CKS-KNW-701"],
            "canonical",
            reason="этап 7: проверка разрешённого перехода",
            changed_by="stage7-tests",
            timestamp="2026-09-17T00:00:00Z",
            new_version="4",
        )
        self.assertEqual(evolved["status"], "PASS", evolved)
        self.assertEqual(evolved["record"]["status"], "canonical")
        self.assertEqual(runtime.records["CKS-KNW-701"]["status"], "knowledge")

        diff = compare_versions(runtime.records["CKS-KNW-701"], evolved["record"])
        self.assertEqual(diff["status"], "CHANGED")
        changed_fields = {item["field"] for item in diff["changed"][0]["fields"]}
        self.assertTrue({"status", "version", "history"}.issubset(changed_fields))

        snapshot = KnowledgeEvolution.create_snapshot(runtime, label="stage7-integral")
        self.assertEqual(KnowledgeEvolution.verify_snapshot(snapshot)["status"], "PASS")
        recovered = KnowledgeEvolution.recover_snapshot(snapshot)
        self.assertEqual(recovered["status"], "PASS", recovered)
        self.assertEqual(recovered["runtime"].records, runtime.records)

        self.assertEqual(records, originals, "Интегральный проход не должен мутировать исходные записи")

    def test_canon_guard_survives_integral_regression(self) -> None:
        source = {
            "id": "CKS-KNW-703",
            "type": "knowledge",
            "status": "validated",
            "owner": "tests",
            "lifecycle": "knowledge",
            "relations": [],
            "evidence": [],
            "history": [],
        }
        result = KnowledgeEvolution.evolve_record(source, "canonical", reason="недостаточно оснований")
        self.assertEqual(result["status"], "FAIL")
        errors = " ".join(result["validation"]["errors"])
        self.assertIn("доказательство", errors)
        self.assertIn("решение", errors)

    def test_graph_persistence_roundtrip_and_dependency_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "graph.json"
            graph = KnowledgeGraph(path)
            graph.add_node("A", "knowledge")
            graph.add_node("B", "knowledge")
            graph.add_node("C", "evidence")
            graph.add_edge("A", "B", "depends_on", evidence=["C"])
            graph.add_edge("B", "C", "depends_on")
            self.assertEqual(graph.dependencies("A", transitive=True), ["B", "C"])
            graph.save()

            loaded = KnowledgeGraph(path)
            self.assertEqual(loaded.to_dict(), graph.to_dict())
            self.assertEqual(loaded.validate()["status"], "PASS")

    def test_federation_keeps_project_canons_independent(self) -> None:
        federation = KnowledgeFederation()
        federation.add_project(
            {
                "project_id": "P1",
                "version": "1",
                "canon_owner": "P1",
                "nodes": [{"id": "KNW-1", "type": "knowledge"}],
                "edges": [],
            }
        )
        federation.add_project(
            {
                "project_id": "P2",
                "version": "9",
                "canon_owner": "P2",
                "nodes": [{"id": "KNW-1", "type": "knowledge"}],
                "edges": [],
            }
        )
        federation.add_cross_project_relation("P1", "KNW-1", "P2", "KNW-1", "depends_on")
        result = federation.validate()
        self.assertEqual(result["status"], "PASS", result)
        self.assertIn("P1::KNW-1", federation.graph.nodes)
        self.assertIn("P2::KNW-1", federation.graph.nodes)
        export = federation.export_index()
        owners = {project["project_id"]: project["canon_owner"] for project in export["projects"]}
        self.assertEqual(owners, {"P1": "P1", "P2": "P2"})
        self.assertIn("не объединяет Canon", export["rule"])

    def test_obsidian_projection_is_derived_and_reproducible(self) -> None:
        runtime = KnowledgeRuntime(self._records())
        with tempfile.TemporaryDirectory() as tmp:
            first = runtime.export_obsidian(tmp)
            second = runtime.export_obsidian(tmp)
            self.assertEqual(first, second)
            note = Path(tmp) / "Знания" / "CKS-KNW-701.md"
            self.assertTrue(note.exists())
            text = note.read_text(encoding="utf-8")
            self.assertIn("не является SSOT", text)
            self.assertIn("архитектура", text)


if __name__ == "__main__":
    unittest.main()
