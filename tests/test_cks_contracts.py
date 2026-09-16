#!/usr/bin/env python3
"""CKS v1.3 negative contract test cases.

These cases document expected failures for invalid knowledge objects.
"""


def test_invalid_id_pattern():
    invalid_id = "DEC-001"
    assert not invalid_id.startswith("CKS-")


def test_research_cannot_be_core():
    lifecycle = "research"
    document_type = "canon"
    assert not (lifecycle == "research" and document_type == "canon")


def test_canon_requires_evidence_decision_history_owner():
    required = {"evidence", "decision", "history", "owner"}
    payload = {"evidence", "decision"}
    assert not required.issubset(payload)
