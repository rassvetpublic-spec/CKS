from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cks_v1_4_migration_adapter import migrate_object  # noqa: E402
from cks_v1_4_review_gate_runner import run_gate  # noqa: E402


class CKSv14RuntimeIntegrationTests(unittest.TestCase):
    def test_migration_is_non_mutating_and_gate_distinguishes_warn(self):
        source = {"id": "CKS-KNW-1402", "type": "knowledge"}
        migrated = migrate_object(source)

        self.assertEqual(source, {"id": "CKS-KNW-1402", "type": "knowledge"})
        self.assertEqual(migrated["version"], "1.4")
        self.assertEqual(migrated["relations"], [])
        self.assertEqual(migrated["metrics"], {})
        self.assertEqual(run_gate({"schema": True, "evidence": False})["status"], "WARN")
        self.assertEqual(run_gate({"schema": True, "evidence": True})["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
