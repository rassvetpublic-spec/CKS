#!/usr/bin/env python3
"""Validate GitHub Issue/PR event metadata without making governance decisions."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


def validate_event(event: dict[str, Any]) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    kind = "unknown"
    payload: dict[str, Any] | None = None

    if isinstance(event.get("pull_request"), dict):
        kind = "pull_request"
        payload = event["pull_request"]
    elif isinstance(event.get("issue"), dict):
        kind = "issue"
        payload = event["issue"]

    if payload is None:
        findings.append({"level": "FAIL", "code": "EVENT_KIND_UNKNOWN", "message": "Issue/PR payload not found"})
    else:
        title = str(payload.get("title") or "").strip()
        body = str(payload.get("body") or "").strip()
        if not title:
            findings.append({"level": "FAIL", "code": "TITLE_MISSING", "message": "Title is required"})
        if not body:
            findings.append({"level": "FAIL", "code": "BODY_MISSING", "message": "Body is required"})
        elif kind == "pull_request":
            for marker in ("## Purpose", "## Classification", "## Validation", "Evidence:"):
                if marker not in body:
                    findings.append({
                        "level": "FAIL",
                        "code": "PR_TEMPLATE_INCOMPLETE",
                        "message": f"Missing PR template marker: {marker}",
                    })
        elif kind == "issue" and "## " not in body:
            findings.append({
                "level": "WARN",
                "code": "ISSUE_UNSTRUCTURED",
                "message": "Issue body has no level-2 sections",
            })

    failures = sum(1 for item in findings if item["level"] == "FAIL")
    warnings = sum(1 for item in findings if item["level"] == "WARN")
    return {
        "schema_version": "1.0",
        "kind": kind,
        "status": "FAIL" if failures else ("WARN" if warnings else "PASS"),
        "summary": {"fail": failures, "warn": warnings},
        "findings": findings,
        "authority": "validation_only",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="CKS Issue/PR metadata guard")
    parser.add_argument("--event", default=os.getenv("GITHUB_EVENT_PATH", ""))
    parser.add_argument("--report", default="artifacts/cks-issue-pr/event-validation.json")
    args = parser.parse_args()

    if not args.event:
        raise SystemExit("GITHUB_EVENT_PATH or --event is required")
    event = json.loads(Path(args.event).read_text(encoding="utf-8"))
    result = validate_event(event)
    report = Path(args.report)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
