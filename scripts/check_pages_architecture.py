from pathlib import Path
import re

forbidden_refs = [
    "actions/deploy-pages",
    "actions/upload-pages-artifact",
    "github-pages-deploy-action",
    "peaceiris/actions-gh-pages",
    "jamesives/github-pages-deploy-action",
]
forbidden_cmd_patterns = [
    r"\bgit\s+push\s+.*\bgh-pages\b",
    r"\bgh-pages\b",
]
allowed = "evidence-hub-publish.yml"
violations = []

for workflow in Path(".github/workflows").glob("*.yml"):
    text = workflow.read_text().lower()
    if workflow.name == allowed:
        continue
    for ref in forbidden_refs:
        if ref in text:
            violations.append((workflow.name, ref))
    for cmd_pattern in forbidden_cmd_patterns:
        if re.search(cmd_pattern, text):
            violations.append((workflow.name, f"cmd:{cmd_pattern}"))

if violations:
    raise SystemExit(f"forbidden pages deploy references: {violations}")

central_text = Path(".github/workflows", allowed).read_text().lower()
for required in ("actions/deploy-pages", "actions/upload-pages-artifact"):
    if required not in central_text:
        raise SystemExit(f"central publisher missing {required}")

print("ok")
