import json
import unittest
from pathlib import Path

class TestDocsPageHealth(unittest.TestCase):
    def test_page_health_json_exists(self):
        data = json.loads(Path('docs/_generated/public-experience/page_health.json').read_text())
        self.assertIn('status', data)

    def test_page_health_counts_home_route(self):
        data = json.loads(Path('docs/_generated/public-experience/page_health.json').read_text())
        self.assertGreaterEqual(data['routes_checked'], 15)

    def test_route_manifest_includes_cybersecurity_sovereign(self):
        manifest = json.loads(Path('docs/_generated/public-experience/route_manifest.json').read_text())
        self.assertIn('/cybersecurity-sovereign/', manifest['routes'])
