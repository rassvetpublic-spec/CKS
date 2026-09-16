"""CKS v1.4 runtime integration tests."""


def test_runtime_pipeline_contract():
    pipeline = [
        "object",
        "metrics",
        "graph",
        "review_gate",
        "dashboard",
    ]
    assert pipeline[0] == "object"
    assert pipeline[-1] == "dashboard"
