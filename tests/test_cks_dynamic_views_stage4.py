#!/usr/bin/env python3
"""Тесты этапа 4: динамические представления и путь «материал → знание»."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cks_dynamic_views import DynamicKnowledgeViews
from cks_knowledge_runtime import KnowledgeRuntime


class DynamicViewsTests(unittest.TestCase):
    def _runtime(self) -> KnowledgeRuntime:
        runtime = KnowledgeRuntime()
        result = runtime.ingest([
            {
                "id": "CKS-EVD-401",
                "title": "Проверка",
                "type": "evidence",
                "status": "validated",
                "owner": "tests",
                "lifecycle": "validation",
                "clusters": ["CKS"],
                "tags": ["факт"],
                "projects": ["CKS"],
                "relations": [],
                "evidence": [],
                "history": [{"status": "captured", "timestamp": "2026-09-01T10:00:00Z"}],
            },
            {
                "id": "CKS-KNW-401",
                "title": "Знание",
                "type": "knowledge",
                "status": "knowledge",
                "owner": "tests",
                "lifecycle": "knowledge",
                "clusters": ["CKS", "Граф"],
                "tags": ["важное"],
                "projects": ["CKS"],
                "relations": [{"target": "CKS-EVD-401", "type": "supported_by"}],
                "evidence": ["CKS-EVD-401"],
                "history": [
                    {"status": "raw", "timestamp": "2026-08-01T10:00:00Z"},
                    {"status": "validated", "timestamp": "2026-09-10T10:00:00Z"},
                ],
                "source": "chat",
            },
            {
                "id": "CKS-IDEA-401",
                "title": "Сырой материал",
                "type": "idea",
                "status": "raw",
                "owner": "tests",
                "lifecycle": "research",
                "clusters": [],
                "tags": [],
                "projects": ["CKS"],
                "relations": [{"target": "CKS-MISSING-401", "type": "related_to"}],
                "evidence": [],
                "history": [],
            },
        ])
        self.assertEqual(result["status"], "PASS", result)
        return runtime

    def test_funnel_shows_input_and_knowledge(self) -> None:
        views = DynamicKnowledgeViews(self._runtime()).full_views()
        funnel = views["воронка_материал_в_знание"]
        self.assertEqual(funnel["objects_total"], 3)
        self.assertEqual(funnel["input"], 1)
        self.assertGreaterEqual(funnel["knowledge_or_canon"], 1)
        self.assertEqual(views["authority"], "derived_view_only")

    def test_connectivity_detects_isolated_or_weak_nodes(self) -> None:
        connectivity = DynamicKnowledgeViews(self._runtime()).connectivity()
        groups = connectivity["группы"]
        self.assertIn("CKS-KNW-401", groups["слабосвязанные"] + groups["связанные"] + groups["узлы_хабы"])

    def test_problems_find_missing_classification_and_broken_reference(self) -> None:
        problems = DynamicKnowledgeViews(self._runtime()).problems()
        self.assertIn("CKS-IDEA-401", problems["без_кластеров"])
        self.assertIn("CKS-IDEA-401", problems["без_тегов"])
        self.assertIn("CKS-IDEA-401 -> CKS-MISSING-401", problems["битые_ссылки"])

    def test_timeline_uses_history_dates(self) -> None:
        timeline = DynamicKnowledgeViews(self._runtime()).timeline()
        self.assertIn("2026-09", timeline["по_месяцам"])
        self.assertIn("CKS-KNW-401", timeline["по_месяцам"]["2026-09"])

    def test_projects_are_projections_not_containers(self) -> None:
        projects = DynamicKnowledgeViews(self._runtime()).project_projections()
        self.assertIn("CKS", projects)
        self.assertIn("по_статусам", projects["CKS"])
        self.assertIn("по_кластерам", projects["CKS"])

    def test_provenance_is_derived(self) -> None:
        provenance = DynamicKnowledgeViews(self._runtime()).provenance()
        self.assertEqual(provenance["CKS-KNW-401"]["source"], "chat")
        self.assertIn("CKS-EVD-401", provenance["CKS-KNW-401"]["evidence"])


if __name__ == "__main__":
    unittest.main()
