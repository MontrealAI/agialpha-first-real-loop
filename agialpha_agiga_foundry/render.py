from pathlib import Path
from .policy import CLAIM_BOUNDARY
def render_page(base,score):
    p=Path(base);p.mkdir(parents=True,exist_ok=True)
    (p/"index.html").write_text(f"<html><body><nav><a href='/agiga-foundry/'>AGI-GA Foundry</a></nav><h1>AGI ALPHA AGI-GA Foundry</h1><p>{CLAIM_BOUNDARY}</p><h2>status cards</h2><div>{score}</div><h2>Workflow buttons</h2><a href='https://github.com/MontrealAI/agialpha-first-real-loop/actions/workflows/agiga-foundry-001-lifecycle.yml'>Run Lifecycle</a><pre>gh workflow run agiga-foundry-001-lifecycle.yml</pre><footer>{CLAIM_BOUNDARY}</footer></body></html>")
