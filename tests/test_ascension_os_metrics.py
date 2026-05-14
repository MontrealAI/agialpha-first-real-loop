import json, tempfile, subprocess, sys, os

def test_metric_outputs_include_boundaries():
    d=tempfile.mkdtemp()
    subprocess.check_call([sys.executable,"-m","agialpha_ascension_os","run-cycle","--repo-root",".","--registry","ascension_os_registry","--out",d])
    for n in ["verified_enterprise_alpha.json","value_to_capacity.json"]:
        data=json.load(open(os.path.join(d,n)))
        assert data["human_review_required"] is True
        assert data["no_auto_merge"] is True
