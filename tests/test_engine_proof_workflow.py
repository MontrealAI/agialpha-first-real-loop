from pathlib import Path


def test_engine002_workflow_safe():
    wf = Path(".github/workflows/agialpha-engine-002-measured-recursive-proof.yml").read_text()
    assert "AGI ALPHA Engine 002 / Measured Recursive Machine Labor Proof" in wf
    assert "contents: read" in wf and "actions: read" in wf
    assert "deploy-pages" not in wf
    assert "auto-merge" not in wf.lower()
