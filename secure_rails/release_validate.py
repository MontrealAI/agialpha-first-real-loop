from pathlib import Path
import json, hashlib
from .release_manifest import validate_manifest

REQUIRED_FILES = [
    "release_manifest.json",
    "RELEASE_NOTES.md",
    "CLAIM_BOUNDARY.md",
    "CUSTOMER_INSTALL.md",
    "MARKETPLACE_READINESS.md",
    "EXPORT_PLAN.md",
    "CHECKSUMS.sha256",
    "artifact_manifest.json",
]


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def validate_bundle(inp: Path):
    errs = []
    for rel in REQUIRED_FILES:
        if not (inp / rel).exists():
            errs.append(f"missing required bundle file: {rel}")

    manifest_path = inp / "release_manifest.json"
    if manifest_path.exists():
        m = json.loads(manifest_path.read_text())
        ok, manifest_errs = validate_manifest(m)
        if not ok:
            errs.extend(manifest_errs)

    manifest_index_path = inp / "artifact_manifest.json"
    if manifest_index_path.exists():
        index = json.loads(manifest_index_path.read_text())
        artifact_list = index.get("artifacts", [])
        if "artifact_manifest.json" not in artifact_list:
            errs.append("artifact_manifest.json missing from artifact_manifest entries")
        for rel in artifact_list:
            p = inp / rel
            if not p.exists():
                errs.append(f"artifact listed but missing: {rel}")

    checksums_path = inp / "CHECKSUMS.sha256"
    if checksums_path.exists():
        lines = [ln.strip() for ln in checksums_path.read_text().splitlines() if ln.strip()]
        checksum_map = {}
        for line in lines:
            if "  " not in line:
                errs.append(f"malformed checksum line: {line}")
                continue
            digest, rel = line.split("  ", 1)
            checksum_map[rel] = digest
        for rel, digest in checksum_map.items():
            p = inp / rel
            if not p.exists():
                errs.append(f"checksummed file missing: {rel}")
                continue
            actual = _sha(p)
            if actual != digest:
                errs.append(f"checksum mismatch: {rel}")

    if errs:
        raise ValueError("; ".join(errs))
