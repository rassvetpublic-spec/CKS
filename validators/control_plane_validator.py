"""CKS v1.5 Control Plane Validator prototype."""

from pathlib import Path

REQUIRED_CONTROL_FILES = [
    "control/system-state.yaml",
    "control/ssot-registry.yaml",
    "control/traceability-model.yaml",
    "control/lifecycle-state-model.yaml",
    "control/automation-governance.yaml",
]


def validate_control_plane(root="."):
    missing = []
    for item in REQUIRED_CONTROL_FILES:
        if not Path(root, item).exists():
            missing.append(item)
    return {"status": "PASS" if not missing else "FAIL", "missing": missing}


def main() -> int:
    result = validate_control_plane()
    print(result)
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
