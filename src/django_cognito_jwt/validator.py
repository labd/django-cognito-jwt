import json
import jwt
import requests
from django.core.cache import cache
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
        return 'https://cognito-idp.%s.amazonaws.com/%s' % (
            self.aws_region, self.aws_user_pool)

    @cached_property
    def _json_web_keys(self):
        response = requests.get(self.pool_url + '/.well-known/jwks.json')
        response.raise_for_status()
        json_data = response.json()
        return {item['kid']: json.dumps(item) for item in json_data['keys']}

    def _get_public_key(self, token):
        try:
            headers = jwt.get_unverified_header(token)
        except jwt.DecodeError as exc:
            raise TokenError(str(exc))

        # Check the cache before we request the keys from the URI
        cache_key = headers['kid']
        jwk_data = cache.get(cache_key)

        if not jwk_data:
            jwk_data = self._json_web_keys.get(headers['kid'])
            cache.set(cache_key, jwk_data, 600)

        if jwk_data:
            return RSAAlgorithm.from_jwk(jwk_data)

    def validate(self, token):
        public_key = self._get_public_key(token)
        if not public_key:
            raise TokenError("No key found for this token")

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
