import unittest, tempfile, json
from pathlib import Path
from secure_rails_pr_guard.evidence_docket import build_evidence
class T(unittest.TestCase):
  def test_build(self):
    with tempfile.TemporaryDirectory() as d:
      p=Path(d); (p/"00_manifest.json").write_text(json.dumps({"claim_boundary":"x"}))
      out=p/"o"; build_evidence(p,out); self.assertTrue((out/"00_manifest.json").exists())
