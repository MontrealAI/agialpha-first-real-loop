import subprocess, tempfile, unittest
class T(unittest.TestCase):
  def test_cli(self):
    with tempfile.TemporaryDirectory() as d:
      cmds=[
      f'python -m secure_rails supply-chain collect --repo-root . --out {d}',
      f'python -m secure_rails supply-chain hash-artifacts --input {d} --out {d}/artifact_manifest.json',
      f'python -m secure_rails supply-chain provenance --repo-root . --artifact-manifest {d}/artifact_manifest.json --out {d}/provenance_record.json',
      f'python -m secure_rails supply-chain repository-health --repo-root . --out {d}/repository_health.json',
      f'python -m secure_rails supply-chain build-report --input {d} --out {d}/supply_chain_report.json',
      f'python -m secure_rails supply-chain render --input {d} --out {d}/summary.md',
      f'python -m secure_rails supply-chain validate --input {d}',
      ]
      for c in cmds: self.assertEqual(subprocess.call(c,shell=True),0)
