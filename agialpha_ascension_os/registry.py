import json
from pathlib import Path

def jwrite(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")

def jread(path,default):
    p=Path(path)
    return default if not p.exists() else json.loads(p.read_text())

def append(path,items):
    cur=jread(path,[])
    if not isinstance(cur,list): cur=[]
    cur.extend(items)
    jwrite(path,cur)
