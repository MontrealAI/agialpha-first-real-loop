def mutate_kernel(kernel:dict,idx:int)->dict:
    c=dict(kernel)
    c['kernel_version']=f"{kernel.get('kernel_version','0.1.0')}-cand{idx}"
    c['candidate_id']=f"candidate-{idx:03d}"
    return c
