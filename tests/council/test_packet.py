import importlib.util
import json
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("check_packet", ROOT / "scripts/check_council_packet.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PacketBudget(unittest.TestCase):
    def setUp(self):
        self.packet = json.loads((ROOT / "council/pilot/handoff.json").read_text(encoding="utf-8"))
        self.budget = yaml.safe_load((ROOT / ".csk/context-budget.yaml").read_text(encoding="utf-8"))

    def test_pilot_fits(self):
        self.assertEqual(module.validate_packet(self.packet, self.budget), [])

    def test_full_chat_field_rejected(self):
        self.packet["full_chat"] = "Conversation"
        self.assertTrue(module.validate_packet(self.packet, self.budget))

    def test_oversized_delta_rejected_without_truncation(self):
        self.packet["delta"] = "x" * 2501
        self.assertTrue(module.validate_packet(self.packet, self.budget))
        self.assertEqual(len(self.packet["delta"]), 2501)

    def test_missing_revision_rejected(self):
        del self.packet["proposal_revision"]
        self.assertTrue(module.validate_packet(self.packet, self.budget))

    def test_too_many_references(self):
        self.packet["references"] = ["file.md"] * 9
        self.assertTrue(module.validate_packet(self.packet, self.budget))


if __name__ == "__main__":
    unittest.main()
