#!/usr/bin/env python3
"""Fail if repository workflow/docs appear to enable automatic merge.
This is a deployment guardrail, not legal advice.
"""
import pathlib, sys, re
root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('.')
fail=[]
patterns=[
    re.compile(r'gh\s+pr\s+merge[^\n]*(--auto|--merge|--squash|--rebase)', re.I),
    re.compile(r'pull-request.*auto.?merge\s*[:=]\s*true', re.I),
    re.compile(r'automerge_enabled\s*[:=]\s*true', re.I),
    re.compile(r'auto.?merge\s*[:=]\s*true', re.I),
]
allowed_context=['open_safe_pr_if_passed=false','open_policy_pr_if_passed=false','automerge_enabled": false','automerge_disabled','no-auto-merge','no automerge','not auto-merge','must not auto-merge','never auto-merge','auto-merge disabled','automerge_allowed": false']
for p in root.rglob('*'):
    if not p.is_file() or p.suffix.lower() not in {'.yml','.yaml','.md','.json','.txt','.py'}:
        continue
    if any(part in {'.git','node_modules','dist','build','_site'} for part in p.parts):
        continue
    text=p.read_text(encoding='utf-8', errors='ignore')
    for pat in patterns:
        for m in pat.finditer(text):
            window=text[max(0,m.start()-160):m.end()+160].lower()
            if any(a in window for a in allowed_context):
                continue
            fail.append((str(p.relative_to(root)), m.group(0)))
if fail:
    print('SecureRails no-auto-merge check FAILED')
    for path, match in fail[:80]:
        print(f'- {path}: {match}')
    sys.exit(1)
print('SecureRails no-auto-merge check passed')
