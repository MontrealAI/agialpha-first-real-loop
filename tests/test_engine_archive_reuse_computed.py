from agialpha_engine.archive_reuse import compare_archive_reuse


def test_archive_reuse_computed_changes_with_raw():
    r1 = compare_archive_reuse({"accepted_task_count": 2, "verified_work_score": 0.4}, {"accepted_task_count": 3, "verified_work_score": 0.5})
    r2 = compare_archive_reuse({"accepted_task_count": 2, "verified_work_score": 0.4}, {"accepted_task_count": 1, "verified_work_score": 0.3})
    assert r1["B6_beats_B5"] is True
    assert r2["B6_beats_B5"] is False
