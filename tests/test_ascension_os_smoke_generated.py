import json, os, subprocess, sys, tempfile
from pathlib import Path


def run(cmd):
    subprocess.check_call([sys.executable, "-m", "agialpha_ascension_os", *cmd])


def test_vertical_slice_commands_and_boundaries():
    d = tempfile.mkdtemp()
    registry = os.path.join(d, "registry")
    cmds = [
        ["discover", "--repo-root", ".", "--registry", registry],
        ["run-cycle", "--repo-root", ".", "--registry", "ascension_os_registry", "--out", d],
        ["run-open-rsi-eval", "--repo-root", ".", "--out", d, "--task-count", "4"],
        ["run-gauntlet", "--repo-root", ".", "--out", d, "--task-count", "4"],
        ["evaluate-archive-reuse", "--repo-root", ".", "--run", d],
        ["build-scorecard", "--repo-root", ".", "--out", d],
        ["verified-enterprise-alpha", "--run", d],
        ["value-to-capacity", "--run", d],
        ["capacity-reinvestment", "--run", d],
    ]
    for c in cmds:
        run(c)
    run(["replay", "--run", d])
    run(["falsification-audit", "--run", d])
    run(["validate", "--run", d])
    run(["build-data", "--registry", "ascension_os_registry", "--out", os.path.join(d, "generated")])

    score = json.loads(Path(d, "22_reports", "ascension_scorecard.json").read_text())
    assert score["human_review_required"] is True
    assert score["autonomous_persistence_allowed"] is False
    assert score["no_auto_merge"] is True
