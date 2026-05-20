from pathlib import Path

from agialpha_engine.sandbox import LocalSandbox


def test_sandbox_patch_does_not_modify_repo_source(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    fixture = repo / "fixture.txt"
    fixture.write_text("before", encoding="utf-8")
    sb = LocalSandbox(repo_root=repo, seed=1337)
    result = sb.apply_candidate_patch(fixture, "after")
    assert result["repo_source_hash_unchanged"] is True
    assert fixture.read_text(encoding="utf-8") == "before"
    assert result["autonomous_persistence_allowed"] is False


def test_sandbox_blocks_path_outside_repo(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("x", encoding="utf-8")
    sb = LocalSandbox(repo_root=repo, seed=1)
    try:
        sb.apply_candidate_patch(outside, "y")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "within repo root" in str(exc)
