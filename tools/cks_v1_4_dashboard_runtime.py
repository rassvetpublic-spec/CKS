"""CKS v1.4 Dashboard runtime prototype.

Builds read-only dashboard data from metrics, graph and review results.
Dashboard is presentation layer and not SSOT.
"""

from datetime import datetime


def build_dashboard(metrics=None, graph=None, review=None):
    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "metrics": metrics or {},
        "graph": graph or {},
        "review_gate": review or {},
        "is_source_of_truth": False,
    }
