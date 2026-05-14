"""Implementation-side comparison record builder."""

from .boundaries import bfields


def build_implementation_comparison(ascension_registry: str) -> dict:
    return {
        "status": "included",
        "ascension_registry": ascension_registry,
        **bfields(),
    }
