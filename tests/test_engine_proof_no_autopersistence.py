from pathlib import Path
from engine_proof_helpers import make_run, read_json


def test_no_automerge_no_pages_deploy(tmp_path):
    out = make_run(tmp_path)
    assert read_json(out / "08_comparison/computed_metrics.json")["unsafe_automerge_count"] == 0
    wf = Path(".github/workflows/agialpha-engine-002-measured-recursive-proof.yml").read_text()
    assert "deploy-pages" not in wf
    assert "gh pr merge" not in wf
