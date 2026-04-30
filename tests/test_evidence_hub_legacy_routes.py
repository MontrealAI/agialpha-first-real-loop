from agialpha_evidence_hub.discover import backfill
from agialpha_evidence_hub.build import build_site

def test_legacy(tmp_path):
    reg=tmp_path/'reg'; out=tmp_path/'site'
    backfill('.',str(reg)); build_site(str(reg),str(out))
    for p in ['helios-001','helios-004','cyber-sovereign-001','cyber-sovereign-002','cyber-sovereign-003','benchmark-gauntlet-001','omega-gauntlet-001']:
        assert (out/p/'index.html').exists()
