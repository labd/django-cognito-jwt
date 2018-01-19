import json
import jwt
import requests
from jwt.algorithms import RSAAlgorithm

from django.utils.functional import cached_property


class TokenError(Exception):
    pass


class TokenValidator:
    def __init__(self, aws_region, aws_user_pool, audience):
        self.aws_region = aws_region
        self.aws_user_pool = aws_user_pool
        self.audience = audience

    @cached_property
    def pool_url(self):
        return f'https://cognito-idp.%s.amazonaws.com/%s' % (
            self.aws_region, self.aws_user_pool)

    @cached_property
    def _json_web_keys(self):
        response = requests.get(self.pool_url + '/.well-known/jwks.json')
        response.raise_for_status()
        json_data = response.json()

        result = {}
        for item in json_data['keys']:
            result[item['kid']] = item
        return result

    def _get_public_key(self, token):
        headers = jwt.get_unverified_header(token)
        kid = headers['kid']
        jwk_data = self.get_jwt_by_kid(kid)
        return RSAAlgorithm.from_jwk(jwk_data)

    def get_jwt_by_kid(self, kid):
        return json.dumps(self._json_web_keys[kid])

    def validate(self, token):
        public_key = self._get_public_key(token)

        try:
            jwt_data = jwt.decode(
                token,
                public_key,
                audience=self.audience,
                issuer=self.pool_url,
                algorithms=['RS256'],
            )
        except (jwt.InvalidTokenError, jwt.ExpiredSignature, jwt.DecodeError) as exc:
            raise TokenError(str(exc))
        return jwt_data
