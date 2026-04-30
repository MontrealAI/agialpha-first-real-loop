FOOTER='No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.'

def page(title,body):
    return f"<html><head><title>{title}</title></head><body><h1>{title}</h1>{body}<hr><footer>{FOOTER}</footer></body></html>"
