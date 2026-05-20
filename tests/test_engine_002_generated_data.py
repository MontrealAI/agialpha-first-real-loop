from engine_proof_helpers import make_run, run_cmd


def test_engine_002_build_data_emits_expected_files(tmp_path):
    out = make_run(tmp_path)
    generated = tmp_path / "generated_engine_002"
    run_cmd("build-proof-data", "--run", str(out), "--out", str(generated))
    expected = {
        "latest.json",
        "summary.json",
        "computed_metrics.json",
        "stronger_claim_status.json",
        "treatment_vs_control.json",
        "falsification.json",
    }
    assert expected.issubset({p.name for p in generated.iterdir() if p.is_file()})
