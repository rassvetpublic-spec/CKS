from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "scripts" / "validate_bootstrap.py"
CONTROL_PLANE = ROOT / "validators" / "control_plane_validator.py"


class WorkflowExitSemanticsTest(unittest.TestCase):
    def run_script(self, script: Path, cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script)],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_bootstrap_fail_returns_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_script(BOOTSTRAP, Path(tmp))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL", result.stdout)

    def test_bootstrap_pass_returns_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "schemas").mkdir()
            (root / "schemas" / "knowledge_object_v1.yaml").write_text("type: object\n", encoding="utf-8")
            (root / "knowledge" / "objects").mkdir(parents=True)
            result = self.run_script(BOOTSTRAP, root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_control_plane_fail_returns_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_script(CONTROL_PLANE, Path(tmp))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL", result.stdout)

    def test_control_plane_pass_returns_zero(self) -> None:
        required = (
            "system-state.yaml",
            "ssot-registry.yaml",
            "traceability-model.yaml",
            "lifecycle-state-model.yaml",
            "automation-governance.yaml",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            control = root / "control"
            control.mkdir()
            for name in required:
                (control / name).write_text("ok: true\n", encoding="utf-8")
            result = self.run_script(CONTROL_PLANE, root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("'status': 'PASS'", result.stdout)


if __name__ == "__main__":
    unittest.main()
