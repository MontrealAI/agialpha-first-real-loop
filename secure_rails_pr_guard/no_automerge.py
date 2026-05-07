def review_no_automerge(texts):
    hits=[]
    for p,t in texts.items():
        l=t.lower()
        if 'automerge' in l or 'auto-merge' in l or 'enable-pull-request-automerge' in l:
            hits.append({'file':p,'issue':'auto-merge-like string'})
    return {'findings':hits,'auto_merge_allowed':False,'claim_boundary':'SecureRails is AI-agent security governance and proof-bound defensive remediation.'}
