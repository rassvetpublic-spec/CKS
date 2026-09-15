"""CKS structure validation entry point."""

from pathlib import Path

REQUIRED = [
    "README.md",
    "protocols",
    "schemas",
    "knowledge",
    "decisions",
    "evidence",
    "graveyard",
]


def validate(root: Path) -> list[str]:
    return [x for x in REQUIRED if not (root / x).exists()]


if __name__ == "__main__":
    missing = validate(Path('.'))
    raise SystemExit(1 if missing else 0)
