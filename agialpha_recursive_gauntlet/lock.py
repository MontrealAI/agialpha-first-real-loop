from .context import *
import json


def canonical_candidate_hash(candidate: dict, patch_text: str) -> str:
    payload = dict(candidate)
    payload.pop("candidate_hash", None)
    return digest_text(json.dumps(payload, sort_keys=True) + patch_text)


def lock_candidates(run: Path):
    cands = []
    for p in sorted((run / "02_candidates").glob("candidate-*/candidate.json")):
        c = read_json(p)
        patch = Path(c["patch_path"]).read_text(encoding="utf-8")
        h = canonical_candidate_hash(c, patch)
        cands.append({"candidate_id": c["candidate_id"], "candidate_hash": h})
    lock = {"locked_at": now_iso(), "claim_boundary": CLAIM_BOUNDARY, "candidates": cands}
    write_json(run / "03_candidate_lock/candidate_lock.json", lock)
    write_json(run / "03_candidate_lock/candidate_hashes.json", cands)
    return lock
