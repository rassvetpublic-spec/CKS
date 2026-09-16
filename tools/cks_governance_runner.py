#!/usr/bin/env python3
"""Единый исполнитель проверок управления CKS.

Governance Runner (исполнитель правил управления) запускает фактические
проверки и агрегирует их результат. Он диагностирует состояние, но не
принимает Decision и не изменяет Canon.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from cks_self_audit import SelfAudit


def run_ci_validator(root: Path) -> dict[str, Any]:
    validator = root / "tools" / "cks_ci.py"
    if not validator.exists():
        return {"status": "FAIL", "error": "tools/cks_ci.py отсутствует"}
    process = subprocess.run(
        [sys.executable, str(validator), "--mode", "all"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "status": "PASS" if process.returncode == 0 else "FAIL",
        "returncode": process.returncode,
        "stdout": process.stdout.strip(),
        "stderr": process.stderr.strip(),
    }


def run_all(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    self_audit = SelfAudit(root_path).run()
    ci = run_ci_validator(root_path)
    statuses = [self_audit.get("status"), ci.get("status")]
    status = "FAIL" if "FAIL" in statuses else ("WARN" if "WARN" in statuses else "PASS")
    return {
        "schema_version": "1.0",
        "kind": "cks_governance_report",
        "status": status,
        "checks": {
            "self_audit": self_audit,
            "legacy_ci_validator": ci,
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
