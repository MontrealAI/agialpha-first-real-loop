#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from secure_rails.incident_response import validate_incident
ok, errs = validate_incident(Path(sys.argv[1]))
for e in errs: print(e)
raise SystemExit(0 if ok else 1)
