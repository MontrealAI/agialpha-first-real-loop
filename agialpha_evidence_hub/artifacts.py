from pathlib import Path

def list_artifact_files(root: str):
    p = Path(root)
    if not p.exists():
        return []
    return [str(x) for x in p.rglob('*') if x.is_file()]
