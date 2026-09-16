"""Checks SSOT registry presence and basic consistency."""


def validate_ssot(record):
    required = ["id", "type", "source", "version", "status"]
    missing = [key for key in required if key not in record]
    return {"status": "PASS" if not missing else "FAIL", "missing": missing}
