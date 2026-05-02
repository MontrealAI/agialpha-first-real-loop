"""Adversarial evaluation helpers for RSI-GOVERNOR-001."""

from __future__ import annotations

from .evaluator import eval_kernel


def evaluate_adversarial_tasks(kernel: dict, tasks: list[dict]) -> list[dict]:
    """Evaluate candidate kernel against adversarial task fixtures."""
    return [eval_kernel(kernel, [task]) for task in tasks]


__all__ = ["evaluate_adversarial_tasks"]
