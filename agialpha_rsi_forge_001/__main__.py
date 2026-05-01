import argparse
from .run import main as run_main
from .replay import main as replay_main
from .audit import main as audit_main
from .vnext import main as vnext_main

def main():
    p=argparse.ArgumentParser(prog="python -m agialpha_rsi_forge_001")
    sub=p.add_subparsers(dest="cmd", required=True)
    pr=sub.add_parser("run"); pr.add_argument("--out", default="runs/rsi-forge-001/latest"); pr.add_argument("--cycles",type=int,default=6); pr.add_argument("--candidates-per-cycle",type=int,default=4); pr.add_argument("--seed",type=int,default=1001)
    pp=sub.add_parser("replay"); pp.add_argument("--docket", default="runs/rsi-forge-001/latest"); pp.add_argument("--out", default=None)
    pa=sub.add_parser("audit"); pa.add_argument("--docket", default="runs/rsi-forge-001/latest"); pa.add_argument("--out", default=None)
    pv=sub.add_parser("vnext"); pv.add_argument("--docket", default="runs/rsi-forge-001/latest"); pv.add_argument("--out", default=None)
    a=p.parse_args()
    if a.cmd=="run": run_main(["--out",a.out,"--cycles",str(a.cycles),"--candidates-per-cycle",str(a.candidates_per_cycle),"--seed",str(a.seed)])
    elif a.cmd=="replay":
        argv=["--docket",a.docket]; 
        if a.out: argv += ["--out",a.out]
        replay_main(argv)
    elif a.cmd=="audit":
        argv=["--docket",a.docket]; 
        if a.out: argv += ["--out",a.out]
        audit_main(argv)
    elif a.cmd=="vnext":
        argv=["--docket",a.docket]; 
        if a.out: argv += ["--out",a.out]
        vnext_main(argv)

if __name__=="__main__":
    main()
