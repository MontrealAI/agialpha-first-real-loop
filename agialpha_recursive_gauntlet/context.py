from __future__ import annotations
import json, hashlib, datetime
from pathlib import Path

CLAIM_BOUNDARY = """AGI ALPHA Recursive Proof Gauntlet produces local, bounded recursive substrate evidence. It does not claim achieved AGI, achieved ASI, superintelligence, empirical SOTA, safe autonomy, cybersecurity certification, official benchmark victory, legal approval, or investment return."""

def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def digest_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()
