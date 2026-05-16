from pathlib import Path


def test_enterprise_pilot_workflow_exists_and_disables_pages_automerge():
    wf = Path('.github/workflows/agialpha-enterprise-pilot-001.yml').read_text().lower()
    assert "agi alpha enterprise pilot 001 / evidence factory" in wf
    assert "workflow_dispatch:" in wf
    assert "schedule:" in wf
    assert "actions/upload-artifact" in wf
    assert "deploy pages" not in wf
    assert "actions/deploy-pages" not in wf
    assert "automerge" not in wf
