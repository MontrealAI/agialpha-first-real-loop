from agialpha_evidence_hub.discover import backfill
from agialpha_evidence_hub.build import build_site
from agialpha_evidence_hub.linkcheck import linkcheck

def test_links(tmp_path):
    reg=tmp_path/'reg'; out=tmp_path/'site'
    backfill('.',str(reg)); build_site(str(reg),str(out)); linkcheck(str(out))
