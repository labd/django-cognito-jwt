import json

import pytest
from django.core.cache import cache

from django_cognito_jwt import validator
from tests.utils import create_jwt_token


def test_validate_token(cognito_well_known_keys, jwk_private_key_one):
    token = create_jwt_token(
        jwk_private_key_one,
        {
            'iss': 'https://cognito-idp.eu-central-1.amazonaws.com/bla',
            'aud': 'my-audience',
            'sub': 'username',
        })
    auth = validator.TokenValidator('eu-central-1', 'bla', 'my-audience')
    auth.validate(token)


def test_validate_token_error_key(cognito_well_known_keys, jwk_private_key_two):
    token = create_jwt_token(
        jwk_private_key_two,
        {
            'iss': 'https://cognito-idp.eu-central-1.amazonaws.com/bla',
            'aud': 'my-audience',
            'sub': 'username',
        })
    auth = validator.TokenValidator('eu-central-1', 'bla', 'my-audience')
    with pytest.raises(validator.TokenError):
        auth.validate(token)


def test_validate_token_error_aud(cognito_well_known_keys, jwk_private_key_one):
    token = create_jwt_token(
        jwk_private_key_one,
        {
            'iss': 'https://cognito-idp.eu-central-1.amazonaws.com/bla',
            'aud': 'other-audience',
            'sub': 'username',
        })
    auth = validator.TokenValidator('eu-central-1', 'bla', 'my-audience')

    with pytest.raises(validator.TokenError):
        auth.validate(token)


def test_validate_token_uses_cache(cognito_well_known_keys, jwk_private_key_one, jwk_public_key_one):
    token = create_jwt_token(
        jwk_private_key_one,
        {
            'iss': 'https://cognito-idp.eu-central-1.amazonaws.com/bla',
            'aud': 'my-audience',
            'sub': 'username',
        })

    auth = validator.TokenValidator('eu-central-1', 'bla', 'my-audience')
    auth.validate(token)

    cache_one = json.loads(cache.get(jwk_public_key_one['kid']))
    assert cache_one == jwk_public_key_one
