import copy
import json
from pathlib import Path
import unittest

from scripts.import_context_package import SUPPORTED_SPLIT_MODES, validate_package


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PACKAGE = ROOT / "examples" / "kat9i_os_import" / "context_package.yaml"


def load_flat_example(path: Path) -> dict:
    """Load the deliberately flat example fixture without adding a YAML dependency."""

    result = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith("["):
            result[key.strip()] = json.loads(value)
        else:
            result[key.strip()] = value.strip('"')
    return result


class ContextPackageContractTests(unittest.TestCase):
    def setUp(self):
        self.valid_package = {
            "id": "KAT9I-IMPORT-001",
            "source_system": "KAT9I_OS",
            "source_reference": "kat9i://run/001",
            "created_at": "2026-09-17T03:00:00+03:00",
            "split_mode": "SPLIT",
            "artifacts": [],
        }

    def test_valid_contract_is_accepted(self):
        self.assertTrue(validate_package(self.valid_package))

    def test_all_documented_split_modes_are_accepted(self):
        for mode in SUPPORTED_SPLIT_MODES:
            with self.subTest(mode=mode):
                package = dict(self.valid_package, split_mode=mode)
                self.assertTrue(validate_package(package))

    def test_each_declared_field_is_required(self):
        for field in tuple(self.valid_package):
            with self.subTest(field=field):
                package = dict(self.valid_package)
                package.pop(field)
                self.assertFalse(validate_package(package))

    def test_source_system_is_fixed_to_kat9i_os(self):
        package = dict(self.valid_package, source_system="OTHER_SYSTEM")
        self.assertFalse(validate_package(package))

    def test_created_at_must_be_datetime_like(self):
        self.assertFalse(validate_package(dict(self.valid_package, created_at="not-a-date")))
        self.assertFalse(validate_package(dict(self.valid_package, created_at=123)))
        self.assertTrue(
            validate_package(dict(self.valid_package, created_at="2026-09-17T00:00:00Z"))
        )

    def test_artifacts_must_be_a_list_but_may_be_empty(self):
        self.assertTrue(validate_package(dict(self.valid_package, artifacts=[])))
        self.assertFalse(validate_package(dict(self.valid_package, artifacts={})))
        self.assertFalse(validate_package(dict(self.valid_package, artifacts="artifact")))

    def test_prohibited_runtime_and_canon_flags_are_rejected(self):
        for flag in (
            "raw_runtime_state",
            "raw_chat_dump",
            "hidden_memory",
            "direct_canon_update",
        ):
            with self.subTest(flag=flag):
                package = dict(self.valid_package, **{flag: True})
                self.assertFalse(validate_package(package))

    def test_explicit_false_prohibited_flags_are_allowed(self):
        package = dict(
            self.valid_package,
            raw_runtime_state=False,
            raw_chat_dump=False,
            hidden_memory=False,
            direct_canon_update=False,
        )
        self.assertTrue(validate_package(package))

    def test_raw_context_dump_type_is_rejected(self):
        package = dict(self.valid_package, type="raw_context_dump")
        self.assertFalse(validate_package(package))

    def test_unknown_metadata_is_not_rejected_without_contract_rule(self):
        package = dict(self.valid_package, trace_id="TRACE-001")
        self.assertTrue(validate_package(package))

    def test_non_mapping_input_is_rejected(self):
        for value in (None, [], "package", 42):
            with self.subTest(value=value):
                self.assertFalse(validate_package(value))

    def test_validation_does_not_mutate_input(self):
        package = copy.deepcopy(self.valid_package)
        before = copy.deepcopy(package)
        validate_package(package)
        self.assertEqual(package, before)

    def test_repository_example_tracks_active_contract(self):
        package = load_flat_example(EXAMPLE_PACKAGE)
        self.assertTrue(validate_package(package))
        self.assertEqual(package["source_system"], "KAT9I_OS")
        self.assertEqual(package["split_mode"], "SPLIT")
        self.assertNotIn("source", package)
        self.assertEqual(package["artifacts"], ["decision.yaml", "evidence.yaml"])


if __name__ == "__main__":
    unittest.main()
