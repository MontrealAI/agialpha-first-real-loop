import argparse
from .lifecycle import run_lifecycle
from .replay import replay_docket
from .falsification import audit

def main():
    p=argparse.ArgumentParser()
    sp=p.add_subparsers(dest='cmd',required=True)
    l=sp.add_parser('lifecycle'); l.add_argument('--repo-root',default='.'); l.add_argument('--cycles',type=int,default=3); l.add_argument('--candidate-niches',type=int,default=64); l.add_argument('--evaluate-niches',type=int,default=16); l.add_argument('--local-variants-per-niche',type=int,default=4); l.add_argument('--candidate-kernel-mutations',type=int,default=4); l.add_argument('--out',required=True)
    r=sp.add_parser('replay'); r.add_argument('--docket',required=True)
    f=sp.add_parser('falsification-audit'); f.add_argument('--docket',required=True)
    a=p.parse_args()
    if a.cmd=='lifecycle': run_lifecycle(a.repo_root,a.cycles,a.candidate_niches,a.evaluate_niches,a.local_variants_per_niche,a.out,candidate_kernel_mutations=a.candidate_kernel_mutations)
    elif a.cmd=='replay': replay_docket(a.docket)
    else: audit(a.docket)
