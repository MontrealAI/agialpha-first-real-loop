#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from secure_rails.trust_center import validate
ok, errs = validate(Path(sys.argv[1] if len(sys.argv)>1 else '.'))
for e in errs: print(e)
raise SystemExit(0 if ok else 1)
