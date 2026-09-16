#!/usr/bin/env python3
"""CKS v1.3 migration audit helper.

Detects documents without metadata markers and possible duplicate rule titles.
The report is advisory and does not modify source documents.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "cks-ci"


def audit():
    findings = []
    seen_titles = {}
    for path in ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        title = None
        for line in text.splitlines()[:20]:
            if line.startswith("# "):
                title = line[2:].strip()
                break
        if title:
            if title in seen_titles:
                findings.append({"level":"WARN","code":"DUPLICATE_TITLE","files":[str(seen_titles[title]),str(path)]})
            else:
                seen_titles[title] = path
        if "type:" not in text[:1500] and "document:" not in text[:1500]:
            findings.append({"level":"WARN","code":"MISSING_METADATA_HEADER","file":str(path)})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "migration-audit.json").write_text(json.dumps({"findings":findings},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

if __name__ == "__main__":
    audit()
