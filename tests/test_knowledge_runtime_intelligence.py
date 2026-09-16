#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from cks_knowledge_intelligence import KnowledgeIntelligence  # noqa: E402
from cks_knowledge_runtime import KnowledgeRuntime  # noqa: E402


FIXTURES = [
    {
        "id": "CKS-KNW-9101",
        "title": "Рабочий граф знаний",
        "type": "knowledge",
        "status": "knowledge",
        "owner": "CKS",
        "lifecycle": "knowledge",
        "version": "2",
        "clusters": ["архитектура", "граф знаний"],
        "tags": ["cks", "graph", "runtime"],
        "projects": ["CKS"],
        "relations": [{"target": "CKS-EVD-9101", "type": "evidenced_by"}],
        "evidence": ["CKS-EVD-9101"],
        "history": [
            {"status": "raw", "timestamp": "2026-09-01T10:00:00Z"},
            {"status": "validated", "timestamp": "2026-09-10T10:00:00Z"},
        ],
        "signals": {"confidence": 0.9, "intuition": "граф может открыть скрытые зависимости"},
    },
    {
        "id": "CKS-KNW-9102",
        "title": "Аналитика знаний",
        "type": "knowledge",
        "status": "evolving",
        "owner": "CKS",
        "lifecycle": "knowledge",
        "version": "1",
        "clusters": ["архитектура", "аналитика"],
        "tags": ["cks", "graph", "intelligence"],
        "projects": ["CKS"],
        "relations": [],
        "evidence": ["CKS-EVD-9101"],
        "history": [{"status": "clustered", "timestamp": "2026-09-11T10:00:00Z"}],
        "signals": {"confidence": 0.75},
    },
    {
        "id": "CKS-EVD-9101",
        "title": "Проверка рабочего графа",
        "type": "evidence",
        "status": "validated",
        "owner": "CKS",
        "lifecycle": "validation",
        "clusters": ["граф знаний"],
        "tags": ["evidence"],
        "projects": ["CKS"],
        "relations": [],
        "evidence": [],
        "history": [],
    },
]


class KnowledgeRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = KnowledgeRuntime()
        result = self.runtime.ingest(FIXTURES)
        self.assertEqual(result["status"], "PASS")

    def test_dynamic_views_show_knowledge_pipeline(self) -> None:
        views = self.runtime.dynamic_views()
        self.assertIn("архитектура", views["по_кластерам"])
        self.assertIn("cks", views["по_тегам"])
        self.assertEqual(views["путь_материал_в_знание"]["знания"]["count"], 2)

    def test_obsidian_export_has_wikilinks_and_russian_labels(self) -> None:
        text = self.runtime.obsidian_markdown("CKS-KNW-9101")
        self.assertIn("status_ru", text)
        self.assertIn("[[CKS-EVD-9101]]", text)
        self.assertIn("Интуиция", text)
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.runtime.export_obsidian(temp_dir)
            self.assertEqual(result["status"], "PASS")
            self.assertTrue((Path(temp_dir) / "CKS_Обзор.md").exists())
            self.assertTrue((Path(temp_dir) / "Знания" / "CKS-KNW-9101.md").exists())

    def test_intelligence_suggests_hidden_links_and_clusters(self) -> None:
        intelligence = KnowledgeIntelligence(self.runtime)
        hidden = intelligence.hidden_links(threshold=0.3)
        pair = {(item["source"], item["target"]) for item in hidden}
        self.assertIn(("CKS-KNW-9101", "CKS-KNW-9102"), pair)
        clusters = intelligence.cluster_suggestions(min_shared_tags=2)
        self.assertTrue(any("CKS-KNW-9101" in item["objects"] and "CKS-KNW-9102" in item["objects"] for item in clusters))

    def test_knowledge_transformation_and_project_map(self) -> None:
        intelligence = KnowledgeIntelligence(self.runtime)
        became = {item["id"]: item for item in intelligence.became_knowledge()}
        self.assertTrue(became["CKS-KNW-9101"]["had_early_stage"])
        project_map = intelligence.project_evolution_map()
        self.assertIn("CKS", project_map["projects"])
        self.assertEqual(len(project_map["projects"]["CKS"]["objects"]), 3)

    def test_quality_audit_is_diagnostic_only(self) -> None:
        audit = KnowledgeIntelligence(self.runtime).quality_audit()
        self.assertEqual(audit["authority"], "diagnostic_only")
        self.assertEqual(len(audit["objects"]), 3)


if __name__ == "__main__":
    unittest.main()
