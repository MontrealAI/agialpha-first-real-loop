"""Open RSI evaluation adapter metadata for AGI ALPHA Engine 001.

This module intentionally avoids benchmark-result claims. It only emits
local, deterministic metadata describing how an external adapter *could* be
wired under human review.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass(frozen=True)
class OpenRSIEvalAdapter:
    """Deterministic adapter metadata for external benchmark handoff."""

    adapter_id: str = "open_rsi_eval_adapter_v1"
    mode: str = "metadata_only"
    external_execution_allowed: bool = False
    official_result_claim_allowed: bool = False
    claim_boundary: str = "No Evidence Docket, no empirical SOTA claim."
    human_review_required: bool = True

    def to_record(self) -> Dict[str, Any]:
        record = asdict(self)
        record.update(
            {
                "status": "pending_human_configuration",
                "notes": (
                    "Adapter metadata only; external benchmark runs and claims "
                    "require human review and an Evidence Docket."
                ),
            }
        )
        return record


def build_open_rsi_eval_adapter_record() -> Dict[str, Any]:
    """Return deterministic adapter metadata for registry/doc generation."""

    return OpenRSIEvalAdapter().to_record()
