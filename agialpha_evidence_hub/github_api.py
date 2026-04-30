import json, subprocess

def discover_runs(limit=200):
    try:
        out=subprocess.check_output(['gh','api',f'/repos/{{owner}}/{{repo}}/actions/runs?per_page={limit}'],text=True)
        return json.loads(out)
    except Exception:
        return {'workflow_runs':[]}
