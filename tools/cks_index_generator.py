#!/usr/bin/env python3
"""Generate a lightweight Knowledge Index for CKS objects."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "knowledge"
OUT = ROOT / "artifacts" / "cks-index" / "knowledge-index.json"


def main() -> int:
    items = []
    if SOURCE.exists():
        for path in SOURCE.rglob("*.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if isinstance(data, dict):
                items.append({
                    "id": data.get("id"),
                    "type": data.get("type"),
                    "status": data.get("status"),
                    "source": path.relative_to(ROOT).as_posix(),
                })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"schema_version": "1.0", "count": len(items), "items": items}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"indexed={len(items)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
