
from pathlib import Path
import json
from .policy_rules import *
from .policy_decision import PolicyDecision


def load_kernel(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))

def validate_kernel(cfg: dict):
    errs=[]
    if cfg.get('human_review_required') is not True: errs.append('human_review_required must be true')
    if cfg.get('autonomous_promotion_allowed') is not False: errs.append('autonomous_promotion_allowed must be false')
    if cfg.get('auto_merge_allowed') is not False: errs.append('auto_merge_allowed must be false')
    if not cfg.get('claim_boundary'): errs.append('claim_boundary missing')
    if cfg.get('default_decision') == 'allow': errs.append('default_decision cannot be allow')
    return errs

def _contains(text, phrase):
    return phrase in text.lower()

def evaluate_context(ctx: dict, kernel: dict) -> dict:
    txt = '\n'.join(ctx.get('text_fields', [])) + '\n' + json.dumps(ctx.get('content', {})).lower()
    d = PolicyDecision(context_id=ctx['context_id'], context_type=ctx['context_type'], source_path=ctx['source_path'])
    for p in FORBIDDEN_CLAIMS:
        if _contains(txt,p) and not any(_contains(txt,n) and p in n for n in NEGATED_ALLOW):
            d.violations.append(f'claim_boundary:{p}')
    for p in FORBIDDEN_SAFETY:
        if _contains(txt,p): d.violations.append(f'safety_boundary:{p}')
    for p in FORBIDDEN_EU:
        if _contains(txt,p): d.violations.append(f'eu_ai_act_boundary:{p}')
    for p in FORBIDDEN_TOKEN:
        if _contains(txt,p): d.violations.append(f'token_utility_boundary:{p}')
    content = ctx.get('content', {}) if isinstance(ctx.get('content'), dict) else {}
    if content.get('human_review_required') is False or content.get('auto_merge_allowed') is True:
        d.violations.append('hard_boundary:human_review_or_automerge')
    if d.violations:
        d.decision='reject'; d.severity='high'
    else:
        d.decision='allow'; d.severity='info'
    return d.finalize().to_dict()
