
from __future__ import annotations
import argparse
from pathlib import Path
from .lifecycle import run_lifecycle
from .replay import run_replay
from .falsification import run_falsification

def main():
    p=argparse.ArgumentParser(prog='agialpha_cyber_ga_sovereign')
    sp=p.add_subparsers(dest='cmd', required=True)
    l=sp.add_parser('lifecycle'); l.add_argument('--repo-root',default='.'); l.add_argument('--cycles',type=int,default=3); l.add_argument('--candidate-niches',type=int,default=64); l.add_argument('--evaluate-niches',type=int,default=24); l.add_argument('--local-variants-per-niche',type=int,default=5); l.add_argument('--out',default='cyber-ga-sovereign-runs/test')
    r=sp.add_parser('replay'); r.add_argument('--docket', required=True)
    f=sp.add_parser('falsification-audit'); f.add_argument('--docket', required=True)
    a=p.parse_args()
    if a.cmd=='lifecycle': run_lifecycle(Path(a.repo_root),a.cycles,a.candidate_niches,a.evaluate_niches,a.local_variants_per_niche,Path(a.out))
    elif a.cmd=='replay': run_replay(Path(a.docket))
    else: run_falsification(Path(a.docket))
if __name__=='__main__': main()
