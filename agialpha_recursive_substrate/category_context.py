"""Category context for AGI ALPHA Recursive Substrate.

Reference map entries are context-only and not implementation claims.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Any


CLAIM_BOUNDARY = (
    "This category context is positioning and research context. It does not claim "
    "AGI ALPHA has achieved AGI, ASI, superintelligence, empirical SOTA, or external validation."
)


@dataclass(frozen=True)
class CategoryContext:
    category: str
    external_context_summary: List[str]
    reference_families: List[str]
    agialpha_original_position: str
    claim_boundary: str = CLAIM_BOUNDARY

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["schema_version"] = "agialpha.recursive_category_context.v1"
        return data


def default_category_context() -> Dict[str, Any]:
    return CategoryContext(
        category="self-improving AI / recursive AI labor / open-ended automated discovery",
        external_context_summary=[
            "The public self-improving AI category is moving toward open-ended algorithms, automated scientific discovery, and AI systems that improve AI.",
            "Open-ended discovery is described as a process that produces and preserves an archive of discoveries that build on one another.",
            "A major public category thesis is AI improving AI first, then applying the playbook to broader science.",
        ],
        reference_families=[
            "AI-generating algorithms",
            "open-ended discovery",
            "quality-diversity algorithms",
            "Darwin Gödel Machine",
            "ADAS",
            "AI Scientist",
            "PromptBreeder",
            "Rainbow Teaming",
            "Automated Capability Discovery",
            "self-improving coding agents",
            "automated red teaming",
            "meta-agentic orchestration",
            "recursive AI labor",
        ],
        agialpha_original_position=(
            "AGI ALPHA implements this category as a governed substrate for proof-bound machine labor: "
            "Work Vaults, MARK allocation, Sovereigns, AGI Jobs, validators, ProofBundles, Evidence Dockets, "
            "policy decisions, settlement, human review, and vNext recursive cycles."
        ),
    ).to_dict()
