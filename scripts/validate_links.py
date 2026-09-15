"""Validate relationships between CKS artifacts.

Reserved for checks:
- decision -> evidence
- canon -> decision
- knowledge -> source
"""


def validate_links():
    return True


if __name__ == "__main__":
    raise SystemExit(0 if validate_links() else 1)
