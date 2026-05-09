#!/usr/bin/env python3
"""Generate a fake GitHub webhook payload and matching signature for local SecureRails tests."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
from pathlib import Path


def build_payload(repo: str, sender: str, event_type: str) -> dict:
    owner, name = repo.split("/", 1)
    return {
        "repository": {
            "name": name,
            "full_name": repo,
            "visibility": "private",
            "owner": {"login": owner},
        },
        "sender": {"login": sender, "email": "redacted@example.invalid"},
        "pull_request": {
            "number": 1,
            "title": "example only",
            "head": {"sha": "abc123", "repo": {"fork": False}},
            "base": {"sha": "def456"},
        },
        "workflow_run": {
            "id": 101,
            "name": "SecureRails PR Guard",
            "conclusion": "success",
            "artifacts_url": "https://api.github.example/artifacts",
        },
        "event_type_hint": event_type,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a fake webhook payload and HMAC signature for local testing.")
    parser.add_argument("--secret", default="demo-webhook-secret", help="Demo secret used only for local simulation.")
    parser.add_argument("--repo", default="octo-org/private-repo")
    parser.add_argument("--sender", default="demo-user")
    parser.add_argument("--event-type", default="pull_request")
    parser.add_argument("--out", required=True, help="Path to write JSON payload.")
    args = parser.parse_args()

    payload = build_payload(args.repo, args.sender, args.event_type)
    rendered_payload = json.dumps(payload, indent=2) + "\n"
    payload_bytes = rendered_payload.encode("utf-8")
    signature = "sha256=" + hmac.new(args.secret.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(payload_bytes)

    print(json.dumps({
        "payload_file": str(out),
        "signature": signature,
        "note": "Fake data only. Do not use in production.",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
