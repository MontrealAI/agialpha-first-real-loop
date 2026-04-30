from agialpha_evidence_hub.build import build_site

def test_legacy(tmp_path):
    build_site('evidence_registry/registry', tmp_path)
    assert (tmp_path/'helios-001/index.html').exists()
