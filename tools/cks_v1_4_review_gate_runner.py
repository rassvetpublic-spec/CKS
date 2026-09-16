"""CKS v1.4 Review Gate runner prototype."""


def run_gate(checks):
    if all(checks.values()):
        return {"status": "PASS", "checks": checks}
    return {"status": "WARN", "checks": checks}
