#!/usr/bin/env python3
"""FULL KNOWLEDGE SNAPSHOT — Этап B.

Проверяет три закрываемых разрыва рабочего графа знаний:
1. Relation History (история связей);
2. Graph Migration Engine (миграция формата графа);
3. Graph Recovery System (восстановление графа).
"""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cks_knowledge_graph_runtime import (
    CURRENT_GRAPH_SCHEMA_VERSION,
    GraphError,
    KnowledgeGraph,
)


class GraphEvolutionStageBTests(unittest.TestCase):
    @staticmethod
    def _graph() -> KnowledgeGraph:
        graph = KnowledgeGraph()
        graph.add_node("A", "knowledge")
        graph.add_node("B", "knowledge")
        graph.add_node("E", "evidence")
        return graph

    def test_relation_history_survives_update_delete_and_roundtrip(self) -> None:
        graph = self._graph()
        edge = graph.add_edge(
            "A",
            "B",
            "depends_on",
            evidence=["E"],
            reason="первичная связь",
            changed_by="stage-b",
            timestamp="2026-09-17T00:00:00Z",
        )
        edge_id = edge["id"]
        self.assertEqual(edge["version"], 1)
        self.assertEqual(graph.relation_history_for(edge_id)[0]["event"], "created")

        updated = graph.update_edge(
            edge_id,
            evidence=["E", "AUX"],
            metadata={"confidence": 0.8},
            reason="уточнение основания",
            changed_by="stage-b",
            timestamp="2026-09-17T00:01:00Z",
        )
        self.assertEqual(updated["version"], 2)
        self.assertEqual([x["event"] for x in graph.relation_history_for(edge_id)], ["created", "updated"])

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "graph.json"
            graph.save(path)
            loaded = KnowledgeGraph(path)
            self.assertEqual(loaded.to_dict(), graph.to_dict())
            self.assertEqual(len(loaded.relation_history_for(edge_id)), 2)

        graph.remove_edge(
            edge_id,
            reason="связь заменена",
            changed_by="stage-b",
            timestamp="2026-09-17T00:02:00Z",
        )
        self.assertEqual(graph.outgoing("A"), [])
        history = graph.relation_history_for(edge_id)
        self.assertEqual([x["event"] for x in history], ["created", "updated", "removed"])
        self.assertEqual(history[-1]["version"], 3)

    def test_graph_migration_1_to_2_is_deterministic_and_non_mutating(self) -> None:
        old = {
            "schema_version": "1.0",
            "derived_index": True,
            "nodes": [
                {"id": "A", "type": "knowledge", "project": None, "lifecycle": None, "metadata": {}},
                {"id": "B", "type": "knowledge", "project": None, "lifecycle": None, "metadata": {}},
            ],
            "edges": [
                {"source": "A", "target": "B", "relation": "depends_on", "evidence": [], "metadata": {}}
            ],
        }
        original = copy.deepcopy(old)
        first = KnowledgeGraph.migrate_payload(old)
        second = KnowledgeGraph.migrate_payload(old)
        self.assertEqual(old, original)
        self.assertEqual(first, second)
        self.assertEqual(first["schema_version"], CURRENT_GRAPH_SCHEMA_VERSION)
        self.assertTrue(first["edges"][0]["id"].startswith("REL-"))
        self.assertEqual(first["edges"][0]["version"], 1)
        self.assertEqual(first["edges"][0]["history"][0]["event"], "migrated")
        self.assertEqual(first["relation_history"][0]["event"], "migrated")

        graph = KnowledgeGraph.from_dict(old)
        self.assertEqual(graph.to_dict()["schema_version"], CURRENT_GRAPH_SCHEMA_VERSION)
        self.assertEqual(graph.validate()["status"], "PASS")

    def test_unknown_graph_schema_is_rejected(self) -> None:
        with self.assertRaises(GraphError):
            KnowledgeGraph.migrate_payload({"schema_version": "99.0", "nodes": [], "edges": []})

    def test_recovery_snapshot_detects_tampering_and_restores_exact_graph(self) -> None:
        graph = self._graph()
        graph.add_edge("A", "B", "depends_on", evidence=["E"], reason="recovery test")
        snapshot = graph.create_recovery_snapshot(label="stage-b")
        self.assertEqual(KnowledgeGraph.verify_recovery_snapshot(snapshot)["status"], "PASS")

        recovered = KnowledgeGraph.recover_snapshot(snapshot)
        self.assertEqual(recovered.to_dict(), graph.to_dict())

        tampered = copy.deepcopy(snapshot)
        tampered["graph"]["nodes"][0]["type"] = "tampered"
        verification = KnowledgeGraph.verify_recovery_snapshot(tampered)
        self.assertEqual(verification["status"], "FAIL")
        self.assertTrue(any("SHA-256" in item for item in verification["errors"]))
        with self.assertRaises(GraphError):
            KnowledgeGraph.recover_snapshot(tampered)

    def test_recovery_snapshot_file_roundtrip(self) -> None:
        graph = self._graph()
        graph.add_edge("A", "B", "depends_on", reason="file recovery")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "recovery.json"
            graph.save_snapshot(path, label="file")
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(KnowledgeGraph.verify_recovery_snapshot(payload)["status"], "PASS")
            restored = KnowledgeGraph.load_snapshot(path)
            self.assertEqual(restored.to_dict(), graph.to_dict())

    def test_previous_stage7_graph_contract_remains_compatible(self) -> None:
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


if __name__ == "__main__":
    unittest.main()
