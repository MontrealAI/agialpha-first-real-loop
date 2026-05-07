import json, os
from pathlib import Path

def load_event(event_path=None):
    if event_path and Path(event_path).exists():
        return json.loads(Path(event_path).read_text())
    return {}

def build_context(repo_root, event=None):
    event=event or {}
    pr=event.get('pull_request',{})
    return {
      'repository': os.getenv('GITHUB_REPOSITORY','MontrealAI/agialpha-first-real-loop'),
      'run_id': os.getenv('GITHUB_RUN_ID','local-run'),
      'run_url': os.getenv('GITHUB_SERVER_URL','https://github.com')+'/'+os.getenv('GITHUB_REPOSITORY','MontrealAI/agialpha-first-real-loop')+'/actions/runs/'+os.getenv('GITHUB_RUN_ID','local-run'),
      'pull_request': {
        'number': pr.get('number', event.get('number','local')),
        'title': pr.get('title','Local PR analysis'),
        'author': (pr.get('user') or {}).get('login','local'),
        'head_sha': (pr.get('head') or {}).get('sha',''),
        'base_sha': (pr.get('base') or {}).get('sha',''),
        'is_fork': bool(((pr.get('head') or {}).get('repo') or {}).get('fork',False)),
      }
    }
