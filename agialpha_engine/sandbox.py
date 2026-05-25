"""Local deterministic sandbox helpers for AGI ALPHA engine proof runs."""
from __future__ import annotations

import hashlib
import json
import os
import random
import subprocess
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any

from .context import BOUNDARIES

FORBIDDEN_TARGET_MARKERS = ("http://", "https://", "ssh://", "git@", "nmap ", "curl ", "wget ")
FORBIDDEN_PATH_SEGMENTS = ("../", "..\\", "/..", "\\..")
FORBIDDEN_NETWORK_CODE_MARKERS = (
    "import socket",
    "from socket",
    "socket.",
    "urllib.request",
    "requests.",
    "http.client",
    "ftplib",
    "telnetlib",
    "__import__(\"socket\"",
    "__import__('socket'",
    "importlib.import_module(\"socket\"",
    "importlib.import_module('socket'",
)


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


def _coerce_text_stream(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


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
        if any(marker in lowered for marker in FORBIDDEN_NETWORK_CODE_MARKERS):
            raise ValueError("sandbox rejected potential network-capable code marker")

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
        if self.repo_root != root and self.repo_root not in root.parents:
            raise ValueError("allowed_root must stay within repo root")
        if not command:
            files_now = snapshot_tree(root)
            return {
                "schema_version": "agialpha.engine.sandbox_record.v1",
                "sandbox_id": sandbox_id,
                "allowed_root": str(root),
                "seed": self.seed,
                "network_disabled": True,
                "repo_mutation_allowed": False,
                "production_actuation_allowed": False,
                "commands_run": [],
                "files_before": files_now,
                "files_after": files_now,
                "diff_summary": {"changed_files": 0, "changed_paths": []},
                "stdout_hash": artifact_hash(""),
                "stderr_hash": artifact_hash(""),
                "status": "fail",
                "blocked_reason": "empty_command",
                "timeout_ms": int(timeout_seconds * 1000),
                "elapsed_ms": 0,
                **BOUNDARIES,
            }
        for arg in command:
            normalized = str(arg).replace("\\", "/")
            if normalized.startswith("/"):
                raise ValueError("absolute path arguments are not allowed in sandbox commands")
            if normalized == ".." or any(marker in normalized for marker in FORBIDDEN_PATH_SEGMENTS):
                raise ValueError("path traversal rejected in command arguments")
        self.assert_safe_text(" ".join(command))
        files_before = snapshot_tree(root)
        start = time.time()
        timeout = False
        result = None
        stdout = ""
        stderr = ""
        blocked_reason = ""
        with tempfile.TemporaryDirectory(prefix="agialpha-run-sandbox-") as td:
            sandbox_root = Path(td) / "root"
            shutil.copytree(root, sandbox_root)
            try:
                safe_env = dict(os.environ)
                safe_env.update({
                    "NO_PROXY": "*",
                    "no_proxy": "*",
                    "HTTP_PROXY": "",
                    "HTTPS_PROXY": "",
                    "ALL_PROXY": "",
                    "http_proxy": "",
                    "https_proxy": "",
                    "all_proxy": "",
                })
                process = subprocess.Popen(
                    command,
                    cwd=sandbox_root,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=safe_env,
                    preexec_fn=os.setsid,
                )
                try:
                    out_text, err_text = process.communicate(timeout=timeout_seconds)
                except subprocess.TimeoutExpired:
                    timeout = True
                    os.killpg(process.pid, 15)
                    try:
                        out_text, err_text = process.communicate(timeout=1.0)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, 9)
                        out_text, err_text = process.communicate()
                    stdout = _coerce_text_stream(out_text)
                    stderr = _coerce_text_stream(err_text)
                    blocked_reason = "timeout_expired"
                    result = subprocess.CompletedProcess(command, returncode=124, stdout=stdout, stderr=stderr)
                else:
                    stdout = _coerce_text_stream(out_text)
                    stderr = _coerce_text_stream(err_text)
                    result = subprocess.CompletedProcess(command, returncode=process.returncode, stdout=stdout, stderr=stderr)
                    blocked_reason = "" if result.returncode == 0 else f"exit_code_{result.returncode}"
            except subprocess.TimeoutExpired as exc:
                timeout = True
                stdout = _coerce_text_stream(exc.stdout)
                stderr = _coerce_text_stream(exc.stderr)
                blocked_reason = "timeout_expired"
            except (FileNotFoundError, OSError) as exc:
                stdout = ""
                stderr = _coerce_text_stream(str(exc))
                blocked_reason = "command_not_executable"
            elapsed_ms = int((time.time() - start) * 1000)
            files_after = snapshot_tree(sandbox_root)
        changed_files = sorted(
            set(files_before.keys()) | set(files_after.keys())
        )
        changed_files = [
            rel for rel in changed_files
            if files_before.get(rel) != files_after.get(rel)
        ]
        mutation_detected = len(changed_files) > 0
        if mutation_detected and not blocked_reason:
            blocked_reason = "repo_mutation_detected"
        status = "pass" if (result is not None and result.returncode == 0 and not timeout and not mutation_detected) else "fail"
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
            "status": status,
            "blocked_reason": blocked_reason,
            "timeout_ms": int(timeout_seconds * 1000),
            "elapsed_ms": elapsed_ms,
            **BOUNDARIES,
        }
