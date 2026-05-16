from pathlib import Path


def test_enterprise_pilot_docs_exist_and_state_boundaries():
    required = [
        "README_ENTERPRISE_PILOT.md",
        "docs/enterprise-pilot/README.md",
        "docs/enterprise-pilot/regulated-boundary.md",
        "docs/enterprise-pilot/not-an-investment-claim.md",
    ]
    for path in required:
        assert Path(path).exists(), path
    text = Path("README_ENTERPRISE_PILOT.md").read_text().lower()
    assert "not regulated decisioning" in text
    assert "utility-only" in text
