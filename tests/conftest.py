import copy

import pytest
from django.conf import settings


def pytest_configure():
    settings.configure(
        COGNITO_AWS_REGION='eu-central-1',
        COGNITO_USER_POOL='bla',
        COGNITO_AUDIENCE='my-client-id',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',

        ],
        MIDDLEWARE_CLASSES=[],
        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'unique-snowflake',
            }
        },
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite',
            },
        },
        ROOT_URLCONF='urls',
    )


def _private_to_public_key(private_key):
    data = copy.deepcopy(private_key)
    del data['d']
    return data


@pytest.fixture()
def jwk_private_key_one():
    return {
        "kty": "RSA",
        "d": (
            "YKOGWFXP3-wWK1OqrKVoTQ5gjkLJPfn2V2ia1tWZ2Ety20W9fpcQmNuS8U"
            "bkl86laVergyup8mE0ZpymxXeNRBYI9MrB_k9DCvpnbxW-S3RN8lT1CxZY"
            "oUPK8spaO5V5StMfZFesAbwhVIK_flp1NUynM3BkRZ-rRPaDS1Ynz-Z8ag"
            "oFAoz3sf946JitajgIyAJUF8wy8j-heXYdOHXeHebBZPvr5bET8hPxapmG"
            "gr2_JpKYQbzJ1Emnn1RlTRqdaUWLLKf-XaiemlB2TLNq5YKg-Cr5yIBfro"
            "gjhGwh0yGXbuTXzn0QWR3MYoAU9BxHq9vzl-X1ZcF1GqPqOBPigQ"
        ),
        "e": "AQAB",
        "use": "sig",
        "kid": "key-one",
        "alg": "RS256",
        "n": (
            "iN7iEEFIhcXYFg0ZxvB_etEwN9-ZgA2-g-WzTpcG2qLKjj2rDr80rGPY7I"
            "fXaEDppME9ZcN-Mw8oUxSBUIllMNpE9dA0XUhuklFDDiF02FShj2jwua-A"
            "k3ORMIgf2ujGPO-b1rkmEKc6TFu_w5jfum9eocaVVIdqYr2j9mG1UCqI0m"
            "d-JuGOZi1_f4hp67Qbve_Bzh_3yvQWsTegFNjp55-MzUX-VZ-IEYqhuzaV"
            "70t0rnnqFrYgnPqrwo03MOGHUhSJTyg0vBO4S-FoW0e8YKVU1CIOClCuiB"
            "qsjkpRBst1DG9094K_PRFcEszIlwt1NUHDMGQV1gHg3zebXxKumQ"
        )
    }


@pytest.fixture()
def jwk_public_key_one(jwk_private_key_one):
    return _private_to_public_key(jwk_private_key_one)


@pytest.fixture()
def jwk_private_key_two():
    return {
        "kty": "RSA",
        "d": (
            "G0-8DUpJmbgnYLVCkKTx481skS7DRS4HZlpwHaqzYZn97tVz9sZ_wJmYK1"
            "ejaZ_n2K6474zutmx2_XOXNdJJkxdbmi_HwF7V0Ha3R-kPiOUcL0FMI2vC"
            "DOjXN8zQG42GYRq1bcrXRBJbSQQK70SiXesv5v1krB0LLr1P8aQTtQw70h"
            "xO1avoeeueKhfHET8tIzVlvXz5s4N0s1fH1C-9Z82vTsqyMo51aBqFjPfB"
            "Yc0k-AjrrQsVqmvWAXW-7nTiBRdMkZ8Jes1rNnJWYliGmepZbOBQRqEu-I"
            "epvAujPdVSsSnQa1zgRKVOgH4KEGVfVtoNY3HoQGaZ5GhiD5BHgQ"
        ),
        "e": "AQAB",
        "use": "sig",
        "kid": "key-two",
        "alg": "RS256",
        "n": (
            "hvHv4nocfMqZB6e-paozbjr9MaCqOmOtoiiUEwvBPbXgrBH2-MpkzsV_A7"
            "OzcMc1R8UMoLE4k4QedFCwM3HwC8CrasH3qkd0GPJA0py1Toa8w7v5TB5e"
            "WmGpi_eBjRQcEyq9xVUE637oIfSmgp3U0QOp4px7FpNw8QhP9eMTUnSo_u"
            "vsN-dASz4h1U-fBVktT-9yfPBbjq7BER3OjIuVlRAFrptK8xdG1XZtzxdC"
            "6O9CGneDwKDcJS-43PGzjyaz4YIRPBPxysZ0veyKxpD-AcC-qAPf0EWdQG"
            "6ik-2wNn-5FIHm01MGNcnh6ntuoyZefA3FRjlvuDrwhz2joE6iqw"
        ),
    }


@pytest.fixture()
def jwk_public_key_two(jwk_private_key_two):
    return _private_to_public_key(jwk_private_key_two)


@pytest.fixture()
def cognito_well_known_keys(responses, jwk_public_key_one, jwk_public_key_two):
    jwk_keys = {
        'keys': [jwk_public_key_one]
    }
    responses.add(
        responses.GET,
        'https://cognito-idp.eu-central-1.amazonaws.com/bla/.well-known/jwks.json',
        json=jwk_keys,
        status=200)
