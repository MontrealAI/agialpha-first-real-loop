import json
from pathlib import Path

def build_evidence(input_dir,out):
    src=Path(input_dir); outp=Path(out); outp.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((src/'00_manifest.json').read_text())
    (outp/'00_manifest.json').write_text(json.dumps(manifest,indent=2))
    (outp/'01_claims_matrix.json').write_text(json.dumps({'allowed_claim':'bounded advisory review only','forbidden_claim':'certification or autonomous claim promotion','claim_boundary':manifest['claim_boundary']},indent=2))
    (outp/'02_scope_and_claim_boundary.md').write_text(manifest['claim_boundary'])
