from engine_proof_helpers import make_run, run_cmd, read_json


def test_falsification_audit_passes_and_checks_bad_fixtures(tmp_path):
    out = make_run(tmp_path)
    run_cmd("falsification-audit-proof", "--run", str(out))
    audit = read_json(out / "14_falsification/falsification_audit.json")
    assert audit["falsification_pass"] is True
    assert audit["checks"]["capability_mutation_rejected"] is True
