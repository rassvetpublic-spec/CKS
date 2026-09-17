#!/usr/bin/env python3
"""Единый исполнитель проверок управления CKS.

Governance Runner v2 запускает фактические проверки, агрегирует их результат
и работает fail-closed: внутренняя ошибка проверки сама считается FAIL.
Runner диагностирует состояние, но не принимает Decision и не изменяет Canon.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from cks_self_audit import SelfAudit


def run_self_audit(root: Path) -> dict[str, Any]:
    try:
        result = SelfAudit(root).run()
    except Exception as exc:  # pragma: no cover - defensive boundary
        return {
            "status": "FAIL",
            "error": f"Self Audit exception: {exc.__class__.__name__}: {exc}",
        }
    if not isinstance(result, dict):
        return {"status": "FAIL", "error": "Self Audit returned non-object result"}
    if result.get("status") not in {"PASS", "WARN", "FAIL"}:
        return {"status": "FAIL", "error": "Self Audit returned unknown status", "result": result}
    return result


def run_ci_validator(root: Path) -> dict[str, Any]:
    validator = root / "tools" / "cks_ci.py"
    if not validator.exists():
        return {"status": "FAIL", "error": "tools/cks_ci.py отсутствует"}
    try:
        process = subprocess.run(
            [sys.executable, str(validator), "--mode", "all"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
    except Exception as exc:  # pragma: no cover - defensive boundary
        return {
            "status": "FAIL",
            "error": f"CI validator exception: {exc.__class__.__name__}: {exc}",
        }
    return {
        "status": "PASS" if process.returncode == 0 else "FAIL",
        "returncode": process.returncode,
        "stdout": process.stdout.strip(),
        "stderr": process.stderr.strip(),
    }


def run_all(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    self_audit = run_self_audit(root_path)
    ci = run_ci_validator(root_path)
    statuses = [self_audit.get("status"), ci.get("status")]
    status = "FAIL" if "FAIL" in statuses else ("WARN" if "WARN" in statuses else "PASS")
    return {
        "schema_version": "2.0",
        "kind": "cks_governance_report",
        "runner_version": "2",
        "status": status,
        "checks": {
            "self_audit": self_audit,
            "legacy_ci_validator": ci,
        },
        "summary": {
            "total_checks": 2,
            "failed_checks": sum(1 for value in statuses if value == "FAIL"),
            "warning_checks": sum(1 for value in statuses if value == "WARN"),
        },
        "authority": "validation_only",
        "rule": "Проверка не является архитектурным решением и не изменяет Canon.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="CKS: единый исполнитель проверок управления")
    parser.add_argument("--root", default=".")
    parser.add_argument("--report")
    args = parser.parse_args()

    result = run_all(args.root)
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        report = Path(args.report)
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(text, encoding="utf-8")
    print(text, end="")
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
