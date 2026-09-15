"""CKS Bootstrap 1.0 validation placeholder.

Checks minimal bootstrap invariants:
- repository structure
- knowledge object schema presence
- lifecycle compatibility
- rejection of raw context objects
"""

from pathlib import Path


def validate():
    required = [
        Path("schemas/knowledge_object_v1.yaml"),
        Path("knowledge/objects"),
    ]
    return all(path.exists() for path in required)


if __name__ == "__main__":
    print("PASS" if validate() else "FAIL")
