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
        generate_replay(Path(args.run), Path(args.out))
    elif args.cmd == 'falsification-audit':
        generate_falsification(Path(args.run), Path(args.out))
    elif args.cmd == 'validate':
        run = Path(args.run); assert (run / '03_candidate_lock/candidate_lock.json').exists(); assert (run / '04_heldout_tasks/heldout_tasks.json').exists(); print('valid')
    elif args.cmd == 'build-data':
        reg = Path(args.registry); init_registry(reg); out = Path(args.out); out.mkdir(parents=True, exist_ok=True); [write_json(out / f, {"claim_boundary": CLAIM_BOUNDARY, "items": []}) for f in ['latest.json', 'runs.json', 'candidates.json', 'heldout_tasks.json', 'evaluations.json', 'summary.json']]
    elif args.cmd == 'emit-manifest':
        run = Path(args.run); write_json(Path(args.out), read_json(run / '00_manifest.json'))


if __name__ == '__main__':
    main()
