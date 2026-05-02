import pathlib
import unittest


class TestRsiGovernorLifecycleOrchestrator(unittest.TestCase):
    def test_lifecycle_workflow_exists_and_orders_jobs(self):
        workflow = pathlib.Path('.github/workflows/rsi-governor-001-lifecycle.yml').read_text(encoding='utf-8')
        self.assertIn('autonomous_candidate_evolution', workflow)
        self.assertIn('replay', workflow)
        self.assertIn('falsification_audit', workflow)
        self.assertIn('safe_pr', workflow)
        self.assertIn('needs: autonomous_candidate_evolution', workflow)
        self.assertIn('needs: [autonomous_candidate_evolution, replay]', workflow)
        self.assertIn('needs: [autonomous_candidate_evolution, falsification_audit]', workflow)


if __name__ == '__main__':
    unittest.main()
