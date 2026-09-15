"""Regression checks for architecture boundaries and integration compatibility."""

import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("validate_council", ROOT / "scripts/validate_council.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CouncilContracts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for directory in (".csk", ".github", "council", "schemas", "protocols", "config", "decisions", "docs"):
            shutil.copytree(ROOT / directory, self.root / directory)

    def mutate(self, file, change):
        path = self.root / file
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(yaml.safe_dump(data), encoding="utf-8")

    def test_baseline(self):
        self.assertEqual(module.validate(self.root), [])

    def test_unknown_project_state(self):
        self.mutate(".csk/integrations.yaml", lambda d: d["project_lifecycle"].update(approved_next="DONE"))
        self.assertIn("Unknown Project lifecycle state", module.validate(self.root))

    def test_approval_without_fresh_review(self):
        self.mutate(".csk/workflow.yaml", lambda d: next(t for t in d["transitions"] if t["event"] == "APPROVE").update(require_current_pass=False))
        self.assertTrue(any("current PASS" in e for e in module.validate(self.root)))

    def test_agent_approval(self):
        self.mutate(".csk/roles.yaml", lambda d: d["roles"]["architect"].update(can_approve=True))
        self.assertIn("Agent cannot approve", module.validate(self.root))

    def test_runtime_in_repository(self):
        pointer = self.root / ".csk/state.json"
        data = json.loads(pointer.read_text())
        data["active_task"] = "CKS-0001"
        pointer.write_text(json.dumps(data))
        self.assertIn("state.json must be a static pointer only", module.validate(self.root))

    def test_revision_bypasses_cycle_limit(self):
        self.mutate(".csk/workflow.yaml", lambda d: next(t for t in d["transitions"] if t["to"] == "REVISION").update(before_cycle_limit=False))
        self.assertIn("Revision must respect cycle limit", module.validate(self.root))

    def test_owner_added_to_knowledge_schema(self):
        self.mutate("council/decisions/decision-candidate.example.yaml", lambda d: d.update(owner="someone"))
        self.assertIn("Decision candidate must use existing schema fields", module.validate(self.root))

    def test_protocol_mismatch(self):
        self.mutate(".csk/integrations.yaml", lambda d: d["qa_worker"]["result_mapping"].update(FAIL="FAIL"))
        self.assertIn("Review protocol mismatch", module.validate(self.root))


if __name__ == "__main__":
    unittest.main()
