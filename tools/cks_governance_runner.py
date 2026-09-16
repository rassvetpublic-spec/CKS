"""CKS Governance Runner.

Single orchestration entry point for governance validators.
Validators report findings; they do not modify canon.
"""

VALIDATORS = [
    "control_plane_validator",
    "ssot_consistency_validator",
    "traceability_validator",
    "lifecycle_guard",
]


def run_all():
    return {"validators": VALIDATORS, "status": "READY"}


if __name__ == "__main__":
    print(run_all())
