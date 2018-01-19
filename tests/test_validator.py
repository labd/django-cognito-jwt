import jwt
import responses

from django_cognito_jwt import validator


@responses.activate
def test_json_web_keys():
    response_content = {
        'keys': [
            {'alg': 'RS256', 'e': 'AQAB', 'kid': 'kid1', 'kty': 'RSA', 'n': 'secret1', 'use': 'sig'},
            {'alg': 'RS256', 'e': 'AQAB', 'kid': 'kid2', 'kty': 'RSA', 'n': 'secret2', 'use': 'sig'}
        ]
    }

    responses.add(
        responses.GET,
        'https://cognito-idp.eu-central-1.amazonaws.com/bla/.well-known/jwks.json',
        json=response_content,
        status=200)

    auth = validator.TokenValidator('eu-central-1', 'bla', 'aud')
    assert auth._json_web_keys == {
        'kid1': {
            'alg': 'RS256',
            'e': 'AQAB',
            'kid': 'kid1',
            'kty': 'RSA',
            'n': 'secret1',
            'use': 'sig'
        },
        'kid2': {
            'alg': 'RS256',
            'e': 'AQAB',
            'kid': 'kid2',
            'kty': 'RSA',
            'n': 'secret2',
            'use': 'sig'
        }
    }
