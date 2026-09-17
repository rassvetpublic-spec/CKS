"""Execute CKS integration regression tests with real exit semantics."""

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = ROOT / "tests"
TEST_PATTERN = "test_cks_*integration*.py"


def run() -> dict:
    """Discover and execute integration tests, returning a compact result."""

    # `tests/` is intentionally not required to be a Python package.  Keep the
    # repository root importable for tests that import CKS scripts, while
    # letting unittest treat the test directory itself as the discovery root.
    root_text = str(ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    suite = unittest.defaultTestLoader.discover(
        start_dir=str(TEST_DIR),
        pattern=TEST_PATTERN,
    )
    test_count = suite.countTestCases()

    if test_count == 0:
        return {
            "status": "FAIL",
            "tests": 0,
            "failures": 0,
            "errors": 0,
            "reason": "no integration tests discovered",
        }

    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return {
        "status": "PASS" if result.wasSuccessful() else "FAIL",
        "tests": test_count,
        "failures": len(result.failures),
        "errors": len(result.errors),
    }


if __name__ == "__main__":
    summary = run()
    print(summary)
    raise SystemExit(0 if summary["status"] == "PASS" else 1)
