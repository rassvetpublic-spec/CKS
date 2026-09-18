from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
TEMPLATES = ROOT / "templates"
DOCS = ROOT / "docs"
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cks_json_schema_validator import validate_instance  # noqa: E402


class TestCksAsyncHandoffV13(unittest.TestCase):
    def setUp(self) -> None:
        self.schema_path = SCHEMAS / "cks-task-state.schema.json"
        self.assertTrue(self.schema_path.is_file(), "Task state schema must exist")
        self.schema = json.loads(self.schema_path.read_text(encoding="utf-8"))

    def test_schema_validates_valid_task_state(self) -> None:
        valid_instance = {
            "task_id": "ISSUE-67",
            "status": "READY",
            "owner": "Worker A",
            "controller": "QA+Review Controller",
            "sha": "298161e88849b2f6942c7595d2c8846c26bdf3b8",
            "base_sha": "a181f885fdf083be12e75e9fbbbb23db239b61d3",
            "channel": "https://github.com/rassvetpublic-spec/CKS/issues/67",
            "evidence": ["reports/test_evidence.md"],
            "verdict": "PENDING",
        }
        errors = validate_instance(valid_instance, self.schema)
        self.assertEqual(errors, [])

    def test_schema_rejects_missing_required_fields(self) -> None:
        invalid_instance = {
            "task_id": "ISSUE-67",
            "status": "IN_PROGRESS",
            # missing owner, sha, channel
        }
        errors = validate_instance(invalid_instance, self.schema)
        self.assertTrue(len(errors) > 0)
        self.assertTrue(any("owner" in err for err in errors))
        self.assertTrue(any("sha" in err for err in errors))
        self.assertTrue(any("channel" in err for err in errors))

    def test_schema_rejects_invalid_lifecycle_status(self) -> None:
        invalid_instance = {
            "task_id": "ISSUE-67",
            "status": "UNKNOWN_STATE",
            "owner": "Worker A",
            "sha": "298161e88849b2f6942c7595d2c8846c26bdf3b8",
            "channel": "GitHub PR conversation",
        }
        errors = validate_instance(invalid_instance, self.schema)
        self.assertTrue(len(errors) > 0)
        self.assertTrue(any("status" in err for err in errors))

    def test_all_lifecycle_states_accepted(self) -> None:
        expected_states = [
            "READY",
            "IN_PROGRESS",
            "HANDOFF",
            "QA",
            "REVIEW",
            "VERDICT",
            "MERGED",
        ]
        for state in expected_states:
            instance = {
                "task_id": "TASK-1",
                "status": state,
                "owner": "Worker A",
                "sha": "abcdef1234567890",
                "channel": "PR",
            }
            errors = validate_instance(instance, self.schema)
            self.assertEqual(errors, [], f"State {state} should be accepted")

    def test_templates_exist_and_reference_v1_3(self) -> None:
        task_tmpl = TEMPLATES / "TASK_TEMPLATE.md"
        handoff_tmpl = TEMPLATES / "HANDOFF_TEMPLATE.md"
        verdict_tmpl = TEMPLATES / "VERDICT_TEMPLATE.md"

        self.assertTrue(task_tmpl.is_file())
        self.assertTrue(handoff_tmpl.is_file())
        self.assertTrue(verdict_tmpl.is_file())

        task_content = task_tmpl.read_text(encoding="utf-8")
        self.assertIn("TASK_ID", task_content)
        self.assertIn("OWNER", task_content)
        self.assertIn("STATUS", task_content)

        handoff_content = handoff_tmpl.read_text(encoding="utf-8")
        self.assertIn("VERSION:\n1.3", handoff_content)
        self.assertIn("TASK_ID:", handoff_content)

        verdict_content = verdict_tmpl.read_text(encoding="utf-8")
        self.assertIn("VERSION:\n1.3", verdict_content)
        self.assertIn("TASK_ID:", verdict_content)

    def test_protocol_document_defines_model(self) -> None:
        doc = DOCS / "CKS_ASYNC_HANDOFF_PROTOCOL_v1.3.md"
        self.assertTrue(doc.is_file())
        content = doc.read_text(encoding="utf-8")
        self.assertIn("CKS ASYNC HANDOFF PROTOCOL v1.3", content)
        self.assertIn("READY → IN_PROGRESS → HANDOFF → QA → REVIEW → VERDICT → MERGED", content)
        self.assertIn("OWNER (Worker A / Worker B)", content)
        self.assertIn("CHECKER (QA Controller)", content)
        self.assertIn("DECIDER (Review Controller / Repo Admin)", content)


if __name__ == "__main__":
    unittest.main()
