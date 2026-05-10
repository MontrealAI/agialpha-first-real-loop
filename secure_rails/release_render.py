from pathlib import Path
import json
from .release_notes import render_notes

def render_notes_file(inp:Path,out:Path):
 m=json.loads((inp/'release_manifest.json').read_text())
 out.write_text(render_notes(m),encoding='utf-8')
