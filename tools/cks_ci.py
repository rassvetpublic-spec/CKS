#!/usr/bin/env python3
"""CKS v1.3 CI validator.

Performs lightweight, dependency-free validation for schemas, traceability,
Canon entry rules, and the Review Gate. Reports are written to
artifacts/cks-ci/ as JSON and Markdown.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "cks-ci"
ID_RE = re.compile(r"\bCKS-([A-Z]+)-([0-9]+)\b")
VALID_ID_RE = re.compile(r"^CKS-[A-Z]+-[0-9]+$")
ALLOWED_RELATIONS = {
    "supports", "contradicts", "implements", "supersedes",
    "depends_on", "derived_from", "validates",
}
CANON_MARKERS = ("evidence", "decision", "history", "owner")


@dataclass
class Finding:
    level: str
    code: str
    path: str
    message: str


def run_git(*args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return ""


def changed_files() -> list[str]:
    base_ref = os.getenv("GITHUB_BASE_REF", "").strip()
    if base_ref:
        text = run_git("diff", "--name-only", f"origin/{base_ref}...HEAD")
        if text:
            return [x for x in text.splitlines() if x]
    text = run_git("diff", "--name-only", "HEAD^", "HEAD")
    if text:
        return [x for x in text.splitlines() if x]
    return []


def parse_metadata(text: str) -> dict[str, object]:
    """Parse simple YAML-like front matter without external dependencies."""
    lines = text.splitlines()
    block: list[str] = []
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            block.append(line)
    else:
        # Also accept an early fenced yaml block.
        start = None
        for i, line in enumerate(lines[:40]):
            if line.strip().lower() in {"```yaml", "```yml"}:
                start = i + 1
                break
        if start is not None:
            for line in lines[start:start + 60]:
                if line.strip() == "```":
                    break
                block.append(line)
    meta: dict[str, object] = {}
    current_list_key: str | None = None
    for raw in block:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("-") and current_list_key:
            meta.setdefault(current_list_key, [])
            if isinstance(meta[current_list_key], list):
                meta[current_list_key].append(line[1:].strip().strip('"\''))
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"\'')
        if not key:
            continue
        if value == "":
            meta[key] = []
            current_list_key = key
        else:
            current_list_key = None
            if value.startswith("[") and value.endswith("]"):
                values = [v.strip().strip('"\'') for v in value[1:-1].split(",") if v.strip()]
                meta[key] = values
            else:
                meta[key] = value
    return meta


def schema_checks(findings: list[Finding]) -> None:
    for rel in ("schemas/cks-knowledge-object.schema.json", "schemas/cks-document-metadata.schema.json"):
        path = ROOT / rel
        if not path.exists():
            findings.append(Finding("FAIL", "SCHEMA_MISSING", rel, "Обязательная JSON Schema отсутствует"))
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            findings.append(Finding("FAIL", "SCHEMA_JSON_INVALID", rel, f"Некорректный JSON: {exc}"))
            continue
        if data.get("type") != "object" or not data.get("required"):
            findings.append(Finding("FAIL", "SCHEMA_CONTRACT_WEAK", rel, "Schema должна описывать object и required-поля"))


def validate_knowledge_json(findings: list[Finding]) -> None:
    base = ROOT / "knowledge"
    if not base.exists():
        return
    required = {"id", "type", "status", "owner", "lifecycle", "relations", "evidence", "history"}
    for path in base.rglob("*.json"):
        rel = path.relative_to(ROOT).as_posix()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            findings.append(Finding("FAIL", "OBJECT_JSON_INVALID", rel, f"Некорректный JSON: {exc}"))
            continue
        if not isinstance(data, dict):
            continue
        missing = sorted(required - set(data))
        if missing:
            findings.append(Finding("FAIL", "OBJECT_REQUIRED_MISSING", rel, "Отсутствуют поля: " + ", ".join(missing)))
        obj_id = str(data.get("id", ""))
        if obj_id and not VALID_ID_RE.match(obj_id):
            findings.append(Finding("FAIL", "OBJECT_ID_INVALID", rel, f"ID не соответствует CKS-TYPE-NUMBER: {obj_id}"))
        for relation in data.get("relations", []) if isinstance(data.get("relations"), list) else []:
            if isinstance(relation, dict):
                rtype = relation.get("type")
                if rtype and rtype not in ALLOWED_RELATIONS:
                    findings.append(Finding("FAIL", "RELATION_TYPE_INVALID", rel, f"Недопустимый relation type: {rtype}"))


def is_canon_candidate(path: str, text: str, meta: dict[str, object]) -> bool:
    if path.startswith("core/") and path.endswith(".md"):
        return True
    return str(meta.get("type", "")).lower() == "canon"


def marker_present(name: str, text: str, meta: dict[str, object]) -> bool:
    value = meta.get(name)
    if isinstance(value, list):
        if value:
            return True
    elif value not in (None, "", []):
        return True
    return re.search(rf"(?im)^\s*{re.escape(name)}\s*:\s*\S+", text) is not None


def document_checks(findings: list[Finding], files: Iterable[str], mode: str) -> None:
    for rel in files:
        if not rel.endswith(".md"):
            continue
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        meta = parse_metadata(text)

        if meta.get("id") and not VALID_ID_RE.match(str(meta["id"])):
            findings.append(Finding("FAIL", "DOC_ID_INVALID", rel, f"Некорректный CKS ID: {meta['id']}"))

        if mode in {"all", "traceability", "review-gate"}:
            refs = {m.group(1) for m in ID_RE.finditer(text)}
            dtype = str(meta.get("type", "")).lower()
            status = str(meta.get("status", "")).lower()
            if dtype == "proposal" and status in {"review", "active"} and "EVD" not in refs:
                findings.append(Finding("WARN", "PROPOSAL_NO_EVIDENCE", rel, "Proposal в review/active не содержит ссылки CKS-EVD-*"))
            if "DEC" in refs and "EVD" not in refs:
                findings.append(Finding("WARN", "DECISION_REF_WITHOUT_EVIDENCE", rel, "Есть ссылка Decision, но нет Evidence"))

        if mode in {"all", "canon", "review-gate"} and is_canon_candidate(rel, text, meta):
            missing = [name for name in CANON_MARKERS if not marker_present(name, text, meta)]
            if missing:
                findings.append(Finding("FAIL", "CANON_GATE_MISSING", rel, "Canon/Core изменение без обязательных полей: " + ", ".join(missing)))
            lifecycle = str(meta.get("lifecycle", "")).lower()
            if lifecycle == "research":
                findings.append(Finding("FAIL", "RESEARCH_CORE_BOUNDARY", rel, "Research lifecycle не может быть Canon/Core"))


def select_files() -> list[str]:
    files = changed_files()
    if files:
        return files
    # Local/manual fallback: do not retroactively fail the whole repository.
    return []


def write_reports(mode: str, findings: list[Finding], files: list[str]) -> dict[str, object]:
    OUT.mkdir(parents=True, exist_ok=True)
    failures = sum(1 for f in findings if f.level == "FAIL")
    warnings = sum(1 for f in findings if f.level == "WARN")
    result = {
        "schema_version": "1.0",
        "mode": mode,
        "status": "FAIL" if failures else ("WARN" if warnings else "PASS"),
        "summary": {"fail": failures, "warn": warnings, "checked_changed_files": len(files)},
        "changed_files": files,
        "findings": [asdict(f) for f in findings],
    }
    (OUT / f"{mode}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = [
        f"# CKS CI Report — {mode}",
        "",
        f"Status: **{result['status']}**",
        f"FAIL: {failures} | WARN: {warnings} | Changed files: {len(files)}",
        "",
        "## Findings",
    ]
    if not findings:
        md.append("- Нарушений не обнаружено.")
    else:
        for f in findings:
            md.append(f"- **{f.level}** `{f.code}` `{f.path}` — {f.message}")
    (OUT / f"{mode}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["all", "traceability", "canon", "review-gate"], default="all")
    args = parser.parse_args()

    findings: list[Finding] = []
    files = select_files()
    schema_checks(findings)
    validate_knowledge_json(findings)
    document_checks(findings, files, args.mode)
    result = write_reports(args.mode, findings, files)
    print(json.dumps(result["summary"], ensure_ascii=False))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
