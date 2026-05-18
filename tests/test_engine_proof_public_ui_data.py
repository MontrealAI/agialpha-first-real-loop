from engine_proof_helpers import make_run, read_json, run_cmd
from agialpha_engine.context import atomic_write_json


def test_generated_public_data_exists(tmp_path):
    out = make_run(tmp_path)
    gen = tmp_path / "generated"
    run_cmd("build-proof-data", "--run", str(out), "--out", str(gen))
    for name in ["latest.json", "summary.json", "mandate_pairs.json", "computed_metrics.json", "treatment_vs_control.json", "stronger_claim_status.json", "falsification.json", "adversarial_docket.json"]:
        assert (gen / name).exists()


def test_render_proof_prominently_marks_unsupported_runs(tmp_path):
    out = make_run(tmp_path)
    summary_path = out / "15_public_summary" / "summary.json"
    summary = read_json(summary_path)
    summary["stronger_claim_status"] = "NOT_SUPPORTED"
    summary["stronger_claim_supported"] = False
    atomic_write_json(summary_path, summary)
    (out / "15_public_summary" / "stronger_claim_status.md").write_text(
        "This run does not support the stronger recursive-improvement claim.\n",
        encoding="utf-8",
    )
    rendered = tmp_path / "rendered"
    run_cmd("render-proof", "--run", str(out), "--out", str(rendered))
    html = (rendered / "index.html").read_text(encoding="utf-8")
    assert "Stronger claim status: NOT_SUPPORTED" in html
    assert "The stronger claim is not supported by this run." in html
