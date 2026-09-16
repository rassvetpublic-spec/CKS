#!/usr/bin/env python3
"""Тесты этапа 6: эволюция, миграция и восстановление знаний CKS."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cks_knowledge_evolution import KnowledgeEvolution
from cks_knowledge_runtime import KnowledgeRuntime
from cks_version_change_analyzer import compare_versions


class KnowledgeEvolutionStage6Tests(unittest.TestCase):
    def _runtime(self) -> KnowledgeRuntime:
        runtime = KnowledgeRuntime()
        result = runtime.ingest(
            [
                {
                    "id": "CKS-EVD-601",
                    "title": "Основание",
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
                },
                {
                    "id": "CKS-DEC-601",
                    "title": "Решение",
                    "type": "decision",
                    "status": "knowledge",
                    "owner": "tests",
                    "lifecycle": "adoption",
                    "clusters": ["CKS"],
                    "tags": ["decision"],
                    "projects": ["CKS"],
                    "relations": [],
                    "evidence": ["CKS-EVD-601"],
                    "history": [],
                },
                {
                    "id": "CKS-KNW-601",
                    "title": "Развиваемое знание",
                    "type": "knowledge",
                    "status": "validated",
                    "owner": "tests",
                    "lifecycle": "knowledge",
                    "version": "3",
                    "clusters": ["CKS", "Эволюция"],
                    "tags": ["migration", "recovery"],
                    "projects": ["CKS"],
                    "relations": [{"target": "CKS-EVD-601", "type": "supported_by"}],
                    "evidence": ["CKS-EVD-601"],
                    "decision": "CKS-DEC-601",
                    "history": [],
                    "signals": {"confidence": 0.9},
                },
            ]
        )
        self.assertEqual(result["status"], "PASS", result)
        return runtime

    def test_legacy_migration_maps_status_and_old_signal_fields(self) -> None:
        source = {
            "id": "CKS-KNW-602",
            "name": "Старый объект",
            "type": "knowledge",
            "status": "active",
            "owner": "tests",
            "lifecycle": "knowledge",
            "project": "CKS",
            "relations": [],
            "evidence": [],
            "history": [],
            "confidence": 0.8,
            "intuition": "старая форма поля",
        }
        before = copy.deepcopy(source)
        result = KnowledgeEvolution.migrate_record(source)
        self.assertEqual(result["status"], "PASS", result)
        self.assertEqual(result["record"]["status"], "knowledge")
        self.assertEqual(result["record"]["projects"], ["CKS"])
        self.assertEqual(result["record"]["signals"]["confidence"], 0.8)
        self.assertEqual(result["record"]["signals"]["intuition"], "старая форма поля")
        self.assertNotIn("confidence", result["record"])
        self.assertNotIn("intuition", result["record"])
        self.assertTrue(result["legacy_status_mapped"])
        self.assertEqual(source, before)

    def test_migration_is_idempotent(self) -> None:
        source = {
            "id": "CKS-KNW-603",
            "type": "knowledge",
            "status": "review",
            "relations": [],
            "evidence": [],
            "history": [],
        }
        first = KnowledgeEvolution.migrate_record(source)
        second = KnowledgeEvolution.migrate_record(first["record"])
        self.assertEqual(first["status"], "PASS")
        self.assertEqual(second["status"], "PASS")
        self.assertEqual(first["record"], second["record"])

    def test_evolution_uses_state_machine_and_records_history(self) -> None:
        runtime = self._runtime()
        source = runtime.records["CKS-KNW-601"]
        before = copy.deepcopy(source)
        result = KnowledgeEvolution.evolve_record(
            source,
            "canonical",
            reason="решение принято",
            changed_by="tests",
            timestamp="2026-09-17T00:00:00Z",
            new_version="4",
        )
        self.assertEqual(result["status"], "PASS", result)
        evolved = result["record"]
        self.assertEqual(evolved["status"], "canonical")
        self.assertEqual(evolved["version"], "4")
        self.assertEqual(evolved["history"][-1]["from_status"], "validated")
        self.assertEqual(evolved["history"][-1]["status"], "canonical")
        self.assertEqual(evolved["history"][-1]["reason"], "решение принято")
        self.assertEqual(source, before)

    def test_evolution_cannot_bypass_canonical_guards(self) -> None:
        source = {
            "id": "CKS-KNW-604",
            "type": "knowledge",
            "status": "validated",
            "owner": "tests",
            "lifecycle": "knowledge",
            "relations": [],
            "evidence": [],
            "history": [],
        }
        result = KnowledgeEvolution.evolve_record(source, "canonical", reason="попытка")
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("доказательство" in item for item in result["validation"]["errors"]))
        self.assertTrue(any("решение" in item for item in result["validation"]["errors"]))

    def test_snapshot_is_deterministic_and_does_not_mutate_runtime(self) -> None:
        runtime = self._runtime()
        before = copy.deepcopy(runtime.records)
        first = KnowledgeEvolution.create_snapshot(runtime, label="stage6")
        second = KnowledgeEvolution.create_snapshot(runtime, label="stage6")
        self.assertEqual(first, second)
        self.assertEqual(first["sha256"], second["sha256"])
        self.assertEqual(runtime.records, before)
        self.assertEqual(KnowledgeEvolution.verify_snapshot(first)["status"], "PASS")

    def test_snapshot_tampering_is_detected(self) -> None:
        snapshot = KnowledgeEvolution.create_snapshot(self._runtime())
        tampered = copy.deepcopy(snapshot)
        tampered["records"][0]["title"] = "подменено"
        result = KnowledgeEvolution.verify_snapshot(tampered)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("sha256" in item for item in result["errors"]))

    def test_recovery_revalidates_and_restores_isolated_runtime(self) -> None:
        runtime = self._runtime()
        snapshot = KnowledgeEvolution.create_snapshot(runtime)
        recovered = KnowledgeEvolution.recover_snapshot(snapshot)
        self.assertEqual(recovered["status"], "PASS", recovered)
        restored = recovered["runtime"]
        self.assertIsNot(restored, runtime)
        self.assertEqual(restored.records, runtime.records)
        restored.records["CKS-KNW-601"]["title"] = "изменено только в восстановленной копии"
        self.assertNotEqual(restored.records["CKS-KNW-601"]["title"], runtime.records["CKS-KNW-601"]["title"])

    def test_recovery_rejects_valid_hash_with_invalid_runtime_data(self) -> None:
        runtime = self._runtime()
        snapshot = KnowledgeEvolution.create_snapshot(runtime)
        invalid = copy.deepcopy(snapshot)
        invalid["records"][0]["signals"] = {"confidence": 2.0}
        payload = {key: value for key, value in invalid.items() if key not in {"sha256", "authority"}}

        import hashlib
        import json

        invalid["sha256"] = hashlib.sha256(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        recovered = KnowledgeEvolution.recover_snapshot(invalid)
        self.assertEqual(recovered["status"], "FAIL")
        self.assertEqual(recovered["verification"]["status"], "PASS")
        self.assertIsNone(recovered["runtime"])

    def test_compare_record_sets_detects_added_removed_and_changed(self) -> None:
        old = [
            {"id": "CKS-KNW-610", "status": "knowledge", "title": "A"},
            {"id": "CKS-KNW-611", "status": "raw", "title": "B"},
        ]
        new = [
            {"id": "CKS-KNW-610", "status": "evolving", "title": "A"},
            {"id": "CKS-KNW-612", "status": "raw", "title": "C"},
        ]
        diff = KnowledgeEvolution.compare_record_sets(old, new)
        self.assertEqual(diff["status"], "CHANGED")
        self.assertEqual(diff["added"], ["CKS-KNW-612"])
        self.assertEqual(diff["removed"], ["CKS-KNW-611"])
        self.assertEqual(diff["changed"][0]["id"], "CKS-KNW-610")
        fields = {item["field"] for item in diff["changed"][0]["fields"]}
        self.assertEqual(fields, {"status"})

    def test_version_change_analyzer_uses_real_diff(self) -> None:
        old = {"id": "CKS-KNW-620", "status": "knowledge", "title": "A"}
        new = {"id": "CKS-KNW-620", "status": "evolving", "title": "A"}
        diff = compare_versions(old, new)
        self.assertEqual(diff["status"], "CHANGED")
        self.assertEqual(diff["added"], [])
        self.assertEqual(diff["removed"], [])
        self.assertEqual(diff["changed"][0]["id"], "CKS-KNW-620")
        self.assertEqual({item["field"] for item in diff["changed"][0]["fields"]}, {"status"})

    def test_evidence_reference_normalization(self) -> None:
        record = {
            "evidence": [
                "CKS-EVD-601",
                {"id": "CKS-EVD-602"},
                {"reference": "CKS-EVD-603"},
                "CKS-EVD-601",
            ]
        }
        self.assertEqual(
            KnowledgeEvolution.evidence_references(record),
            ["CKS-EVD-601", "CKS-EVD-602", "CKS-EVD-603"],
        )


if __name__ == "__main__":
    unittest.main()
