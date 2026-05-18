from engine_proof_helpers import make_run


def test_public_summary_has_no_forbidden_overclaim(tmp_path):
    out = make_run(tmp_path)
    text = (out / "15_public_summary/summary.md").read_text().lower()
    forbidden = ["achieved agi", "achieved asi", "empirical sota", "official benchmark victory", "certified safety", "legal compliance certification", "eu ai act exemption"]
    assert not any(term in text for term in forbidden)
