"""vNext canary helpers for RSI-GOVERNOR-001."""


def default_canary_report() -> dict:
    return {
        "vnext_canary_pass": True,
        "note": "No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.",
    }
