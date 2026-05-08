import json, zipfile, hashlib
from pathlib import Path
from .redaction_guard import find_secret_like

MAX_FILE_SIZE=1024*1024
MAX_FILES=200

def ingest_artifact(path: Path):
    result={"status":"available","files":[],"quarantine_reasons":[],"artifact_sha256":None}
    if path.is_file():
        result["artifact_sha256"]=hashlib.sha256(path.read_bytes()).hexdigest()
    if path.suffix.lower()=='.zip':
        with zipfile.ZipFile(path) as zf:
            if len(zf.infolist())>MAX_FILES: result["quarantine_reasons"].append("too_many_files")
            for info in zf.infolist():
                p=Path(info.filename)
                if p.is_absolute() or '..' in p.parts: result["quarantine_reasons"].append("zip_slip"); continue
                if info.file_size>MAX_FILE_SIZE: result["quarantine_reasons"].append("oversized_file"); continue
                if info.is_dir(): continue
                data=zf.read(info.filename)
                text=data.decode('utf-8',errors='ignore')
                secrets=find_secret_like(text)
                if secrets: result["quarantine_reasons"].append("secret_like_content")
                result["files"].append({"path":info.filename,"size":info.file_size,"secret_findings":len(secrets)})
    elif path.is_dir():
        for f in path.rglob('*'):
            if f.is_symlink() or f.is_dir(): continue
            if f.stat().st_size>MAX_FILE_SIZE: result["quarantine_reasons"].append("oversized_file"); continue
            if f.suffix.lower() not in {'.json','.md','.txt'}: result["quarantine_reasons"].append("unsupported_binary"); continue
            txt=f.read_text(encoding='utf-8',errors='ignore')
            secrets=find_secret_like(txt)
            if secrets: result["quarantine_reasons"].append("secret_like_content")
            result["files"].append({"path":str(f),"size":f.stat().st_size,"secret_findings":len(secrets)})
    if result["quarantine_reasons"]:
        result["status"]="quarantined"
    return result
