#!/usr/bin/env python3
"""Fail-safe helper for CKS E4.5 main branch protection.

The helper is intentionally conservative:
- no mutation unless --apply is passed;
- requires an explicit admin-capable token from CKS_GITHUB_ADMIN_TOKEN or GITHUB_TOKEN;
- validates the exact required check names and canonical producer workflows on the current branch head before applying;
- allows repeated executions of the same canonical workflow, but rejects a required context produced by a second workflow;
- requires pull-request merging while requiring zero approving reviews;
- refuses to replace an existing, different protection rule unless --replace-existing is passed;
- reads the protection state back after mutation and fails if it does not match the intended policy.

This tool changes repository governance only. It does not touch repository contents, Canon, or Frozen Core.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from typing import Any, Iterable

API_VERSION = "2022-11-28"
DEFAULT_REPO = "rassvetpublic-spec/CKS"
DEFAULT_BRANCH = "main"
REQUIRED_CHECKS = (
    "Package 003 integrated automation gate",
    "boundary",
    "canon-guard",
    "traceability",
    "governance",
    "validate-control-plane",
    "validate-bootstrap",
)
EXPECTED_CHECK_WORKFLOWS = {
    "Package 003 integrated automation gate": ".github/workflows/cks-package-003-automation.yml",
    "boundary": ".github/workflows/cks-boundary-check.yml",
    "canon-guard": ".github/workflows/cks-canon-evidence-guard.yml",
    "traceability": ".github/workflows/cks-traceability-check.yml",
    "governance": ".github/workflows/cks-governance-runner.yml",
    "validate-control-plane": ".github/workflows/cks-control-plane-validation.yml",
    "validate-bootstrap": ".github/workflows/bootstrap-check.yml",
}
PRODUCER_WORKFLOW_FIELD = "_cks_producer_workflow_path"


class ProtectionError(RuntimeError):
    pass


def _api_url(repo: str, suffix: str) -> str:
    return f"https://api.github.com/repos/{repo}/{suffix.lstrip('/')}"


def api_request(
    method: str,
    url: str,
    token: str,
    payload: dict[str, Any] | None = None,
) -> tuple[int, Any]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "cks-e4-branch-protection-helper",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return response.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            body: Any = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            body = raw
        return exc.code, body


def required_check_counts(check_runs: Iterable[dict[str, Any]]) -> Counter[str]:
    return Counter(
        str(run.get("name"))
        for run in check_runs
        if isinstance(run, dict) and run.get("name") is not None
    )


def required_check_producers(
    check_runs: Iterable[dict[str, Any]],
    required_checks: Iterable[str] = REQUIRED_CHECKS,
) -> dict[str, list[str]]:
    required = set(required_checks)
    producers: dict[str, set[str]] = {name: set() for name in required}
    for run in check_runs:
        if not isinstance(run, dict):
            continue
        name = str(run.get("name") or "")
        if name not in required:
            continue
        producer = run.get(PRODUCER_WORKFLOW_FIELD)
        if producer:
            producers[name].add(str(producer))
    return {name: sorted(values) for name, values in producers.items()}


def validate_check_surface(
    check_runs: Iterable[dict[str, Any]],
    required_checks: Iterable[str] = REQUIRED_CHECKS,
    expected_workflows: dict[str, str] | None = None,
) -> None:
    runs = [run for run in check_runs if isinstance(run, dict)]
    required = tuple(required_checks)
    expected = EXPECTED_CHECK_WORKFLOWS if expected_workflows is None else expected_workflows
    counts = required_check_counts(runs)
    missing = [name for name in required if counts[name] == 0]
    unresolved: list[str] = []
    ambiguous: dict[str, list[str]] = {}
    unexpected: dict[str, list[str]] = {}

    for name in required:
        matching = [run for run in runs if str(run.get("name") or "") == name]
        if not matching:
            continue
        producer_values = {
            str(run.get(PRODUCER_WORKFLOW_FIELD))
            for run in matching
            if run.get(PRODUCER_WORKFLOW_FIELD)
        }
        if len(producer_values) != len(
            {
                str(run.get(PRODUCER_WORKFLOW_FIELD))
                for run in matching
                if run.get(PRODUCER_WORKFLOW_FIELD)
            }
        ):
            raise AssertionError("producer normalization must be deterministic")
        if any(not run.get(PRODUCER_WORKFLOW_FIELD) for run in matching):
            unresolved.append(name)
            continue
        if len(producer_values) > 1:
            ambiguous[name] = sorted(producer_values)
        expected_path = expected.get(name)
        if expected_path is None:
            unresolved.append(name)
        elif producer_values != {expected_path}:
            unexpected[name] = sorted(producer_values)

    if missing or unresolved or ambiguous or unexpected:
        details = []
        if missing:
            details.append(f"missing={missing}")
        if unresolved:
            details.append(f"unresolved_producer={sorted(set(unresolved))}")
        if ambiguous:
            details.append(f"ambiguous_producers={ambiguous}")
        if unexpected:
            details.append(f"unexpected_producers={unexpected}")
        raise ProtectionError(
            "Required check surface is not safe for protection: " + ", ".join(details)
        )


def build_protection_payload(
    required_checks: Iterable[str] = REQUIRED_CHECKS,
) -> dict[str, Any]:
    return {
        "required_status_checks": {
            "strict": True,
            "contexts": list(required_checks),
        },
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": False,
            "require_code_owner_reviews": False,
            "required_approving_review_count": 0,
            "require_last_push_approval": False,
        },
        "restrictions": None,
        "required_linear_history": False,
        "allow_force_pushes": False,
        "allow_deletions": False,
        "block_creations": False,
        "required_conversation_resolution": False,
        "lock_branch": False,
        "allow_fork_syncing": False,
    }


def protection_contexts(protection: dict[str, Any] | None) -> list[str]:
    if not protection:
        return []
    status_checks = protection.get("required_status_checks") or {}
    contexts = status_checks.get("contexts") or []
    return [str(item) for item in contexts]


def pull_request_requirement_matches(protection: dict[str, Any] | None) -> bool:
    if not protection:
        return False
    reviews = protection.get("required_pull_request_reviews")
    if not isinstance(reviews, dict):
        return False
    return (
        reviews.get("required_approving_review_count") == 0
        and not bool(reviews.get("dismiss_stale_reviews"))
        and not bool(reviews.get("require_code_owner_reviews"))
        and not bool(reviews.get("require_last_push_approval"))
    )


def _protection_flag_enabled(protection: dict[str, Any], name: str) -> bool:
    setting = protection.get(name) or {}
    return bool(setting.get("enabled")) if isinstance(setting, dict) else bool(setting)


def protection_matches(
    protection: dict[str, Any] | None,
    required_checks: Iterable[str] = REQUIRED_CHECKS,
) -> bool:
    if not protection:
        return False
    expected = sorted(required_checks)
    actual = sorted(protection_contexts(protection))
    strict = bool((protection.get("required_status_checks") or {}).get("strict"))
    admins = _protection_flag_enabled(protection, "enforce_admins")
    no_push_restrictions = protection.get("restrictions") is None
    disabled_target_flags = (
        "required_linear_history",
        "allow_force_pushes",
        "allow_deletions",
        "block_creations",
        "required_conversation_resolution",
        "lock_branch",
        "allow_fork_syncing",
    )
    return (
        actual == expected
        and strict
        and admins
        and pull_request_requirement_matches(protection)
        and no_push_restrictions
        and all(
            not _protection_flag_enabled(protection, name)
            for name in disabled_target_flags
        )
    )


def validate_existing_protection(
    protection: dict[str, Any] | None,
    replace_existing: bool = False,
) -> None:
    if protection is None or protection_matches(protection):
        return
    if not replace_existing:
        raise ProtectionError(
            "A different branch-protection rule already exists. "
            "Refusing to replace it without --replace-existing."
        )


def get_branch(repo: str, branch: str, token: str) -> dict[str, Any]:
    encoded = urllib.parse.quote(branch, safe="")
    status, body = api_request("GET", _api_url(repo, f"branches/{encoded}"), token)
    if status != 200 or not isinstance(body, dict):
        raise ProtectionError(f"Cannot read branch {repo}:{branch}: HTTP {status}: {body}")
    return body


def _actions_run_id(check_run: dict[str, Any]) -> int | None:
    details_url = str(check_run.get("details_url") or check_run.get("html_url") or "")
    if not details_url:
        return None
    parts = [part for part in urllib.parse.urlparse(details_url).path.split("/") if part]
    try:
        runs_index = parts.index("runs")
        return int(parts[runs_index + 1])
    except (ValueError, IndexError):
        return None


def get_actions_workflow_path(repo: str, run_id: int, token: str) -> str:
    status, body = api_request(
        "GET",
        _api_url(repo, f"actions/runs/{run_id}"),
        token,
    )
    if status != 200 or not isinstance(body, dict):
        raise ProtectionError(
            f"Cannot resolve workflow producer for Actions run {run_id}: HTTP {status}: {body}"
        )
    path = body.get("path")
    if not isinstance(path, str) or not path:
        raise ProtectionError(
            f"Actions run {run_id} does not contain a workflow path"
        )
    return path


def get_check_runs(repo: str, sha: str, token: str) -> list[dict[str, Any]]:
    status, body = api_request(
        "GET",
        _api_url(repo, f"commits/{sha}/check-runs?per_page=100"),
        token,
    )
    if status != 200 or not isinstance(body, dict):
        raise ProtectionError(f"Cannot read check-runs for {sha}: HTTP {status}: {body}")
    raw_runs = body.get("check_runs")
    if not isinstance(raw_runs, list):
        raise ProtectionError("GitHub check-runs response did not contain a list")

    runs = [dict(run) for run in raw_runs if isinstance(run, dict)]
    workflow_cache: dict[int, str] = {}
    required = set(REQUIRED_CHECKS)
    for run in runs:
        name = str(run.get("name") or "")
        if name not in required:
            continue
        run_id = _actions_run_id(run)
        if run_id is None:
            raise ProtectionError(
                f"Cannot resolve producer workflow run for required check {name!r}"
            )
        if run_id not in workflow_cache:
            workflow_cache[run_id] = get_actions_workflow_path(repo, run_id, token)
        run[PRODUCER_WORKFLOW_FIELD] = workflow_cache[run_id]
    return runs


def get_protection(repo: str, branch: str, token: str) -> dict[str, Any] | None:
    encoded = urllib.parse.quote(branch, safe="")
    status, body = api_request(
        "GET",
        _api_url(repo, f"branches/{encoded}/protection"),
        token,
    )
    if status == 404:
        return None
    if status != 200 or not isinstance(body, dict):
        raise ProtectionError(
            f"Cannot read protection for {repo}:{branch}: HTTP {status}: {body}"
        )
    return body


def apply_protection(
    repo: str,
    branch: str,
    token: str,
    replace_existing: bool = False,
) -> dict[str, Any]:
    branch_state = get_branch(repo, branch, token)
    sha = str((branch_state.get("commit") or {}).get("sha") or "")
    if not sha:
        raise ProtectionError("Branch response does not contain a head SHA")

    check_runs = get_check_runs(repo, sha, token)
    validate_check_surface(check_runs)

    current = get_protection(repo, branch, token)
    if current is not None and protection_matches(current):
        return current
    validate_existing_protection(current, replace_existing=replace_existing)

    payload = build_protection_payload()
    encoded = urllib.parse.quote(branch, safe="")
    status, body = api_request(
        "PUT",
        _api_url(repo, f"branches/{encoded}/protection"),
        token,
        payload,
    )
    if status != 200 or not isinstance(body, dict):
        raise ProtectionError(f"Protection update failed: HTTP {status}: {body}")

    verified = get_protection(repo, branch, token)
    verified_branch = get_branch(repo, branch, token)
    if not bool(verified_branch.get("protected")):
        raise ProtectionError("Read-back failed: branch is still reported as unprotected")
    if not protection_matches(verified):
        raise ProtectionError(
            "Read-back failed: protection rule does not exactly match the intended policy"
        )
    return verified


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually mutate GitHub branch protection. Without this flag, only preflight is run.",
    )
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="Allow replacing a different existing protection rule. Use only after manual review.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    token = os.environ.get("CKS_GITHUB_ADMIN_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        print(
            "ERROR: set CKS_GITHUB_ADMIN_TOKEN (preferred) or GITHUB_TOKEN to an admin-capable token",
            file=sys.stderr,
        )
        return 2

    try:
        branch_state = get_branch(args.repo, args.branch, token)
        sha = str((branch_state.get("commit") or {}).get("sha") or "")
        check_runs = get_check_runs(args.repo, sha, token)
        validate_check_surface(check_runs)
        current = get_protection(args.repo, args.branch, token)
        validate_existing_protection(current, replace_existing=args.replace_existing)

        plan = {
            "repo": args.repo,
            "branch": args.branch,
            "head_sha": sha,
            "currently_protected": bool(branch_state.get("protected")),
            "current_required_contexts": protection_contexts(current),
            "current_policy_matches_target": protection_matches(current),
            "observed_required_check_producers": required_check_producers(check_runs),
            "desired_required_contexts": list(REQUIRED_CHECKS),
            "desired_check_producers": EXPECTED_CHECK_WORKFLOWS,
            "desired_payload": build_protection_payload(),
            "replace_existing": bool(args.replace_existing),
            "apply": bool(args.apply),
        }
        print(json.dumps(plan, indent=2, ensure_ascii=False))

        if not args.apply:
            print(
                "DRY-RUN PASS: check surface, canonical producers, and existing protection state are safe; "
                "no mutation performed"
            )
            return 0

        final_state = apply_protection(
            args.repo,
            args.branch,
            token,
            replace_existing=args.replace_existing,
        )
        print(
            json.dumps(
                {
                    "status": "VERIFIED",
                    "required_contexts": protection_contexts(final_state),
                    "strict": bool(
                        (final_state.get("required_status_checks") or {}).get("strict")
                    ),
                    "pull_request_required": pull_request_requirement_matches(final_state),
                    "enforce_admins": bool(
                        (final_state.get("enforce_admins") or {}).get("enabled")
                    ),
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0
    except ProtectionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
