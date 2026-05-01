import tempfile
import unittest
from pathlib import Path

from agialpha_evidence_hub.build import build_site


class T(unittest.TestCase):
    def test_root_ui_is_html_shell_not_json_dump(self):
        with tempfile.TemporaryDirectory() as out:
            build_site('evidence_registry', out)
            index_text = Path(out, 'index.html').read_text()
            self.assertIn('<html', index_text)
            self.assertIn('AGI ALPHA Evidence Mission Control', index_text)
            self.assertNotIn('<pre>{', index_text)


if __name__ == '__main__':
    unittest.main()
