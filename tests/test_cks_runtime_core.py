#!/usr/bin/env python3
"""Интеграционные тесты рабочего ядра CKS без внешних зависимостей."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cks_knowledge_federation import KnowledgeFederation
from cks_knowledge_graph_runtime import GraphError, KnowledgeGraph
from cks_runtime_pipeline import run_pipeline
from cks_traceability_engine import TraceabilityEngine


class KnowledgeGraphRuntimeTests(unittest.TestCase):
    def test_persistent_graph_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "graph.json"
            graph = KnowledgeGraph(path)
            graph.add_node("CKS-KNW-1", "knowledge")
            graph.add_node("CKS-EVD-1", "evidence")
            graph.add_edge("CKS-KNW-1", "CKS-EVD-1", "evidenced_by")
            graph.save()

            loaded = KnowledgeGraph(path)
            self.assertEqual(set(loaded.nodes), {"CKS-KNW-1", "CKS-EVD-1"})
            self.assertEqual(len(loaded.edges), 1)
            self.assertEqual(loaded.validate()["status"], "PASS")

    def test_broken_edge_is_rejected(self) -> None:
        graph = KnowledgeGraph()
        graph.add_node("CKS-KNW-1", "knowledge")
        with self.assertRaises(GraphError):
            graph.add_edge("CKS-KNW-1", "CKS-MISSING-1", "depends_on")

    def test_transitive_dependencies(self) -> None:
        graph = KnowledgeGraph()
        for node_id in ("A", "B", "C"):
            graph.add_node(node_id, "knowledge")
        graph.add_edge("A", "B", "depends_on")
        graph.add_edge("B", "C", "depends_on")
        self.assertEqual(graph.dependencies("A", transitive=True), ["B", "C"])


class TraceabilityRuntimeTests(unittest.TestCase):
    def test_chain_is_built_from_real_references(self) -> None:
        engine = TraceabilityEngine()
        result = engine.ingest([
            {"id": "CKS-EVD-1", "type": "evidence"},
            {"id": "CKS-DEC-1", "type": "decision"},
            {"id": "CKS-CHG-1", "type": "change"},
            {"id": "CKS-REV-1", "type": "review"},
            {
                "id": "CKS-KNW-1",
                "type": "knowledge",
                "evidence": ["CKS-EVD-1"],
                "decision": "CKS-DEC-1",
                "changes": ["CKS-CHG-1"],
                "reviews": ["CKS-REV-1"],
            },
        ])
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["edges"], 4)
        chain = engine.chain("CKS-KNW-1")
        self.assertEqual(len(chain["outgoing"]), 4)

    def test_missing_reference_fails(self) -> None:
        engine = TraceabilityEngine()
        result = engine.ingest([
            {"id": "CKS-KNW-1", "type": "knowledge", "evidence": ["CKS-EVD-404"]},
        ])
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["broken_references"][0]["target"], "CKS-EVD-404")


class FederationTests(unittest.TestCase):
    def test_projects_keep_namespaces_and_cross_links(self) -> None:
        federation = KnowledgeFederation()
        federation.add_project({
            "project_id": "alpha",
            "nodes": [{"id": "K1", "type": "knowledge"}],
            "edges": [],
        })
        federation.add_project({
            "project_id": "beta",
            "nodes": [{"id": "E1", "type": "evidence"}],
            "edges": [],
        })
        federation.add_cross_project_relation("alpha", "K1", "beta", "E1", "evidenced_by")
        exported = federation.export_index()
        self.assertIn("alpha::K1", federation.graph.nodes)
        self.assertIn("beta::E1", federation.graph.nodes)
        self.assertTrue(exported["derived_federation_index"])
        self.assertEqual(federation.validate()["status"], "PASS")


class RuntimePipelineTests(unittest.TestCase):
    def test_pipeline_connects_trace_and_federation(self) -> None:
        records = [
            {"id": "CKS-EVD-1", "type": "evidence"},
            {"id": "CKS-KNW-1", "type": "knowledge", "evidence": ["CKS-EVD-1"]},
        ]
        projects = [
            {
                "project_id": "one",
                "nodes": [
                    {"id": "K1", "type": "knowledge"},
                    {"id": "E1", "type": "evidence"},
                ],
                "edges": [{"source": "K1", "target": "E1", "relation": "evidenced_by"}],
            }
        ]
        result = run_pipeline(root=ROOT, records=records, projects=projects)
        self.assertNotEqual(result["status"], "FAIL", result)
        self.assertEqual(result["traceability"]["edges"], 1)
        self.assertEqual(result["federation"]["projects"], 1)
        self.assertEqual(result["authority"], "diagnostic_only")


if __name__ == "__main__":
    unittest.main()
