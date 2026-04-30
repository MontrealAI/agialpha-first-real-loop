from pathlib import Path
import re


def parse_workflow_dispatch_inputs(workflow_text: str) -> dict:
    """Best-effort parser for top-level workflow_dispatch inputs."""
    inputs = {}
    in_dispatch = False
    in_inputs = False
    for line in workflow_text.splitlines():
        if re.match(r"^\s*workflow_dispatch\s*:", line):
            in_dispatch = True
            continue
        if in_dispatch and re.match(r"^\s*inputs\s*:", line):
            in_inputs = True
            continue
        if in_inputs:
            m = re.match(r"^\s{4,}([A-Za-z0-9_-]+)\s*:\s*$", line)
            if m:
                inputs[m.group(1)] = {}
                continue
            if line.strip() and not line.startswith(" "):
                break
    return inputs


def workflow_gh_command(workflow_file: str, has_dispatch: bool) -> str | None:
    if not has_dispatch:
        return None
    return f"gh workflow run {Path(workflow_file).name}"
