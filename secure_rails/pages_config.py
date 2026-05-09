def infer_pages_url(owner:str, repository:str)->str:
    return f"https://{owner.lower()}.github.io/{repository}/"
