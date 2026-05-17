import json
import unittest
from pathlib import Path

class TestDocsPublicExperienceInventory(unittest.TestCase):
    def test_public_experience_inventory_exists(self):
        p = Path('docs/_generated/public-experience/site_manifest.json')
        self.assertTrue(p.exists())
        data = json.loads(p.read_text())
        self.assertTrue('workflow_count' in data or 'workflows' in data)
