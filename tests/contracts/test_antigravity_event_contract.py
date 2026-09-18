"""Контрактные проверки Antigravity Event Contract v1."""

EVENTS = {
    "SYSTEM_READY",
    "SYSTEM_IDLE",
    "TASK_CREATED",
    "TASK_RUNNING",
    "TASK_COMPLETED",
    "TASK_FAILED",
    "QA_RUNNING",
    "QA_PASS",
    "BLOCKED",
    "MERGE_READY",
    "EVIDENCE_READY",
}


def test_required_events_exist():
    assert "TASK_RUNNING" in EVENTS
    assert "QA_PASS" in EVENTS
    assert "EVIDENCE_READY" in EVENTS


def test_gui_is_not_decision_layer():
    forbidden = {"CHANGE_CANON", "CREATE_DECISION", "MODIFY_CKS"}
    assert forbidden.isdisjoint(EVENTS)
