import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pathlib import Path
import sys
from secure_rails.review_decision import load_and_validate_decision
errs=load_and_validate_decision(Path(sys.argv[1]))
print("ok" if not errs else "\n".join(errs))
raise SystemExit(0 if not errs else 1)
