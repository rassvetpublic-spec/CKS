import tempfile
import unittest
from pathlib import Path

from tools.cks_migration_audit import audit, source_markdown_paths


class Package003MigrationAuditTests(unittest.TestCase):
    def make_root(self):
        temp = tempfile.TemporaryDirectory()
        return temp, Path(temp.name)

    def test_generated_artifacts_are_excluded(self):
        temp, root = self.make_root()
        try:
            (root / "docs").mkdir()
            (root / "artifacts" / "cks-ci").mkdir(parents=True)
            (root / "reports").mkdir()
            (root / "docs" / "source.md").write_text("# Source\ntype: report\n", encoding="utf-8")
            (root / "artifacts" / "cks-ci" / "generated.md").write_text("# Generated\n", encoding="utf-8")
            (root / "reports" / "generated.md").write_text("# Generated 2\n", encoding="utf-8")

            paths = [p.relative_to(root).as_posix() for p in source_markdown_paths(root)]
            self.assertEqual(paths, ["docs/source.md"])
        finally:
            temp.cleanup()

    def test_paths_and_findings_are_deterministic(self):
        temp, root = self.make_root()
        try:
            (root / "docs").mkdir()
            (root / "docs" / "z.md").write_text("# Same\n", encoding="utf-8")
            (root / "docs" / "a.md").write_text("# Same\n", encoding="utf-8")

            first = audit(root)
            second = audit(root)
            self.assertEqual(first, second)
            self.assertEqual(first["schema_version"], "2.1")
            self.assertTrue(first["advisory"])
            self.assertTrue(first["derived_artifact"])
            self.assertFalse(first["ssot"])
            duplicate = [x for x in first["findings"] if x["code"] == "DUPLICATE_TITLE"]
            self.assertEqual(duplicate[0]["files"], ["docs/a.md", "docs/z.md"])
        finally:
            temp.cleanup()

    def test_clean_metadata_document_passes(self):
        temp, root = self.make_root()
        try:
            (root / "docs").mkdir()
            (root / "docs" / "one.md").write_text("# One\ntype: report\n", encoding="utf-8")
            result = audit(root)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["finding_count"], 0)
            self.assertEqual(result["checked_files"], 1)
        finally:
            temp.cleanup()

    def test_missing_metadata_is_warn_not_fail(self):
        temp, root = self.make_root()
        try:
            (root / "docs").mkdir()
            (root / "docs" / "one.md").write_text("# One\nNo metadata.\n", encoding="utf-8")
            result = audit(root)
            self.assertEqual(result["status"], "WARN")
            self.assertGreater(result["finding_count"], 0)
        finally:
            temp.cleanup()


if __name__ == "__main__":
    unittest.main()
