import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from agialpha_evidence_hub.build import build_site
from agialpha_evidence_hub.workflow_dispatch import parse_workflow_dispatch_inputs


class TestEvidenceHubWorkflowLaunchpad(unittest.TestCase):
    def test_workflow_catalog_generates_gh_commands(self):
        with tempfile.TemporaryDirectory() as td:
            registry = Path(td) / 'registry'
            subprocess.run([
                'python','-m','agialpha_evidence_hub','workflow-catalog','--repo-root','.', '--registry', str(registry)
            ], check=True)
            data = json.loads((registry / 'workflow_catalog.json').read_text())
            self.assertTrue(data['workflows'])
            self.assertTrue(any(w['has_workflow_dispatch'] for w in data['workflows']))
            self.assertTrue(any((w.get('gh_command') or '').startswith('gh workflow run') for w in data['workflows']))

    def test_dispatch_inputs_do_not_include_push_paths(self):
        workflow = Path('.github/workflows/benchmark-gauntlet-001-autonomous.yml').read_text()
        inputs = parse_workflow_dispatch_inputs(workflow)
        self.assertIn('challenge_dir', inputs)
        self.assertNotIn('paths', inputs)

    def test_launchpad_uses_workflow_file_field(self):
        with tempfile.TemporaryDirectory() as td:
            reg = Path(td) / 'registry'
            out = Path(td) / 'site'
            reg.mkdir(parents=True)
            (reg / 'runs.json').write_text('[]')
            (reg / 'experiments.json').write_text('[]')
            (reg / 'workflows.json').write_text(json.dumps([
                {'name': 'Replay', 'slug': 'replay', 'workflow_file': '.github/workflows/replay.yml', 'gh_command': 'gh workflow run replay.yml'}
            ]))
            build_site(str(reg), str(out))
            html = (out / 'launchpad' / 'index.html').read_text()
            self.assertIn('replay.yml', html)
            self.assertIn('gh workflow run replay.yml', html)

    def test_build_consumes_workflow_catalog_when_workflows_json_empty(self):
        with tempfile.TemporaryDirectory() as td:
            reg = Path(td) / 'registry'
            out = Path(td) / 'site'
            reg.mkdir(parents=True)
            (reg / 'runs.json').write_text('[]')
            (reg / 'experiments.json').write_text('[]')
            (reg / 'workflows.json').write_text('[]')
            (reg / 'workflow_catalog.json').write_text(json.dumps({'workflows':[{'workflow_file':'.github/workflows/replay.yml','name':'Replay','gh_command':'gh workflow run replay.yml'}]}))
            build_site(str(reg), str(out))
            html = (out / 'launchpad' / 'index.html').read_text()
            self.assertIn('Replay', html)
            self.assertIn('gh workflow run replay.yml', html)
            published = json.loads((out / 'data' / 'workflow_catalog.json').read_text())
            self.assertEqual(1, len(published['workflows']))

    def test_launchpad_does_not_fabricate_command_without_dispatch(self):
        with tempfile.TemporaryDirectory() as td:
            reg = Path(td) / 'registry'
            out = Path(td) / 'site'
            reg.mkdir(parents=True)
            (reg / 'runs.json').write_text('[]')
            (reg / 'experiments.json').write_text('[]')
            (reg / 'workflows.json').write_text('[]')
            (reg / 'workflow_catalog.json').write_text(json.dumps({'workflows':[{'workflow_file':'.github/workflows/no-dispatch.yml','name':'No Dispatch','gh_command':None}]}))
            build_site(str(reg), str(out))
            html = (out / 'launchpad' / 'index.html').read_text()
            self.assertIn('workflow_dispatch not enabled', html)
            self.assertNotIn('gh workflow run no-dispatch.yml', html)

    def test_workflow_catalog_includes_yaml_extension(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            wf_dir = root / '.github' / 'workflows'
            wf_dir.mkdir(parents=True)
            (wf_dir / 'alpha.yaml').write_text('on:\n  workflow_dispatch:\n')
            registry = root / 'registry'
            subprocess.run(['python','-m','agialpha_evidence_hub','workflow-catalog','--repo-root',str(root),'--registry',str(registry)], check=True)
            data = json.loads((registry / 'workflow_catalog.json').read_text())
            files = {w['workflow_file'] for w in data['workflows']}
            self.assertIn('.github/workflows/alpha.yaml', files)


if __name__ == '__main__':
    unittest.main()
