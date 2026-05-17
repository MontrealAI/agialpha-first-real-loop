import json
import unittest
from pathlib import Path

class TestDocsPublicRoutes(unittest.TestCase):
    def test_major_routes_indexed(self):
        data = json.loads(Path('docs/_generated/public-experience/route_manifest.json').read_text())
        self.assertIn('/secure-rails/', data['routes'])
