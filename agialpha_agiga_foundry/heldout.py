def generate_heldout_tasks(lock_hashes, count:int=15):
    if isinstance(lock_hashes, str):
        lock_hashes=[lock_hashes]
    tasks=[]
    for lock_hash in lock_hashes:
        for i in range(count):
            tasks.append({"task_id":f"heldout-{i:02d}","lock_hash":lock_hash})
    return tasks
