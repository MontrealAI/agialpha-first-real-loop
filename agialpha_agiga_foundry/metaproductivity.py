"""Lineage metaproductivity helpers for AGI-GA Foundry."""

from __future__ import annotations

def lineage_metaproductivity(descendant_solved_niches_enabled_by_archive: int, accepted_parent_capabilities: int):
    """Compute lineage metaproductivity ratio or return 'unavailable'."""
    if accepted_parent_capabilities <= 0:
        return "unavailable"
    return descendant_solved_niches_enabled_by_archive / accepted_parent_capabilities
