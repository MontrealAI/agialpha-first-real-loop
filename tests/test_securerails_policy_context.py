import tempfile
import unittest
from pathlib import Path

from secure_rails.policy_context import build_context


class T(unittest.TestCase):
    def test_benchmark_filename_not_mark_allocation(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'benchmark-note.md'
            p.write_text('certified secure', encoding='utf-8')
            context = build_context(str(p), 'auto')
            self.assertEqual(context['context_type'], 'generic_text')

    def test_permission_filename_not_github_app(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'workflow_permission_review.json'
            p.write_text('{"claim":"certified secure"}', encoding='utf-8')
            context = build_context(str(p), 'auto')
            self.assertEqual(context['context_type'], 'generic_text')


if __name__ == '__main__':
    unittest.main()
