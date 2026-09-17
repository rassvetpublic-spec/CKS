#!/usr/bin/env python3
"""Fail-safe helper for CKS E4.5 main branch protection.

The helper is intentionally conservative:
- no mutation unless --apply is passed;
- requires an explicit admin-capable token from CKS_GITHUB_ADMIN_TOKEN or GITHUB_TOKEN;
- validates the exact required check names on the current branch head before applying;
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


def validate_check_surface(
    check_runs: Iterable[dict[str, Any]],
    required_checks: Iterable[str] = REQUIRED_CHECKS,
) -> None:
    counts = required_check_counts(check_runs)
    missing = [name for name in required_checks if counts[name] == 0]
    ambiguous = [name for name in required_checks if counts[name] > 1]
    if missing or ambiguous:
        details = []
        if missing:
            details.append(f"missing={missing}")
        if ambiguous:
            details.append(f"ambiguous={ambiguous}")
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


def protection_matches(
    protection: dict[str, Any] | None,
    required_checks: Iterable[str] = REQUIRED_CHECKS,
) -> bool:
    if not protection:
        return False
    expected = sorted(required_checks)
    actual = sorted(protection_contexts(protection))
    strict = bool((protection.get("required_status_checks") or {}).get("strict"))
    admins = bool((protection.get("enforce_admins") or {}).get("enabled"))
    force_pushes = bool((protection.get("allow_force_pushes") or {}).get("enabled"))
    deletions = bool((protection.get("allow_deletions") or {}).get("enabled"))
    return (
        actual == expected
        and strict
        and admins
        and pull_request_requirement_matches(protection)
        and not force_pushes
        and not deletions
    )


def get_branch(repo: str, branch: str, token: str) -> dict[str, Any]:
    encoded = urllib.parse.quote(branch, safe="")
    status, body = api_request("GET", _api_url(repo, f"branches/{encoded}"), token)
    if status != 200 or not isinstance(body, dict):
        raise ProtectionError(f"Cannot read branch {repo}:{branch}: HTTP {status}: {body}")
    return body


def get_check_runs(repo: str, sha: str, token: str) -> list[dict[str, Any]]:
    status, body = api_request(
        "GET",
        _api_url(repo, f"commits/{sha}/check-runs?per_page=100"),
        token,
    )
    if status != 200 or not isinstance(body, dict):
        raise ProtectionError(f"Cannot read check-runs for {sha}: HTTP {status}: {body}")
    runs = body.get("check_runs")
    if not isinstance(runs, list):
        raise ProtectionError("GitHub check-runs response did not contain a list")
    return [run for run in runs if isinstance(run, dict)]


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
    if current is not None:
        if protection_matches(current):
            return current
        if not replace_existing:
            raise ProtectionError(
                "A different branch-protection rule already exists. "
                "Refusing to replace it without --replace-existing."
            )

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

        plan = {
            "repo": args.repo,
            "branch": args.branch,
            "head_sha": sha,
            "currently_protected": bool(branch_state.get("protected")),
            "current_required_contexts": protection_contexts(current),
            "desired_required_contexts": list(REQUIRED_CHECKS),
            "desired_payload": build_protection_payload(),
            "apply": bool(args.apply),
        }
        print(json.dumps(plan, indent=2, ensure_ascii=False))

        if not args.apply:
            print("DRY-RUN PASS: check surface is safe; no mutation performed")
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
