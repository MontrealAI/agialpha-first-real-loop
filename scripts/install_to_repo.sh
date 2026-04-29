#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-.}"
mkdir -p "$TARGET"
cp -R .github "$TARGET/"
cp -R agialpha_evidence_factory "$TARGET/"
cp -R config "$TARGET/"
cp -R tests "$TARGET/"
cp -R evidence-docket "$TARGET/"
cp pyproject.toml "$TARGET/"
cp README.md "$TARGET/EVIDENCE_FACTORY_README.md"
echo "Installed AGI ALPHA Evidence Factory into $TARGET"
