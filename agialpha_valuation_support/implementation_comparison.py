"""Implementation-side comparison record builder."""

from .core import bfields


def build_implementation_comparison(ascension_registry: str) -> dict:
    return {
        "status": "included",
        "ascension_registry": ascension_registry,
        **bfields(),
    }
