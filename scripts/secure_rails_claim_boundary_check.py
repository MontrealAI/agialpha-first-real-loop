#!/usr/bin/env python3
"""SecureRails claim-boundary check.

CI guardrail for public-facing overclaims. It intentionally allows forbidden phrases
when they appear inside explicit negative, forbidden, policy-list, or replacement
language. This is a guardrail, not legal advice or complete compliance review.
"""
import sys, pathlib, re

ROOT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('.')
TEXT_EXTS = {'.md','.html','.txt','.yml','.yaml','.json','.py','.js','.ts','.tsx','.jsx'}
FORBIDDEN = [
    'achieved AGI','achieved ASI','empirical SOTA','safe autonomy','certified secure',
    'security certification','cybersecurity certification','guaranteed security','guaranteed compliance',
    'guaranteed economic return','guaranteed investment return','official benchmark victory',
    'offensive cyber capability','autonomous production remediation','guaranteed appreciation',
    'profit rights','dividend','passive income','investment product','token yield'
]
SAFE_HINTS = [
    'does not claim','do not claim','does not certify','not claim','not a','not an','not ', 'no ', 'without ',
    'must not','never claim','never','forbidden','prohibited','banned','unsafe phrase','use instead',
    'replacement language','forbidden positive claim','forbidden_positive_claim','forbidden claim','forbidden_claim',
    'avoid','avoids','not marketed as','do not describe','not describe','is not','are not','claim boundary',
    'mandatory boundary','not legal advice','record security certifications if any','if any','review required',
    'not an investment','not investment','non investment','not offensive','not autonomous','not certification',
    'not cybersecurity certification','not security certification','not empirical sota','not achieved agi',
    'securerails is not','does not make','does not provide','does not perform','does not promote',
    'not supported','out of scope','exclusion','exclusions','excluded','forbidden economic framing',
    'forbidden token framing','not be marketed','do not market','must never','should not',
    'not achieved asi','not safe autonomy','no evidence docket','utility-only','utility only','must include',
    'do not use','forbidden token framing','claims to never make','red-zone','blocked_or_escalate'
]
SKIP_DIRS = {'.git','node_modules','.venv','venv','__pycache__','dist','build','_site'}
SKIP_FILES = {
    'scripts/secure_rails_claim_boundary_check.py',
    'config/securerails_claim_boundary_policy.json',
    'config/securerails_token_utility_policy.json',
    'policies/securerails_claim_boundaries.json',
    'policies/securerails_token_utility_boundary.json'
}

def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r'[*_`#>\[\]{}()"\']+', ' ', s)
    s = re.sub(r'[^a-z0-9$]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def safe_context(raw: str) -> bool:
    n = norm(raw)
    return any(h in n for h in SAFE_HINTS)

failures=[]
for p in ROOT.rglob('*'):
    rel = str(p.relative_to(ROOT)) if p.is_file() else ''
    if any(part in SKIP_DIRS for part in p.parts):
        continue
    if rel in SKIP_FILES:
        continue
    if not p.is_file() or p.suffix.lower() not in TEXT_EXTS:
        continue
    try:
        text=p.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    lines=text.splitlines()
    normalized_lines=[norm(x) for x in lines]
    for term in FORBIDDEN:
        term_low=norm(term)
        for i, line in enumerate(normalized_lines):
            if term_low not in line:
                continue
            raw_window='\n'.join(lines[max(0, i-10):min(len(lines), i+11)])
            # Allow explicit negative/policy contexts, but fail standalone positive claims.
            if safe_context(raw_window):
                continue
            failures.append((rel, term, norm(raw_window)))

if failures:
    print('SecureRails claim-boundary check FAILED')
    for path, term, window in failures[:120]:
        print(f'- {path}: unsafe positive claim {term!r} near: {window}')
    sys.exit(1)
print('SecureRails claim-boundary check passed')
