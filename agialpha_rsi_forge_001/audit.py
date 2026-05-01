import argparse, json, pathlib
from .utils import read_json, write_json, now_iso

def audit(docket):
    d = pathlib.Path(docket)
    summary = read_json(d/"15_summary_tables"/"summary.json", {})
    lineage = read_json(d/"03_kernel_lineage"/"lineage.json", [])
    errors, warnings = [], []
    boundary = (summary.get("claim_boundary") or "").lower()
    if "does not claim" not in boundary: errors.append("claim_boundary_missing")
    if len({r.get("source_hash") for r in lineage}) != len(lineage): errors.append("source_did_not_change_each_cycle")
    if summary.get("move37_dossier_count",0) < 1: warnings.append("no_move37_dossier")
    # Falsification probes: the audit explicitly catches reset, shrinkage, and ECI inflation.
    probes = {"cycle_reset_caught": False, "archive_shrinkage_caught": False, "eci_inflation_caught": False}
    if lineage:
        st = read_json(d/"02_rsi_state_chain"/f"state_cycle_{lineage[-1]['cycle']:02d}.json", {})
        if st:
            probes["cycle_reset_caught"] = st.get("cycle_index") != 0
            probes["archive_shrinkage_caught"] = len(st.get("archive",{}).get("accepted_kernels",[])) >= len(lineage)
            probes["eci_inflation_caught"] = all(e.get("eci_level") != "E5_EXTERNALLY_VALIDATED" for e in st.get("eci_ledger", []))
    if not all(probes.values()): errors.append("falsification_probe_failure")
    report = {"experiment":"RSI-FORGE-001","generated_at":now_iso(),"status":"pass" if not errors else "fail","errors":errors,"warnings":warnings,"falsification_probes":probes}
    write_json(d/"13_falsification_audit"/"falsification_audit.json", report)
    write_json(d/"falsification_audit.json", report)
    return report

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--docket", default="runs/rsi-forge-001/latest")
    p.add_argument("--out", default=None)
    a=p.parse_args(argv)
    r=audit(a.docket)
    if a.out: write_json(a.out, r)
    print(json.dumps(r, indent=2, sort_keys=True))
    raise SystemExit(0 if r["status"]=="pass" else 1)

if __name__=="__main__":
    main()
