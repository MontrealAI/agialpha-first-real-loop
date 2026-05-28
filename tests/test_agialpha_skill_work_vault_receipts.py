import json
from pathlib import Path
from types import SimpleNamespace

from agialpha_engine.network_compounding import run_network_compounding


def _read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_work_vault_receipts_cover_every_skill_import(tmp_path):
    run_dir = tmp_path / "run"
    registry_dir = tmp_path / "registry"
    run_network_compounding(
        SimpleNamespace(
            repo_root=".",
            registry=str(registry_dir),
            out=str(run_dir),
            jobs=5,
            target_agents=3,
            heldout_tasks=5,
            seed=123,
        )
    )

    imports = _read(run_dir / "05_skill_import" / "skill_import_events.json")["skill_import_events"]
    receipts_doc = _read(run_dir / "08_work_vault" / "skill_work_vault_receipts.json")
    receipts = receipts_doc["receipts"]

    import_ids = {row["import_id"] for row in imports}
    covered_import_ids = {
        import_id
        for receipt in receipts
        for import_id in receipt.get("covered_import_ids", [])
    }

    assert receipts_doc["receipt_count"] == len(receipts) == 2
    assert receipts_doc["covered_import_count"] == len(imports) == 6
    assert covered_import_ids == import_ids
    assert sum(receipt["skill_import_fee_units"] for receipt in receipts) == len(imports)
    assert {receipt["skill_id"] for receipt in receipts} == {"skill-1", "skill-4"}
    assert all(receipt["wallet_used"] is False for receipt in receipts)
    assert all(receipt["custody_used"] is False for receipt in receipts)
    assert all(receipt["payment_executed"] is False for receipt in receipts)
    assert all(receipt["token_price_used"] is False for receipt in receipts)
    assert all(receipt["investment_claim_made"] is False for receipt in receipts)
