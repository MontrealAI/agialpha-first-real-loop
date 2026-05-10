import json
from pathlib import Path

def render(input_dir: Path, out_file: Path):
    rep = json.loads((input_dir / '05_canary_report.json').read_text()) if (input_dir / '05_canary_report.json').exists() else json.loads((input_dir / 'canary_report.json').read_text())
    md = (
        "# SecureRails E2E Pilot Canary 001\n\n"
        f"Fixtures passed: {rep['fixtures_passed']}/{rep['fixture_count']}\n\n"
        f"Boundary preserved: {rep['$AGIALPHA_utility_only_boundary_pass']}\n"
    )
    out_file.write_text(md, encoding='utf-8')
