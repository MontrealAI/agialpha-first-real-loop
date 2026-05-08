# Multi-Repo Evidence Ingestion

Architecture: external repo artifact pointer -> intake validation -> append-only registry -> generated summaries.

Safety controls include zip-slip protection, max file size/count, redaction checks, digest capture, quarantine for unsafe or expired artifacts, and no untrusted code execution.
