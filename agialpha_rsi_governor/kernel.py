import hashlib, json
from pathlib import Path
load_kernel = lambda p: json.loads(Path(p).read_text())
kernel_hash = lambda k: hashlib.sha256(json.dumps(k, sort_keys=True).encode()).hexdigest()
