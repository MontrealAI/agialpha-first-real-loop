"""Adversarial fixture builders for falsification checks."""
from __future__ import annotations

def default_adversarial_fixtures() -> dict[str, list[dict[str, str]]]:
    return {
        "bad_claim_fixtures": [{"id": "unsafe_claim_positive", "expect_blocked": "true"}],
        "regulated_fixtures": [{"id": "regulated_decisioning_claim", "expect_blocked": "true"}],
        "fake_metric_fixtures": [{"id": "fake_b6_win", "expect_blocked": "true"}, {"id": "fake_vrci_constant", "expect_blocked": "true"}],
    }
