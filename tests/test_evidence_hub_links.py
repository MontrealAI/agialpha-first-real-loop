from agialpha_evidence_hub.linkcheck import linkcheck

def test_links(tmp_path):
    (tmp_path/'index.html').write_text('ok')
    linkcheck(tmp_path)
