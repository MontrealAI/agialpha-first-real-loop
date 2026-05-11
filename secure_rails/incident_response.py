from pathlib import Path
import json
REQUIRED=['incident_id','detected_at','severity','affected_scope','safety_counters','evidence','containment','human_reviewer','status','claim_boundary','lessons_learned','archive_update']
COUNTERS=['raw_secret_leak_count','external_target_scan_count','exploit_execution_count','malware_generation_count','social_engineering_content_count','unsafe_automerge_count','critical_safety_incidents']

def validate_incident(path: Path)->tuple[bool,list[str]]:
    d=json.loads(path.read_text(encoding='utf-8'))
    errs=[f'missing {k}' for k in REQUIRED if k not in d]
    sc=d.get('safety_counters',{})
    errs += [f'missing safety counter {k}' for k in COUNTERS if k not in sc]
    return (not errs, errs)
