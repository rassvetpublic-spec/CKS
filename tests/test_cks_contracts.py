from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import cks_ci  # noqa: E402


class CKSContractTests(unittest.TestCase):
    def test_invalid_id_pattern_is_rejected_by_real_validator(self):
        self.assertIsNone(cks_ci.VALID_ID_RE.fullmatch("DEC-001"))
        self.assertIsNotNone(cks_ci.VALID_ID_RE.fullmatch("CKS-DEC-001"))

    def test_research_cannot_be_core(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "core").mkdir(parents=True)
            path = root / "core" / "research.md"
            path.write_text(
                "---\n"
                "id: CKS-DOC-999\n"
                "type: canon\n"
                "lifecycle: research\n"
                "evidence: CKS-EVD-999\n"
                "decision: CKS-DEC-999\n"
                "history: created\n"
                "owner: CKS\n"
                "---\n",
                encoding="utf-8",
            )
            findings = []
            with mock.patch.object(cks_ci, "ROOT", root):
                cks_ci.document_checks(findings, ["core/research.md"], "review-gate")
            self.assertIn("RESEARCH_CORE_BOUNDARY", {item.code for item in findings})

    def test_canon_requires_evidence_decision_history_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "core").mkdir(parents=True)
            path = root / "core" / "incomplete.md"
            path.write_text(
                "---\n"
                "id: CKS-DOC-998\n"
                "type: canon\n"
                "lifecycle: frozen\n"
                "evidence: CKS-EVD-998\n"
                "decision: CKS-DEC-998\n"
                "---\n",
                encoding="utf-8",
            )
            findings = []
            with mock.patch.object(cks_ci, "ROOT", root):
                cks_ci.document_checks(findings, ["core/incomplete.md"], "review-gate")
            gate = [item for item in findings if item.code == "CANON_GATE_MISSING"]
            self.assertEqual(len(gate), 1)
            self.assertIn("history", gate[0].message)
            self.assertIn("owner", gate[0].message)


if __name__ == "__main__":
    unittest.main()
