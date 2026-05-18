from engine_proof_helpers import make_run


def test_run_proof_creates_full_run(tmp_path):
    out = make_run(tmp_path)
    required = [
        "00_manifest.json", "01_claim_boundary.md", "02_mandate_pairs/mandate_pairs.json",
        "03_mandate_A_training/tasks.json", "03_mandate_A_training/raw_results.json", "03_mandate_A_training/generated_capabilities.json",
        "04_capability_freeze/frozen_capabilities.json", "04_capability_freeze/capability_hashes.json", "04_capability_freeze/mutation_check.json",
        "05_heldout_mandate_B/heldout_fixtures.json", "05_heldout_mandate_B/leakage_check.json",
        "06_treatment_run/raw_results.json", "07_shadow_control_run/raw_results.json",
        "08_comparison/computed_metrics.json", "08_comparison/vRCI.json", "08_comparison/B6_vs_B5.json",
        "10_proofbundles/proofbundle_index.json", "11_evidence_dockets/docket_index.json",
        "12_adversarial_docket/falsification_attempts.json", "13_replay/replay_report.json", "14_falsification/falsification_audit.json",
        "15_public_summary/summary.json", "15_public_summary/stronger_claim_status.md", "evidence-run-manifest.json",
    ]
    assert all((out / rel).exists() for rel in required)
