from pathlib import Path
import argparse, json
from .core import build_evidence_docket


def main():
    parser = argparse.ArgumentParser(description="Run the AGI ALPHA First Real Loop.")
    parser.add_argument("--out", default="runs/coldchain-energy-loop-001", help="Output Evidence Docket directory")
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parents[1]
    docket = build_evidence_docket(project_root, Path(args.out))
    print(json.dumps({
        "docket_id": docket["docket_id"],
        "loop_passed": docket["loop_passed"],
        "docket_hash": docket["docket_hash"],
        "output": str(Path(args.out)),
    }, indent=2))

if __name__ == "__main__":
    main()
