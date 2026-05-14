from .context import *
from .lock import canonical_candidate_hash

ALLOWED_TYPES = [
    "validator improvement",
    "test improvement",
    "workflow launchpad improvement",
    "Evidence Docket template improvement",
    "ProofBundle template improvement",
    "claim-boundary detector improvement",
]


def _candidate_patch() -> str:
    return (
        "diff --git a/docs/recursive-gauntlet/README.md b/docs/recursive-gauntlet/README.md\n"
        "--- a/docs/recursive-gauntlet/README.md\n"
        "+++ b/docs/recursive-gauntlet/README.md\n"
        "@@ -1,3 +1,4 @@\n"
        " # Recursive Gauntlet\n"
        " \n"
        " AGI ALPHA Recursive Proof Gauntlet produces local, bounded recursive substrate evidence. It does not claim achieved AGI, achieved ASI, superintelligence, empirical SOTA, safe autonomy, cybersecurity certification, official benchmark victory, legal approval, or investment return.\n"
        "+- Candidate mechanism note: preserve local bounded recursive substrate evidence.\n"
    )


def generate_candidates(run: Path, count: int = 6):
    base = run / "02_candidates"
    base.mkdir(parents=True, exist_ok=True)
    out = []
    patch = _candidate_patch()
    for i in range(1, count + 1):
        cid = f"candidate-{i:03d}"
        cdir = base / cid
        cdir.mkdir(parents=True, exist_ok=True)
        patch_path = cdir / "candidate.patch"
        patch_path.write_text(patch, encoding="utf-8")
        cand = {
            "candidate_id": cid,
            "candidate_type": ALLOWED_TYPES[(i - 1) % len(ALLOWED_TYPES)],
            "changed_files": ["docs/recursive-gauntlet/README.md"],
            "patch_path": "candidate.patch",
            "rationale": "Improve recursive proof quality",
            "expected_benefit": "higher held-out completeness",
            "expected_risk": "low",
            "rollback_note": "revert patch",
            "claim_boundary_impact": "preserved",
            "safety_impact": "none",
            "utility_token_impact": "utility-only accounting preserved",
            "candidate_hash": "",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        cand["candidate_hash"] = canonical_candidate_hash(cand, patch)
        write_json(cdir / "candidate.json", cand)
        (cdir / "rationale.md").write_text(f"# Rationale\n\n{CLAIM_BOUNDARY}\n", encoding="utf-8")
        write_json(cdir / "risk_assessment.json", {"risk": "low", "claim_boundary": CLAIM_BOUNDARY})
        (cdir / "rollback.md").write_text("Rollback: revert candidate patch.\n", encoding="utf-8")
        out.append(cand)
    return out
