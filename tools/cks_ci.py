#!/usr/bin/env python3
"""CKS CI validator.

Performs dependency-free validation for schemas, knowledge objects,
traceability, Canon entry rules, and Review Gate execution. Reports are
written to artifacts/cks-ci/ as JSON and Markdown.
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

try:
    from cks_json_schema_validator import validate_instance
except ImportError:  # support import as tools.cks_ci in tests
    from tools.cks_json_schema_validator import validate_instance

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "cks-ci"
ID_RE = re.compile(r"\bCKS-([A-Z]+)-([0-9]+)\b")
VALID_ID_RE = re.compile(r"^CKS-[A-Z]+-[0-9]+$")
TOP_LEVEL_YAML_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$")
ALLOWED_RELATIONS = {
    "supports", "contradicts", "implements", "supersedes",
    "depends_on", "derived_from", "validates",
}
CANON_MARKERS = ("evidence", "decision", "history", "owner")
DISTILLATE_TELEMETRY_FIELDS = {"worker_id", "task_id", "rule_hash", "status"}
DISTILLATE_STATUS = {"PASS", "FAIL", "BLOCKED"}
DISTILLATE_DATA_TYPES = {"FACT", "DECISION", "RULE", "OBSERVATION", "TEMPORARY"}


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


def _event_before_sha() -> str:
    explicit = os.getenv("CKS_BASE_SHA", "").strip()
    if explicit:
        return explicit
    event_path = os.getenv("GITHUB_EVENT_PATH", "").strip()
    if not event_path:
        return ""
    try:
        payload = json.loads(Path(event_path).read_text(encoding="utf-8"))
    except Exception:
        return ""
    value = payload.get("before")
    return str(value).strip() if value else ""


def changed_files() -> list[str]:
    """Return the full changed-file set for PRs or multi-commit pushes."""
    base_ref = os.getenv("GITHUB_BASE_REF", "").strip()
    if base_ref:
        for base in (f"origin/{base_ref}", base_ref):
            text = run_git("diff", "--name-only", f"{base}...HEAD")
            if text:
                return [x for x in text.splitlines() if x]

    before = _event_before_sha()
    if before and set(before) != {"0"}:
        text = run_git("diff", "--name-only", before, "HEAD")
        if text:
            return [x for x in text.splitlines() if x]

    text = run_git("diff", "--name-only", "HEAD^", "HEAD")
    if text:
        return [x for x in text.splitlines() if x]
    return []


def parse_metadata(text: str) -> dict[str, object]:
    """Parse simple YAML-like Markdown metadata without external dependencies."""
    lines = text.splitlines()
    block: list[str] = []
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            block.append(line)
    else:
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


def _yaml_top_level(text: str) -> tuple[dict[str, str | None], list[str]]:
    data: dict[str, str | None] = {}
    duplicates: list[str] = []
    for raw in text.splitlines():
        if not raw or raw[0].isspace() or raw.lstrip().startswith("#"):
            continue
        match = TOP_LEVEL_YAML_RE.match(raw)
        if not match:
            continue
        key, value = match.groups()
        if key in data:
            duplicates.append(key)
        cleaned = (value or "").strip()
        if cleaned and cleaned[0:1] in {'"', "'"} and cleaned[-1:] == cleaned[0:1]:
            cleaned = cleaned[1:-1]
        data[key] = cleaned or None
    return data, duplicates


def _yaml_section(text: str, section: str) -> dict[str, str | None]:
    result: dict[str, str | None] = {}
    active = False
    base_indent = 0
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if not active:
            if indent == 0 and stripped == f"{section}:":
                active = True
                base_indent = indent
            continue
        if indent <= base_indent:
            break
        if indent != base_indent + 2 or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        cleaned = value.strip()
        if cleaned and cleaned[0:1] in {'"', "'"} and cleaned[-1:] == cleaned[0:1]:
            cleaned = cleaned[1:-1]
        result[key.strip()] = cleaned or None
    return result


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


def _validate_distillate_yaml(path: Path, findings: list[Finding]) -> None:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8", errors="replace")
    top, duplicates = _yaml_top_level(text)
    if duplicates:
        findings.append(Finding("FAIL", "YAML_DUPLICATE_TOP_LEVEL_KEY", rel, "Повторяются ключи: " + ", ".join(sorted(set(duplicates)))))
    for field in ("version", "telemetry"):
        if field not in top:
            findings.append(Finding("FAIL", "DISTILLATE_REQUIRED_MISSING", rel, f"Нет обязательного поля {field}"))
    telemetry = _yaml_section(text, "telemetry")
    missing = sorted(DISTILLATE_TELEMETRY_FIELDS - set(telemetry))
    if missing:
        findings.append(Finding("FAIL", "DISTILLATE_TELEMETRY_MISSING", rel, "Нет telemetry-полей: " + ", ".join(missing)))
    status = telemetry.get("status")
    if status and status not in DISTILLATE_STATUS:
        findings.append(Finding("FAIL", "DISTILLATE_STATUS_INVALID", rel, f"Недопустимый telemetry.status: {status}"))
    if "data_plane" in top:
        plane = _yaml_section(text, "data_plane")
        dtype = plane.get("type")
        if dtype and dtype not in DISTILLATE_DATA_TYPES:
            findings.append(Finding("FAIL", "DISTILLATE_TYPE_INVALID", rel, f"Недопустимый data_plane.type: {dtype}"))
        if "payload" not in plane:
            findings.append(Finding("FAIL", "DISTILLATE_PAYLOAD_MISSING", rel, "data_plane задан без payload"))


def validate_knowledge_json(findings: list[Finding]) -> None:
    """Validate canonical knowledge JSON and fail closed on unclassified YAML.

    Canonical knowledge objects are JSON and are checked against the active
    JSON Schema. YAML remains allowed only for explicitly typed contracts such
    as distillate_object; this prevents YAML knowledge objects from silently
    bypassing validation.
    """
    base = ROOT / "knowledge"
    if not base.exists():
        return

    schema_path = ROOT / "schemas" / "cks-knowledge-object.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception:
        return  # schema_checks reports the root cause

    canonical_count = 0
    for path in sorted(base.rglob("*.json")):
        rel = path.relative_to(ROOT).as_posix()
        canonical_count += 1
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            findings.append(Finding("FAIL", "OBJECT_JSON_INVALID", rel, f"Некорректный JSON: {exc}"))
            continue
        if not isinstance(data, dict):
            findings.append(Finding("FAIL", "OBJECT_ROOT_INVALID", rel, "Корень knowledge object должен быть JSON object"))
            continue
        for error in validate_instance(data, schema):
            findings.append(Finding("FAIL", "OBJECT_SCHEMA_INVALID", rel, error))
        for relation in data.get("relations", []) if isinstance(data.get("relations"), list) else []:
            if isinstance(relation, dict):
                rtype = relation.get("type")
                if rtype and rtype not in ALLOWED_RELATIONS:
                    findings.append(Finding("FAIL", "RELATION_TYPE_INVALID", rel, f"Недопустимый relation type: {rtype}"))

    if canonical_count == 0:
        findings.append(Finding("FAIL", "KNOWLEDGE_OBJECTS_NOT_VALIDATED", "knowledge/", "Не найдено ни одного канонического JSON knowledge object"))

    yaml_paths = sorted(list(base.rglob("*.yaml")) + list(base.rglob("*.yml")))
    for path in yaml_paths:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        top, duplicates = _yaml_top_level(text)
        if duplicates:
            findings.append(Finding("FAIL", "YAML_DUPLICATE_TOP_LEVEL_KEY", rel, "Повторяются ключи: " + ", ".join(sorted(set(duplicates)))))
        object_kind = top.get("object")
        if object_kind == "distillate_object":
            _validate_distillate_yaml(path, findings)
            continue
        if "id" in top or object_kind == "knowledge_object":
            findings.append(Finding(
                "FAIL",
                "KNOWLEDGE_OBJECT_YAML_NONCANONICAL",
                rel,
                "Канонический knowledge object в YAML обходит JSON Schema; мигрируйте объект в JSON",
            ))
            continue
        findings.append(Finding(
            "FAIL",
            "KNOWLEDGE_YAML_UNCLASSIFIED",
            rel,
            "YAML в knowledge/ не привязан к явно поддерживаемому контракту",
        ))


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


def select_files(findings: list[Finding]) -> list[str]:
    files = changed_files()
    if files:
        return files
    event_name = os.getenv("GITHUB_EVENT_NAME", "").strip()
    if os.getenv("GITHUB_ACTIONS", "").lower() == "true" and event_name in {"push", "pull_request", "pull_request_target"}:
        findings.append(Finding(
            "FAIL",
            "CHANGED_FILES_UNRESOLVED",
            ".git",
            "CI не смог определить изменённые файлы; проверка не может завершиться ложным PASS",
        ))
    return []


def write_reports(mode: str, findings: list[Finding], files: list[str]) -> dict[str, object]:
    OUT.mkdir(parents=True, exist_ok=True)
    failures = sum(1 for f in findings if f.level == "FAIL")
    warnings = sum(1 for f in findings if f.level == "WARN")
    result = {
        "schema_version": "1.1",
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
    files = select_files(findings)
    schema_checks(findings)
    validate_knowledge_json(findings)
    document_checks(findings, files, args.mode)
    result = write_reports(args.mode, findings, files)
    print(json.dumps(result["summary"], ensure_ascii=False))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
