"""Lifecycle state guard prototype."""

ALLOWED_STATES = [
    "DISCOVERED",
    "RESEARCHED",
    "PROPOSED",
    "REVIEWED",
    "ACCEPTED",
    "CANONICAL",
    "DEPRECATED",
    "ARCHIVED",
]


def validate_state(state):
    return {"status": "PASS" if state in ALLOWED_STATES else "FAIL"}
