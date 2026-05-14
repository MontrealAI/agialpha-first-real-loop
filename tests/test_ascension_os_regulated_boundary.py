import tempfile, subprocess, sys, os, json

def test_regulated_boundary_schema_and_defaults():
    d=tempfile.mkdtemp()
    subprocess.check_call([sys.executable,"-m","agialpha_ascension_os","run-cycle","--repo-root",".","--registry",d+"/reg","--out",d])
    triage=json.load(open(os.path.join(d,"regulated_boundary_triage.json")))
    assert triage["schema_version"]=="agialpha.regulated_boundary_triage.v1"
    assert triage["synthetic_fixture_only"] is True
    assert triage["allowed_mode"]=="safe_enterprise_workflow"
