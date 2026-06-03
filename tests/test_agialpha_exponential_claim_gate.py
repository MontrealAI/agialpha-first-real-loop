import json
import subprocess
import tempfile
from pathlib import Path

from agialpha_engine.network_skill_metrics import EXPONENTIAL_GATE_HARD_SAFETY_COUNTERS


def zero_exponential_gate_safety_counters(**overrides):
    counters = {key: 0 for key in EXPONENTIAL_GATE_HARD_SAFETY_COUNTERS}
    counters.update(overrides)
    return counters


def test_exponential_claim_defaults_to_strategic_target_without_multicycle_evidence():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / 'run'
        reg = Path(td) / 'reg'
        subprocess.check_call([
            'python','-m','agialpha_engine','network-compounding-run',
            '--repo-root','.','--registry',str(reg),'--out',str(run),
            '--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'
        ])
        metrics = json.loads((run / '07_metrics/network_skill_metrics.json').read_text())
        assert metrics['exponential_compounding_supported'] is False
        assert 'strategic target' in metrics['exponential_compounding_status']


def test_exponential_claim_remains_blocked_even_after_replay_and_falsification():
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / 'run'
        reg = Path(td) / 'reg'
        subprocess.check_call([
            'python','-m','agialpha_engine','network-compounding-run',
            '--repo-root','.','--registry',str(reg),'--out',str(run),
            '--jobs','5','--target-agents','3','--heldout-tasks','5','--seed','123'
        ])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-replay','--run',str(run)])
        subprocess.check_call(['python','-m','agialpha_engine','network-compounding-falsification-audit','--run',str(run)])
        metrics = json.loads((run / '07_metrics/network_skill_metrics.json').read_text())
        assert metrics['exponential_compounding_supported'] is False
        assert metrics['compounding_exponent_proxy'] in {'not_supported', 'pending', 'not_reported', 'unavailable', 'skipped_with_reason'}


def test_exponential_gate_requires_three_raw_log_backed_superlinear_cycles():
    from agialpha_engine.network_skill_metrics import evaluate_exponential_compounding_gate

    blocked = evaluate_exponential_compounding_gate(
        compounding_cycles=[
            {"network_skill_propagation_lift": 0.01, "raw_task_result_ids": ["raw-1"]},
            {"network_skill_propagation_lift": 0.03, "raw_task_result_ids": ["raw-2"]},
        ],
        replay_pass=True,
        falsification_pass=True,
        metrics_computed_from_raw_logs=True,
        safety_counters=zero_exponential_gate_safety_counters(),
    )
    assert blocked["exponential_compounding_supported"] is False
    assert blocked["compounding_exponent_proxy"] == "not_supported"
    assert "strategic target" in blocked["exponential_compounding_status"]

    supported = evaluate_exponential_compounding_gate(
        compounding_cycles=[
            {"network_skill_propagation_lift": 0.01, "raw_task_result_ids": ["raw-1"]},
            {"network_skill_propagation_lift": 0.03, "raw_task_result_ids": ["raw-2"]},
            {"network_skill_propagation_lift": 0.08, "raw_task_result_ids": ["raw-3"]},
        ],
        replay_pass=True,
        falsification_pass=True,
        metrics_computed_from_raw_logs=True,
        safety_counters=zero_exponential_gate_safety_counters(),
    )
    assert supported["exponential_compounding_supported"] is True
    assert supported["superlinear_growth_observed"] is True
    assert supported["compounding_exponent_proxy"] > 1


def test_exponential_gate_blocks_boundary_violations_and_missing_raw_ids():
    from agialpha_engine.network_skill_metrics import evaluate_exponential_compounding_gate

    gate = evaluate_exponential_compounding_gate(
        compounding_cycles=[
            {"network_skill_propagation_lift": 0.01, "raw_task_result_ids": ["raw-1"]},
            {"network_skill_propagation_lift": 0.03, "raw_task_result_ids": []},
            {"network_skill_propagation_lift": 0.08, "raw_task_result_ids": ["raw-3"]},
        ],
        replay_pass=True,
        falsification_pass=True,
        metrics_computed_from_raw_logs=True,
        safety_counters=zero_exponential_gate_safety_counters(critical_safety_incidents=1),
    )
    assert gate["exponential_compounding_supported"] is False
    assert gate["hard_safety_ok"] is False
    assert "local bounded network skill propagation only" in gate["exponential_compounding_status"]


def test_exponential_gate_requires_complete_reported_zero_safety_ledger():
    from agialpha_engine.network_skill_metrics import evaluate_exponential_compounding_gate

    cycles = [
        {"network_skill_propagation_lift": 0.01, "raw_task_result_ids": ["raw-1"]},
        {"network_skill_propagation_lift": 0.03, "raw_task_result_ids": ["raw-2"]},
        {"network_skill_propagation_lift": 0.08, "raw_task_result_ids": ["raw-3"]},
    ]
    omitted = evaluate_exponential_compounding_gate(
        compounding_cycles=cycles,
        replay_pass=True,
        falsification_pass=True,
        metrics_computed_from_raw_logs=True,
        safety_counters=None,
    )
    assert omitted["exponential_compounding_supported"] is False
    assert set(omitted["missing_hard_safety_counters"]) == set(EXPONENTIAL_GATE_HARD_SAFETY_COUNTERS)
    assert omitted["hard_safety_ok"] is False

    incomplete_counters = zero_exponential_gate_safety_counters()
    incomplete_counters.pop("unsafe_automerge_count")
    incomplete = evaluate_exponential_compounding_gate(
        compounding_cycles=cycles,
        replay_pass=True,
        falsification_pass=True,
        metrics_computed_from_raw_logs=True,
        safety_counters=incomplete_counters,
    )
    assert incomplete["exponential_compounding_supported"] is False
    assert incomplete["missing_hard_safety_counters"] == ["unsafe_automerge_count"]


def test_exponential_gate_rejects_sentinel_or_non_collection_raw_ids():
    from agialpha_engine.network_skill_metrics import evaluate_exponential_compounding_gate

    gate = evaluate_exponential_compounding_gate(
        compounding_cycles=[
            {"network_skill_propagation_lift": 0.01, "raw_task_result_ids": "not_reported"},
            {"network_skill_propagation_lift": 0.03, "raw_task_result_ids": ["pending"]},
            {"network_skill_propagation_lift": 0.08, "raw_task_result_ids": ["raw-3"]},
        ],
        replay_pass=True,
        falsification_pass=True,
        metrics_computed_from_raw_logs=True,
        safety_counters=zero_exponential_gate_safety_counters(),
    )
    assert gate["exponential_compounding_supported"] is False
    assert gate["raw_cycle_evidence_valid"] is False
    assert gate["invalid_raw_cycle_evidence"] == [0, 1]
    assert "strategic target" in gate["exponential_compounding_status"]
