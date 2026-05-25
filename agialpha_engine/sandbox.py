"""Local deterministic sandbox helpers for AGI ALPHA engine proof runs."""
from __future__ import annotations

import hashlib
import json
import random
import subprocess
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any

from .context import BOUNDARIES

FORBIDDEN_TARGET_MARKERS = ("http://", "https://", "ssh://", "git@", "nmap ", "curl ", "wget ")


def canonical_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def artifact_hash(data: Any) -> str:
    return hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot_tree(root: Path) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = str(path.relative_to(root))
        snapshot[rel] = file_hash(path)
    return snapshot


class LocalSandbox:
    """A deterministic local-only execution boundary.

    The proof pilot uses in-process fixture evaluation only.  This class records
    the equal constraints used by treatment and shadow control and rejects
    network/external-target/production-actuation requests before they can run.
    """

    def __init__(self, repo_root: Path, seed: int, budget_units: int = 100) -> None:
        self.repo_root = Path(repo_root).resolve()
        self.seed = seed
        self.random = random.Random(seed)
        self.constraints = {
            "execution_scope": "local_only",
            "network_allowed": False,
            "external_targets_allowed": False,
            "production_actuation_allowed": False,
            "safe_filesystem_root": str(self.repo_root),
            "deterministic_seed": seed,
            "budget_units": budget_units,
            **BOUNDARIES,
        }

    def assert_safe_text(self, text: str) -> None:
        lowered = text.lower()
        if any(marker in lowered for marker in FORBIDDEN_TARGET_MARKERS):
            raise ValueError("sandbox rejected external target or network marker")

    def describe(self) -> dict[str, Any]:
        return dict(self.constraints)

    def apply_candidate_patch(self, fixture_path: Path, replacement_text: str) -> dict[str, Any]:
        fixture_path = Path(fixture_path).resolve()
        if not fixture_path.is_file():
            raise ValueError("fixture_path must be a file")
        if self.repo_root not in fixture_path.parents:
            raise ValueError("fixture_path must stay within repo root")
        rel = fixture_path.relative_to(self.repo_root)
        if ".." in rel.parts:
            raise ValueError("path traversal rejected")
        with tempfile.TemporaryDirectory(prefix="agialpha-sandbox-") as td:
            temp_root = Path(td)
            temp_fixture = temp_root / rel
            temp_fixture.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(fixture_path, temp_fixture)
            before_hash = file_hash(temp_fixture)
            temp_fixture.write_text(replacement_text, encoding="utf-8")
            after_hash = file_hash(temp_fixture)
            return {
                "sandbox_root": str(temp_root),
                "relative_fixture": str(rel),
                "input_hash": before_hash,
                "sandbox_output_hash": after_hash,
                "repo_source_hash_unchanged": file_hash(fixture_path) == before_hash,
                "autonomous_persistence_allowed": False,
            }

    def run_local_command(self, *, sandbox_id: str, command: list[str], allowed_root: Path, timeout_seconds: float = 5.0) -> dict[str, Any]:
        """Run a deterministic local-only command inside `allowed_root`.

        The command is executed with shell=False and with no network action by policy.
        This returns a normalized sandbox record schema used by Engine-003.
        """
        root = Path(allowed_root).resolve()
        if not root.exists() or not root.is_dir():
            raise ValueError("allowed_root must be an existing directory")
        if ".." in Path(*command).parts:
            raise ValueError("path traversal rejected in command")
        self.assert_safe_text(" ".join(command))
        files_before = snapshot_tree(root)
        start = time.time()
        timeout = False
        result = None
        stdout = ""
        stderr = ""
        blocked_reason = ""
        try:
            result = subprocess.run(
                command,
                cwd=root,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False,
            )
            stdout = result.stdout
            stderr = result.stderr
            blocked_reason = "" if result.returncode == 0 else f"exit_code_{result.returncode}"
        except subprocess.TimeoutExpired as exc:
            timeout = True
            stdout = exc.stdout or ""
            stderr = exc.stderr or ""
            blocked_reason = "timeout_expired"
        elapsed_ms = int((time.time() - start) * 1000)
        files_after = snapshot_tree(root)
        changed_files = sorted(
            set(files_before.keys()) | set(files_after.keys())
        )
        changed_files = [
            rel for rel in changed_files
            if files_before.get(rel) != files_after.get(rel)
        ]
        return {
            "schema_version": "agialpha.engine.sandbox_record.v1",
            "sandbox_id": sandbox_id,
            "allowed_root": str(root),
            "seed": self.seed,
            "network_disabled": True,
            "repo_mutation_allowed": False,
            "production_actuation_allowed": False,
            "commands_run": [" ".join(command)],
            "files_before": files_before,
            "files_after": files_after,
            "diff_summary": {"changed_files": len(changed_files), "changed_paths": changed_files},
            "stdout_hash": artifact_hash(stdout),
            "stderr_hash": artifact_hash(stderr),
            "status": "pass" if (result is not None and result.returncode == 0 and not timeout) else "fail",
            "blocked_reason": blocked_reason,
            "timeout_ms": int(timeout_seconds * 1000),
            "elapsed_ms": elapsed_ms,
            **BOUNDARIES,
        }
