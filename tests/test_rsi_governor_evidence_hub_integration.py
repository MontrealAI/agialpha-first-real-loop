import unittest

from agialpha_evidence_hub import discover, canonicalize, validate, build, render, needed_update


class TestRSIGovernorEvidenceHubIntegration(unittest.TestCase):
    def test_modules_import_with_governance_kernel_hooks(self):
        self.assertIsNotNone(discover)
        self.assertIsNotNone(canonicalize)
        self.assertIsNotNone(validate)
        self.assertIsNotNone(build)
        self.assertIsNotNone(render)
        self.assertIsNotNone(needed_update)


if __name__ == "__main__":
    unittest.main()
