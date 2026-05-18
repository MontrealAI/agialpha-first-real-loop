from pathlib import Path


def test_engine_proof_docs_exist():
    paths = [
        "README_AGIALPHA_ENGINE_PROOF.md", "docs/agialpha-engine-proof/README.md",
        "docs/agialpha-engine-proof/measured-recursive-claim.md", "docs/agialpha-engine-proof/operator-guide.md", "docs/agialpha-engine-proof/reviewer-guide.md",
    ]
    assert all(Path(p).exists() for p in paths)
