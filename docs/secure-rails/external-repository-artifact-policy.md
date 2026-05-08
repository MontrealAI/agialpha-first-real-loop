# External Repository Artifact Policy

Artifacts are parsed as untrusted data only (.json/.md/.txt). No script execution, no importing artifact Python, and no trusted HTML rendering.

Unsafe findings are quarantined. Raw secrets are never printed; only salted hashes and metadata are recorded.
