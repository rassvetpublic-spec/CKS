#!/usr/bin/env python3
"""CKS migration audit helper.

Detects documents without metadata markers and possible duplicate rule titles.
The report is advisory and does not modify source documents or make Decisions.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "cks-ci" / "migration-audit.json"


def audit(root: Path = ROOT) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    seen_titles: dict[str, Path] = {}
    for path in root.rglob("*.md"):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        title = None
        for line in text.splitlines()[:20]:
            if line.startswith("# "):
                title = line[2:].strip()
                break
        if title:
            if title in seen_titles:
                findings.append({
                    "level": "WARN",
                    "code": "DUPLICATE_TITLE",
                    "files": [
                        seen_titles[title].relative_to(root).as_posix(),
                        path.relative_to(root).as_posix(),
                    ],
                })
            else:
                seen_titles[title] = path
        if "type:" not in text[:1500] and "document:" not in text[:1500]:
            findings.append({
                "level": "WARN",
                "code": "MISSING_METADATA_HEADER",
                "file": path.relative_to(root).as_posix(),
            })
    return {
        "schema_version": "2.0",
        "status": "WARN" if findings else "PASS",
        "advisory": True,
        "finding_count": len(findings),
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="CKS migration audit")
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--output", default=str(OUT))
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output = Path(args.output).resolve()
    result = audit(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "finding_count": result["finding_count"]}, ensure_ascii=False))
    # Advisory by design: findings are migration debt, not an automatic Decision.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
