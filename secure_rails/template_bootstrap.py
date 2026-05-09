
from __future__ import annotations
import json
from pathlib import Path
from .repo_context import write_detected_context
from .instance_config import build_instance_config, load_and_validate
from .template_health import write_template_health
from .setup_report import write_setup_report

def detect(repo_root:Path, out:Path):
    return write_detected_context(repo_root, out)

def init(repo_root:Path, owner:str, repository:str, instance_name:str, instance_type:str, pages_url:str, out:Path):
    cfg=build_instance_config(owner, repository, instance_name, instance_type, pages_url)
    out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(cfg, indent=2), encoding='utf-8'); return cfg

def validate(config:Path):
    return load_and_validate(config)

def health_check(repo_root:Path, config:Path, out:Path):
    cfg=json.loads(config.read_text())
    return write_template_health(repo_root, cfg.get('full_repository','unknown'), out)

def report(repo_root:Path, config:Path, out:Path):
    cfg=json.loads(config.read_text())
    health_path=out.parent/'template_health.json'
    health=write_template_health(repo_root, cfg.get('full_repository','unknown'), health_path)
    write_setup_report(cfg, health, out)
    (out.parent/'next_steps.md').write_text(
        "## Next Steps\n- Run SecureRails Compliance Guard\n- Require human review before merge\n",
        encoding='utf-8',
    )
