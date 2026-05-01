import argparse, json, pathlib
from .utils import read_json, write_json, now_iso
from .tasks import heldout_tasks
from .scoring import evaluate_source
from .kernel_factory import kernel_source

def vnext(docket):
    d = pathlib.Path(docket)
    lineage = read_json(d/"03_kernel_lineage"/"lineage.json", [])
    if not lineage: raise RuntimeError("lineage_missing")
    final = d/"03_kernel_lineage"/f"accepted_kernel_v{lineage[-1]['cycle']}.py"
    final_src = final.read_text(encoding="utf-8")
    b5_src = kernel_source(["claim_boundary_guard","replay_baseline_gate","security_safety_counters","artifact_publication_gate"], "B5_no_archive_vnext")
    tasks = heldout_tasks()
    b6 = evaluate_source(final_src, tasks)
    b5 = evaluate_source(b5_src, tasks)
    delta = round(b6["mean_quality"] - b5["mean_quality"], 4)
    report = {"experiment":"RSI-FORGE-001-vNEXT","generated_at":now_iso(),"status":"pass" if delta>0 else "fail","transfer_task_count":len(tasks),"B6_final_rsi_archive_reuse":b6,"B5_no_archive_reuse":b5,"vnext_transfer_delta":delta,"claim_boundary":"Local CI/proxy transfer only; not empirical SOTA or external validation."}
    write_json(d/"10_vnext_transfer"/"vnext_transfer_report.json", report)
    write_json(d/"vnext_transfer_report.json", report)
    return report

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--docket", default="runs/rsi-forge-001/latest")
    p.add_argument("--out", default=None)
    a=p.parse_args(argv)
    r=vnext(a.docket)
    if a.out: write_json(a.out, r)
    print(json.dumps(r, indent=2, sort_keys=True))
    raise SystemExit(0 if r["status"]=="pass" else 1)

if __name__=="__main__":
    main()
