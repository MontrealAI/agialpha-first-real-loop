#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from secure_rails.security_txt import validate_security_txt_template
ok, errs = validate_security_txt_template(Path(sys.argv[1]))
for e in errs: print(e)
raise SystemExit(0 if ok else 1)
