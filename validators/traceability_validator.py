"""Traceability chain validator prototype."""


def validate_trace(trace):
    required = ["object_id", "evidence", "decision", "changes", "reviews"]
    missing = [key for key in required if key not in trace]
    return {"status": "PASS" if not missing else "FAIL", "missing": missing}
