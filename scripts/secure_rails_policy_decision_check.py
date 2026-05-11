#!/usr/bin/env python3
import json, sys
p=sys.argv[1]
d=json.load(open(p))
req=['schema_version','decision','required_human_review','auto_merge_allowed']
missing=[k for k in req if k not in d]
if missing:
    print('missing',missing); raise SystemExit(1)
if d['required_human_review'] is not True or d['auto_merge_allowed'] is not False:
    raise SystemExit(1)
print('ok')
