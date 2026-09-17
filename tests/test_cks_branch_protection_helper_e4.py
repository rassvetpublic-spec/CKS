import unittest

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
        self.assertIsNone(payload["required_pull_request_reviews"])
        self.assertIsNone(payload["restrictions"])
        self.assertFalse(payload["allow_force_pushes"])
        self.assertFalse(payload["allow_deletions"])

    def test_readback_match_requires_exact_contexts_and_guardrails(self):
        protection = {
            "required_status_checks": {
                "strict": True,
                "contexts": list(helper.REQUIRED_CHECKS),
            },
            "enforce_admins": {"enabled": True},
            "allow_force_pushes": {"enabled": False},
            "allow_deletions": {"enabled": False},
        }
        self.assertTrue(helper.protection_matches(protection))

        protection["required_status_checks"]["contexts"].append("validate")
        self.assertFalse(helper.protection_matches(protection))


if __name__ == "__main__":
    unittest.main()
