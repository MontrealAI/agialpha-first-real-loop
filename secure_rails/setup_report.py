from pathlib import Path

def write_setup_report(config:dict, health:dict, out:Path)->None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"# SecureRails Template Bootstrap Setup Report\n\n- Instance: {config['full_repository']}\n- Type: {config['instance_type']}\n- Pages: {config.get('public_pages_url','')}\n- Template health: {health['status']}\n\n## Doctrine\nNo Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.\n", encoding='utf-8')
