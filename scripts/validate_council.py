"""Validate static Council contracts without running workers or writing state."""

import json
from pathlib import Path
import sys

import yaml


def read_yaml(root, path):
    return yaml.safe_load((root / path).read_text(encoding="utf-8"))


def validate(root):
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    cfg = read_yaml(root, ".csk/council.yaml")
    roles = read_yaml(root, ".csk/roles.yaml")["roles"]
    integration = read_yaml(root, ".csk/integrations.yaml")
    flow = read_yaml(root, ".csk/workflow.yaml")
    require(cfg["core_policy"] == "frozen", "CORE must remain frozen")
    require(cfg["runtime_owner"] == "external", "Runtime must stay external")
    require(cfg["runtime_state"] == "${CKS_BRIDGE_HOME}/state", "State must stay external")
    require(cfg["workflow"]["max_review_cycles"] == 3, "Review limit must be 3")
    require(cfg["workflow"]["human_gate_required"] is True, "Human gate required")
    for key in ("automatic_promotion", "automatic_execution"):
        require(cfg["workflow"][key] is False, f"{key} must be disabled")
    for path in cfg["contracts"].values():
        require((root / path).is_file(), f"Missing contract: {path}")
    for path in cfg["artifacts"].values():
        require((root / path).is_dir(), f"Missing artifact directory: {path}")
    for role in roles.values():
        require((root / role["prompt"]).is_file(), "Missing role prompt")
    for name in ("architect", "reviewer"):
        require(roles[name]["can_approve"] is False, "Agent cannot approve")
    require(roles["human_gate"]["required"] is True, "Owner required")
    require(roles["human_gate"]["empty_allowlist"] == "deny", "Empty owner list must deny")
    pointer = json.loads((root / ".csk/state.json").read_text(encoding="utf-8"))
    require(pointer == {"version": "0.1.0", "kind": "external_state_pointer",
                        "location": "${CKS_BRIDGE_HOME}/state", "tracked_runtime_state": False},
            "state.json must be a static pointer only")
    qa = integration["qa_worker"]
    require(qa["enabled"] is False, "QA binding is not implemented in phase 1")
    require(qa["raw_chat_allowed"] is False, "Raw chats are forbidden")
    require(qa["freshness"] == "exact_head_and_proposal_revision", "QA freshness required")
    require(qa["result_mapping"] == {"PASS": "PASS", "FAIL": "REJECT",
                                      "NEEDS_REVISION": "NEEDS_REVIEW"}, "Review protocol mismatch")
    lifecycle = integration["project_lifecycle"]
    require(lifecycle["enabled"] is False, "Project binding is not implemented in phase 1")
    states = read_yaml(root, lifecycle["source"])["project"]["lifecycle"]
    mapped = list(lifecycle["council_mapping"].values()) + [lifecycle["approved_next"],
              lifecycle["rejected_next"]] + lifecycle["execution_sequence"]
    require(all(s in states for s in mapped), "Unknown Project lifecycle state")
    require(lifecycle["closure_promotes_knowledge"] is False, "Closure cannot promote knowledge")
    transitions = flow["transitions"]
    for t in transitions:
        require(t["from"] in cfg["workflow"]["stages"] and t["to"] in cfg["workflow"]["stages"],
                "Unknown Council stage")
        if t["to"] == "REVISION":
            require(t.get("before_cycle_limit") is True, "Revision must respect cycle limit")
    approvals = [t for t in transitions if t["event"] == "APPROVE"]
    require(len(approvals) == 1, "Exactly one approval transition required")
    for t in approvals:
        require(t["from"] == "DECISION" and t["to"] == "CLOSED" and
                all(t.get(k) is True for k in ("require_current_pass", "require_evidence", "require_human")),
                "Approval must require current PASS, evidence and human")
    require(flow["cycle_limit_policy"] == "reject_or_new_linked_proposal", "Cycle limit cannot auto-approve")
    schema = read_yaml(root, "schemas/decision_record_v1.yaml")["fields"]
    candidate = read_yaml(root, "council/decisions/decision-candidate.example.yaml")
    require(set(candidate) == set(schema), "Decision candidate must use existing schema fields")
    require(candidate["status"] == "draft", "Example cannot be accepted knowledge")
    pilot_path = root / "council/pilot/decision-candidate.yaml"
    if pilot_path.exists():
        pilot = read_yaml(root, "council/pilot/decision-candidate.yaml")
        require(set(pilot) == set(schema), "Pilot decision must use existing schema fields")
        require(pilot["status"] == "draft", "Pilot has no approval; must remain draft")
        require(bool(pilot["evidence_refs"]), "Pilot needs source references")
        for ref in pilot["evidence_refs"]:
            require((root / ref).is_file(), f"Missing pilot evidence: {ref}")
    for filename in ("council-proposal.yml", "council-review.yml"):
        form = read_yaml(root, ".github/ISSUE_TEMPLATE/" + filename)
        require(all(form.get(k) for k in ("name", "description", "body")), "Invalid Issue form")
        ids = [entry["id"] for entry in form["body"] if entry["type"] != "markdown"]
        require(len(ids) == len(set(ids)), "Duplicate Issue form IDs")
    return errors


if __name__ == "__main__":
    try:
        failures = validate(Path(__file__).resolve().parents[1])
    except (KeyError, TypeError, ValueError, OSError, yaml.YAMLError) as exc:
        failures = [f"Invalid Council configuration: {exc}"]
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    if not failures:
        print("PASS: Council static contracts; external integrations disabled")
    raise SystemExit(bool(failures))
