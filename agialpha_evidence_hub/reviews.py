def normalize_external_review(status='not_started', attestations='not_reported', issue_url=None):
    return {'status': status, 'attestations': attestations, 'issue_url': issue_url}
