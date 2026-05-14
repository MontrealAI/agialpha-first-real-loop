import argparse
from pathlib import Path
from .context import *
from .candidate_mechanisms import generate_candidates
from .lock import lock_candidates
from .heldout_generator import generate_heldout
from .evaluator import evaluate
from .replay import generate_replay
from .falsification import generate_falsification
from .promotion import generate_promotion
from .render import render_scoreboard
from .registry import init_registry


def _manifest(run):
    return {"schema_version": "agialpha.recursive_gauntlet.run.v1", "run_id": run.name, "generated_at": now_iso(), "repository": "MontrealAI/agialpha-first-real-loop", "commit_sha": "unknown", "status": "pending", "candidate_mechanisms_generated": 0, "candidate_mechanisms_locked": 0, "heldout_tasks_generated_after_lock": 0, "candidate_beats_incumbent": "not_reported", "candidate_advantage_delta": "not_reported", "replay_pass": "not_reported", "falsification_pass": "not_reported", "promotion_status": "not_started", "hard_safety_counters": {"raw_secret_leak_count": 0, "external_target_scan_count": 0, "exploit_execution_count": 0, "malware_generation_count": 0, "social_engineering_content_count": 0, "unsafe_automerge_count": 0, "critical_safety_incidents": 0}, "claim_boundary": CLAIM_BOUNDARY}




def _ingest_runs_into_registry(reg: Path):
    runs_root = Path("recursive-gauntlet-runs")
    runs = read_json(reg / "runs.json") if (reg / "runs.json").exists() else {"claim_boundary": CLAIM_BOUNDARY, "items": []}
    candidates = read_json(reg / "candidates.json") if (reg / "candidates.json").exists() else {"claim_boundary": CLAIM_BOUNDARY, "items": []}
    evaluations = read_json(reg / "evaluations.json") if (reg / "evaluations.json").exists() else {"claim_boundary": CLAIM_BOUNDARY, "items": []}
    heldout = read_json(reg / "heldout_tasks.json") if (reg / "heldout_tasks.json").exists() else {"claim_boundary": CLAIM_BOUNDARY, "items": []}

    seen_runs = {x.get("run_id") for x in runs.get("items", []) if isinstance(x, dict)}
    if runs_root.exists():
        for run_dir in sorted(p for p in runs_root.iterdir() if p.is_dir()):
            manifest = run_dir / "00_manifest.json"
            if not manifest.exists():
                continue
            m = read_json(manifest)
            run_id = m.get("run_id", run_dir.name)
            if run_id not in seen_runs:
                runs.setdefault("items", []).append(m)
                seen_runs.add(run_id)
            for cp in sorted((run_dir / "02_candidates").glob("candidate-*/candidate.json")):
                candidates.setdefault("items", []).append(read_json(cp))
            ev = run_dir / "05_evaluations/candidate_vs_incumbent.json"
            if ev.exists():
                evaluations.setdefault("items", []).append(read_json(ev))
            ht = run_dir / "04_heldout_tasks/heldout_tasks.json"
            if ht.exists():
                heldout.setdefault("items", []).extend(read_json(ht).get("tasks", []))

    write_json(reg / "runs.json", runs)
    write_json(reg / "candidates.json", candidates)
    write_json(reg / "evaluations.json", evaluations)
    write_json(reg / "heldout_tasks.json", heldout)
    latest = runs.get("items", [])[-1] if runs.get("items") else {"claim_boundary": CLAIM_BOUNDARY, "items": []}
    write_json(reg / "latest.json", latest if isinstance(latest, dict) else {"claim_boundary": CLAIM_BOUNDARY, "items": []})

def _build_data(reg: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    mapping = {
        "latest.json": "latest.json",
        "runs.json": "runs.json",
        "candidates.json": "candidates.json",
        "heldout_tasks.json": "heldout_tasks.json",
        "evaluations.json": "evaluations.json",
    }
    for out_name, reg_name in mapping.items():
        src = reg / reg_name
        if src.exists():
            write_json(out / out_name, read_json(src))
        else:
            write_json(out / out_name, {"claim_boundary": CLAIM_BOUNDARY, "items": []})
    summary = {
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at": now_iso(),
        "run_count": len(read_json(out / "runs.json").get("items", [])),
        "candidate_count": len(read_json(out / "candidates.json").get("items", [])),
        "heldout_task_count": len(read_json(out / "heldout_tasks.json").get("items", [])),
        "evaluation_count": len(read_json(out / "evaluations.json").get("items", [])),
    }
    write_json(out / "summary.json", summary)


def main():
    p = argparse.ArgumentParser(); sp = p.add_subparsers(dest='cmd', required=True)
    a = sp.add_parser('generate-candidates'); a.add_argument('--repo-root'); a.add_argument('--out', required=True); a.add_argument('--candidate-count', type=int, default=6)
    b = sp.add_parser('lock-candidates'); b.add_argument('--run', required=True)
    c = sp.add_parser('generate-heldout'); c.add_argument('--run', required=True); c.add_argument('--task-count', type=int, default=16)
    d = sp.add_parser('evaluate'); d.add_argument('--repo-root', required=True); d.add_argument('--run', required=True)
    e = sp.add_parser('replay'); e.add_argument('--run', required=True); e.add_argument('--out', required=True)
    f = sp.add_parser('falsification-audit'); f.add_argument('--run', required=True); f.add_argument('--out', required=True)
    g = sp.add_parser('validate'); g.add_argument('--run', required=True)
    h = sp.add_parser('build-data'); h.add_argument('--registry', required=True); h.add_argument('--out', required=True)
    i = sp.add_parser('emit-manifest'); i.add_argument('--run', required=True); i.add_argument('--out', required=True)
    args = p.parse_args()
    if args.cmd == 'generate-candidates':
        run = Path(args.out); run.mkdir(parents=True, exist_ok=True); m = _manifest(run); cands = generate_candidates(run, args.candidate_count); m['candidate_mechanisms_generated'] = len(cands); write_json(run / '00_manifest.json', m)
    elif args.cmd == 'lock-candidates':
        run = Path(args.run); l = lock_candidates(run); m = read_json(run / '00_manifest.json'); m['candidate_mechanisms_locked'] = len(l['candidates']); write_json(run / '00_manifest.json', m)
    elif args.cmd == 'generate-heldout':
        run = Path(args.run); t = generate_heldout(run, args.task_count); m = read_json(run / '00_manifest.json'); m['heldout_tasks_generated_after_lock'] = len(t); write_json(run / '00_manifest.json', m)
    elif args.cmd == 'evaluate':
        run = Path(args.run); inc, cr, best, delta = evaluate(run, Path(args.repo_root))
        beats = delta > 0 if isinstance(delta, (int, float)) else "not_reported"
        status = generate_promotion(run, beats is True)
        m = read_json(run / '00_manifest.json'); m['status'] = 'success'; m['candidate_beats_incumbent'] = beats; m['candidate_advantage_delta'] = delta; m['promotion_status'] = status; write_json(run / '00_manifest.json', m); render_scoreboard(run, m)
    elif args.cmd == 'replay':
        run = Path(args.run); report = generate_replay(run, Path(args.out))
        manifest = run / '00_manifest.json'
        if manifest.exists():
            m = read_json(manifest); m['replay_pass'] = report.get('replay_pass', 'not_reported'); write_json(manifest, m)
        if not report.get('replay_pass', False):
            raise SystemExit(1)
    elif args.cmd == 'falsification-audit':
        run = Path(args.run); report = generate_falsification(run, Path(args.out))
        manifest = run / '00_manifest.json'
        if manifest.exists():
            m = read_json(manifest); m['falsification_pass'] = report.get('falsification_pass', 'not_reported'); write_json(manifest, m)
        if not report.get('falsification_pass', False):
            raise SystemExit(1)
    elif args.cmd == 'validate':
        run = Path(args.run); assert (run / '03_candidate_lock/candidate_lock.json').exists(); assert (run / '04_heldout_tasks/heldout_tasks.json').exists(); print('valid')
    elif args.cmd == 'build-data':
        reg = Path(args.registry)
        if not reg.exists():
            init_registry(reg)
        _ingest_runs_into_registry(reg)
        _build_data(reg, Path(args.out))
    elif args.cmd == 'emit-manifest':
        run = Path(args.run); write_json(Path(args.out), read_json(run / '00_manifest.json'))


if __name__ == '__main__':
    main()
