from pathlib import Path

def test_docs_exist():
    assert Path("docs/enterprise-pilot/README.md").exists()
    assert Path("docs/enterprise-pilot/templates/customer-review-record.md").exists()
