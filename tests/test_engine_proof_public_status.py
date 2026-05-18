from agialpha_engine.metrics import compute_metrics
from engine_proof_helpers import make_run, read_json


def test_unsupported_status_and_supported_requires_gates(tmp_path):
    out = make_run(tmp_path)
    metrics = read_json(out / "08_comparison/computed_metrics.json")
    assert metrics["stronger_claim_supported"] is True
    status = (out / "15_public_summary/stronger_claim_status.md").read_text().strip()
    assert status == "This run supports the local bounded claim that AGI ALPHA demonstrated machine labor that recursively improves in a measured, falsifiable way."
    unsupported = compute_metrics({"mandate_pairs": [], "treatment_results": [], "shadow_control_results": [], "safety_counters": {}})
    assert unsupported["stronger_claim_supported"] is False
