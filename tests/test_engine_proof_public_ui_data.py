from engine_proof_helpers import make_run, run_cmd


def test_generated_public_data_exists(tmp_path):
    out = make_run(tmp_path)
    gen = tmp_path / "generated"
    run_cmd("build-proof-data", "--run", str(out), "--out", str(gen))
    for name in ["latest.json", "summary.json", "mandate_pairs.json", "computed_metrics.json", "treatment_vs_control.json", "stronger_claim_status.json", "falsification.json", "adversarial_docket.json"]:
        assert (gen / name).exists()
