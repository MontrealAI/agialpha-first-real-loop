from .context import *
import json

ALLOWED_TYPES = [
    "validator improvement",
    "test improvement",
    "workflow launchpad improvement",
    "Evidence Docket template improvement",
    "ProofBundle template improvement",
    "claim-boundary detector improvement",
]


def generate_candidates(run: Path, count: int = 6):
    base = run / "02_candidates"
    base.mkdir(parents=True, exist_ok=True)
    out = []
    patch = (
        "diff --git a/docs/recursive-gauntlet/README.md b/docs/recursive-gauntlet/README.md\n"
        "+Local bounded recursive substrate evidence candidate note\n"
    )
    for i in range(1, count + 1):
        cid = f"candidate-{i:03d}"
        cdir = base / cid
        cdir.mkdir(parents=True, exist_ok=True)
        (cdir / "candidate.patch").write_text(patch + "\n", encoding="utf-8")
        cand = {
            "candidate_id": cid,
            "candidate_type": ALLOWED_TYPES[(i - 1) % len(ALLOWED_TYPES)],
            "changed_files": ["docs/recursive-gauntlet/README.md"],
            "patch_path": str((cdir / "candidate.patch").as_posix()),
            "rationale": "Improve recursive proof quality",
            "expected_benefit": "higher held-out completeness",
            "expected_risk": "low",
            "rollback_note": "revert patch",
            "claim_boundary_impact": "preserved",
            "safety_impact": "none",
            "utility_token_impact": "utility-only accounting preserved",
            "candidate_hash": "",
        }
        cand["candidate_hash"] = digest_text(json.dumps(cand, sort_keys=True) + patch)
        write_json(cdir / "candidate.json", cand)
        (cdir / "rationale.md").write_text(f"# Rationale\n\n{CLAIM_BOUNDARY}\n", encoding="utf-8")
        write_json(cdir / "risk_assessment.json", {"risk": "low", "claim_boundary": CLAIM_BOUNDARY})
        (cdir / "rollback.md").write_text("Rollback: revert candidate patch.\n", encoding="utf-8")
        out.append(cand)
    return out
