import json
import tempfile
import unittest
from pathlib import Path

from tools.cks_index_generator import build_index
from tools.cks_json_schema_validator import validate_instance


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "cks-knowledge-object.schema.json").read_text(encoding="utf-8"))


VALID_OBJECT = {
    "id": "CKS-KNOWLEDGE-9001",
    "type": "knowledge",
    "status": "draft",
    "owner": "test-owner",
    "lifecycle": "development",
    "relations": [],
    "evidence": [],
    "history": [],
}


class Package003AutomationTests(unittest.TestCase):
    def test_valid_knowledge_object_satisfies_active_schema(self):
        self.assertEqual(validate_instance(VALID_OBJECT, SCHEMA), [])

    def test_missing_required_field_fails_active_schema(self):
        invalid = dict(VALID_OBJECT)
        invalid.pop("owner")
        errors = validate_instance(invalid, SCHEMA)
        self.assertTrue(errors)
        self.assertTrue(any("owner" in error for error in errors))

    def test_index_is_deterministic_and_explicitly_non_ssot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "knowledge"
            source.mkdir()
            one = dict(VALID_OBJECT, id="CKS-KNOWLEDGE-2", title="Two")
            two = dict(VALID_OBJECT, id="CKS-KNOWLEDGE-1", title="One")
            (source / "z.json").write_text(json.dumps(one), encoding="utf-8")
            (source / "a.json").write_text(json.dumps(two), encoding="utf-8")

            first = build_index(source, root)
            second = build_index(source, root)
            self.assertEqual(first, second)
            self.assertTrue(first["derived_index"])
            self.assertTrue(first["derived_artifact"])
            self.assertFalse(first["ssot"])
            self.assertEqual(first["generator"], "cks_index_generator")
            self.assertEqual([x["id"] for x in first["items"]], ["CKS-KNOWLEDGE-1", "CKS-KNOWLEDGE-2"])

    def test_index_surfaces_parse_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "knowledge"
            source.mkdir()
            (source / "broken.json").write_text("{broken", encoding="utf-8")
            result = build_index(source, root)
            self.assertEqual(result["count"], 0)
            self.assertEqual(len(result["parse_errors"]), 1)


if __name__ == "__main__":
    unittest.main()
