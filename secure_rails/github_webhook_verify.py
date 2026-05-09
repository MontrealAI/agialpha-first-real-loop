
import hashlib, hmac

def verify_github_webhook_signature(secret: bytes, payload: bytes, signature_header: str) -> bool:
    if not secret or not payload or not isinstance(signature_header, str):
        return False
    if not signature_header.startswith('sha256='):
        return False
    sent = signature_header.split('=', 1)[1].strip()
    if not sent:
        return False
    digest = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, sent)
