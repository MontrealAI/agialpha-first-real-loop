from pathlib import Path

def render(repo_root: Path, out: Path):
    out.mkdir(parents=True,exist_ok=True)
    (out/'index.md').write_text('# SecureRails Trust Center Generated\n',encoding='utf-8')
