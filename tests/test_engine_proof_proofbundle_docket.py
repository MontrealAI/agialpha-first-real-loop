from engine_proof_helpers import make_run, read_json


def test_proofbundle_and_evidence_docket_complete(tmp_path):
    out = make_run(tmp_path)
    assert read_json(out / "10_proofbundles/proofbundle_index.json")["proofbundle_complete"] is True
    assert read_json(out / "11_evidence_dockets/docket_index.json")["evidence_docket_complete"] is True
