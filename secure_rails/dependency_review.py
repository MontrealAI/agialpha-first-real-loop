from pathlib import Path
import json

def dependency_review_record(out, available=False):
    rec={'status':'unavailable' if not available else 'available','claim_boundary':'Dependency review is advisory evidence and not certification.'}
    Path(out).write_text(json.dumps(rec,indent=2))
    return rec
