
from pathlib import Path
import hashlib, json


def detect_context_type(path: Path) -> str:
    n = path.name.lower()
    if 'work-vault' in n or 'work_vault' in n: return 'work_vault'
    if 'mark' in n: return 'mark_allocation'
    if 'sovereign' in n: return 'sovereign'
    if 'release' in n: return 'release'
    if 'trust' in n: return 'trust_center'
    if 'security' in n and 'baseline' in n: return 'repo_security'
    if 'github' in n and 'app' in n: return 'github_app'
    return 'generic_text'


def build_context(path: Path, context_type: str='auto') -> dict:
    b = path.read_bytes()
    text = b.decode('utf-8', errors='replace')
    content = {}
    if path.suffix.lower() in {'.json'}:
        try: content = json.loads(text)
        except Exception: content = {}
    source_hash = hashlib.sha256(b).hexdigest()
    ctype = detect_context_type(path) if context_type == 'auto' else context_type
    return {
        'schema_version':'securerails.policy_context.v1',
        'context_id': source_hash[:24],
        'context_type': ctype,
        'source_path': str(path),
        'source_hash': source_hash,
        'repository':'MontrealAI/agialpha-first-real-loop',
        'content':content,
        'text_fields':[text],
        'metadata':{},
        'claim_boundary':''
    }
