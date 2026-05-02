def generate_heldout_tasks(lock_hash:str,count:int=15):
    return [{"task_id":f"heldout-{i:02d}","lock_hash":lock_hash} for i in range(count)]
