#!/usr/bin/env python3
import json, sys
p=sys.argv[1]
d=json.load(open(p))
req=["decision","required_human_review","auto_merge_allowed","claim_boundary"]
missing=[k for k in req if k not in d]
if missing:
    print("missing:",missing); raise SystemExit(1)
if d.get("auto_merge_allowed") is not False: raise SystemExit(1)
if d.get("required_human_review") is not True: raise SystemExit(1)
print("decision valid")
