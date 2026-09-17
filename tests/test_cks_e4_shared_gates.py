import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SharedGateTests(unittest.TestCase):
    def read(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_structure_workflows_use_shared_gate(self):
        for rel in (
            ".github/workflows/cks-compliance.yml",
            ".github/workflows/cks-knowledge-check.yml",
        ):
            text = self.read(rel)
            self.assertIn("uses: ./.github/actions/cks-structure-gate", text)
            self.assertNotIn("test -d protocols", text)

    def test_structure_gate_keeps_required_directories(self):
        text = self.read(".github/actions/cks-structure-gate/action.yml")
        for name in ("docs", "schemas", "protocols", "evidence", "decisions", "graveyard"):
            self.assertIn(name, text)
        self.assertIn("set -euo pipefail", text)

    def test_review_workflows_use_shared_gate(self):
        for rel in (
            ".github/workflows/cks-review-gate.yml",
            ".github/workflows/cks-boundary-check.yml",
        ):
            text = self.read(rel)
            self.assertIn("uses: ./.github/actions/cks-review-gate", text)
            self.assertNotIn("run: python tools/cks_ci.py --mode review-gate", text)

    def test_review_gate_executes_validator(self):
        text = self.read(".github/actions/cks-review-gate/action.yml")
        self.assertIn("python tools/cks_ci.py --mode review-gate", text)


if __name__ == "__main__":
    unittest.main()
