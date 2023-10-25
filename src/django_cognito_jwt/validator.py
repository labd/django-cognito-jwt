import json
from typing import Literal

import jwt
import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.functional import cached_property
from jwt.algorithms import RSAAlgorithm


class TokenError(Exception):
    pass


class TokenValidator:
    def __init__(self, aws_region, aws_user_pool, audience, token_type: Literal["id", "access"] = "id"):
        self.aws_region = aws_region
        self.aws_user_pool = aws_user_pool
        self.audience = audience
        self.token_type = token_type

        if token_type not in ["id", "access"]:
            raise TokenError("Invalid token type. Choose either id or access token.")

    @cached_property
    def pool_url(self):
        return "https://cognito-idp.%s.amazonaws.com/%s" % (
            self.aws_region,
            self.aws_user_pool,
        )

    @cached_property
    def _json_web_keys(self):
        response = requests.get(self.pool_url + "/.well-known/jwks.json")
        response.raise_for_status()
        json_data = response.json()
        return {item["kid"]: json.dumps(item) for item in json_data["keys"]}

    def _get_public_key(self, token):
        try:
            headers = jwt.get_unverified_header(token)
        except jwt.DecodeError as exc:
            raise TokenError(str(exc))

        if getattr(settings, "COGNITO_PUBLIC_KEYS_CACHING_ENABLED", False):
            cache_key = "django_cognito_jwt:%s" % headers["kid"]
            jwk_data = cache.get(cache_key)

            if not jwk_data:
                jwk_data = self._json_web_keys.get(headers["kid"])
                timeout = getattr(settings, "COGNITO_PUBLIC_KEYS_CACHING_TIMEOUT", 300)
                cache.set(cache_key, jwk_data, timeout=timeout)
        else:
            jwk_data = self._json_web_keys.get(headers["kid"])

        if jwk_data:
            return RSAAlgorithm.from_jwk(jwk_data)

    def validate(self, token):
        public_key = self._get_public_key(token)
        if not public_key:
            raise TokenError("No key found for this token")

        try:
            params = {
                "jwt": token,
                "key": public_key,
                "issuer": self.pool_url,
                "algorithms": ["RS256"]
            }
            if self.token_type == "id":
                params.update({"audience": self.audience})

            jwt_data = jwt.decode(**params)
            if self.token_type == "access":
                if "access" not in jwt_data["token_use"]:
                    raise TokenError("Incorrect token use")
                if jwt_data["client_id"] not in self.audience:
                    raise TokenError("Incorrect client_id")
        except (
            jwt.InvalidTokenError,
            jwt.ExpiredSignatureError,
            jwt.DecodeError,
        ) as exc:
            raise TokenError(str(exc))
        return jwt_data
