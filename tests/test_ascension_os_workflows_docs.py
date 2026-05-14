from pathlib import Path

def test_workflow_files_exist():
    assert Path('.github/workflows/agialpha-ascension-os-001-lifecycle.yml').exists()
    assert Path('.github/workflows/agialpha-valuation-support-001.yml').exists()

def test_docs_exist():
    for p in [
        'README_ASCENSION_OS.md','README_VALUATION_SUPPORT.md','docs/ascension-os/README.md','docs/valuation-support/README.md'
    ]:
        assert Path(p).exists()
