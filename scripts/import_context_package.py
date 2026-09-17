"""Validate KAT9I_OS context packages before CKS ingestion.

This module enforces the active v1 exchange contract without promoting or
mutating knowledge in CKS.  It intentionally remains a validator only.
"""

from datetime import datetime
from typing import Any


REQUIRED_FIELDS = (
    "id",
    "source_system",
    "source_reference",
    "created_at",
    "split_mode",
    "artifacts",
)

SUPPORTED_SPLIT_MODES = frozenset(
    {
        "SPLIT",
        "AUDIT",
        "REVIEW",
        "RESEARCH",
        "MIGRATION",
        "CLEANUP",
        "MERGE",
        "CANON CHECK",
    }
)

PROHIBITED_TRUTHY_FLAGS = (
    "raw_runtime_state",
    "raw_chat_dump",
    "hidden_memory",
    "direct_canon_update",
)


def _is_datetime(value: Any) -> bool:
    """Return True for a datetime object or an ISO-8601 datetime string."""

    if isinstance(value, datetime):
        return True
    if not isinstance(value, str) or not value:
        return False

    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        datetime.fromisoformat(candidate)
    except ValueError:
        return False
    return True


def validate_package(package: dict) -> bool:
    """Return whether *package* satisfies the active KAT9I_OS v1 contract."""

    if not isinstance(package, dict):
        return False

    if any(field not in package for field in REQUIRED_FIELDS):
        return False

    if not isinstance(package["id"], str):
        return False
    if package["source_system"] != "KAT9I_OS":
        return False
    if not isinstance(package["source_reference"], str):
        return False
    if not _is_datetime(package["created_at"]):
        return False
    if package["split_mode"] not in SUPPORTED_SPLIT_MODES:
        return False
    if not isinstance(package["artifacts"], list):
        return False

    if any(package.get(flag) for flag in PROHIBITED_TRUTHY_FLAGS):
        return False

    if package.get("type") == "raw_context_dump":
        return False

    return True


if __name__ == "__main__":
    print("CKS context package validator ready")
