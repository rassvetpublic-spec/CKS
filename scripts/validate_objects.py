"""Basic CKS object validation placeholder.

Validates future Knowledge Object, Decision Record and Evidence Record contracts.
"""

from pathlib import Path

REQUIRED_DIRS = [
    "knowledge",
    "decisions",
    "evidence",
    "graveyard",
]


def validate_structure(root=Path('.')):
    return all((root / item).exists() for item in REQUIRED_DIRS)


if __name__ == "__main__":
    raise SystemExit(0 if validate_structure() else 1)
