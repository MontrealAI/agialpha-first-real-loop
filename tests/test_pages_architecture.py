import unittest
from pathlib import Path


class TestPagesArchitecture(unittest.TestCase):
    def test_only_central_workflow_uses_pages_actions(self):
        workflows = sorted(Path('.github/workflows').glob('*.yml'))
        deploy_refs = []
        upload_refs = []
        for wf in workflows:
            text = wf.read_text()
            if 'actions/deploy-pages' in text:
                deploy_refs.append(wf.as_posix())
            if 'actions/upload-pages-artifact' in text:
                upload_refs.append(wf.as_posix())

        self.assertEqual(deploy_refs, ['.github/workflows/evidence-hub-publish.yml'])
        self.assertEqual(upload_refs, ['.github/workflows/evidence-hub-publish.yml'])

    def test_architecture_script(self):
        import subprocess

        subprocess.check_call(['python', 'scripts/check_pages_architecture.py'])


if __name__ == '__main__':
    unittest.main()
