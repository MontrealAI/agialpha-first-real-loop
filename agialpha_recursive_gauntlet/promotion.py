from .context import *
def generate_promotion(run: Path,eligible:bool):
 p=run/"11_promotion"; p.mkdir(parents=True,exist_ok=True); status="human_review_required" if eligible else "not_eligible"; (p/"promotion_dossier.md").write_text("# Promotion Dossier\n\n"+CLAIM_BOUNDARY+"\n",encoding="utf-8"); write_json(p/"safe_pr_plan.json",{"status":status,"no_automerge":True,"claim_boundary":CLAIM_BOUNDARY}); (p/"human_review_required.md").write_text("Human review required before persistence.\n",encoding="utf-8"); return status
