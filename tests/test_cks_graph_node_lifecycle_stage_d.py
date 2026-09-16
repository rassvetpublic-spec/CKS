#!/usr/bin/env python3
"""FULL KNOWLEDGE SNAPSHOT — Этап D: Graph Object Lifecycle + Node Versioning."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cks_graph_node_versioning import initialize_node, node_history, node_version, transition_node, update_node
from cks_knowledge_graph_runtime import GraphError, KnowledgeGraph


class GraphNodeLifecycleStageDTests(unittest.TestCase):
    def test_version_history_survives_graph_roundtrip(self) -> None:
        graph = KnowledgeGraph()
        initialize_node(graph, "A", "knowledge", lifecycle="raw", changed_by="stage-d")
        self.assertEqual(node_version(graph, "A"), 1)
        transition_node(graph, "A", "captured", reason="материал принят")
        update_node(graph, "A", metadata_patch={"tag": "graph"}, reason="добавлена классификация")
        self.assertEqual(node_version(graph, "A"), 3)
        self.assertEqual([x["event"] for x in node_history(graph, "A")], ["created", "updated", "updated"])

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "graph.json"
            graph.save(path)
            loaded = KnowledgeGraph(path)
            self.assertEqual(node_version(loaded, "A"), 3)
            self.assertEqual(node_history(loaded, "A"), node_history(graph, "A"))

    def test_canon_guard_cannot_be_bypassed_through_graph_node(self) -> None:
        graph = KnowledgeGraph()
        initialize_node(graph, "A", "knowledge", lifecycle="validated")
        with self.assertRaises(GraphError):
            transition_node(graph, "A", "canonical", reason="без основания")
        transition_node(
            graph,
            "A",
            "canonical",
            reason="решение принято",
            evidence_count=1,
            decision_ref="ADR-TEST",
        )
        self.assertEqual(graph.nodes["A"]["lifecycle"], "canonical")

    def test_terminal_lifecycle_is_respected(self) -> None:
        graph = KnowledgeGraph()
        initialize_node(graph, "A", "knowledge", lifecycle="superseded")
        transition_node(graph, "A", "archived", reason="историческая версия")
        with self.assertRaises(GraphError):
            transition_node(graph, "A", "knowledge", reason="попытка возврата")

    def test_service_metadata_cannot_be_overwritten_directly(self) -> None:
        graph = KnowledgeGraph()
        initialize_node(graph, "A", "knowledge")
        with self.assertRaises(GraphError):
            update_node(graph, "A", metadata_patch={"_cks_node_versioning": {}}, reason="обход")

    def test_noop_does_not_increment_version(self) -> None:
        graph = KnowledgeGraph()
        initialize_node(graph, "A", "knowledge", lifecycle="raw")
        update_node(graph, "A", lifecycle="raw", reason="без изменения")
        self.assertEqual(node_version(graph, "A"), 1)


if __name__ == "__main__":
    unittest.main()
