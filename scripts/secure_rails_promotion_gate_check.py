import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pathlib import Path
import json,sys
from secure_rails.human_review import validate_promotion_gate
errs=validate_promotion_gate(json.loads(Path(sys.argv[1]).read_text()))
print("ok" if not errs else "\n".join(errs))
raise SystemExit(0 if not errs else 1)
