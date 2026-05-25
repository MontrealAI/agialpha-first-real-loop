from __future__ import annotations

from pathlib import Path
from .context import atomic_write_json, BOUNDARIES


def render_network_routes(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    atomic_write_json(out / "routes.json", {
        "routes": ["/agialpha-skill-network/", "/experiments/agialpha-engine-003/"],
        "nav_label": "Skill Network",
        **BOUNDARIES,
    })
