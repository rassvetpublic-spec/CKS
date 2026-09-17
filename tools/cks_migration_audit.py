#!/usr/bin/env python3
"""CKS migration audit helper.

Detects documents without metadata markers and possible duplicate rule titles.
The report is advisory and does not modify source documents or make Decisions.
Generated reports are excluded so the audit cannot create its own migration debt.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "cks-ci" / "migration-audit.json"
GENERATED_ROOTS = {"artifacts", "reports"}


def source_markdown_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for path in root.rglob("*.md"):
        rel = path.relative_to(root)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if rel.parts and rel.parts[0] in GENERATED_ROOTS:
            continue
        paths.append(path)
    return sorted(paths, key=lambda p: p.relative_to(root).as_posix())


def audit(root: Path = ROOT) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    seen_titles: dict[str, Path] = {}
    checked_files = source_markdown_paths(root)

    for path in checked_files:
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
        "schema_version": "2.1",
        "status": "WARN" if findings else "PASS",
        "advisory": True,
        "derived_artifact": True,
        "ssot": False,
        "checked_files": len(checked_files),
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
    print(json.dumps({
        "status": result["status"],
        "checked_files": result["checked_files"],
        "finding_count": result["finding_count"],
    }, ensure_ascii=False))
    # Advisory by design: findings are migration debt, not an automatic Decision.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
