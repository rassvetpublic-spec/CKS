from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
README = SCHEMAS / "README.md"
CI = ROOT / "tools" / "cks_ci.py"


class SchemaContractSelectionIssue51Tests(unittest.TestCase):
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

    def test_bootstrap_knowledge_object_contract_is_legacy_only(self) -> None:
        legacy = (SCHEMAS / "knowledge_object_v1.yaml").read_text(encoding="utf-8")
        self.assertIn("bootstrap_scope_only: true", legacy)

        readme = README.read_text(encoding="utf-8")
        self.assertRegex(
            readme,
            r"(?m)^\| `knowledge_object_v1\.yaml` \| LEGACY \|",
        )

    def test_ci_report_schema_drift_is_explicitly_not_false_green(self) -> None:
        schema = json.loads(
            (SCHEMAS / "cks-ci-report.schema.json").read_text(encoding="utf-8")
        )
        source = CI.read_text(encoding="utf-8")
        self.assertEqual("1.0", schema["properties"]["schema_version"]["const"])
        self.assertIn('"schema_version": "1.1"', source)

        readme = README.read_text(encoding="utf-8")
        self.assertRegex(
            readme,
            r"(?m)^\| `cks-ci-report\.schema\.json` \| REVIEW \|",
        )


if __name__ == "__main__":
    unittest.main()
