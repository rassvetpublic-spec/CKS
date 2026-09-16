#!/usr/bin/env python3
"""Тесты этапа 2: рабочий контур знаний и машина состояний."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
VALIDATORS = ROOT / "validators"
for path in (TOOLS, VALIDATORS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from cks_knowledge_runtime import KnowledgeRuntime
from cks_knowledge_state_machine import validate_record_transition, validate_status, validate_transition
from lifecycle_guard import validate_state


class KnowledgeNormalizationTests(unittest.TestCase):
    def test_clusters_tags_and_projects_are_trimmed_and_deduplicated(self) -> None:
        record = KnowledgeRuntime.normalize({
            "id": "CKS-KNW-200",
            "type": "knowledge",
            "status": "raw",
            "clusters": [" Архитектура ", "Архитектура", "Граф"],
            "tags": [" идея ", "идея", "важное"],
            "projects": [" CKS ", "CKS"],
        })
        self.assertEqual(record["clusters"], ["Архитектура", "Граф"])
        self.assertEqual(record["tags"], ["важное", "идея"])
        self.assertEqual(record["projects"], ["CKS"])

    def test_runtime_rejects_unknown_status(self) -> None:
        record = KnowledgeRuntime.normalize({
            "id": "CKS-KNW-201",
            "type": "knowledge",
            "status": "неизвестно",
        })
        errors = KnowledgeRuntime.validate(record)
        self.assertTrue(any("неизвестный status" in item for item in errors))


class KnowledgeStateMachineTests(unittest.TestCase):
    def test_normal_progression_is_allowed(self) -> None:
        self.assertEqual(validate_transition("raw", "captured")["status"], "PASS")
        self.assertEqual(validate_transition("captured", "normalized")["status"], "PASS")

    def test_raw_cannot_jump_to_canonical(self) -> None:
        result = validate_transition(
            "raw",
            "canonical",
            evidence_count=2,
            decision_ref="CKS-DEC-1",
        )
        self.assertEqual(result["status"], "FAIL")

    def test_canonical_requires_evidence_and_decision(self) -> None:
        result = validate_transition("validated", "canonical")
        self.assertEqual(result["status"], "FAIL")
        self.assertGreaterEqual(len(result["errors"]), 2)

    def test_canonical_is_allowed_with_evidence_and_decision(self) -> None:
        result = validate_transition(
            "validated",
            "canonical",
            evidence_count=1,
            decision_ref="CKS-DEC-1",
        )
        self.assertEqual(result["status"], "PASS", result)

    def test_archived_is_terminal(self) -> None:
        self.assertEqual(validate_transition("archived", "evolving")["status"], "FAIL")

    def test_backward_transition_requires_reason(self) -> None:
        self.assertEqual(validate_transition("disputed", "researched")["status"], "FAIL")
        self.assertEqual(
            validate_transition("disputed", "researched", reason="нужна повторная проверка")["status"],
            "PASS",
        )

    def test_legacy_statuses_are_mapped_without_becoming_new_canon(self) -> None:
        self.assertEqual(validate_status("draft")["canonical"], "raw")
        self.assertEqual(validate_status("review")["canonical"], "validated")
        self.assertEqual(validate_status("active")["canonical"], "knowledge")

    def test_record_transition_reads_evidence_and_decision(self) -> None:
        record = {
            "id": "CKS-KNW-202",
            "status": "validated",
            "evidence": ["CKS-EVD-1"],
            "decision": "CKS-DEC-1",
        }
        self.assertEqual(validate_record_transition(record, "canonical")["status"], "PASS")


class CompatibilityTests(unittest.TestCase):
    def test_old_system_lifecycle_api_still_works(self) -> None:
        self.assertEqual(validate_state("PROPOSED")["status"], "PASS")
        self.assertEqual(validate_state("unknown")["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
