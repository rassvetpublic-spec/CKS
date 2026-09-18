from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
README = SCHEMAS / "README.md"
CI = ROOT / "tools" / "cks_ci.py"
ACTIVE_KNOWLEDGE_OBJECT = SCHEMAS / "cks-knowledge-object.schema.json"
LEGACY_KNOWLEDGE_OBJECT = SCHEMAS / "knowledge_object_v1.yaml"
CI_REPORT_SCHEMA = SCHEMAS / "cks-ci-report.schema.json"

TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import cks_ci  # noqa: E402
from cks_json_schema_validator import validate_instance  # noqa: E402


class TestSchemaContractSelectionIssue51(unittest.TestCase):
    def test_registry_covers_every_schema_file(self) -> None:
        readme = README.read_text(encoding="utf-8")
        documented = set(
            re.findall(
                r"^\| `([^`]+)` \| (?:ACTIVE|COMPATIBILITY|LEGACY|REVIEW) \|",
                readme,
                flags=re.MULTILINE,
            )
        )
        actual = {
            path.name
            for path in SCHEMAS.iterdir()
            if path.is_file() and path.suffix.lower() in {".json", ".yaml", ".yml"}
        }
        self.assertEqual(actual, documented)

    def test_readme_documents_every_schema_file(self) -> None:
        text = README.read_text(encoding="utf-8")
        schema_files = sorted(
            path.name
            for path in SCHEMAS.iterdir()
            if path.is_file() and path.name != README.name
        )

        self.assertGreater(len(schema_files), 0)
        for filename in schema_files:
            with self.subTest(filename=filename):
                self.assertIn(f"`{filename}`", text)

    def test_new_knowledge_object_contract_is_unambiguous(self) -> None:
        text = README.read_text(encoding="utf-8")

        self.assertIn(
            "NEW_KNOWLEDGE_OBJECT_CONTRACT = schemas/cks-knowledge-object.schema.json",
            text,
        )
        self.assertIn(
            "LEGACY_KNOWLEDGE_OBJECT_CONTRACT = schemas/knowledge_object_v1.yaml",
            text,
        )
        self.assertIn(
            "Для **любого нового универсального объекта знания CKS** использовать только "
            "`schemas/cks-knowledge-object.schema.json`",
            text,
        )

    def test_canonical_knowledge_object_uses_active_json_schema(self) -> None:
        source = CI.read_text(encoding="utf-8")
        self.assertIn(
            'schema_path = ROOT / "schemas" / "cks-knowledge-object.schema.json"',
            source,
        )
        self.assertIn("KNOWLEDGE_OBJECT_YAML_NONCANONICAL", source)

        readme = README.read_text(encoding="utf-8")
        self.assertRegex(
            readme,
            r"(?m)^\| `cks-knowledge-object\.schema\.json` \| ACTIVE \|",
        )

    def test_active_knowledge_object_contract_is_json_schema(self) -> None:
        schema = json.loads(ACTIVE_KNOWLEDGE_OBJECT.read_text(encoding="utf-8"))

        self.assertEqual(
            schema.get("$schema"),
            "https://json-schema.org/draft/2020-12/schema",
        )
        self.assertEqual(
            schema.get("$id"),
            "https://cks.local/schemas/cks-knowledge-object.schema.json",
        )
        self.assertTrue(
            {"id", "type", "status", "owner", "lifecycle", "relations", "evidence", "history"}
            <= set(schema.get("required", []))
        )
        self.assertTrue(schema.get("additionalProperties"))

    def test_bootstrap_knowledge_object_contract_is_legacy_only(self) -> None:
        legacy = (SCHEMAS / "knowledge_object_v1.yaml").read_text(encoding="utf-8")
        self.assertIn("purpose: minimal knowledge object for CKS Bootstrap 1.0", legacy)
        self.assertIn("bootstrap_scope_only: true", legacy)

        readme = README.read_text(encoding="utf-8")
        self.assertRegex(
            readme,
            r"(?m)^\| `knowledge_object_v1\.yaml` \| LEGACY \|",
        )

    def test_legacy_bootstrap_contract_is_preserved_for_compatibility(self) -> None:
        text = LEGACY_KNOWLEDGE_OBJECT.read_text(encoding="utf-8")

        self.assertIn("purpose: minimal knowledge object for CKS Bootstrap 1.0", text)
        self.assertIn("bootstrap_scope_only: true", text)
        self.assertIn("knowledge_object_v1.yaml` | LEGACY", README.read_text(encoding="utf-8"))

    def test_ci_report_schema_contract_is_active_and_valid(self) -> None:
        schema = json.loads(CI_REPORT_SCHEMA.read_text(encoding="utf-8"))
        source = CI.read_text(encoding="utf-8")

        self.assertEqual("1.1", schema["properties"]["schema_version"]["const"])
        self.assertEqual(["1.1"], schema["properties"]["schema_version"]["enum"])
        self.assertIn('"schema_version": "1.1"', source)

        readme = README.read_text(encoding="utf-8")
        self.assertRegex(
            readme,
            r"(?m)^\| `cks-ci-report\.schema\.json` \| ACTIVE \|",
        )

        report = cks_ci.write_reports("all", [], ["tests/test_cks_schema_contract_selection_issue51.py"])
        self.assertEqual(report["schema_version"], "1.1")
        errors = validate_instance(report, schema)
        self.assertEqual(errors, [])

    def test_validator_const_keyword_support(self) -> None:
        schema = {"type": "object", "properties": {"version": {"const": "1.1"}}}
        self.assertEqual(validate_instance({"version": "1.1"}, schema), [])

        errors = validate_instance({"version": "1.0"}, schema)
        self.assertEqual(len(errors), 1)
        self.assertIn("does not match const '1.1'", errors[0])

        self.assertEqual(validate_instance(True, {"const": True}), [])
        self.assertGreater(len(validate_instance(1, {"const": True})), 0)

    def test_knowledge_validation_skips_inbox(self) -> None:
        findings: list[cks_ci.Finding] = []
        cks_ci.validate_knowledge_json(findings)
        inbox_failures = [f for f in findings if "inbox" in f.path]
        self.assertEqual(inbox_failures, [])

    def test_knowledge_validation_records_finding_on_schema_load_failure(self) -> None:
        import tempfile
        from unittest import mock

        findings: list[cks_ci.Finding] = []
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / "knowledge").mkdir()
            with mock.patch.object(cks_ci, "ROOT", tmp_root):
                cks_ci.validate_knowledge_json(findings)
        self.assertTrue(any(f.code == "SCHEMA_LOAD_FAILED" for f in findings))


SchemaContractSelectionIssue51Tests = TestSchemaContractSelectionIssue51


if __name__ == "__main__":
    unittest.main()
