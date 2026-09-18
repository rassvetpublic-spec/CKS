import unittest
from pathlib import Path


class TestCKSWorkerStateProtocolV3(unittest.TestCase):
    def setUp(self):
        self.doc_path = Path("docs/CKS_WORKER_STATE_PROTOCOL_v3.md")

    def test_protocol_file_exists(self):
        self.assertTrue(self.doc_path.exists(), "docs/CKS_WORKER_STATE_PROTOCOL_v3.md must exist")

    def test_required_states_present(self):
        content = self.doc_path.read_text(encoding="utf-8")
        expected_states = [
            "DISCOVERED",
            "CLAIMED",
            "PREPARING",
            "RUNNING",
            "DISTILLING",
            "WAITING_QA",
            "DONE",
            "BLOCKED",
            "ABORTED",
        ]
        for state in expected_states:
            self.assertIn(state, content, f"State {state} must be documented")

    def test_anti_poisoning_and_invariants_present(self):
        content = self.doc_path.read_text(encoding="utf-8")
        self.assertIn("Anti-Poisoning", content)
        self.assertIn("distillate_object_v1", content)
        self.assertIn("WORKER_REPORT v1", content)
        self.assertIn("Exact HEAD SHA", content)
        self.assertIn("0 LLM tokens", content)
        self.assertIn("C:\\GIT\\", content)


if __name__ == "__main__":
    unittest.main()
