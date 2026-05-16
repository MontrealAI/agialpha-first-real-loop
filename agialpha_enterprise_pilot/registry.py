from pathlib import Path
import json
def wj(p,d): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
