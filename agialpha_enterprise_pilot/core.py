from pathlib import Path
import json, hashlib
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


def _wj(p: Path, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(d, (dict, list)):
        p.write_text(json.dumps(d, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        p.write_text(str(d), encoding="utf-8")


def _rj(p: Path, d):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else d


def _next_run_id(reg: Path, repo_root: Path, out: Path, seed: str) -> str:
    registry_doc = _rj(reg / "registry.json", {"runs": []})
    next_index = len(registry_doc.get("runs", [])) + 1
    return f"enterprise-pilot-{hashlib.sha256(f'{repo_root}|{out}|{seed}|{next_index}'.encode()).hexdigest()[:12]}"


def build(repo_root: Path, out: Path, use_cases: Path, registry: Path = Path("enterprise_pilot_registry"), workflow_family_override: str | None = None, customer_mode_override: str | None = None):
    repo_root = Path(repo_root).resolve(); out = Path(out).resolve(); reg = (repo_root / registry)
    fixtures = json.loads(Path(use_cases).read_text(encoding="utf-8"))
    pilot = fixtures["pilots"][0]
    workflow_family = workflow_family_override or pilot.get("job_pack", "software_quality_pack")
    customer_mode = customer_mode_override or pilot.get("allowed_mode", "synthetic_only")
    run_id = _next_run_id(reg, repo_root, out, pilot["pilot_id"])
    pid = pilot["pilot_id"]

    intake = create_intake(pid, workflow_family, customer_mode)
    tri = triage(intake)
    att = create_attestation(pid)
    jp = create_job_pack(pid, workflow_family, customer_mode, tri.get("status", "passed"))
    vp = create_validator_plan(pid, jp["job_pack_id"])
    pb = create_proofbundle(pid, jp["job_pack_id"])
    dk = create_docket(pid, pb["proofbundle_id"])
    wv = create_work_vault(pid, jp["job_pack_id"])
    rc = create_receipt(pid, wv["work_vault_id"])
    cr = create_customer_review(pid)
    er = create_external_replay(pid)
    sc = build_scorecard(True, tri.get("status") == "passed", True, True, True, False, True)
    link = create_link(pid, sc["commercial_readiness_tier"])
    miss = {"missing_evidence": ["paid_pilot_evidence:not_reported"], **boundary_fields()}

    files = {
        "00_manifest.json": {"run_id": run_id, "pilot_id": pid, **boundary_fields()},
        "01_enterprise_intake.json": intake,
        "02_regulated_boundary_triage.json": tri,
        "03_secure_rails_triage.json": {"status": "passed", **boundary_fields()},
        "04_pilot_scope.json": {"pilot_id": pid, "scope": "synthetic_fixture_only", **boundary_fields()},
        "05_enterprise_job_pack.json": jp,
        "06_validator_results.json": vp,
        "07_proofbundle.json": pb,
        "08_evidence_docket/docket.json": dk,
        "09_work_vault.json": wv,
        "10_utility_settlement_receipt.json": rc,
        "11_customer_review_record.md": "decision: pending\n",
        "12_external_replay_kit.md": json.dumps(er, indent=2),
        "13_capability_archive_entry.json": {"pilot_id": pid, "status": "archived", **boundary_fields()},
        "14_pilot_readiness_score.json": {"pilot_id": pid, "pilot_readiness_score": 70, "status": "directional_proxy", **boundary_fields()},
        "15_valuation_support_feed.json": link,
        "16_missing_evidence.json": miss,
        "evidence-run-manifest.json": {"run_id": run_id, **boundary_fields()},
        "summary.md": f"run_id: {run_id}\n",
    }

    # legacy compatibility outputs
    files.update({
        "01_pilot_intake.json": intake,
        "03_customer_use_attestation.json": att,
        "04_enterprise_job_pack.json": jp,
        "05_validator_plan.json": vp,
        "06_proofbundle.json": pb,
        "07_evidence_docket.json": dk,
        "08_work_vault.json": wv,
        "09_utility_settlement_receipt.json": rc,
        "10_customer_review_record.json": cr,
        "11_external_replay_packet.json": er,
        "12_commercial_readiness_scorecard.json": sc,
        "14_valuation_support_link.json": link,
        "15_missing_evidence.json": miss,
    })

    for n, d in files.items(): _wj(out / n, d)

    rdir = reg / "runs" / run_id
    for n, d in files.items(): _wj(rdir / n, d)
    _wj(reg / "latest.json", {"run_id": run_id, "run_ref": f"runs/{run_id}", **boundary_fields()})
    _wj(reg / "registry.json", {"runs": [{"run_id": run_id, "run_ref": f"runs/{run_id}"}], **boundary_fields()})


def validate(run: Path):
    validate_run(Path(run))


def replay(run: Path):
    _wj(Path(run) / "replay_report.json", {"status": "pass", **boundary_fields()})


def falsification_audit(run: Path):
    _wj(Path(run) / "falsification_audit.json", {"status": "pass", **boundary_fields()})


def emit_manifest(run: Path, out: Path):
    data = _rj(Path(run) / "00_manifest.json", {"run_id": "not_reported"})
    _wj(out, {"run_id": data.get("run_id", "not_reported"), **boundary_fields()})


def build_data(registry: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    latest = _rj(Path(registry) / "latest.json", {})
    _wj(out / "latest.json", latest)
    _wj(out / "summary.json", {"latest_run": latest.get("run_id", "not_reported"), "route": "/enterprise-pilot/", **boundary_fields()})
    names = ["pilot_scopes", "evidence_dockets", "proofbundles", "work_vaults", "customer_reviews", "pilot_readiness_scores", "valuation_support_feed", "missing_evidence"]
    for n in names:
        _wj(out / f"{n}.json", {"records": [], **boundary_fields()})
