#!/usr/bin/env python3
"""Единый рабочий контур CKS v1.5.

Pipeline (последовательность обработки) связывает рабочий граф знаний,
трассируемость, федерацию проектов и самопроверку. Результат является
диагностическим снимком и не является источником истины или решением.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from cks_knowledge_federation import KnowledgeFederation
from cks_self_audit import SelfAudit
from cks_traceability_engine import TraceabilityEngine


def run_pipeline(
    *,
    root: str | Path,
    records: list[dict[str, Any]] | None = None,
    projects: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    trace_engine = TraceabilityEngine()
    trace_result = trace_engine.ingest(records or []) if records is not None else {
        "status": "SKIP",
        "records": 0,
        "edges": 0,
        "broken_references": [],
    }

    federation = KnowledgeFederation()
    federation_error: str | None = None
    if projects is not None:
        try:
            for project in projects:
                federation.add_project(project)
            federation_result = federation.validate()
        except Exception as exc:
            federation_error = str(exc)
            federation_result = {"status": "FAIL", "error": federation_error}
    else:
        federation_result = {"status": "SKIP", "projects": 0}

    self_audit = SelfAudit(root).run()
    statuses = [trace_result.get("status"), federation_result.get("status"), self_audit.get("status")]
    overall = "FAIL" if "FAIL" in statuses else ("WARN" if "WARN" in statuses else "PASS")

    return {
        "schema_version": "1.0",
        "kind": "cks_runtime_snapshot",
        "status": overall,
        "traceability": trace_result,
        "federation": federation_result,
        "self_audit": self_audit,
        "derived": {
            "trace_graph": trace_engine.export() if records is not None else None,
            "federation_index": federation.export_index() if projects is not None and federation_error is None else None,
        },
        "authority": "diagnostic_only",
        "rules": [
            "Граф не является SSOT.",
            "Автоматизация не принимает Decision.",
            "Федерация не объединяет Canon проектов.",
        ],
    }


def _read_optional_list(path: str | None) -> list[dict[str, Any]] | None:
    if not path:
        return None
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"Ожидался JSON-массив: {path}")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="CKS: единый рабочий контур")
    parser.add_argument("--root", default=".")
    parser.add_argument("--records", help="JSON-массив объектов для трассируемости")
    parser.add_argument("--projects", help="JSON-массив манифестов проектов")
    parser.add_argument("--output", required=True, help="Файл диагностического снимка JSON")
    args = parser.parse_args()

    try:
        result = run_pipeline(
            root=args.root,
            records=_read_optional_list(args.records),
            projects=_read_optional_list(args.projects),
        )
    except (ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 1

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "output": str(output)}, ensure_ascii=False))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
