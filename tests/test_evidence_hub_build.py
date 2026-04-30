from agialpha_evidence_hub.build import build_site
from pathlib import Path

def test_build(tmp_path):
    build_site('evidence_registry/registry', tmp_path)
    assert (tmp_path/'index.html').exists()
