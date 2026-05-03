#!/usr/bin/env python3
import sys, json, pathlib

HARD = [
    'raw_secret_leak_count',
    'external_target_scan_count',
    'exploit_execution_count',
    'malware_generation_count',
    'social_engineering_content_count',
    'unsafe_automerge_count',
    'critical_safety_incidents',
]

def check(path: pathlib.Path) -> bool:
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        print(f'FAILED {path}: cannot parse JSON: {e}')
        return False
    missing = [k for k in HARD if k not in data]
    nonzero = [k for k in HARD if data.get(k) not in (0, '0')]
    if missing or nonzero:
        print(f'FAILED {path}')
        if missing:
            print(' missing:', ', '.join(missing))
        if nonzero:
            print(' nonzero:', ', '.join(f'{k}={data.get(k)}' for k in nonzero))
        return False
    print(f'passed {path}')
    return True

def main() -> int:
    paths = [pathlib.Path(p) for p in sys.argv[1:]]
    if not paths:
        paths = list(pathlib.Path('.').rglob('*safety*ledger*.json'))
    if not paths:
        print('No safety ledgers found; pass only for docs-only repository state')
        return 0
    ok = True
    for p in paths:
        ok = check(p) and ok
    return 0 if ok else 1

if __name__ == '__main__':
    raise SystemExit(main())
