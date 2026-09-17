import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
README = SCHEMAS / "README.md"
ACTIVE_KNOWLEDGE_OBJECT = SCHEMAS / "cks-knowledge-object.schema.json"
LEGACY_KNOWLEDGE_OBJECT = SCHEMAS / "knowledge_object_v1.yaml"


class TestSchemaContractSelectionIssue51(unittest.TestCase):
    def test_readme_documents_every_schema_file(self):
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

    def test_new_knowledge_object_contract_is_unambiguous(self):
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
            "для **любого нового универсального объекта знания CKS** использовать только "
            "`schemas/cks-knowledge-object.schema.json`",
            text,
        )

    def test_active_knowledge_object_contract_is_json_schema(self):
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

    def test_legacy_bootstrap_contract_is_preserved_for_compatibility(self):
        text = LEGACY_KNOWLEDGE_OBJECT.read_text(encoding="utf-8")

        self.assertIn("purpose: minimal knowledge object for CKS Bootstrap 1.0", text)
        self.assertIn("bootstrap_scope_only: true", text)
        self.assertIn("knowledge_object_v1.yaml` | LEGACY", README.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
