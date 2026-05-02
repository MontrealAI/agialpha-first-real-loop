"""Promotion gate utilities for proof-gated persistence."""

def promotion_allowed(*, evidence_docket_present: bool, replay_passed: bool, falsification_passed: bool, human_reviewed: bool) -> bool:
    """Promotion is allowed only when all proof gates pass and human review exists."""
    return all([evidence_docket_present, replay_passed, falsification_passed, human_reviewed])
