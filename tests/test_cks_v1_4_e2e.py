from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cks_v1_4_dashboard_runtime import build_dashboard  # noqa: E402
from cks_v1_4_graph_builder import build_graph  # noqa: E402
from cks_v1_4_metrics_calculator import KnowledgeMetrics, calculate_health  # noqa: E402
from cks_v1_4_review_gate_runner import run_gate  # noqa: E402


class CKSv14EndToEndTests(unittest.TestCase):
    def test_v1_4_pipeline_computes_real_derived_output(self):
        objects = [
            {
                "id": "CKS-KNW-1401",
                "type": "knowledge",
                "relations": [
                    {"source": "CKS-KNW-1401", "target": "CKS-EVD-1401", "relation": "supports"}
                ],
            },
            {"id": "CKS-EVD-1401", "type": "evidence", "relations": []},
        ]
        metrics = calculate_health(KnowledgeMetrics(80, 90, 70, 60))
        graph = build_graph(objects)
        review = run_gate({"schema": True, "evidence": True})
        dashboard = build_dashboard(metrics=metrics, graph=graph, review=review)

        self.assertEqual(metrics["health_score"], 75)
        self.assertEqual(len(graph["nodes"]), 2)
        self.assertEqual(len(graph["edges"]), 1)
        self.assertEqual(review["status"], "PASS")
        self.assertEqual(dashboard["metrics"]["health_score"], 75)
        self.assertEqual(dashboard["graph"]["edges"][0]["relation"], "supports")
        self.assertFalse(dashboard["is_source_of_truth"])


if __name__ == "__main__":
    unittest.main()
