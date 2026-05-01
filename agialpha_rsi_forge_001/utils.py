import hashlib, json, pathlib, time, shutil

def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def ensure_dir(p):
    pathlib.Path(p).mkdir(parents=True, exist_ok=True)
    return pathlib.Path(p)

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def sha256_json(obj):
    return sha256_text(canonical(obj))

def read_json(path, default=None):
    p = pathlib.Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))

def write_json(path, obj):
    p = pathlib.Path(path)
    ensure_dir(p.parent)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False), encoding="utf-8")
    return str(p)

def write_text(path, text):
    p = pathlib.Path(path)
    ensure_dir(p.parent)
    p.write_text(text, encoding="utf-8")
    return str(p)

def hash_tree(root):
    root = pathlib.Path(root)
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.name != "hash_manifest.json":
            out[str(p.relative_to(root))] = sha256_text(p.read_text(encoding="utf-8", errors="replace"))
    return out
