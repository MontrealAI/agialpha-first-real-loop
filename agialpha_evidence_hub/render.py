import html
FOOTER='No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.'
CLAIM='This hub records bounded Evidence Docket experiments. It does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, real-world certification, guaranteed economic return, or civilization-scale capability. Stronger claims require independent replay, official public benchmarks, cost/safety review, delayed outcomes, and external audit.'

def page(title,body):
    return f"<html><head><meta charset='utf-8'><title>{html.escape(title)}</title></head><body><h1>{html.escape(title)}</h1>{body}<hr><footer>{html.escape(FOOTER)}</footer></body></html>"
