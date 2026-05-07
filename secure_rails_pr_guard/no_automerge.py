import re

ENABLE_PATTERNS = [
    re.compile(r'enable-pull-request-automerge', re.I),
    re.compile(r'gh\s+pr\s+merge\s+.*--auto', re.I),
    re.compile(r'auto_merge\s*:\s*true', re.I),
    re.compile(r'automerge\s*:\s*true', re.I),
]


def review_no_automerge(texts):
    hits = []
    for p, t in texts.items():
        for idx, line in enumerate(t.splitlines(), 1):
            for pattern in ENABLE_PATTERNS:
                if pattern.search(line):
                    hits.append({'file': p, 'line': idx, 'issue': 'auto-merge enablement pattern'})
                    break
    return {'findings': hits, 'auto_merge_allowed': False, 'claim_boundary': 'SecureRails is AI-agent security governance and proof-bound defensive remediation.'}
