"""Check bounded handoff data; never execute it or load referenced documents."""

import json
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
IDENTITY = {"repository", "task_id", "proposal_revision", "base_reference", "pr_head"}


def validate_packet(packet, budget):
    if not isinstance(packet, dict):
        return ["Packet must be an object"]
    errors = []
    expected = IDENTITY | set(budget["field_limits"]) | {"references"}
    if set(packet) != expected:
        errors.append("Packet fields must match contract; full_chat and extra fields are forbidden")
    size = len(json.dumps(packet, ensure_ascii=False, separators=(",", ":")))
    if size > budget["max_packet_chars"]:
        errors.append("Packet exceeds character budget; narrow scope, do not silently truncate")
    for name, limit in budget["field_limits"].items():
        value = packet.get(name)
        if not isinstance(value, str) or len(value) > limit:
            errors.append(f"Invalid or oversized field: {name}")
    for name in ("repository", "task_id", "base_reference"):
        if not isinstance(packet.get(name), str) or not packet[name].strip():
            errors.append(f"Missing identity: {name}")
    revision = packet.get("proposal_revision")
    if type(revision) is not int or revision < 1:
        errors.append("proposal_revision must be a positive integer")
    head = packet.get("pr_head")
    if head is not None and (not isinstance(head, str) or not head.strip()):
        errors.append("pr_head must be a nonempty string or null for local drafts")
    refs = packet.get("references")
    if not isinstance(refs, list) or len(refs) > budget["max_references"]:
        errors.append("Invalid references count")
    elif any(not isinstance(r, str) or not r.strip() or len(r) > budget["max_reference_chars"] for r in refs):
        errors.append("Invalid or oversized reference")
    return errors


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/check_council_packet.py <packet.json>")
    try:
        budget = yaml.safe_load((ROOT / ".csk/context-budget.yaml").read_text(encoding="utf-8"))
        packet = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        errors = validate_packet(packet, budget)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        raise SystemExit(str(exc))
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: bounded handoff ({len(json.dumps(packet, ensure_ascii=False, separators=(',', ':')))} characters; token usage not measured)")
