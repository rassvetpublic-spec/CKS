"""Контрактные проверки архитектуры Antigravity GUI."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"


def test_required_architecture_documents_exist():
    required = [
        "ADR-001-ANTIGRAVITY-GUI-CONTRACTS.md",
        "ANTIGRAVITY-EVENT-CONTRACT-v1.md",
        "ANTIGRAVITY-EVIDENCE-ADAPTER-v1.md",
        "ANTIGRAVITY-QA-CONTEXT-BRIDGE-v1.md",
    ]
    for item in required:
        assert (DOCS / item).exists()


def test_architecture_rules():
    text = "\n".join(p.read_text(encoding="utf-8") for p in DOCS.glob("*ANTIGRAVITY*.md"))
    assert "CKS не зависит от Electron" in text
    assert "QA_CONTEXT = PR_HEAD + BASE_REFERENCE" in text
    assert "Event Contract" in text
