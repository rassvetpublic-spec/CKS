#!/usr/bin/env python3
"""Тесты этапа 3: Obsidian-представление CKS."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cks_knowledge_runtime import KnowledgeRuntime
from cks_obsidian_export import ObsidianExport


class ObsidianExportTests(unittest.TestCase):
    def _runtime(self) -> KnowledgeRuntime:
        runtime = KnowledgeRuntime()
        result = runtime.ingest([
            {
                "id": "CKS-EVD-301",
                "title": "Доказательство",
                "type": "evidence",
                "status": "validated",
                "owner": "tests",
                "lifecycle": "validation",
                "clusters": ["Граф знаний"],
                "tags": ["проверено"],
                "projects": ["CKS"],
                "relations": [],
                "evidence": [],
                "history": [],
            },
            {
                "id": "CKS-KNW-301",
                "title": "Объект знания",
                "type": "knowledge",
                "status": "knowledge",
                "owner": "tests",
                "lifecycle": "knowledge",
                "clusters": ["Граф знаний"],
                "tags": ["важное", "runtime"],
                "projects": ["CKS"],
                "relations": [
                    {"target": "CKS-EVD-301", "type": "supported_by"}
                ],
                "evidence": ["CKS-EVD-301"],
                "history": [],
                "signals": {"intuition": "есть скрытая связь", "confidence": 0.8},
            },
        ])
        self.assertEqual(result["status"], "PASS", result)
        return runtime

    def test_export_creates_obsidian_structure(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = ObsidianExport(self._runtime()).export(root)
            self.assertEqual(result["status"], "PASS")
            self.assertTrue((root / "Знания" / "CKS-KNW-301.md").exists())
            self.assertTrue((root / "Кластеры" / "Граф_знаний.md").exists())
            self.assertTrue((root / "Теги" / "важное.md").exists())
            self.assertTrue((root / "Проекты" / "CKS.md").exists())
            self.assertTrue((root / "Статусы" / "knowledge.md").exists())
            self.assertTrue((root / "Карты" / "CKS_Граф.canvas").exists())

    def test_object_note_contains_wikilinks_and_russian_navigation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            ObsidianExport(self._runtime()).export(root)
            text = (root / "Знания" / "CKS-KNW-301.md").read_text(encoding="utf-8")
            self.assertIn("[[CKS-EVD-301]]", text)
            self.assertIn("## Навигация CKS", text)
            self.assertIn("[[Кластеры/Граф_знаний|Граф знаний]]", text)
            self.assertIn("[[Проекты/CKS|CKS]]", text)
            self.assertIn("Интуиция", text)

    def test_canvas_contains_nodes_and_relation_edge(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = ObsidianExport(self._runtime()).export(root)
            canvas = json.loads((root / "Карты" / "CKS_Граф.canvas").read_text(encoding="utf-8"))
            self.assertEqual(len(canvas["nodes"]), 2)
            self.assertGreaterEqual(len(canvas["edges"]), 1)
            labels = {edge.get("label") for edge in canvas["edges"]}
            self.assertIn("supported_by", labels)
            self.assertEqual(result["authority"], "derived_view_only")

    def test_obsidian_is_not_marked_as_ssot(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            ObsidianExport(self._runtime()).export(root)
            guide = (root / "OBSIDIAN_CKS_README.md").read_text(encoding="utf-8")
            self.assertIn("только представление", guide)
            self.assertIn("не должно автоматически менять SSOT или Canon", guide)


if __name__ == "__main__":
    unittest.main()
