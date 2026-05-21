
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

from .context import BOUNDARIES

SUPPORTED_SENTENCE = "In this local repo-owned benchmark, AGI ALPHA demonstrated machine labor that recursively improves in a measured, falsifiable way."
NOT_SUPPORTED_SENTENCE = "Not demonstrated yet."

class RecursiveMachineLaborClaimGate:
    claim = "machine_labor_recursively_improves_measured_falsifiable"

    @staticmethod
    def evaluate(run_dir: Path) -> dict[str, Any]:
        run_dir = Path(run_dir)
        metrics = json.loads((run_dir/'06_metrics'/'computed_metrics.json').read_text())
        req = {
            'at_least_3_adjacent_mandates': metrics.get('adjacent_mandates_completed',0) >= 3,
            'm1_frozen_capability': metrics.get('frozen_capability_packages_created',0) >= 1,
            'm2_b6_beats_b5': metrics.get('m2_b6_beats_b5') is True,
            'm3_b6_beats_b5': metrics.get('m3_b6_beats_b5') is True,
            'computed_not_hardcoded': isinstance(metrics.get('vRCI_value', metrics.get('vRCI_computed')), (int, float)) and metrics.get('metrics_computed_from_raw_results') is True and metrics.get('hardcoded_metric_markers_found') == 0,
            'b6_beats_b5': metrics.get('B6_beats_B5') is True,
            'heldout_evaluated': metrics.get('heldout_descendant_mandates_evaluated',0) >= 1,
            'replay_pass': metrics.get('replay_passes',0) >= 1,
            'falsification_pass': metrics.get('falsification_pass') is True,
            'adversarial_caught': metrics.get('adversarial_fixtures_generated',0) > 0 and metrics.get('adversarial_fixtures_caught',0) > 0,
            'rejected_preserved': metrics.get('rejected_variants_preserved',0) > 0,
            'human_review_required': metrics.get('human_review_required_count',0) > 0,
            'no_auto_merge': metrics.get('unsafe_automerge_count') == 0,
            'safety_zero': metrics.get('critical_safety_incidents') == 0,
        }
        failed = [k for k,v in req.items() if not v]
        status = 'supported' if not failed else 'blocked'
        return {
            'schema_version': 'agialpha.engine.claim_gate.v2',
            'claim': RecursiveMachineLaborClaimGate.claim,
            'claim_text': SUPPORTED_SENTENCE if status == 'supported' else NOT_SUPPORTED_SENTENCE,
            'status': status,
            'allowed_public_wording': SUPPORTED_SENTENCE if status == 'supported' else NOT_SUPPORTED_SENTENCE,
            'blocked_reasons': failed,
            'supporting_artifacts': ['06_metrics/computed_metrics.json','11_replay/replay_report.json','12_falsification/falsification_audit.json'],
            'raw_metric_sources': metrics.get('raw_metric_sources',[]),
            'computed_not_hardcoded': req['computed_not_hardcoded'],
            'human_review_required': True,
            'autonomous_persistence_allowed': False,
            'claim_boundary': metrics.get('claim_boundary') or BOUNDARIES['claim_boundary'],
        }
