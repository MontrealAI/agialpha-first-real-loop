from agialpha_evidence_hub.discover import backfill
from agialpha_evidence_hub.build import build_site

def test_build(tmp_path):
    reg=tmp_path/'reg'; out=tmp_path/'site'
    backfill('.',str(reg)); build_site(str(reg),str(out))
    assert (out/'index.html').exists()
