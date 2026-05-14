from .context import *
def lock_candidates(run: Path):
    cands=[]
    for p in sorted((run/'02_candidates').glob('candidate-*/candidate.json')):
        c=read_json(p); patch=Path(c['patch_path']).read_text(encoding='utf-8')
        h=digest_text(json.dumps(c,sort_keys=True)+patch)
        cands.append({"candidate_id":c['candidate_id'],"candidate_hash":h})
    lock={"locked_at":now_iso(),"claim_boundary":CLAIM_BOUNDARY,"candidates":cands}
    write_json(run/'03_candidate_lock/candidate_lock.json',lock); write_json(run/'03_candidate_lock/candidate_hashes.json',cands); return lock
