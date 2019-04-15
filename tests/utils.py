import json

import jwt
from jwt.algorithms import RSAAlgorithm


def create_jwt_token(private_key, payload):
    key = json.dumps(private_key)
    key_id = private_key["kid"]

    secret = RSAAlgorithm.from_jwk(key)
    return jwt.encode(payload, secret, algorithm="RS256", headers={"kid": key_id})
