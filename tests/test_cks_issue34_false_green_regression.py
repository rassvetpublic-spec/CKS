import json
import os
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


VALID_OBJECT = {
    "id": "CKS-KNW-9001",
    "type": "knowledge",
    "status": "knowledge",
    "owner": "CKS",
    "lifecycle": "knowledge",
    "relations": [],
    "evidence": [],
    "history": [],
}


class Issue34FalseGreenRegressionTests(unittest.TestCase):
    def _temp_root(self) -> tuple[tempfile.TemporaryDirectory, Path]:
        holder = tempfile.TemporaryDirectory()
        root = Path(holder.name)
        (root / "schemas").mkdir(parents=True)
        (root / "knowledge" / "objects").mkdir(parents=True)
        schema = (ROOT / "schemas" / "cks-knowledge-object.schema.json").read_text(encoding="utf-8")
        (root / "schemas" / "cks-knowledge-object.schema.json").write_text(schema, encoding="utf-8")
        (root / "knowledge" / "objects" / "valid.json").write_text(
            json.dumps(VALID_OBJECT, ensure_ascii=False), encoding="utf-8"
        )
        return holder, root

    def test_repository_has_real_canonical_objects_and_no_yaml_bypass(self):
        findings = []
        cks_ci.validate_knowledge_json(findings)
        failures = [item for item in findings if item.level == "FAIL"]
        self.assertEqual(failures, [], [item.__dict__ for item in failures])
        self.assertTrue(any((ROOT / "knowledge").rglob("*.json")))
        self.assertFalse((ROOT / "knowledge" / "objects" / "example_object.yaml").exists())
        self.assertFalse((ROOT / "knowledge" / "objects" / "concept_multi_worker_sync.yaml").exists())
        self.assertFalse((ROOT / "knowledge" / "examples" / "CKS-OBJ-001-rule-example.yaml").exists())

    def test_yaml_knowledge_object_fails_closed(self):
        holder, root = self._temp_root()
        try:
            bad = root / "knowledge" / "objects" / "bypass.yaml"
            bad.write_text(
                "id: CKS-KNW-9999\n"
                "type: knowledge\n"
                "status: knowledge\n"
                "owner: CKS\n"
                "lifecycle: knowledge\n",
                encoding="utf-8",
            )
            findings = []
            with mock.patch.object(cks_ci, "ROOT", root):
                cks_ci.validate_knowledge_json(findings)
            codes = {item.code for item in findings}
            self.assertIn("KNOWLEDGE_OBJECT_YAML_NONCANONICAL", codes)
        finally:
            holder.cleanup()

    def test_explicit_distillate_yaml_contract_is_not_misclassified(self):
        holder, root = self._temp_root()
        try:
            distillate = root / "knowledge" / "objects" / "distillate.yaml"
            distillate.write_text(
                "schema: cks\n"
                "version: 1\n"
                "object: distillate_object\n"
                "telemetry:\n"
                "  worker_id: W-1\n"
                "  task_id: task-1\n"
                "  rule_hash: abc\n"
                "  status: PASS\n"
                "data_plane:\n"
                "  type: OBSERVATION\n"
                "  payload: ok\n",
                encoding="utf-8",
            )
            findings = []
            with mock.patch.object(cks_ci, "ROOT", root):
                cks_ci.validate_knowledge_json(findings)
            failures = [item for item in findings if item.level == "FAIL"]
            self.assertEqual(failures, [], [item.__dict__ for item in failures])
        finally:
            holder.cleanup()

    def test_push_diff_uses_event_before_sha(self):
        with tempfile.TemporaryDirectory() as tmp:
            event = Path(tmp) / "event.json"
            event.write_text(json.dumps({"before": "abc123"}), encoding="utf-8")
            env = {
                "GITHUB_EVENT_PATH": str(event),
                "GITHUB_BASE_REF": "",
                "CKS_BASE_SHA": "",
            }
            with mock.patch.dict(os.environ, env, clear=False):
                with mock.patch.object(cks_ci, "run_git") as run_git:
                    run_git.side_effect = lambda *args: "a.md\nb.py" if args == ("diff", "--name-only", "abc123", "HEAD") else ""
                    self.assertEqual(cks_ci.changed_files(), ["a.md", "b.py"])

    def test_ci_does_not_pass_when_changed_files_are_unresolved(self):
        findings = []
        with mock.patch.object(cks_ci, "changed_files", return_value=[]):
            with mock.patch.dict(os.environ, {"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "push"}, clear=False):
                self.assertEqual(cks_ci.select_files(findings), [])
        self.assertIn("CHANGED_FILES_UNRESOLVED", {item.code for item in findings})

    def test_architecture_ssot_points_to_existing_file(self):
        registry = (ROOT / "control" / "ssot-registry.yaml").read_text(encoding="utf-8")
        self.assertIn("architecture:\n    path: ARCHITECTURE.md", registry)
        self.assertTrue((ROOT / "ARCHITECTURE.md").is_file())
        self_audit = (ROOT / "tools" / "cks_self_audit.py").read_text(encoding="utf-8")
        self.assertIn('"path: ARCHITECTURE.md"', self_audit)
        self.assertIn('"SSOT_ARCHITECTURE_PATH"', self_audit)


if __name__ == "__main__":
    unittest.main()
