import unittest
from pathlib import Path

class TestCKSArchitectureHealthMetrics(unittest.TestCase):
    def setUp(self):
        self.doc_path = Path("docs/CKS_ARCHITECTURE_HEALTH_METRICS_v1.md")

    def test_doc_exists(self):
        self.assertTrue(self.doc_path.exists(), "CKS_ARCHITECTURE_HEALTH_METRICS_v1.md should exist")

    def test_required_metrics_present(self):
        content = self.doc_path.read_text(encoding="utf-8")
        self.assertIn("Readiness Metric", content)
        self.assertIn("Risk Metric", content)
        self.assertIn("Quality Metric", content)
        self.assertIn("Coverage Metric", content)

    def test_single_score_prohibition_present(self):
        content = self.doc_path.read_text(encoding="utf-8")
        self.assertIn("Single Composite Score", content)

if __name__ == "__main__":
    unittest.main()
