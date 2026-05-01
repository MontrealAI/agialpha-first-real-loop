"""Canonicalization helpers for evidence hub records."""

from __future__ import annotations

from typing import Any


def canonical_experiment_slug(value: str) -> str:
    """Return a conservative canonical experiment slug."""
    return "-".join(part for part in value.strip().lower().replace("_", "-").split("-") if part)


def canonical_family(slug: str) -> str:
    """Infer family from canonical slug prefix."""
    token = canonical_experiment_slug(slug)
    if "-" not in token:
        return token
    head, tail = token.rsplit("-", 1)
    return head if tail.isdigit() else token


def canonical_metric(value: Any) -> Any:
    """Normalize missing metrics to doctrinal placeholder tokens."""
    if value is None:
        return "not_reported"
    if isinstance(value, str) and not value.strip():
        return "not_reported"
    return value
