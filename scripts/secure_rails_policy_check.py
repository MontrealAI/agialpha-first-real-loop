#!/usr/bin/env python3
import subprocess, sys
root = sys.argv[1] if len(sys.argv)>1 else "."
cmd=[sys.executable,"-m","secure_rails","policy","evaluate-repo","--repo-root",root,"--out","/tmp/securerails-policy-decisions"]
raise SystemExit(subprocess.call(cmd))
