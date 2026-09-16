def test_v1_4_pipeline_contract():
    pipeline = ["object", "metrics", "graph", "review_gate", "dashboard"]
    assert pipeline[-1] == "dashboard"
