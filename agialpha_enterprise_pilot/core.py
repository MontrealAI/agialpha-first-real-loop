from pathlib import Path
import json, hashlib, shutil
from .intake import create_intake
from .regulated_boundary import triage
from .customer_attestation import create_attestation
from .job_packs import create_job_pack
from .validators import create_validator_plan
from .proofbundle import create_proofbundle
from .docket import create_docket
from .work_vault import create_work_vault
from .settlement_receipt import create_receipt
from .customer_review import create_customer_review
from .external_replay import create_external_replay
from .commercial_readiness import build_scorecard
from .pilot_outcomes import render_outcome_md
from .valuation_support_link import create_link
from .validate import validate_run
from .boundaries import boundary_fields

def _wj(p: Path, d: dict):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def _rj(p: Path, d: dict):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else d

def build(repo_root: Path, out: Path, workflow_family: str, customer_mode: str, registry: Path = Path("enterprise_pilot_registry")):
    run_id = hashlib.sha256(str(Path(out).resolve()).encode()).hexdigest()[:12]
    pid = f"pilot-{run_id}"
    intake = create_intake(pid, workflow_family, customer_mode)
    tri = triage(intake)
    att = create_attestation(pid)
    jp = create_job_pack(pid, workflow_family, customer_mode)
    vp = create_validator_plan(pid, jp["job_pack_id"])
    pb = create_proofbundle(pid, jp["job_pack_id"])
    dk = create_docket(pid, pb["proofbundle_id"])
    wv = create_work_vault(pid, jp["job_pack_id"])
    rc = create_receipt(pid, wv["work_vault_id"])
    cr = create_customer_review(pid)
    er = create_external_replay(pid)
    sc = build_scorecard()
    link = create_link(pid, sc["commercial_readiness_tier"])
    miss = {"missing_evidence": link["missing_evidence"], **boundary_fields()}

    out.mkdir(parents=True, exist_ok=True)
    _wj(out / "00_manifest.json", {"run_id": run_id, "pilot_id": pid, **boundary_fields()})
    mapping = [
        ("01_pilot_intake.json", intake), ("02_regulated_boundary_triage.json", tri), ("03_customer_use_attestation.json", att),
        ("04_enterprise_job_pack.json", jp), ("05_validator_plan.json", vp), ("06_proofbundle.json", pb),
        ("07_evidence_docket.json", dk), ("08_work_vault.json", wv), ("09_utility_settlement_receipt.json", rc),
        ("10_customer_review_record.json", cr), ("11_external_replay_packet.json", er), ("12_commercial_readiness_scorecard.json", sc),
        ("14_valuation_support_link.json", link), ("15_missing_evidence.json", miss),
    ]
    for n, d in mapping:
        _wj(out / n, d)
    (out / "13_pilot_outcome_dossier.md").write_text(render_outcome_md(pid, sc["commercial_readiness_tier"]), encoding="utf-8")
    (out / "summary.md").write_text(f"run_id: {run_id}\n", encoding="utf-8")
    _wj(out / "evidence-run-manifest.json", {"run_id": run_id, **boundary_fields()})

    reg = Path(registry)
    rdir = reg / "runs" / run_id
    rdir.mkdir(parents=True, exist_ok=True)
    for f in out.iterdir():
        if f.is_file():
            shutil.copy2(f, rdir / f.name)
    _wj(reg / "latest.json", {"run_id": run_id, "run_ref": f"runs/{run_id}", **boundary_fields()})
    _wj(reg / "registry.json", {"runs": [{"run_id": run_id}], **boundary_fields()})
    for k, n in [("pilots", "01_pilot_intake.json"), ("pilot_intakes", "01_pilot_intake.json"), ("regulated_boundary_triage", "02_regulated_boundary_triage.json"), ("customer_attestations", "03_customer_use_attestation.json"), ("job_packs", "04_enterprise_job_pack.json"), ("proofbundles", "06_proofbundle.json"), ("evidence_dockets", "07_evidence_docket.json"), ("work_vaults", "08_work_vault.json"), ("settlement_receipts", "09_utility_settlement_receipt.json"), ("customer_reviews", "10_customer_review_record.json"), ("external_replay_packets", "11_external_replay_packet.json"), ("commercial_readiness_scorecards", "12_commercial_readiness_scorecard.json"), ("valuation_support_links", "14_valuation_support_link.json"), ("missing_evidence", "15_missing_evidence.json")]:
        _wj(reg / f"{k}.json", _rj(out / n, {}))
    _wj(reg / "pilot_outcomes.json", {"path": str(out / "13_pilot_outcome_dossier.md"), **boundary_fields()})
    (reg / "CHANGELOG.md").write_text("- append-only registry\n", encoding="utf-8")

def validate(run: Path):
    validate_run(Path(run))

def build_data(registry: Path, out: Path):
    registry = Path(registry)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    latest = _rj(registry / "latest.json", {})
    _wj(out / "latest.json", latest)
    for n in ["summary", "pilots", "commercial_readiness_scorecards", "customer_reviews", "external_replay_packets", "valuation_support_links", "missing_evidence"]:
        _wj(out / f"{n}.json", _rj(registry / f"{n}.json", {"not_reported": True, **boundary_fields()}))
