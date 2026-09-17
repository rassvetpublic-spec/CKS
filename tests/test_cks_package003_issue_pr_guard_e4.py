import unittest

from tools.cks_issue_pr_guard import validate_event


TASK_BODY = """## Goal
G
## Context
C
## Decision needed
D
## Evidence
E
## Acceptance criteria
A
"""

DECISION_BODY = """## Context
C
## Options
A / B
## Decision
A
## Evidence
E
## Status
draft
"""

DONOR_BODY = """## Donor System
External
## Purpose
Audit
## Extracted Patterns
Pattern
## Rejected Elements
None
## Decision
Adapt
"""

PR_BODY = """## Purpose
Change
## Classification
- [x] documentation
## Validation
- Context impact: none
- Canon impact: none
- Evidence: tests
"""


class Package003IssuePrGuardTests(unittest.TestCase):
    def issue(self, body: str):
        return validate_event({"issue": {"title": "Issue", "body": body}})

    def pr(self, body: str):
        return validate_event({"pull_request": {"title": "PR", "body": body}})

    def test_task_template_passes(self):
        self.assertEqual(self.issue(TASK_BODY)["status"], "PASS")

    def test_decision_template_passes(self):
        self.assertEqual(self.issue(DECISION_BODY)["status"], "PASS")

    def test_donor_audit_template_passes(self):
        self.assertEqual(self.issue(DONOR_BODY)["status"], "PASS")

    def test_recognized_incomplete_template_fails(self):
        result = self.issue("## Goal\nG\n## Context\nC\n")
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any(x["code"] == "ISSUE_TEMPLATE_INCOMPLETE" for x in result["findings"]))

    def test_generic_structured_issue_is_advisory(self):
        result = self.issue("## Status\nTracking\n## Notes\nOperational\n")
        self.assertEqual(result["status"], "WARN")
        self.assertEqual(result["summary"]["fail"], 0)

    def test_unstructured_issue_is_advisory(self):
        self.assertEqual(self.issue("plain body")["status"], "WARN")

    def test_default_pr_template_passes(self):
        self.assertEqual(self.pr(PR_BODY)["status"], "PASS")

    def test_incomplete_pr_template_fails(self):
        result = self.pr("## Purpose\nChange\n")
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any(x["code"] == "PR_TEMPLATE_INCOMPLETE" for x in result["findings"]))

    def test_missing_payload_fails(self):
        self.assertEqual(validate_event({})["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
