"""Baseline ladder computation for RSI-GOVERNOR-001."""

from __future__ import annotations

from typing import Any, Dict, Iterable

from .evaluator import eval_kernel


def compute_baseline_ladder(incumbent_kernel: Dict[str, Any], tasks: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    task_list = list(tasks)
    b0 = {"scoring_weights": {}, "future_work_recommendation_policy": {}, "safety_policy": {}}
    b1 = {**incumbent_kernel, "kernel_name": "B1_static_checklist"}
    b2 = {**incumbent_kernel, "kernel_name": "B2_current_simple_publisher"}
    b3 = {**incumbent_kernel, "kernel_name": "B3_heuristic_hub_repair"}
    b4 = {**incumbent_kernel, "kernel_name": "B4_unstructured_self_modification"}
    b5 = {**incumbent_kernel, "kernel_name": "B5_incumbent_governance_kernel"}
    return {
        "B0": eval_kernel(b0, task_list, baseline=True),
        "B1": eval_kernel(b1, task_list, baseline=True),
        "B2": eval_kernel(b2, task_list, baseline=True),
        "B3": eval_kernel(b3, task_list, baseline=True),
        "B4": eval_kernel(b4, task_list, baseline=True),
        "B5": eval_kernel(b5, task_list, baseline=True),
        "ladder": ["B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"],
    }


__all__ = ["compute_baseline_ladder"]
