"""CKS v1.4 Dashboard runtime compatibility layer.

Builds read-only dashboard data from metrics, graph and review results.
Dashboard is presentation layer and not SSOT.
"""

from datetime import datetime, timezone


def build_dashboard(metrics=None, graph=None, review=None):
    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return {
        "generated_at": generated_at,
        "metrics": metrics or {},
        "graph": graph or {},
        "review_gate": review or {},
        "is_source_of_truth": False,
    }
