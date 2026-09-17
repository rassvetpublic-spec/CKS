#!/usr/bin/env python3
"""Validate GitHub Issue/PR event metadata without making governance decisions."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


ISSUE_TEMPLATE_PROFILES: dict[str, tuple[str, ...]] = {
    "task": (
        "## Goal",
        "## Context",
        "## Decision needed",
        "## Evidence",
        "## Acceptance criteria",
    ),
    "decision": (
        "## Context",
        "## Options",
        "## Decision",
        "## Evidence",
        "## Status",
    ),
    "donor_audit": (
        "## Donor System",
        "## Purpose",
        "## Extracted Patterns",
        "## Rejected Elements",
        "## Decision",
    ),
}

ISSUE_TEMPLATE_SIGNATURES = {
    "task": "## Goal",
    "decision": "## Options",
    "donor_audit": "## Donor System",
}

PR_TEMPLATE_MARKERS = (
    "## Purpose",
    "## Classification",
    "## Validation",
    "Context impact:",
    "Canon impact:",
    "Evidence:",
)


def _validate_issue_body(body: str, findings: list[dict[str, str]]) -> None:
    """Validate known issue templates while keeping generic structured issues advisory."""

    matched_profile = None
    for profile, signature in ISSUE_TEMPLATE_SIGNATURES.items():
        if signature in body:
            matched_profile = profile
            break

    if matched_profile is None:
        if "## " not in body:
            findings.append({
                "level": "WARN",
                "code": "ISSUE_UNSTRUCTURED",
                "message": "Issue body has no level-2 sections",
            })
        else:
            findings.append({
                "level": "WARN",
                "code": "ISSUE_TEMPLATE_UNKNOWN",
                "message": "Issue is structured but does not match a registered CKS issue template",
            })
        return

    for marker in ISSUE_TEMPLATE_PROFILES[matched_profile]:
        if marker not in body:
            findings.append({
                "level": "FAIL",
                "code": "ISSUE_TEMPLATE_INCOMPLETE",
                "message": f"{matched_profile} template is missing marker: {marker}",
            })


def _validate_pr_body(body: str, findings: list[dict[str, str]]) -> None:
    for marker in PR_TEMPLATE_MARKERS:
        if marker not in body:
            findings.append({
                "level": "FAIL",
                "code": "PR_TEMPLATE_INCOMPLETE",
                "message": f"Missing PR template marker: {marker}",
            })


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
            _validate_pr_body(body, findings)
        elif kind == "issue":
            _validate_issue_body(body, findings)

    failures = sum(1 for item in findings if item["level"] == "FAIL")
    warnings = sum(1 for item in findings if item["level"] == "WARN")
    return {
        "schema_version": "1.1",
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
