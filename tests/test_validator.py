import pytest

from django_cognito_jwt import validator
from utils import create_jwt_token


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


@pytest.mark.parametrize("is_cache_enabled,responses_calls", [
    (None, 2),
    (False, 2),
    (True, 1),
])
def test_validate_token_caching(cognito_well_known_keys, jwk_private_key_one, settings, responses, is_cache_enabled,
                                responses_calls):
    if is_cache_enabled is not None:
        settings.COGNITO_PUBLIC_KEYS_CACHING_ENABLED = is_cache_enabled

    token = create_jwt_token(
        jwk_private_key_one,
        {
            'iss': 'https://cognito-idp.eu-central-1.amazonaws.com/bla',
            'aud': 'my-audience',
            'sub': 'username',
        })
    auth = validator.TokenValidator('eu-central-1', 'bla', 'my-audience')
    auth.validate(token)
    assert len(responses.calls) == 1

    auth_again = validator.TokenValidator('eu-central-1', 'bla', 'my-audience')
    auth_again.validate(token)
    assert len(responses.calls) == responses_calls
