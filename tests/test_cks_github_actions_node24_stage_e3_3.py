from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"

LEGACY_ACTIONS = (
    "actions/checkout@v4",
    "actions/setup-python@v5",
    "actions/upload-artifact@v4",
)


class GitHubActionsNode24GuardTests(unittest.TestCase):
    def test_no_legacy_node20_action_majors_remain(self):
        workflow_files = sorted(
            list(WORKFLOW_DIR.glob("*.yml")) + list(WORKFLOW_DIR.glob("*.yaml"))
        )
        self.assertTrue(workflow_files, "No GitHub Actions workflows found")

        offenders = []
        for path in workflow_files:
            text = path.read_text(encoding="utf-8")
            for action in LEGACY_ACTIONS:
                if action in text:
                    offenders.append(f"{path.relative_to(ROOT)}: {action}")

        self.assertEqual(
            offenders,
            [],
            "Legacy Node.js 20 action majors remain:\n" + "\n".join(offenders),
        )

    def test_node24_action_majors_are_present(self):
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(
                list(WORKFLOW_DIR.glob("*.yml")) + list(WORKFLOW_DIR.glob("*.yaml"))
            )
        )
        self.assertIn("actions/checkout@v5", combined)
        self.assertIn("actions/setup-python@v6", combined)
        self.assertIn("actions/upload-artifact@v6", combined)


if __name__ == "__main__":
    unittest.main()
