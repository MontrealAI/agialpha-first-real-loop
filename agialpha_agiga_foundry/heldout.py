def generate_heldout_tasks(reveal_anchor:str, count:int=15):
    return [
        {"task_id":f"heldout-{i:02d}","reveal_anchor":reveal_anchor,"public_seed":"agiga-heldout-v1"}
        for i in range(count)
    ]
