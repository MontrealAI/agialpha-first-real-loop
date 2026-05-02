import hashlib, json
from pathlib import Path

def lock_candidates(candidates:list,out_dir:Path):
    out_dir.mkdir(parents=True,exist_ok=True)
    hashes={}
    for c in candidates:
        blob=json.dumps(c,sort_keys=True).encode()
        h=hashlib.sha256(blob).hexdigest()
        hashes[c['candidate_id']]=h
    root_input=json.dumps(hashes,sort_keys=True).encode()
    lock_root_hash=hashlib.sha256(root_input).hexdigest()
    manifest={"locked":True,"candidate_hashes":hashes,"lock_root_hash":lock_root_hash}
    (out_dir/'candidate_lock_manifest.json').write_text(json.dumps(manifest,indent=2))
    return manifest
