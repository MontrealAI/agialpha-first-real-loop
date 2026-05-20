from engine_proof_helpers import make_run, run_cmd


def test_engine_002_render_includes_stronger_claim_status(tmp_path):
    out = make_run(tmp_path)
    rendered = tmp_path / "rendered"
    run_cmd("render-proof", "--run", str(out), "--out", str(rendered))
    html = (rendered / "index.html").read_text(encoding="utf-8")
    assert "AGI ALPHA Engine" in html
    assert "Stronger claim status:" in html
