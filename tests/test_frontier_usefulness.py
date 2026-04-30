import json, tempfile, pathlib
from agialpha_usefulness_frontier.core import run_frontier, replay_portfolio


def test_frontier_run_and_replay():
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / 'README.md').write_text('claim boundary: does not claim achieved AGI\n')
        out = root / 'out'
        result = run_frontier(root, out)
        assert result['summary']['task_count'] == 6
        assert (out / 'index.html').exists()
        rep = replay_portfolio(out, root / 'replay')
        assert rep['replay_passes'] == 6
