"""Validate KAT9I_OS context packages before CKS ingestion.

This module enforces the active v1 exchange contract without promoting or
mutating knowledge in CKS. It intentionally remains a validator only.
"""

from datetime import datetime
import json
from pathlib import Path
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


def _parse_yaml_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value.startswith("[") and value.endswith("]"):
        parsed = json.loads(value)
        if not isinstance(parsed, list):
            raise ValueError("inline collection must be a list")
        return parsed
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none", "~"}:
        return None
    return value


def load_context_package(path: str | Path) -> dict[str, Any]:
    """Load the active flat context-package YAML contract fail-closed.

    The exchange instance is intentionally flat. Both inline JSON-style lists
    and ordinary YAML block lists are accepted. Nested mappings are rejected
    explicitly instead of being silently misparsed by ad-hoc test code.
    """

    result: dict[str, Any] = {}
    current_list_key: str | None = None
    source = Path(path)

    for line_number, raw in enumerate(source.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if raw[0].isspace():
            if current_list_key and stripped.startswith("-"):
                result[current_list_key].append(_parse_yaml_scalar(stripped[1:].strip()))
                continue
            raise ValueError(f"line {line_number}: nested mapping is outside the active flat context-package contract")

        current_list_key = None
        if ":" not in raw:
            raise ValueError(f"line {line_number}: expected key: value")
        key, value = raw.split(":", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"line {line_number}: empty key")
        if key in result:
            raise ValueError(f"line {line_number}: duplicate key {key!r}")

        value = value.strip()
        if value == "":
            result[key] = []
            current_list_key = key
        else:
            result[key] = _parse_yaml_scalar(value)

    return result


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
