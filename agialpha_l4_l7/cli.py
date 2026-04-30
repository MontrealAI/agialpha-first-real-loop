import argparse
from pathlib import Path
from .core import run_all, replay, falsify

def parse_ints(s): return [int(x.strip()) for x in s.split(',') if x.strip()]

def main(argv=None):
    p=argparse.ArgumentParser(prog='agialpha_l4_l7'); sub=p.add_subparsers(dest='cmd',required=True)
    r=sub.add_parser('run-all'); r.add_argument('--source-docket',default='evidence-docket'); r.add_argument('--out',default='runs/l4-l7/manual'); r.add_argument('--docs',default='docs/l4-l7'); r.add_argument('--agents',default='1,2,4,8,16'); r.add_argument('--nodes',default='1,2,4,8'); r.add_argument('--repo-root',default='.')
    rp=sub.add_parser('replay'); rp.add_argument('--bundle',required=True); rp.add_argument('--out',required=True)
    f=sub.add_parser('falsify'); f.add_argument('--bundle',required=True); f.add_argument('--out',required=True)
    a=p.parse_args(argv)
    if a.cmd=='run-all': print(run_all(Path(a.source_docket),Path(a.out),Path(a.docs),parse_ints(a.agents),parse_ints(a.nodes),Path(a.repo_root)))
    elif a.cmd=='replay': print(replay(Path(a.bundle),Path(a.out)))
    elif a.cmd=='falsify': print(falsify(Path(a.bundle),Path(a.out)))
if __name__=='__main__': main()
