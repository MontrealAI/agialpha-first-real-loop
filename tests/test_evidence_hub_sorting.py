import json
from agialpha_evidence_hub.registry import save_registry
from agialpha_evidence_hub.build import build_site

def test_sorting(tmp_path):
    reg=tmp_path/'reg'; out=tmp_path/'site'
    runs=[{'run_id':'old','generated_at':'2020-01-01T00:00:00Z','experiment_slug':'a','status':'pending','claim_boundary':'does not claim','run_url':'#'},{'run_id':'new','generated_at':'2021-01-01T00:00:00Z','experiment_slug':'a','status':'success','claim_boundary':'does not claim','run_url':'#'}]
    save_registry(str(reg),{'runs':runs,'experiments':[{'experiment_slug':'a','claim_boundary':'does not claim'}],'workflows':[]})
    build_site(str(reg),str(out))
    data=json.loads((out/'data'/'runs.json').read_text())
    assert data[0]['run_id']=='new'
