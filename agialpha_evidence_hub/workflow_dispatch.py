from pathlib import Path
import re


def parse_workflow_dispatch_inputs(workflow_text: str) -> dict:
    """Best-effort parser for top-level workflow_dispatch inputs."""
    inputs = {}
    in_dispatch = False
    in_inputs = False
    dispatch_indent = None
    inputs_indent = None

    for line in workflow_text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))

        if re.match(r"^\s*workflow_dispatch\s*:", line):
            in_dispatch = True
            in_inputs = False
            dispatch_indent = indent
            continue

        if in_dispatch and dispatch_indent is not None and indent <= dispatch_indent:
            in_dispatch = False
            in_inputs = False

        if in_dispatch and re.match(r"^\s*inputs\s*:", line):
            in_inputs = True
            inputs_indent = indent
            continue

        if in_inputs and inputs_indent is not None and indent <= inputs_indent:
            in_inputs = False

        if in_inputs:
            m = re.match(r"^\s{4,}([A-Za-z0-9_-]+)\s*:\s*$", line)
            if m:
                inputs[m.group(1)] = {}

    return inputs


def workflow_gh_command(workflow_file: str, has_dispatch: bool) -> str | None:
    if not has_dispatch:
        return None
    return f"gh workflow run {Path(workflow_file).name}"
