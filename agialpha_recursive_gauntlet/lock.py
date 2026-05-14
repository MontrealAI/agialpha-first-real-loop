from .context import *
import json


def canonical_candidate_hash(candidate: dict, patch_text: str) -> str:
    payload = dict(candidate)
    payload.pop("candidate_hash", None)
    return digest_text(json.dumps(payload, sort_keys=True) + patch_text)


def _resolve_patch_path(candidate_file: Path, patch_path: str) -> Path:
    p = Path(patch_path)
    if p.is_absolute():
        return p
    rel_to_candidate = (candidate_file.parent / p).resolve()
    if rel_to_candidate.exists():
        return rel_to_candidate
    rel_to_run = (candidate_file.parents[2] / p).resolve()
    if rel_to_run.exists():
        return rel_to_run
    rel_to_cwd = (Path.cwd() / p).resolve()
    return rel_to_cwd


def lock_candidates(run: Path):
    cands = []
    for p in sorted((run / "02_candidates").glob("candidate-*/candidate.json")):
        c = read_json(p)
        patch_path = _resolve_patch_path(p, c["patch_path"])
        patch = patch_path.read_text(encoding="utf-8")
        h = canonical_candidate_hash(c, patch)
        cands.append({"candidate_id": c["candidate_id"], "candidate_hash": h})
    lock = {"locked_at": now_iso(), "claim_boundary": CLAIM_BOUNDARY, "candidates": cands}
    write_json(run / "03_candidate_lock/candidate_lock.json", lock)
    write_json(run / "03_candidate_lock/candidate_hashes.json", cands)
    return lock
