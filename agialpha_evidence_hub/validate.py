import re
SECURITY = ['safety_incidents','policy_violations','raw_secret_leak_count','external_target_scan_count','exploit_execution_count','malware_generation_count','unsafe_automerge_count']
UNSAFE=[r'achieved agi',r'achieved asi',r'empirical sota',r'safe autonomy',r'real-world security certification',r'guaranteed economic return',r'civilization-scale capability']

def validate_manifest(m):
    for k in ['schema_version','experiment_slug','claim_boundary','run_id','status']:
        if not m.get(k): raise ValueError(f'missing {k}')
    text=(m.get('claim_boundary','')+' '+m.get('experiment_name','')).lower()
    for pat in UNSAFE:
        if re.search(pat,text) and 'does not claim' not in text:
            raise ValueError('unsafe claim detected')
    if any(x in m.get('experiment_slug','') for x in ['cyber','gauntlet','omega']):
        metrics=m.get('metrics',{})
        for k in SECURITY:
            if k not in metrics: raise ValueError(f'missing security counter {k}')
