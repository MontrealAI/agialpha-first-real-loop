import json
from pathlib import Path
from .policy import CLAIM_BOUNDARY

def write_docket(base, payload):
    d = Path(base) / "agiga-foundry-evidence-docket"
    d.mkdir(parents=True, exist_ok=True)
    for sub in ["03_policy","04_opportunity_intermediates","05_generated_niches","06_validated_niches","07_rejected_niches","08_baselines","09_solution_attempts","10_validators","11_local_evolution_variants","12_proof_bundles","13_replay_logs","14_falsification_audit","15_cost_ledgers","16_safety_ledgers","17_qd_archive","18_lineage_graph","19_capability_archive","20_sovereign_opportunity_dossiers","21_vnext_descendant_tasks","22_summary_tables"]:
        (d / sub).mkdir(parents=True, exist_ok=True)
    (d / "02_scope_and_claim_boundary.md").write_text(CLAIM_BOUNDARY)
    for name, obj in payload.items():
        p = d / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(obj, indent=2))
    (d / "REPLAY_INSTRUCTIONS.md").write_text("python -m agialpha_agiga_foundry replay --docket <path>\n" + CLAIM_BOUNDARY)
    return d
