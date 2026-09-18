import unittest
from pathlib import Path


class TestCKSDecisionVerificationProtocolV3(unittest.TestCase):
    def setUp(self):
        self.doc_path = Path("docs/CKS_DECISION_VERIFICATION_PROTOCOL_v3.md")
        self.schema_path = Path("schemas/cks_decision_verification_protocol_v3.yaml")

    def test_protocol_file_exists(self):
        self.assertTrue(self.doc_path.exists(), "docs/CKS_DECISION_VERIFICATION_PROTOCOL_v3.md must exist")

    def test_schema_file_exists(self):
        self.assertTrue(self.schema_path.exists(), "schemas/cks_decision_verification_protocol_v3.yaml must exist")

    def test_required_gates_present(self):
        content = self.doc_path.read_text(encoding="utf-8")
        expected_gates = [
            "Gate 1",
            "Gate 2",
            "Gate 3",
            "Gate 4",
            "Gate 5",
            "Gate 6",
            "Gate 7",
        ]
        for gate in expected_gates:
            self.assertIn(gate, content, f"{gate} must be documented")

    def test_invariants_and_storage_boundary_present(self):
        content = self.doc_path.read_text(encoding="utf-8")
        self.assertIn("Anti-Poisoning", content)
        self.assertIn("Exact HEAD SHA", content)
        self.assertIn("WORKER_REPORT v1", content)
        self.assertIn("C:\\GIT\\", content)
        self.assertIn("evidence_refs", content)


if __name__ == "__main__":
    unittest.main()
