import hashlib, json, uuid
from pathlib import Path

def _guess_context_type(path: Path):
    n = path.name.lower()
    full = str(path).lower()
    if "work-vault" in n or "work_vault" in n or "/work_vaults/" in full or "work_vaults" in full: return "work_vault"
    if "mark-allocation" in n or "mark_allocation" in n: return "mark_allocation"
    if "sovereign" in n: return "sovereign"
    if "pilot" in n: return "customer_pilot"
    if "github-app" in n or "permission" in n: return "github_app"
    if "release" in n: return "release"
    if "trust" in n: return "trust_center"
    if "repo-security" in n or "baseline" in n: return "repo_security"
    return "generic_text"

def build_context(path: str, context_type: str = "auto"):
    p = Path(path)
    raw = p.read_text(encoding="utf-8")
    content = {}
    if p.suffix.lower() in {".json"}:
        try: content = json.loads(raw)
        except json.JSONDecodeError: content = {"raw": raw}
    text_fields = [raw]
    ctype = _guess_context_type(p) if context_type == "auto" else context_type
    return {
      "schema_version":"securerails.policy_context.v1",
      "context_id":str(uuid.uuid5(uuid.NAMESPACE_URL, str(p.resolve()))),
      "context_type":ctype,
      "source_path":str(p),
      "source_hash":hashlib.sha256(raw.encode()).hexdigest(),
      "repository":"MontrealAI/agialpha-first-real-loop",
      "content":content,
      "text_fields":text_fields,
      "metadata":{},
      "claim_boundary":"SecureRails is AI-agent security governance and proof-bound defensive remediation.",
    }
