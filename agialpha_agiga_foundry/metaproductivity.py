"""Lineage metaproductivity helpers for AGI-GA Foundry."""

def lineage_metaproductivity(descendant_solved_niches_enabled_by_archive: int, accepted_parent_capabilities: int) -> float:
    """Compute lineage metaproductivity as descendants solved per accepted parent capability."""
    if accepted_parent_capabilities <= 0:
        return 0.0
    return descendant_solved_niches_enabled_by_archive / accepted_parent_capabilities
