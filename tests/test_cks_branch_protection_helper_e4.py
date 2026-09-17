import os
import unittest
from unittest.mock import patch

from tools import cks_apply_branch_protection as helper


class BranchProtectionHelperE4Tests(unittest.TestCase):
    def test_required_checks_are_exact_and_do_not_use_ambiguous_validate_name(self):
        self.assertEqual(len(helper.REQUIRED_CHECKS), 7)
        self.assertNotIn("validate", helper.REQUIRED_CHECKS)
        self.assertEqual(
            helper.REQUIRED_CHECKS,
            (
                "Package 003 integrated automation gate",
                "boundary",
                "canon-guard",
                "traceability",
                "governance",
                "validate-control-plane",
                "validate-bootstrap",
            ),
        )

    def test_check_surface_accepts_exact_required_checks_even_with_unrelated_duplicate(self):
        runs = [{"name": name} for name in helper.REQUIRED_CHECKS]
        runs.extend([{"name": "validate"}, {"name": "validate"}])
        helper.validate_check_surface(runs)

    def test_check_surface_rejects_missing_required_check(self):
        runs = [{"name": name} for name in helper.REQUIRED_CHECKS[:-1]]
        with self.assertRaises(helper.ProtectionError):
            helper.validate_check_surface(runs)

    def test_check_surface_rejects_ambiguous_required_check(self):
        runs = [{"name": name} for name in helper.REQUIRED_CHECKS]
        runs.append({"name": "boundary"})
        with self.assertRaises(helper.ProtectionError):
            helper.validate_check_surface(runs)

    def test_payload_is_fail_safe_and_exact(self):
        payload = helper.build_protection_payload()
        self.assertEqual(
            payload["required_status_checks"]["contexts"],
            list(helper.REQUIRED_CHECKS),
        )
        self.assertTrue(payload["required_status_checks"]["strict"])
        self.assertTrue(payload["enforce_admins"])

        reviews = payload["required_pull_request_reviews"]
        self.assertIsInstance(reviews, dict)
        self.assertEqual(reviews["required_approving_review_count"], 0)
        self.assertFalse(reviews["dismiss_stale_reviews"])
        self.assertFalse(reviews["require_code_owner_reviews"])
        self.assertFalse(reviews["require_last_push_approval"])

        self.assertIsNone(payload["restrictions"])
        self.assertFalse(payload["required_linear_history"])
        self.assertFalse(payload["allow_force_pushes"])
        self.assertFalse(payload["allow_deletions"])
        self.assertFalse(payload["block_creations"])
        self.assertFalse(payload["required_conversation_resolution"])
        self.assertFalse(payload["lock_branch"])
        self.assertFalse(payload["allow_fork_syncing"])

    def test_pull_request_requirement_rejects_null_or_approval_requirement(self):
        self.assertFalse(helper.pull_request_requirement_matches({}))
        self.assertFalse(
            helper.pull_request_requirement_matches(
                {"required_pull_request_reviews": None}
            )
        )
        self.assertFalse(
            helper.pull_request_requirement_matches(
                {
                    "required_pull_request_reviews": {
                        "required_approving_review_count": 1,
                        "dismiss_stale_reviews": False,
                        "require_code_owner_reviews": False,
                        "require_last_push_approval": False,
                    }
                }
            )
        )

    def _matching_protection(self):
        return {
            "required_status_checks": {
                "strict": True,
                "contexts": list(helper.REQUIRED_CHECKS),
            },
            "required_pull_request_reviews": {
                "required_approving_review_count": 0,
                "dismiss_stale_reviews": False,
                "require_code_owner_reviews": False,
                "require_last_push_approval": False,
            },
            "enforce_admins": {"enabled": True},
            "restrictions": None,
            "required_linear_history": {"enabled": False},
            "allow_force_pushes": {"enabled": False},
            "allow_deletions": {"enabled": False},
            "block_creations": {"enabled": False},
            "required_conversation_resolution": {"enabled": False},
            "lock_branch": {"enabled": False},
            "allow_fork_syncing": {"enabled": False},
        }

    def test_readback_match_requires_exact_contexts_pr_requirement_and_guardrails(self):
        protection = self._matching_protection()
        self.assertTrue(helper.protection_matches(protection))

        protection["required_status_checks"]["contexts"].append("validate")
        self.assertFalse(helper.protection_matches(protection))

    def test_readback_match_rejects_each_enabled_non_target_guardrail(self):
        for field in (
            "required_linear_history",
            "allow_force_pushes",
            "allow_deletions",
            "block_creations",
            "required_conversation_resolution",
            "lock_branch",
            "allow_fork_syncing",
        ):
            with self.subTest(field=field):
                protection = self._matching_protection()
                protection[field]["enabled"] = True
                self.assertFalse(helper.protection_matches(protection))

    def test_readback_match_rejects_push_restrictions(self):
        protection = self._matching_protection()
        protection["restrictions"] = {
            "users": [{"login": "restricted-user"}],
            "teams": [],
            "apps": [],
        }
        self.assertFalse(helper.protection_matches(protection))

    def test_existing_protection_preflight_accepts_none_and_matching_policy(self):
        helper.validate_existing_protection(None)
        helper.validate_existing_protection(self._matching_protection())

    def test_existing_protection_preflight_rejects_different_policy_without_override(self):
        protection = self._matching_protection()
        protection["required_status_checks"]["strict"] = False
        with self.assertRaises(helper.ProtectionError):
            helper.validate_existing_protection(protection)

    def test_existing_protection_preflight_rejects_linear_history_difference(self):
        protection = self._matching_protection()
        protection["required_linear_history"]["enabled"] = True
        with self.assertRaises(helper.ProtectionError):
            helper.validate_existing_protection(protection)

    def test_existing_protection_preflight_allows_explicit_replace_override(self):
        protection = self._matching_protection()
        protection["required_status_checks"]["strict"] = False
        helper.validate_existing_protection(protection, replace_existing=True)

    def test_main_dry_run_fails_closed_on_different_existing_policy(self):
        protection = self._matching_protection()
        protection["required_linear_history"]["enabled"] = True
        branch = {"commit": {"sha": "abc123"}, "protected": True}
        runs = [{"name": name} for name in helper.REQUIRED_CHECKS]
        with patch.dict(os.environ, {"CKS_GITHUB_ADMIN_TOKEN": "test-token"}, clear=True), \
             patch.object(helper, "get_branch", return_value=branch), \
             patch.object(helper, "get_check_runs", return_value=runs), \
             patch.object(helper, "get_protection", return_value=protection):
            self.assertEqual(helper.main([]), 1)


if __name__ == "__main__":
    unittest.main()
