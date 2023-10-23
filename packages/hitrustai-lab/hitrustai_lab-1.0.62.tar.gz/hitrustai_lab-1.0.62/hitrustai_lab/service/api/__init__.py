from hashlib import sha256
from .exception import TokenMissingError, MacValidateError


def encrypt_token(token: str, timestamp: str):
    return sha256((token+timestamp).encode("utf-8")).hexdigest()


def mac_validation(req: dict, token: str):
    '''Mac Validate'''
    mac, timestamp = req.get("mac"), req.get("timestamp")
    if mac is None:
        raise TokenMissingError('0103', 'MAC token invalid/missing.')
    elif timestamp is None:
        raise TokenMissingError('0104', 'Timestamp token invalid/missing.')
    else:
        if mac != encrypt_token(token, timestamp):
            raise MacValidateError('9903', 'Mac token validate failed.')


def get_policy_score(total_score: float):
    return round((total_score*(-2) + 1), 6)

