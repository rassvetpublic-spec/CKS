#!/usr/bin/env python3
"""Generate a lightweight, derived Knowledge Index for CKS objects.

The index is operational output only and never replaces source objects.
JSON and simple top-level YAML/front-matter metadata are supported without
external dependencies.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "knowledge"
OUT = ROOT / "artifacts" / "cks-index" / "knowledge-index.json"
TOP_LEVEL = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")


def _scalar(value: str) -> Any:
    value = value.strip()
    if not value or value in {"|", ">"}:
        return None
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


def parse_simple_metadata(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix == ".json":
        data = json.loads(text)
        return data if isinstance(data, dict) else {}

    lines = text.splitlines()
    if path.suffix == ".md":
        if not lines or lines[0].strip() != "---":
            return {}
        block: list[str] = []
        for line in lines[1:]:
            if line.strip() == "---":
                break
            block.append(line)
        lines = block

    data: dict[str, Any] = {}
    for raw in lines:
        if not raw or raw[0].isspace() or raw.lstrip().startswith("#"):
            continue
        match = TOP_LEVEL.match(raw)
        if not match:
            continue
        key, value = match.groups()
        parsed = _scalar(value)
        if parsed is not None:
            data[key] = parsed
    return data


def build_index(source: Path = SOURCE, root: Path = ROOT) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    parse_errors: list[dict[str, str]] = []
    if source.exists():
        paths = sorted(
            path for path in source.rglob("*")
            if path.is_file() and path.suffix.lower() in {".json", ".yaml", ".yml", ".md"}
        )
        for path in paths:
            try:
                data = parse_simple_metadata(path)
            except Exception as exc:
                parse_errors.append({
                    "source": path.relative_to(root).as_posix(),
                    "error": f"{exc.__class__.__name__}: {exc}",
                })
                continue
            object_id = data.get("id")
            if not object_id:
                continue
            items.append({
                "id": object_id,
                "type": data.get("type"),
                "status": data.get("status"),
                "title": data.get("title") or data.get("name"),
                "source": path.relative_to(root).as_posix(),
            })
    items.sort(key=lambda item: (str(item.get("id") or ""), item["source"]))
    return {
        "schema_version": "2.1",
        "derived_index": True,
        "derived_artifact": True,
        "ssot": False,
        "generator": "cks_index_generator",
        "count": len(items),
        "parse_errors": parse_errors,
        "items": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="CKS Knowledge Index generator")
    parser.add_argument("--source", default=str(SOURCE))
    parser.add_argument("--output", default=str(OUT))
    args = parser.parse_args()

    source = Path(args.source).resolve()
    output = Path(args.output).resolve()
    result = build_index(source, ROOT)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"indexed={result['count']} parse_errors={len(result['parse_errors'])}")
    return 1 if result["parse_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
